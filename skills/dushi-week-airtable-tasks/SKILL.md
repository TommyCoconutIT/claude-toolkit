---
name: dushi-week-airtable-tasks
description: Headless, automated variant of the Dushi Week builder. Reads a lead Pipeline record from Airtable, copies the matching segment template from Itinerary Items V2 verbatim, then analyzes quiz answers and outputs personalization suggestions as text for human review. No PATCH calls, no HTML, no microsite — just the Airtable tasks. Triggered by GitHub Actions on every new lead.
---

# dushi-week-airtable-tasks

Automated itinerary task generator for Tommy Coconut Private Resorts.
You are running **headlessly** in GitHub Actions — no human is watching.
Use `bash` (curl) for all Airtable reads and writes. The `AIRTABLE_API_KEY` environment variable is already set.

**Three-phase flow:**
1. Read Pipeline `Segment` → pick the matching Template Trip → copy its Itinerary Items V2 records 1:1
2. Analyze quiz answers → output Voice Bible-compliant personalization suggestions as text
3. Print summary — suggestions are NOT applied to Body Text until human approval

**Never write or PATCH records based on personalization. Never invent backstory.**

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

## STEP 2 — Determine segment & template Trip

Read `Segment` (`fldnh3gJKZH9BQS8s`) from the Pipeline record. This is the **only** source for picking the template — do not re-derive segment from adult/child counts or quiz answers.

Map the Pipeline segment value to the exact **Template Trip Nickname** in the Trips table:

| Pipeline `Segment` | Template Trip Nickname | Expected item count |
|---|---|---|
| `couple` | `Template Couple` | 19 |
| `friends` | `Template Friends` | 19 |
| `family-young-kids` | `Template Family young kids` | 16 |
| `family-teens` | `Template Family teens` | 17 |
| `family-young-adults` | `Template Family young adults` | 17 |
| `multi-gen` | `Template Multi gen` | 16 |

If `Segment` is blank, halt and print an error — do not guess.

Optionally verify the template Trip exists:

```bash
TEMPLATE_NAME="Template Couple"  # from table above

curl -s "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblomZtSy0qeghyPE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode 'filterByFormula={Trip Nickname}="'"${TEMPLATE_NAME}"'"' \
  --data-urlencode "fields[]=Trip Nickname" \
  --data-urlencode "fields[]=Segment"
```

You should get exactly one Trip record back. Store its record ID for logging — but **do not** use `{Trip} = "recXXX"` as a filter on Itinerary Items (that formula does not match via the REST API in this base). Use the Trip Name lookup filter in Step 4 instead.

⚠️ **Never filter template items by Guest Record ID or `Guests Total (lookup)`.** All six template Trips share the same template guest (`rec7QFzJ2s342F0IZ`). Filtering by guest ID returns a mixed bag of items from every template — that is the bug you must avoid.

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

## STEP 4 — Fetch the template week (1:1 source)

Pull **every** Itinerary Items V2 record belonging to the template Trip — and **only** that Trip.

Use the full Template Trip Nickname from Step 2 in a `Trip Name (lookup)` filter. Use the **complete name** (e.g. `Template Family young kids`, not `Template Family young`) to avoid matching the wrong family template:

```bash
TEMPLATE_NAME="Template Couple"  # exact value from Step 2 table

curl -s "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode 'filterByFormula=SEARCH("'"${TEMPLATE_NAME}"'", ARRAYJOIN({Trip Name (lookup)}))' \
  --data-urlencode "sort[0][field]=fldPlg98rFGiaCCSH" \
  --data-urlencode "sort[0][direction]=asc" \
  --data-urlencode "sort[1][field]=fldwpxPJaMXbSd3P5" \
  --data-urlencode "sort[1][direction]=asc"
```

Page through all results using the `offset` parameter (max 100 records per page).

**Validation — halt if this fails:**
- Record count must exactly match the Expected item count from Step 2
- Every returned record's `Trip Name (lookup)` must contain the template name
- If count is wrong or any record belongs to a different template, **stop** — do not write anything

For each template record, store these **writable** fields (by field ID):

| Field | Field ID | Copy? |
|---|---|---|
| Activity Catalog | `fldgERH9Wh0Pl9zkp` | ✅ yes |
| Day Number | `fldPlg98rFGiaCCSH` | ✅ yes |
| Slot | `fldDekHGP9CCIfgJl` | ✅ yes |
| Header | `fldQx8ZJCw7Mw652T` | ✅ yes (if present) |
| Body Text | `fldBcHXSRTzi6Tqg6` | ✅ yes — verbatim |
| Sort Order | `fldwpxPJaMXbSd3P5` | ✅ yes (if present) |
| Status | `fldt7AsmEOz8Jgzc0` | ✅ yes — copy from template |
| Base Pro Tip | `fldWdPQqDdfQ1gnEc` | ✅ yes — verbatim |
| Show Pro Tip | `fldAkfpwgSUP8tVWG` | ✅ yes (if present) |
| Show About | `fldnO7FOyDt9WVqxE` | ✅ yes (if present) |
| About Story | `fldt4lKoGD8iJbVi5` | ✅ yes (if present) |
| Is Hero For Day | `fldH4nM55rGIyxYxn` | ✅ yes (if present) |
| Manual Override Reason | `fldy9Dpgfhx2zXsJj` | ✅ yes (if present) |

**Do NOT copy** these (lookups, formulas, or wrong links):
- `Trip` — template Trip link stays on the template; new items link to Pipeline only
- `Pipeline` — set to the new lead's Pipeline ID in Step 5
- `Custom Notes` — leave blank (Step 6 writes AI suggestions here)
- Any field ending in `(lookup)` or `(from …)` — computed, not writable
- `Item Name` — formula field

---

## STEP 5 — Write itinerary items to Airtable (1:1 clone)

Create **exactly one new record per template record** — same count, same fields, same values. The **only** differences from the template are:
1. `Pipeline` link → the new lead's `PIPELINE_ID`
2. No `Trip` link (lead-stage items are Pipeline-only until booking)

**Do not add, remove, reorder, or rewrite any template items.** Do not pull activities from Activity Catalog separately. Do not invent slots.

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
          "fldgERH9Wh0Pl9zkp": ["ACTIVITY_CATALOG_ID_FROM_TEMPLATE"],
          "fldPlg98rFGiaCCSH": 1,
          "fldDekHGP9CCIfgJl": "Morning",
          "fldQx8ZJCw7Mw652T": "<header copied verbatim>",
          "fldBcHXSRTzi6Tqg6": "<body text copied verbatim>",
          "fldwpxPJaMXbSd3P5": 110,
          "fldt7AsmEOz8Jgzc0": "Suggested",
          "fldWdPQqDdfQ1gnEc": "<pro tip copied verbatim>",
          "fldAkfpwgSUP8tVWG": true
        }
      }
    ]
  }'
```

After all batches complete, verify: `records_created == template_records_fetched`. If not, report the mismatch in the summary.

**Field reference (writes only):**

| Field | Field ID | Notes |
|---|---|---|
| Pipeline | `fldWzo3ZUygqaiwyB` | `["PIPELINE_ID"]` — the only link on lead-stage items |
| Activity Catalog | `fldgERH9Wh0Pl9zkp` | copied from template |
| Day Number | `fldPlg98rFGiaCCSH` | copied from template |
| Slot | `fldDekHGP9CCIfgJl` | copied from template |
| Header | `fldQx8ZJCw7Mw652T` | copied from template |
| Body Text | `fldBcHXSRTzi6Tqg6` | **copied verbatim — do not rewrite** |
| Sort Order | `fldwpxPJaMXbSd3P5` | copied from template |
| Status | `fldt7AsmEOz8Jgzc0` | copied from template |
| Base Pro Tip | `fldWdPQqDdfQ1gnEc` | copied from template |
| Show Pro Tip | `fldAkfpwgSUP8tVWG` | copied from template |
| Show About | `fldnO7FOyDt9WVqxE` | copied from template (if set) |
| About Story | `fldt4lKoGD8iJbVi5` | copied from template (if set) |
| Is Hero For Day | `fldH4nM55rGIyxYxn` | copied from template (if set) |
| Manual Override Reason | `fldy9Dpgfhx2zXsJj` | copied from template (if set) |

---

## STEP 6 — Generate and store personalization suggestions

Re-read the quiz answers extracted in Step 1. For each answer, ask: **does any written itinerary record have a sentence where inserting a real detail from this answer would make it feel written for this specific guest?**

Rules:
- Only use quiz data that is factual and specific (dietary restriction, named activity wish, named reason for trip, group detail)
- Maximum one suggestion per record — one surgical sentence swap or insert, not a rewrite
- 3–8 suggestions is the target. If quiz answers are sparse, produce fewer or none
- Do not invent context not present in the quiz

Voice Bible rules apply to every suggested sentence:
- No banned hospitality words (nestled, pampered, tranquil, exclusive, curated, seamless, world-class, unforgettable)
- Specific over generic — real names, real times, real details from the quiz
- Objects have feelings, Tommy leads, guest follows
- Never invent a fact not present in the quiz data

### 6a — PATCH each suggested record's Custom Notes field

For each suggested item, PATCH its `Custom Notes` field (`fldzXDgi0Es2J77Sb`) with the following two-line format. **Do NOT touch `Body Text` (`fldBcHXSRTzi6Tqg6`) — the template copy stays unchanged until the human accepts.**

```
[AI] <proposed replacement body text — 1–2 sentences, Voice Bible compliant>
Reason: <one line — which quiz answer drives this change>
```

```bash
curl -s -X PATCH "https://api.airtable.com/v0/appFRLV1H76ohiIQS/tblrehbZFtArMtwr5/<recordId>" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "fldzXDgi0Es2J77Sb": "[AI] <suggested body text>\nReason: <reason>"
    }
  }'
```

### 6b — Print summary to stdout

After all PATCHes, print a readable summary:

```
📝 Day <N> — <Slot> — <Header>
   Current: "<first sentence of the current body text>"
   Suggested: "<same text written to CUSTOM_NOTES after [AI] prefix>"
   Reason: <reason>
```

---

## STEP 7 — Done

Print a short summary:

```
✅ Itinerary tasks written for pipeline_id: <id>
   Guest: <FirstName> <LastName> (<email>)
   Segment: <segment>
   Template Trip: <Template Trip Nickname>
   Dates: <arrival> → <departure>
   Template records fetched: <count> (expected: <expected count>)
   Records created: <count>
   Personalization suggestions: <count> (stored in Custom Notes — awaiting human accept/decline in portal)
```

Do not update the Pipeline status. Do not open a PR. Do not write HTML. Do not PATCH Body Text. Your job is done.
