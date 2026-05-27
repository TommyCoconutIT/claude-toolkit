---
name: dushi-week-airtable-tasks
description: Headless, automated variant of the Dushi Week builder. Reads a lead Pipeline record from Airtable, copies the matching segment template from Itinerary Items V2 verbatim, and writes the records linked to that Pipeline. Then outputs personalization suggestions for human review. No human gates, no HTML, no microsite — just the Airtable tasks. Triggered by GitHub Actions on every new lead.
---

# dushi-week-airtable-tasks

Automated itinerary task generator for Tommy Coconut Private Resorts.
You are running **headlessly** in GitHub Actions — no human is watching.
Use `bash` (curl) for all Airtable reads and writes. The `AIRTABLE_API_KEY` environment variable is already set.

**Core rule: do NOT write copy from scratch. Pull the segment template from Airtable and copy it verbatim. Only the Pipeline link changes. Personalization suggestions are output as text at the end — they are NOT written to Airtable.**

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
- Motivation ("What made you decide to do this now?") — used for personalization suggestions only

---

## STEP 2 — Determine guest type & template record ID

Using `Segment`, adult/child/infant counts, and quiz answers, classify into one of the six segments and look up its template Guest Record ID:

| Guest type | When | Template Guest Record ID |
|---|---|---|
| **couple** | 2 adults, no kids | `rec7QFzJ2s342F0IZ` |
| **friends** | 3+ adults, no kids | `rec2R9SiqXz5VUQVX` |
| **family-teens** | kids 10–17 | `recX78q5CWqslAm1e` |
| **family-young-kids** | children under 10 | `recjG9FwdBH0683UX` |
| **family-young-adults** | kids 18–25 | `recptPrA2LnvarKhu` |
| **multi-gen** | mixed adults + kids across age brackets | `reczs1Jiwbh6BVMQO` |

⚠️ If `multi-gen` is selected, note that Days 7–8 are missing from the template — flag this in the summary output.

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

## STEP 4 — Fetch the segment template items

Pull all template items for the guest's segment. Filter by the Template Guest Record ID from Step 2 using field `fldjwBB7eAU9BPa8j`. Sort by day number ascending.

```bash
TEMPLATE_GUEST_ID="rec7QFzJ2s342F0IZ"  # replace with actual value from Step 2

curl -s "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "filterByFormula=SEARCH(\"${TEMPLATE_GUEST_ID}\", ARRAYJOIN({fldjwBB7eAU9BPa8j}))" \
  --data-urlencode "sort[0][field]=fldPlg98rFGiaCCSH" \
  --data-urlencode "sort[0][direction]=asc"
```

Page through all results using the `offset` parameter if needed (Airtable returns max 100 records per page).

For each template record, store:
- `fldPlg98rFGiaCCSH` — Day Number
- `fldDekHGP9CCIfgJl` — Slot
- `fldQx8ZJCw7Mw652T` — Header
- `fldBcHXSRTzi6Tqg6` — Body Text
- `fldwpxPJaMXbSd3P5` — Sort Order
- `fldWdPQqDdfQ1gnEc` — Base Pro Tip
- `fldAkfpwgSUP8tVWG` — Show Pro Tip

---

## STEP 5 — Write itinerary items to Airtable

For each template record fetched in Step 4, create a new record in `Itinerary Items V2` linked to the new Pipeline. **Copy every field value verbatim from the template — do not rewrite body text or pro tips.** Only the Pipeline link is different.

Batch up to 10 records per POST request:

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
          "fldQx8ZJCw7Mw652T": "<header from template>",
          "fldBcHXSRTzi6Tqg6": "<body text copied verbatim from template>",
          "fldwpxPJaMXbSd3P5": 1,
          "fldt7AsmEOz8Jgzc0": "Draft",
          "fldWdPQqDdfQ1gnEc": "<pro tip copied verbatim from template>",
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
| Day Number | `fldPlg98rFGiaCCSH` | Number | copied from template |
| Slot | `fldDekHGP9CCIfgJl` | Select | copied from template |
| Header | `fldQx8ZJCw7Mw652T` | Text | copied from template |
| Body Text | `fldBcHXSRTzi6Tqg6` | Text | **copied verbatim — do not rewrite** |
| Sort Order | `fldwpxPJaMXbSd3P5` | Number | copied from template |
| Status | `fldt7AsmEOz8Jgzc0` | Select | always `"Draft"` |
| Base Pro Tip | `fldWdPQqDdfQ1gnEc` | Text | copied from template |
| Show Pro Tip | `fldAkfpwgSUP8tVWG` | Checkbox | copied from template |

---

## STEP 6 — Output personalization suggestions

After all records are written, print a **Personalization Suggestions** block. This is text output only — do NOT write these to Airtable. A human will review and apply approved changes manually.

Based on the quiz answers (dietary flags, motivation, activity wishlist, group composition), identify 3–8 specific itinerary items where a small copy change would meaningfully personalize the experience for this guest.

Format each suggestion as:

```
📝 Day <N> — <Slot> — <Header>
   Current: "<first sentence of current body text>"
   Suggested: "<proposed replacement sentence>"
   Reason: <one line — what quiz data drives this change>
```

Only suggest changes that are grounded in actual quiz answers. Do not hallucinate backstory. If the quiz answers don't surface anything actionable, output fewer suggestions or none.

---

## STEP 7 — Done

Print a short summary:

```
✅ Itinerary tasks written for pipeline_id: <id>
   Guest: <FirstName> <LastName> (<email>)
   Segment: <guest type>
   Dates: <arrival> → <departure>
   Template records copied: <count>
   Personalization suggestions: <count> (see above — not written to Airtable)
```

Do not update the Pipeline status. Do not open a PR. Do not write HTML. Your job is done.
