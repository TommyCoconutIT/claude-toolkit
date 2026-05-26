---
name: dushi-week-airtable-tasks
description: Headless, automated variant of the Dushi Week builder. Reads a lead Pipeline record from Airtable, generates a personalised 7-night itinerary plan, and writes the result as Itinerary Items V2 records linked to that Pipeline. No human gates, no HTML, no microsite — just the Airtable tasks. Triggered by GitHub Actions on every new lead.
---

# dushi-week-airtable-tasks

Automated itinerary task generator for Tommy Coconut Private Resorts.
You are running **headlessly** — no human is watching. Proceed without asking for confirmation.

---

## STEP 1 — Read the Pipeline record

Fetch the Pipeline record using the `pipeline_id` passed as the input to this run.

- **Base:** `appFRLV1H76ohiIQS`
- **Table:** `tblb7gP5D3NYND9a0` (Pipeline)

Use `list_records_for_table` with `recordIds: [pipeline_id]` and request these fields:

| Field name | Field ID | What it gives you |
|---|---|---|
| Email | `fldvNQMiLWRW04G2Q` | Guest email |
| FirstName | `fldhvA77gRGoG65ZT` | First name |
| LastName | `fldlX19qjZfNcCgJv` | Last name |
| DateArrival | `fld2MQtX4nrfMKw6d` | Arrival date (ISO) |
| DateDeparture | `fldyqrnO9Px1JhWnx` | Departure date (ISO) |
| Adults | `fld3j3KNEbByQVbyQ` | Adult count |
| Children | `fldBqEBUnBSdFyvzS` | Child count |
| Infants | `fld5cXA7IDHtdJ4bC` | Infant count |
| Quiz Answers Raw | `fld85HtV5j2DDf8Z9` | JSON `[{q, a}]` array — quiz responses |
| Segment | `fldnh3gJKZH9BQS8s` | Guest segment (couple / family / friends / etc.) |
| Basecamp | `fld15SzszbTcHufZT` | Linked estate name |
| estateFirst | `fld2IqqKZZpPmeyOD` | Estate preference 1 |
| whoComing | `flddaaVzF8WIJz3sn` | Who's in the group |

Parse `Quiz Answers Raw` as JSON. Extract at minimum:
- Arrival / departure dates (cross-check with the structured fields)
- Dietary restrictions / allergies
- Activity wishlist ("What catches your eye?")
- Group composition ("Who's coming?")
- Motivation ("What made you decide to do this now?") — use in personalisation

---

## STEP 2 — Determine guest type

Using `Segment`, adult/child/infant counts, and the quiz answers, classify the group into one of:

| Guest type | When |
|---|---|
| **couple** | 2 adults, no kids |
| **family-young-kids** | children under 5 |
| **family-teens** | kids 10–17 |
| **family-young-adults** | kids 18–25 |
| **friends** | 3+ adults, no kids |
| **multi-gen** | mixed adults + kids across age brackets |

This drives the day rhythm and activity mix (see island knowledge below).

---

## STEP 3 — Check for existing itinerary items (idempotency)

Before writing anything, check whether this Pipeline already has Itinerary Items V2 records linked to it.

Search `tblrehbZFtArMtwr5` filtering on `fldWzo3ZUygqaiwyB = pipeline_id`.

- If records exist: **delete them all first** using `delete_records_for_table`. This makes the run idempotent — a second trigger after quiz completion simply replaces the earlier draft.
- If no records exist: proceed.

---

## STEP 4 — Build the 7-day itinerary plan

Using the island knowledge below and the guest context from Step 1–2, generate a **concrete day-by-day plan** for the 7 nights.

### Island knowledge (concise)

**Fixed anchors (always schedule these):**
- **Day 2 or 3 — Flamingo Walk** at Landhuis Daniel or Chogogo. Morning only. Skip for infants. Family favourite — schedule early in the week.
- **Wednesday evening — Sunset Club** at Tommy Coconut (fixed TC event). All groups attend.
- **One afternoon — Boat Day** (snorkelling, Caribbean sea, captain's briefing). Central week. Do not schedule on Days 1 or 7.
- **One dinner — Plasa Bieu** (local food market, authentic, cheap, kids love it). Best Tue–Fri.
- **One dinner — Culinary Pass** restaurant (confirm which one — Boathouse / Gesto / Zanzibar depending on party). Always a Culinary Pass evening for Dushi Week guests.
- **One morning — Flamingo Beach** at Jan Thiel (shallow, calm, suitable for all family types).

**Guest-type rhythm:**
- **Young family**: nap window 1 PM sacred, no evening activities after 8 PM, Poko Poko beach over party beach.
- **Teen family**: 10 AM starts, teens at Mambo Beach, padel afternoon, snorkelling is a hit.
- **Couple**: fully flexible, add romantic dinner option (Karakter), Poko Poko afternoons, Discovery Dive if interested.
- **Friends**: sunset drinks on the deck, Jaanchie's for lunch, late evenings fine.

**Good default filler activities per slot:**
- Morning: beach, Flamingo Walk, snorkelling, padel, kayak
- Afternoon: Poko Poko time at the villa, Sea Aquarium, Jan Thiel beach club
- Evening: Sunset Club (Wed), Plasa Bieu, Culinary Pass dinner, Karakter (couples)

**Days 1 & 7:** Keep light — arrival/departure logistics. Day 1: afternoon arrival, evening settle in + welcome drinks. Day 7: morning at the villa + departure after breakfast.

---

## STEP 5 — Write itinerary items to Airtable

For each activity block in your 7-day plan, create one record in `Itinerary Items V2`.

- **Base:** `appFRLV1H76ohiIQS`
- **Table:** `tblrehbZFtArMtwr5`

Use `create_records_for_table` in batches of up to 10 records.

**Field mapping per record:**

| Field | Field ID | Value |
|---|---|---|
| Pipeline | `fldWzo3ZUygqaiwyB` | `[pipeline_id]` (array with one record ID) |
| Day Number | `fldPlg98rFGiaCCSH` | Integer 1–7 |
| Slot | `fldDekHGP9CCIfgJl` | `"Morning"` / `"Afternoon"` / `"Evening"` / `"All-Day"` |
| Header | `fldQx8ZJCw7Mw652T` | Time-block label e.g. `"9:00 AM — Flamingo Walk"` |
| Body Text | `fldBcHXSRTzi6Tqg6` | 2–4 sentence personalised description of the activity |
| Sort Order | `fldwpxPJaMXbSd3P5` | Sequential integer (1, 2, 3…) across all records |
| Status | `fldt7AsmEOz8Jgzc0` | `"Draft"` |
| Base Pro Tip | `fldWdPQqDdfQ1gnEc` | Optional practical tip (e.g. "Book the boat by Day 2 to secure your preferred captain.") |
| Show Pro Tip | `fldAkfpwgSUP8tVWG` | `true` if Base Pro Tip is non-empty, otherwise `false` |

**Aim for 3–5 activity blocks per day** (Morning, Afternoon, Evening + optional All-Day anchor).
Total records: roughly 21–35.

**Body Text guidance:**
- Write in the Tommy Coconut voice: warm, direct, personal. Not a hotel brochure.
- Reference what you know about the guest from the quiz answers where relevant.
- Keep it scannable — 2 sentences is fine. 4 is the max.

---

## STEP 6 — Done

After all records are created, print a short summary:

```
✅ Itinerary tasks written for pipeline_id: <id>
   Guest: <FirstName> <LastName> (<email>)
   Dates: <arrival> → <departure>
   Records created: <count>
```

Do not update the Pipeline status. Do not open a PR. Do not write HTML. Your job is done.
