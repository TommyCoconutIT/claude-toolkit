#!/usr/bin/env python3
"""Clone Itinerary Items V2 from the master template Trip onto a lead Pipeline.

Copies every writable template field 1:1. The only differences on the new records:
  - Pipeline link → lead PIPELINE_ID
  - No Trip link (lead-stage items are Pipeline-only)

Usage:
  PIPELINE_ID=recXXX AIRTABLE_API_KEY=patXXX python3 scripts/clone-template-itinerary.py

Optional env vars:
  TEMPLATE_TRIP_NAME  Trip name to clone from (default: "Template — Master")

Exits 0 on success, 1 on validation failure.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

BASE_ID = "appFRLV1H76ohiIQS"
IIV2_TABLE = "tblrehbZFtArMtwr5"
LEADS_TABLE = "tblxw3UgaOTAmz4FQ"

TEMPLATE_TRIP_NAME = os.environ.get("TEMPLATE_TRIP_NAME", "Template — Master")

# Monday=0 … Sunday=6, matching Python's date.weekday().
_DOW = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6,
}

# Writable fields copied verbatim from template → lead (Airtable field names).
COPY_FIELDS = [
    "Activity Catalog",
    "Day Number",
    "Weekday",
    "Slot",
    "Header",
    "Body Text",
    "Sort Order",
    "Status",
    "Base Pro Tip",
    "Show Base Pro Tip?",
    "Show About?",
    "About Story",
    "Is Hero For Day",
]


def api(method: str, path: str, body: dict | None = None) -> dict:
    key = os.environ["AIRTABLE_API_KEY"]
    url = f"https://api.airtable.com/v0/{BASE_ID}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"Airtable {method} {path} failed ({exc.code}): {detail}") from exc


def list_records(table: str, formula: str, sort: list[tuple[str, str]] | None = None) -> list[dict]:
    records: list[dict] = []
    params: dict[str, str] = {
        "filterByFormula": formula,
        "pageSize": "100",
    }
    if sort:
        for i, (field_id, direction) in enumerate(sort):
            params[f"sort[{i}][field]"] = field_id
            params[f"sort[{i}][direction]"] = direction

    offset: str | None = None
    while True:
        q = dict(params)
        if offset:
            q["offset"] = offset
        payload = api("GET", f"{table}?{urllib.parse.urlencode(q)}")
        records.extend(payload.get("records", []))
        offset = payload.get("offset")
        if not offset:
            break
    return records


def delete_records(record_ids: list[str]) -> None:
    for i in range(0, len(record_ids), 10):
        batch = record_ids[i : i + 10]
        query = "&".join(f"records[]={rid}" for rid in batch)
        api("DELETE", f"{IIV2_TABLE}?{query}")


def remap_day_number(
    weekday_str: str,
    arrival_dow: int,
    trip_length: int | None,
) -> int | None:
    """Return the 1-based day number for this weekday given the arrival day of week.

    Returns None when the computed day falls outside the trip window.
    Saturday-to-Saturday (arrival_dow == 5) always maps Day 1 → Saturday,
    which matches the template exactly (no change).
    """
    template_dow = _DOW.get(weekday_str)
    if template_dow is None:
        return None
    days_offset = (template_dow - arrival_dow) % 7
    day_number = days_offset + 1
    if trip_length is not None and day_number > trip_length:
        return None
    return day_number


def build_create_fields(
    template_fields: dict,
    lead_id: str,
    arrival_dow: int | None,
    trip_length: int | None,
    max_template_day: int | None,
) -> dict | None:
    """Return fields for a new record, or None if the item falls outside the trip window."""
    out: dict = {"Lead": [lead_id]}

    weekday_str = template_fields.get("Weekday")
    template_day_number = template_fields.get("Day Number")
    day_number_override: int | None = None

    # Day 1 items are always the arrival-day activities — pin them to Day 1
    # regardless of their Weekday value or the guest's arrival weekday.
    if template_day_number == 1:
        day_number_override = 1
    elif max_template_day is not None and template_day_number == max_template_day:
        # Departure-day items (the last day in the template) always land on the
        # FINAL itinerary day, whatever the stay length. Pin them to trip_length
        # when we know it (this also prevents the weekday remap from collapsing a
        # Saturday departure onto Day 1, since Day 1 shares the same weekday).
        # When trip_length is unknown, leave the template Day Number verbatim.
        if trip_length is not None:
            day_number_override = trip_length
    elif weekday_str and arrival_dow is not None:
        day_number_override = remap_day_number(weekday_str, arrival_dow, trip_length)
        if day_number_override is None:
            return None  # outside trip window — skip
    elif trip_length is not None and template_day_number is not None:
        # No weekday remap possible (e.g. nights known but no arrival date): keep the
        # template Day Number, but still drop anything past the final itinerary day.
        if template_day_number > trip_length:
            return None  # outside trip window — skip

    for name in COPY_FIELDS:
        if name == "Day Number" and day_number_override is not None:
            out["Day Number"] = day_number_override
            continue
        if name not in template_fields:
            continue
        value = template_fields[name]
        if value is None:
            continue
        out[name] = value

    return out


def record_key(fields: dict, use_weekday: bool = False) -> tuple:
    ac = fields.get("Activity Catalog") or []
    ac_id = ac[0] if ac else None
    if use_weekday:
        return (fields.get("Weekday"), fields.get("Slot"), ac_id, fields.get("Sort Order"))
    return (fields.get("Day Number"), fields.get("Slot"), ac_id, fields.get("Sort Order"))


def compare_template_to_lead(
    template: dict, lead: dict, skip_fields: set[str] = frozenset()
) -> list[str]:
    mismatches: list[str] = []
    for name in COPY_FIELDS:
        if name in skip_fields:
            continue
        t_val = template.get(name)
        l_val = lead.get(name)
        if t_val != l_val:
            mismatches.append(f"{name}: template={t_val!r} lead={l_val!r}")
    return mismatches


def main() -> int:
    lead_id = os.environ.get("LEAD_ID")
    if not lead_id:
        print("ERROR: LEAD_ID env var is required", file=sys.stderr)
        return 1
    if not os.environ.get("AIRTABLE_API_KEY"):
        print("ERROR: AIRTABLE_API_KEY env var is required", file=sys.stderr)
        return 1

    lead = api("GET", f"{LEADS_TABLE}/{lead_id}")
    fields = lead.get("fields", {})
    guest = fields.get("Name", "").strip()
    email = fields.get("Email", "")

    # Parse arrival/departure dates for day-number remapping.
    arrival_dow: int | None = None
    trip_length: int | None = None
    arrival_date_str = fields.get("Date Arrival")
    departure_date_str = fields.get("Date Departure")
    requested_nights = fields.get("Requested Nights")

    if arrival_date_str:
        try:
            arrival_dt = date.fromisoformat(str(arrival_date_str)[:10])
            arrival_dow = arrival_dt.weekday()  # Monday=0 … Sunday=6
            if departure_date_str:
                departure_dt = date.fromisoformat(str(departure_date_str)[:10])
                trip_length = (departure_dt - arrival_dt).days + 1
        except ValueError:
            print(
                f"WARNING: Could not parse dates ({arrival_date_str!r}, {departure_date_str!r})"
                " — falling back to Requested Nights / template Day Numbers.",
                file=sys.stderr,
            )

    # Fallback: no usable departure date, but the guest told us how many nights in the
    # quiz ("Requested Nights"). Nights + 1 = itinerary day count (7 nights → 8 days,
    # matching the Saturday-to-Saturday template). This lets us size the week and pin
    # the departure day even when no arrival weekday is known (→ no weekday remap, but
    # truncation + departure pinning still apply).
    if trip_length is None and isinstance(requested_nights, (int, float)) and requested_nights > 0:
        trip_length = int(requested_nights) + 1

    # Day numbers get transformed whenever we know the arrival weekday (full remap) OR
    # the trip length (truncation + departure-day pinning) — either changes Day Number,
    # so verification must match on Weekday rather than Day Number in both cases.
    remapping = arrival_dow is not None or trip_length is not None
    print(f"Lead: {lead_id} ({guest} / {email})")
    print(f"Template: {TEMPLATE_TRIP_NAME}")
    if arrival_dow is not None:
        dow_name = next(k for k, v in _DOW.items() if v == arrival_dow)
        print(f"Arrival: {arrival_date_str} ({dow_name}), trip length: {trip_length} day(s) — remapping day numbers")
    elif trip_length is not None:
        print(
            f"No arrival date — using Requested Nights={requested_nights} → trip length: "
            f"{trip_length} day(s). Truncating + pinning departure day (no weekday remap)."
        )

    existing = list_records(
        IIV2_TABLE,
        f'SEARCH("{lead_id}", ARRAYJOIN({{Lead}}))',
    )
    if existing:
        print(
            f"Found {len(existing)} existing itinerary item(s) for {lead_id} — "
            "skipping template clone. AI personalization will run on existing items."
        )
        return 0

    template_records = list_records(
        IIV2_TABLE,
        f'SEARCH("{TEMPLATE_TRIP_NAME}", ARRAYJOIN({{Trip Name (lookup)}}))',
        sort=[
            ("fldPlg98rFGiaCCSH", "asc"),
            ("fldwpxPJaMXbSd3P5", "asc"),
        ],
    )

    if len(template_records) == 0:
        print(
            f"ERROR: Template {TEMPLATE_TRIP_NAME!r} returned 0 items — "
            "check the Trip Name in Airtable.",
            file=sys.stderr,
        )
        return 1

    for rec in template_records:
        trip_names = rec.get("fields", {}).get("Trip Name (lookup)", [])
        if not any(TEMPLATE_TRIP_NAME in (name or "") for name in trip_names):
            print(
                f"ERROR: Record {rec['id']} belongs to wrong template: {trip_names}",
                file=sys.stderr,
            )
            return 1

    # The departure-day items are those on the template's last day. Used to pin them to
    # the final itinerary day regardless of stay length.
    template_day_numbers = [
        r["fields"].get("Day Number")
        for r in template_records
        if isinstance(r["fields"].get("Day Number"), (int, float))
    ]
    max_template_day = int(max(template_day_numbers)) if template_day_numbers else None

    # Build the fields for every template record; skip items outside the trip window.
    records_to_create = []
    skipped = 0
    for r in template_records:
        new_fields = build_create_fields(r["fields"], lead_id, arrival_dow, trip_length, max_template_day)
        if new_fields is None:
            skipped += 1
        else:
            records_to_create.append(new_fields)

    if skipped:
        print(f"Skipped {skipped} template item(s) outside the trip window.")

    created: list[dict] = []
    for i in range(0, len(records_to_create), 10):
        batch = records_to_create[i : i + 10]
        payload = {"records": [{"fields": f} for f in batch]}
        result = api("POST", IIV2_TABLE, payload)
        created.extend(result.get("records", []))

    if len(created) != len(records_to_create):
        print(
            f"ERROR: Created {len(created)} records but expected {len(records_to_create)}",
            file=sys.stderr,
        )
        return 1

    # Use Weekday-based keys when remapping so Day Number differences don't confuse the lookup.
    skip_verify = {"Day Number"} if remapping else set()
    template_by_key = {
        record_key(r["fields"], use_weekday=remapping): r["fields"]
        for r in template_records
        if record_key(r["fields"], use_weekday=remapping)[0] is not None  # skip items with no key
    }
    lead_by_key = {
        record_key(r["fields"], use_weekday=remapping): r["fields"]
        for r in created
    }

    flag_mismatches = 0
    for key, template_fields in template_by_key.items():
        lead_fields = lead_by_key.get(key)
        if not lead_fields:
            # When remapping, template items outside the window won't have a lead record — OK.
            if not remapping:
                print(f"ERROR: Missing lead record for template key {key}", file=sys.stderr)
                flag_mismatches += 1
            continue
        diffs = compare_template_to_lead(template_fields, lead_fields, skip_fields=skip_verify)
        if diffs:
            flag_mismatches += 1
            day = template_fields.get("Day Number")
            slot = template_fields.get("Slot")
            header = template_fields.get("Header", "")
            print(f"MISMATCH Day {day} {slot} {header!r}:")
            for d in diffs:
                print(f"  - {d}")

    about_on_template = sum(1 for r in template_records if r["fields"].get("Show About?"))
    about_on_lead = sum(1 for r in created if r["fields"].get("Show About?"))
    pro_on_template = sum(1 for r in template_records if r["fields"].get("Show Base Pro Tip?"))
    pro_on_lead = sum(1 for r in created if r["fields"].get("Show Base Pro Tip?"))

    print()
    print(f"✅ Cloned {len(created)} itinerary items for {lead_id}")
    print(f"   Template: {TEMPLATE_TRIP_NAME}")
    if remapping:
        print(f"   Day remapping: active ({skipped} template item(s) outside trip window skipped)")
    print(f"   Show About? rows: {about_on_template} template → {about_on_lead} lead")
    print(f"   Show Base Pro Tip? rows: {pro_on_template} template → {pro_on_lead} lead")

    if flag_mismatches:
        print(f"ERROR: {flag_mismatches} record(s) failed 1:1 field verification", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
