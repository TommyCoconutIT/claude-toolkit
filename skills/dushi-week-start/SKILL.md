---
name: dushi-week-start
description: Full Dushi Week pipeline. One entry point — fetches guest data from Airtable, builds the itinerary, builds the microsite, opens the PR, updates Airtable, writes the WhatsApp message. Start here for every new Dushi Week build.
---

# /dushi-week-start

Single entry point for the full Dushi Week build pipeline. You are orchestrating five steps:
fetch → build itinerary → build microsite → ship → update Airtable + write WhatsApp.

**Read `references/lessons-learned.md` inside `dushi-week-builder` before writing anything.**

---

## STEP 1 — Get the Pipeline record ID

Ask the user:
> "Paste the Pipeline record ID for this guest (starts with `rec`)."

⚠️ **Two pipeline records exist per guest — make sure you have the right one:**

| Record type | What it is | Used for |
|---|---|---|
| **Lead pipeline** | `tblb7gP5D3NYND9a0` — has Q&A, guest profile, phone, email | Fetching guest data (Step 2) |
| **Offer/payment pipeline** | Britt creates this separately — has Total Amount, Payment_Gateway="Stripe" | `bookingUrl` + `bookingPipelineId` in the microsite |

The user should paste the **offer/payment pipeline ID** — this is what the portal pay page reads at `?t=<id>`. If they paste the lead pipeline ID, the pay page won't find the record. If unsure, ask Britt which `rec…` she created for the offer.

To fetch **guest data**, search the lead pipeline table by email if needed:
- Base: `appFRLV1H76ohiIQS`
- Table: `tblb7gP5D3NYND9a0`
- Search by email field `fldvNQMiLWRW04G2Q`

---

## STEP 2 — Fetch guest data from Airtable

Fetch the Pipeline record using `list_records_for_table` with `recordIds`.

Extract these fields:

| What | Field ID | Notes |
|---|---|---|
| Guest name | `fldd9fzwjjktigoIg` | Linked record — use the `.name` value |
| Email | `fldvNQMiLWRW04G2Q` | Used for dedupe in registry |
| Phone | `fldFq2PKwy9MJi1pY` | E.g. "+1 2182341857" |
| Estate | `fld15SzszbTcHufZT` | Linked record — use the `.name` value |
| All-in price (USD) | `fldCkP5EaAocQfUeU` | Number |
| Share token slug | `fldKJaQGh2XGBDBfT` | E.g. "fairburnloriscott" |
| Payment token | `fldZIAV3Qr8RaTixS` | Ignore this field — not used for the booking URL |
| Adults count | `fld3j3KNEbByQVbyQ` | Number |
| Q&A responses | `fld85HtV5j2DDf8Z9` | JSON string — parse it |

From the Q&A JSON, extract these questions:
- `"Arrival date"` → arrival date
- `"Departure date"` → departure date
- `"Does anyone in the family have food allergies or dietary restrictions?"` → dietary
- `"Who's coming?"` → group members
- `"What made you decide to do this vacation now?"` → motivation (use in the letter)
- `"What catches your eye?"` → activity wishlist

Build the booking URL: `https://portal.tommycoconutprivateresorts.com/payments/pay?t=<pipeline_record_id>`
The `?t=` value is the Pipeline record ID (e.g. `recHq43qTtZAyFIUq`), NOT the short token in `fldZIAV3Qr8RaTixS`.

**Cover hero image — do this every build:**
1. If `fld15SzszbTcHufZT` (Basecamp/Estate) is empty on the Pipeline record, set it now: `update_records_for_table` with `{"fld15SzszbTcHufZT": ["<basecamp_record_id>"]}`.
2. Fetch the Cloudinary public ID from the Basecamps table: base `appFRLV1H76ohiIQS` → table `tblGc7g7uBedgS3Ui` → record matching the estate → field `fldwENhluLhDMIhdG` (e.g. `dushi-hideaway`, `palm-breeze`, `hh-hero-people`).
3. Build the cover image URL: `https://res.cloudinary.com/tommy-coconut/image/upload/w_1600,h_800,c_fill,g_auto,q_auto:best/<slug>`
4. Use this URL for the `cover-page::before` background in the itinerary HTML. Do NOT use the hardcoded Palm Breeze URL from the template skeleton.

---

## STEP 3 — Check the Dushi Weeks registry

In the Dushi Weeks table (`tblGHUrF6PGkqrnn3` in base `appFRLV1H76ohiIQS`):

1. **Dedupe** — search by email (`fldmR0EH5pSLGZbKK`). If a row exists, you are updating an existing build. Tell the user and show them the existing row before continuing.

2. **Next Build #** — list all records, take `max(fldgT8XqFQj1sqJMb) + 1`. This is the `<N>` in `FamilyDushiWeek<N>`.

---

## STEP 4 — Confirm with the user

Before building anything, show a confirmation block:

```
GUEST:       [name]
EMAIL:       [email]
ESTATE:      [estate]
DATES:       [arrival] → [departure]
PRICE:       $[amount]
BUILD #:     [N]
SLUG:        <FamilyPascalCase>DushiWeek<N>
BOOKING URL: https://portal.tommycoconutprivateresorts.com/payments/pay?t=[token]
DIETARY:     [dietary or "None noted"]
GROUP:       [members]
```

Ask: "Does this look right? Type `go` to start the build."

Do not proceed until the user confirms.

---

## STEP 5 — Build the itinerary

Now invoke the `dushi-week-builder` skill logic directly. You have all the guest data — do not ask the user to re-enter it. Feed it in.

Key context to pass into the builder:
- All fields from Step 2
- Build # and slug from Step 3
- Guest type (derive from the data: couple / family / friends — use adult count + "Who's coming?" answer)
- Motivation quote (from Q&A) → use verbatim in the letter, it's gold

Follow all instructions in `dushi-week-builder/SKILL.md` and its `references/` files fully.
The output is a complete printable itinerary document.

**⛔ GATE 1 — Hard stop. Say:**
> "Itinerary is ready. Boy needs to review before we build the microsite. Reply `approved` when ready."

Do not proceed until you receive `approved`.

---

## STEP 6 — Build the microsite

Invoke `dushi-week-microsite-from-itinerary` skill logic. You already have:
- The itinerary from Step 5
- The slug, booking URL, share token, price, expiry from Step 2–3

**Derive mode from the Pipeline status field (`fldvNoCtn1157G37W`) fetched in Step 2:**
- `Lead` or `Offer Sent` → `mode: "prospect"`
- `Booked` / `On Island` / `Departed` / `Alumni` → `mode: "guest"` (no offer block needed)

For prospect mode, populate the `offer` block:
```typescript
offer: {
  expiresAtISO: "<48 hours from deploy time in ISO with -04:00 offset>",
  // Reset this if you push a hotfix after initial deploy — always 48h from latest push.
  priceLabel: "$[amount] · 7 nights · [N] guests · all-in",
  shareTokenSlug: "[share_token_slug]",
  referralCreditUsd: 500,
  whatsappMessage: "Hi Britt — it's [Guest Names]. We want to lock the Dushi Week ([dates], [estate]). Send the payment link.",
  bookingUrl: "https://portal.tommycoconutprivateresorts.com/payments/pay?t=[payment_token]",
  bookingPipelineId: "[pipeline_record_id]",
  paymentAmountUsd: [amount],
}
```

Set `whatsapp.groupInviteUrl` to `"REPLACE_WITH_[FAMILY]_GROUP_INVITE"` — remind the user to fill this before sending the link.

Run `npm run typecheck` from `apps/web/`. Must exit 0.

**⛔ GATE 2 — Open the PR. Say:**
> "PR is open. Boy needs to review and merge. Reply `merged` when done."

---

## STEP 7 — Verify the deploy

After the user replies `merged`:

Poll until green:
```bash
until gh api repos/TommyCoconutIT/tommy-os/deployments \
  --jq '[.[] | select(.environment=="Production")] | first | .statuses_url' \
  | xargs gh api --jq '.[] | select(.state) | .state' | grep -q "success"; do sleep 30; done
echo "Deploy green"
```

Or just check: `gh run list --repo TommyCoconutIT/tommy-os --limit 3`

Confirm the live URL returns the correct hero Cloudinary ID with:
```bash
curl -s https://www.tommycoconutprivateresorts.com/<slug> | grep -o 'cloudinary[^"]*' | head -3
```

---

## STEP 8 — Update Airtable automatically

Once the deploy is green, update two tables without asking the user.

### Dushi Weeks table (`tblGHUrF6PGkqrnn3`)

If a row already existed (from Step 3 dedupe): update it.
If not: create a new row.

Fields to write:

| Field | Field ID | Value |
|---|---|---|
| Cartel | `fldxIghKQfJ4IwSd7` | "The [Family] Cartel" |
| Build # | `fldgT8XqFQj1sqJMb` | [N] |
| Email | `fldmR0EH5pSLGZbKK` | [email] |
| Estate | `fldHL6DdMX64gBWNs` | [estate name] |
| Arrival | `fldgbCN2bocNp9csC` | [arrival ISO date] |
| Departure | `fldiNX3g8emNAyamI` | [departure ISO date] |
| Nights | `fldBNnYlsPC8msLJH` | [number of nights] |
| Status | `fldorTqskBJLu6f47` | "Offer Sent" |
| Microsite | `fldFXPQyAm1Mwjiy2` | "https://www.tommycoconutprivateresorts.com/[slug]" |
| Built on | `fldJ4XgfFaVA3x8Yp` | today's date (ISO) |

### Pipeline table (`tblb7gP5D3NYND9a0`)

Update the Pipeline record's status field:
- `fldvNoCtn1157G37W` → "Offer Sent"

---

## STEP 9 — Write the WhatsApp message

Write the send message using the `tommy-coconut-voice` skill + `dushi-week-builder` guest type framing.

For couples use this structure (from the voice bible):
- Open by naming the Must Life they're escaping
- One line on what this week was built for, specifically for them
- The link
- Deadline (offer expiry, in island time)
- "Vacation is holy. 🥥"

Present the message to the user. Do not send it — Boy sends it.

---

## STEP 10 — Build the offer email

Generate a branded HTML offer email and save it to the guest's local folder so Boy can send it via Safari → Apple Mail.

**File path**: `~/Desktop/Leads- dushi week/[family]/email-[family]-offer.html`
(use the same folder the itinerary HTML lives in — lowercase hyphenated family name)

### Email structure

| Section | Content |
|---|---|
| **Header** | Navy bar · "Tommy Coconut Private Resorts · Curaçao" in gold, uppercase, tracked |
| **Hero** | Full-width Cloudinary estate image (`w_1200,h_640,c_fill,g_auto,q_auto:best/<estate-slug>`) with dark gradient overlay · "DUSHI WEEK™" eyebrow (gold) + cartel name (white, Playfair Display) |
| **Body** | TC voice offer copy — lead with the motivation/Must Life hook from the letter, 2–3 short paragraphs |
| **Highlights block** | Gold left-border box · "What's included" label · bullet the key inclusions (Two Coconut meals if applicable, headline experiences, iCar, concierge) |
| **CTA button** | Gold `#FFC125`, navy text, "View Your Dushi Week →" · links to microsite URL · plain URL below button for copy-paste |
| **Expiry block** | Navy bar · offer deadline in island time · price label |
| **Dietary note** | Turquoise left-border box (only if dietary restriction exists) · always puts action on guest: "let the server know" — never "TC has handled it" |
| **Signature** | Boy's name (Playfair Display), role, WhatsApp `+5999 696 8263`, `boy@tommycoconut.com` |
| **Footer** | Navy bar · "VACATION IS HOLY. 🥥" · TC address |

### Design tokens

| Token | Value |
|---|---|
| Navy | `#002D42` |
| Gold | `#FFC125` |
| Turquoise | `#7EDCD5` |
| Background | `#FDFBF7` |
| Body text | `#4A4A4A` |
| Fonts | Playfair Display + Lato (Google Fonts) |
| Max width | 620px, centered |

### Sending instructions (tell Boy after presenting the file)

1. Open the file in **Safari** (`File → Open File`)
2. `File → Share → Email This Page`
3. Apple Mail opens with the email fully rendered
4. Add the guest email as recipient and send

Present the file path to the user. Do not send the email — Boy sends it.

---

## Summary of what this skill automates vs. what stays human

| Step | Automated | Human |
|---|---|---|
| Fetch guest data | ✅ Airtable MCP | — |
| Dedupe + Build # | ✅ Airtable MCP | — |
| Write itinerary | ✅ Claude | — |
| Approve itinerary | — | ✅ Boy reviews |
| Build microsite | ✅ Claude | — |
| TypeScript check | ✅ Claude | — |
| Open PR | ✅ Claude | — |
| Merge PR | — | ✅ Boy reviews + merges |
| Verify deploy | ✅ Claude | — |
| Update Airtable | ✅ Claude | — |
| Write WhatsApp | ✅ Claude | — |
| Send WhatsApp | — | ✅ Boy sends |
| Build offer email | ✅ Claude | — |
| Send offer email | — | ✅ Boy sends |
