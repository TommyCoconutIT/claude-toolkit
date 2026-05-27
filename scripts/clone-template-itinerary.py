#!/usr/bin/env python3
"""Clone Itinerary Items V2 from a segment template Trip onto a lead Pipeline.

Copies every writable template field 1:1. The only differences on the new records:
  - Pipeline link → lead PIPELINE_ID
  - No Trip link (lead-stage items are Pipeline-only)

Usage:
  PIPELINE_ID=recXXX AIRTABLE_API_KEY=patXXX python3 scripts/clone-template-itinerary.py

Exits 0 on success, 1 on validation failure.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_ID = "appFRLV1H76ohiIQS"
IIV2_TABLE = "tblrehbZFtArMtwr5"
PIPELINE_TABLE = "tblb7gP5D3NYND9a0"

SEGMENT_TO_TEMPLATE: dict[str, tuple[str, int]] = {
    "couple": ("Template Couple", 21),
    "friends": ("Template Friends", 22),
    "family-young-kids": ("Template Family young kids", 18),
    "family-teens": ("Template Family teens", 19),
    "family-young-adults": ("Template Family young adults", 20),
    "multi-gen": ("Template Multi gen", 18),
}

# Writable fields copied verbatim from template → lead (Airtable field names).
COPY_FIELDS = [
    "Activity Catalog",
    "Day Number",
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


def build_create_fields(template_fields: dict, pipeline_id: str) -> dict:
    out: dict = {"Pipeline": [pipeline_id]}
    for name in COPY_FIELDS:
        if name not in template_fields:
            continue
        value = template_fields[name]
        if value is None:
            continue
        if name == "Activity Catalog" and isinstance(value, list):
            out[name] = value
        else:
            out[name] = value
    return out


def record_key(fields: dict) -> tuple:
    ac = fields.get("Activity Catalog") or []
    ac_id = ac[0] if ac else None
    return (
        fields.get("Day Number"),
        fields.get("Slot"),
        ac_id,
        fields.get("Sort Order"),
    )


def compare_template_to_lead(template: dict, lead: dict) -> list[str]:
    mismatches: list[str] = []
    for name in COPY_FIELDS:
        t_val = template.get(name)
        l_val = lead.get(name)
        if t_val != l_val:
            mismatches.append(f"{name}: template={t_val!r} lead={l_val!r}")
    return mismatches


def main() -> int:
    pipeline_id = os.environ.get("PIPELINE_ID")
    if not pipeline_id:
        print("ERROR: PIPELINE_ID env var is required", file=sys.stderr)
        return 1
    if not os.environ.get("AIRTABLE_API_KEY"):
        print("ERROR: AIRTABLE_API_KEY env var is required", file=sys.stderr)
        return 1

    pipeline = api("GET", f"{PIPELINE_TABLE}/{pipeline_id}")
    fields = pipeline.get("fields", {})
    segment = fields.get("Segment")
    if not segment:
        print("ERROR: Pipeline Segment is blank — cannot pick template", file=sys.stderr)
        return 1

    if segment not in SEGMENT_TO_TEMPLATE:
        print(f"ERROR: Unknown Segment {segment!r}", file=sys.stderr)
        return 1

    template_name, expected_count = SEGMENT_TO_TEMPLATE[segment]
    guest = f"{fields.get('FirstName', '')} {fields.get('LastName', '')}".strip()
    email = fields.get("Email", "")

    print(f"Pipeline: {pipeline_id} ({guest} / {email})")
    print(f"Segment: {segment} → {template_name} (expected {expected_count} items)")

    existing = list_records(
        IIV2_TABLE,
        f'SEARCH("{pipeline_id}", ARRAYJOIN({{Pipeline}}))',
    )
    if existing:
        print(f"Deleting {len(existing)} existing lead itinerary item(s)...")
        delete_records([r["id"] for r in existing])

    template_records = list_records(
        IIV2_TABLE,
        f'SEARCH("{template_name}", ARRAYJOIN({{Trip Name (lookup)}}))',
        sort=[
            ("fldPlg98rFGiaCCSH", "asc"),
            ("fldwpxPJaMXbSd3P5", "asc"),
        ],
    )

    if len(template_records) != expected_count:
        print(
            f"ERROR: Template {template_name!r} returned {len(template_records)} items, "
            f"expected {expected_count}. Halting — nothing written.",
            file=sys.stderr,
        )
        return 1

    for rec in template_records:
        trip_names = rec.get("fields", {}).get("Trip Name (lookup)", [])
        if not any(template_name in (name or "") for name in trip_names):
            print(
                f"ERROR: Record {rec['id']} belongs to wrong template: {trip_names}",
                file=sys.stderr,
            )
            return 1

    created: list[dict] = []
    for i in range(0, len(template_records), 10):
        batch = template_records[i : i + 10]
        payload = {
            "records": [
                {"fields": build_create_fields(r["fields"], pipeline_id)}
                for r in batch
            ]
        }
        result = api("POST", IIV2_TABLE, payload)
        created.extend(result.get("records", []))

    if len(created) != len(template_records):
        print(
            f"ERROR: Created {len(created)} records but template had {len(template_records)}",
            file=sys.stderr,
        )
        return 1

    template_by_key = {record_key(r["fields"]): r["fields"] for r in template_records}
    lead_by_key = {record_key(r["fields"]): r["fields"] for r in created}

    flag_mismatches = 0
    for key, template_fields in template_by_key.items():
        lead_fields = lead_by_key.get(key)
        if not lead_fields:
            print(f"ERROR: Missing lead record for template key {key}", file=sys.stderr)
            flag_mismatches += 1
            continue
        diffs = compare_template_to_lead(template_fields, lead_fields)
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
    print(f"✅ Cloned {len(created)} itinerary items for {pipeline_id}")
    print(f"   Template: {template_name}")
    print(f"   Show About? rows: {about_on_template} template → {about_on_lead} lead")
    print(f"   Show Base Pro Tip? rows: {pro_on_template} template → {pro_on_lead} lead")

    if flag_mismatches:
        print(f"ERROR: {flag_mismatches} record(s) failed 1:1 field verification", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
