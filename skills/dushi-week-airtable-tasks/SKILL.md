---
name: dushi-week-airtable-tasks
description: Headless, automated variant of the Dushi Week builder. Reads a lead Pipeline record from Airtable, generates a personalised 7-night itinerary plan, and writes the result as Itinerary Items V2 records linked to that Pipeline. No human gates, no HTML, no microsite — just the Airtable tasks. Triggered by GitHub Actions on every new lead.
---

# dushi-week-airtable-tasks

Automated itinerary task generator for Tommy Coconut Private Resorts.
You are running **headlessly** in GitHub Actions — no human is watching.
Use `bash` (curl) for all Airtable reads and writes. The `AIRTABLE_API_KEY` environment variable is already set.

---

## STEP 1 — Read the Pipeline record

Fetch the Pipeline record via curl:

```bash
curl -s "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblb7gP5D3NYND9a0/${PIPELINE_ID}" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY"
```

Parse the `fields` object from the JSON response. Extract:

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
| Quiz Answers Raw | `fld85HtV5j2DDf8Z9` | JSON `[{q, a}]` — quiz responses |
| Segment | `fldnh3gJKZH9BQS8s` | Guest segment |
| Basecamp | `fld15SzszbTcHufZT` | Linked estate (array of record IDs) |
| whoComing | `flddaaVzF8WIJz3sn` | Who's in the group |

Parse `Quiz Answers Raw` as JSON. Extract at minimum:
- Dietary restrictions / allergies
- Activity wishlist ("What catches your eye?")
- Group composition ("Who's coming?")
- Motivation ("What made you decide to do this now?") — use in personalisation

---

## STEP 2 — Determine guest type

Using `Segment`, adult/child/infant counts, and quiz answers, classify into:

| Guest type | When |
|---|---|
| **couple** | 2 adults, no kids |
| **family-young-kids** | children under 5 |
| **family-teens** | kids 10–17 |
| **family-young-adults** | kids 18–25 |
| **friends** | 3+ adults, no kids |
| **multi-gen** | mixed adults + kids across age brackets |

---

## STEP 3 — Delete any existing itinerary items (idempotency)

List existing Itinerary Items V2 linked to this Pipeline:

```bash
curl -s "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "filterByFormula=SEARCH(\"${PIPELINE_ID}\", ARRAYJOIN({Pipeline}))" \
  --data-urlencode "fields[]=fldWzo3ZUygqaiwyB"
```

If any records are returned, delete them in batches of up to 10:

```bash
# Repeat for each batch of up to 10 record IDs
curl -s -X DELETE "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "records[]=recAAA" --data-urlencode "records[]=recBBB"
```

---

## STEP 4 — Build the 7-day itinerary plan

Using the island knowledge below and the guest context from Steps 1–2, generate a day-by-day plan for the 7 nights.

### Island knowledge

**Fixed anchors (always schedule):**
- **Day 2 or 3 — Flamingo Walk** at Landhuis Daniel or Chogogo. Morning only. Skip for infants.
- **Wednesday evening — Sunset Club** (fixed TC event). All groups attend.
- **One afternoon — Boat Day** (snorkelling, Caribbean sea). Central week. Not Days 1 or 7.
- **One dinner — Plasa Bieu** (local food market). Best Tue–Fri.
- **One dinner — Culinary Pass restaurant** (Boathouse / Gesto / Zanzibar). Always one Culinary Pass evening.
- **One morning — Flamingo Beach** at Jan Thiel. Calm, shallow, suits all types.

**Guest-type rhythm:**
- **Young family**: nap window 1 PM sacred, no evening activities after 8 PM, Poko Poko beach over party beach.
- **Teen family**: 10 AM starts, Mambo Beach, padel afternoon, snorkelling.
- **Couple**: fully flexible, romantic dinner option (Karakter), Poko Poko afternoons.
- **Friends**: sunset drinks on the deck, Jaanchie's for lunch, late evenings fine.

**Days 1 & 7:** Keep light. Day 1: afternoon arrival, evening settle in + welcome drinks. Day 7: morning at the villa + departure after breakfast.

**Voice reminder:** You have the Tommy Coconut Voice Bible loaded above. Body text must pass the Voice Bible sanity check — no banned words, Stage 3 register (first names, warm, direct, specific), one Papiamentu flavor word across the whole itinerary.

---

## STEP 5 — Write itinerary items to Airtable

For each activity block, create a record in `Itinerary Items V2` using the REST API. Batch up to 10 records per request.

```bash
curl -s -X POST "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "fields": {
          "fldWzo3ZUygqaiwyB": ["PIPELINE_ID"],
          "fldPlg98rFGiaCCSH": 1,
          "fldDekHGP9CCIfgJl": "Morning",
          "fldQx8ZJCw7Mw652T": "9:00 AM — Flamingo Walk",
          "fldBcHXSRTzi6Tqg6": "Body text here.",
          "fldwpxPJaMXbSd3P5": 1,
          "fldt7AsmEOz8Jgzc0": "Draft",
          "fldWdPQqDdfQ1gnEc": "Optional pro tip.",
          "fldAkfpwgSUP8tVWG": true
        }
      }
    ]
  }'
```

**Field reference:**

| Field | Field ID | Type | Notes |
|---|---|---|---|
| Pipeline | `fldWzo3ZUygqaiwyB` | Array | `["PIPELINE_ID"]` — array with one record ID |
| Day Number | `fldPlg98rFGiaCCSH` | Number | 1–7 |
| Slot | `fldDekHGP9CCIfgJl` | Select | `"Morning"` / `"Afternoon"` / `"Evening"` / `"All-Day"` |
| Header | `fldQx8ZJCw7Mw652T` | Text | Time-block label e.g. `"9:00 AM — Flamingo Walk"` |
| Body Text | `fldBcHXSRTzi6Tqg6` | Text | 2–4 sentences in TC voice |
| Sort Order | `fldwpxPJaMXbSd3P5` | Number | Sequential across all records |
| Status | `fldt7AsmEOz8Jgzc0` | Select | `"Draft"` |
| Base Pro Tip | `fldWdPQqDdfQ1gnEc` | Text | Optional practical tip |
| Show Pro Tip | `fldAkfpwgSUP8tVWG` | Checkbox | `true` if Base Pro Tip is non-empty |

**Aim for 3–5 activity blocks per day.** Total records: 21–35.

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
