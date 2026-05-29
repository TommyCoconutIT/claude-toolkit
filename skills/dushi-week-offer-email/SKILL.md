---
name: dushi-week-offer-email
description: "Prepares and triggers the branded offer email for a Dushi Week lead or confirmed guest via Tommy OS. Fetches all data from Airtable (Pipeline, Basecamps, Dushi Weeks registry), writes personalized TC voice copy, populates the OfferSentMicrosite React Email template props, and updates the Pipeline status to trigger send through Tommy OS. Triggers: 'build the offer email', 'write the email', 'generate the email for [guest]', 'offer email for [cartel name]', any request to send the TC offer email after a Dushi Week itinerary or microsite has been built."
---

# Dushi Week Offer Email

Produces a single self-contained HTML file:
`~/Desktop/Leads-dushi-week/[family]/email-[family]-offer.html`

Boy opens it in Safari → File → Share → Email This Page → Apple Mail renders it → add recipient → send.

---

## Step 1 — Fetch Data from Airtable

**All data comes from Airtable. Do not invent values, do not reuse anything from the itinerary HTML skeleton. Every field below must be fetched live.**

If you already have this data from a `dushi-week-start` run in the same session, skip to the extraction table — do not re-fetch.

### 1A — Get the Pipeline record

**Base:** `appFRLV1H76ohiIQS` · **Table:** `tblb7gP5D3NYND9a0`

Search by email if you have it (`fldvNQMiLWRW04G2Q`), or use the record ID the user provides.

Fetch these fields:

| What you need | Field ID | Notes |
|---|---|---|
| Guest name | `fldd9fzwjjktigoIg` | Linked record — use `.name` value |
| Guest email | `fldvNQMiLWRW04G2Q` | Used as the To: address |
| Estate name | `fld15SzszbTcHufZT` | Linked record — use `.name` value. Also gives you the estate record ID for 1B. |
| All-in price (USD) | `fldCkP5EaAocQfUeU` | Number |
| Adults count | `fld3j3KNEbByQVbyQ` | Number |
| Nights count | Derive from Q&A "How many nights?" | From Q&A JSON |
| Package status | `fldvNoCtn1157G37W` | Lead / Offer Sent / Booked — drives prospect vs. guest mode |
| Q&A JSON | `fld85HtV5j2DDf8Z9` | Parse as JSON array — see extraction table below |

**Parse the Q&A JSON** and extract these answers:

| Q&A question | Use for |
|---|---|
| `"What made you decide to do this vacation now?"` | Motivation hook — use verbatim in body copy |
| `"Who's coming?"` | Segment (Couple / Friends / Family) |
| `"How many nights?"` | Nights count for price label |
| `"Does anyone in the family have food allergies or dietary restrictions?"` | Drives turquoise dietary box |
| `"Private Boat Adventure: which version?"` | Morning cruise (10 AM) vs. Sunset cruise (3 PM) — use correct label in inclusions |
| `"How did you find us?"` | Optional — can strengthen the body copy hook |
| `"Arrival date"` / `"Departure date"` | Dates for context |

### 1B — Get the estate Cloudinary slug

**Base:** `appFRLV1H76ohiIQS` · **Table:** `tblGc7g7uBedgS3Ui`

Use the estate record ID from the linked field in 1A. Fetch:
- `fldwENhluLhDMIhdG` — Cloudinary public ID (e.g. `dushi-hideaway`, `palm-breeze`, `hh-hero-people`)

This slug is used to build the hero image URL:
```
https://res.cloudinary.com/tommy-coconut/image/upload/w_1200,h_640,c_fill,g_auto,q_auto:best/<slug>
```

**Never hardcode an estate slug.** Always pull it from this field.

### 1C — Get the microsite URL

**Base:** `appFRLV1H76ohiIQS` · **Table:** `tblGHUrF6PGkqrnn3` (Dushi Weeks registry)

Search by guest email (`fldmR0EH5pSLGZbKK`). If a row exists:
- `fldFXPQyAm1Mwjiy2` — Microsite URL (e.g. `https://www.tommycoconutprivateresorts.com/MillmusgDushiWeek71`)
- `fldxIghKQfJ4IwSd7` — Cartel name (e.g. "The Millmusg Cartel")

If no registry row exists yet (email not sent / microsite not deployed), use what the user provides. Do not invent a URL.

### 1D — Confirm before writing

Once all three fetches are done, confirm what you have:

```
GUEST:        [name]
EMAIL:        [email]
ESTATE:       [estate name]
CLOUDINARY:   [slug]
MICROSITE:    [URL or "not deployed yet"]
PRICE:        $[amount] · [N] nights · [N] guests
PACKAGE:      One Coconut / Two Coconut
MOTIVATION:   "[verbatim Q&A answer]"
BOAT:         Morning cruise with beach BBQ / Private Sunset Cruise
DIETARY:      [restriction or "None"]
```

If anything is missing or ambiguous, ask once before proceeding.

---

## Step 2 — Write the Email Body Copy

Load the `tommy-coconut-voice` skill before writing.

The email body is 2–3 short paragraphs. Structure:

1. **Must Life hook** — open with the life they're escaping. Use the motivation quote verbatim if it exists ("For next April I turn 65" becomes "Sixty-five deserves more than a dinner reservation."). If no quote, use what you know about them (location, segment, season).
2. **The week** — one paragraph on what this specific week is built for. Name the headline experience (boat day, dive, milestone) and the estate. Keep it concrete.
3. **The move** — short. "Your Dushi Week is ready. The link is above. The offer is open until [expiry in island time]."

**No banned words.** No: nestled, pampered, tranquil, exclusive, curated, bespoke, journey, magical, unforgettable, immersive, elevated.

**No liability language.** No dietary promises ("it's handled"). No outcome guarantees.

**Sign-off:** Always "VACATION IS HOLY." — never the full "Tommy Coconut" sign-off in the body; that's in the signature block.

---

## Step 3 — Build the Inclusions Block

For **Two Coconut / Double Dushi** builds:
- "[N] nights at [Estate Name]" — use actual nights from Q&A, not "7" unless that's what the record shows
- "All meals, drinks & dining experiences included"
- "Private airport pickup + SUV for the week" — include only if Q&A "Do you want to be picked up from the airport?" = Yes and "Do you want a SUV to explore?" = Yes
- **Boat line** — use the Q&A answer from `"Private Boat Adventure: which version?"`:
  - "Morning cruise with beach BBQ" → "Private Boat Day with Captain Magic Mike (morning cruise + beach BBQ)"
  - "Sunset cruise" → "Private Sunset Cruise with Captain Magic Mike"
  - Null / no answer → omit — do not invent a boat type
- "Welcome massage for two"
- "Sunset Club Wednesday"
- "Flamingo Hike at dawn"
- "Concierge via WhatsApp — Boy, Britt & the crew"
- (any additional inclusions the user or pipeline explicitly confirms — no freelance additions)

For **One Coconut / Standard** builds:
- "[N] nights at [Estate Name]"
- "Airport pickup + SUV for the week" — same Q&A gate as above
- "Culinary Pass — 5 dinners at the island's best tables ($35/person/dinner)"
- **Boat line** — same Q&A lookup as Two Coconut above
- "Welcome massage for two"
- "Sunset Club Wednesday"
- "Flamingo Hike at dawn"
- "Concierge via WhatsApp — Boy, Britt & the crew"

Never write "$35" or mention credits in a Two Coconut build. Search the draft for "$35" and "credit" before saving — delete any instance.

---

## Step 4 — Populate the OfferSentMicrosite Template Props

The email is rendered by the `OfferSentMicrosite` React Email component in Tommy OS
(`apps/web/src/emails/offer-sent-microsite.tsx`). Do not build an HTML file. Populate the props below and pass them through Tommy OS.

### Current props (`EmailTemplateProps`)

| Prop | Type | Value to pass | Source |
|---|---|---|---|
| `guestName` | `string` | First name(s) from Pipeline name field — "You two," if no name | Step 1A · `fldd9fzwjjktigoIg` |
| `tripName` | `string` | Cartel name from Dushi Weeks registry — e.g. "The Millmusg Cartel" | Step 1C · `fldxIghKQfJ4IwSd7` |
| `arrivalDate` | `string` | ISO date — e.g. `"2027-04-25"` | Step 1A Q&A `"Arrival date"` |
| `departureDate` | `string` | ISO date — e.g. `"2027-04-30"` | Step 1A Q&A `"Departure date"` |
| `offerWeeklyRate` | `number` | Price as a number — e.g. `3800` | Step 1A · `fldCkP5EaAocQfUeU` |
| `shareUrl` | `string` | Full microsite URL | Step 1C · `fldFXPQyAm1Mwjiy2` |

### ⚠️ Template blockers — three props missing from the current template

The following props do not exist yet in `EmailTemplateProps`. Until they are added to the template, these parts of the email cannot be personalized:

| Missing prop | What it unlocks | Fix required |
|---|---|---|
| `heroCloudinaryId: string` | Estate-specific hero image — currently hardcoded to `bh-hero-with-people` (Bayside Hill) regardless of guest estate | Add prop to `EmailTemplateProps`, replace hardcoded src with `https://res.cloudinary.com/tommy-coconut/image/upload/w_1200,h_640,c_fill,g_auto,q_auto:best/${heroCloudinaryId}` |
| `bodyLines?: string[]` | Personalized body copy from Step 2 — currently hardcoded generic paragraphs | Add prop, render as `{bodyLines?.map((line, i) => <Text key={i} style={p}>{line}</Text>)}` with fallback to current hardcoded copy |
| `offerExpiresAt?: string` | Offer deadline (48h from deploy, island time) — currently the expiry block shows trip arrival date, not offer deadline | Add prop, render in the expiry `<Section>` alongside or instead of arrival date |

**When building an email:** assemble all six current props. Flag any blockers to Boy if the estate is not Bayside Hill, or if personalized copy matters for this send.

**When the blockers are fixed:** also pass:
- `heroCloudinaryId` — from Step 1B (Basecamps `fldwENhluLhDMIhdG`)
- `bodyLines` — the 2–3 paragraphs written in Step 2, as a string array (salutation as first element)
- `offerExpiresAt` — ISO datetime string, 48h from microsite deploy, UTC-4

---

## Step 5 — Trigger the Send via Tommy OS

The email is sent through Tommy OS, not via Safari or Apple Mail. Present the populated props to Boy and update Airtable — Tommy OS handles delivery.

### 5A — Present the props to Boy

Show a confirmation block:

```
TEMPLATE:      OfferSentMicrosite
guestName:     "[value]"
tripName:      "[value]"
arrivalDate:   "[ISO]"
departureDate: "[ISO]"
offerWeeklyRate: [number]
shareUrl:      "[URL]"

BLOCKERS:      [list any of the three missing props that affect this build, or "None — template is up to date"]
```

Do not trigger the send until Boy confirms.

### 5B — Update Airtable Pipeline status

Once Boy confirms, update the Pipeline record:
- **Base:** `appFRLV1H76ohiIQS` · **Table:** `tblb7gP5D3NYND9a0`
- Field `fldvNoCtn1157G37W` → `"Offer Sent"`

This status change is the signal Tommy OS reads to trigger the email send.

---

## Quick Pre-Send Checklist

Before presenting props to Boy:

- [ ] All six `EmailTemplateProps` values populated from Airtable — none invented
- [ ] `shareUrl` is the live deployed microsite URL, not a placeholder
- [ ] `offerWeeklyRate` is a number (not a string, not null)
- [ ] `arrivalDate` / `departureDate` are valid ISO strings from Q&A — flag if Q&A has mismatched dates (e.g. departure before arrival — data entry error)
- [ ] Template blockers flagged if estate is not Bayside Hill or personalized copy is needed
- [ ] Body copy (Step 2) has no banned words and no liability language
- [ ] Inclusions (Step 3) have no "$35" / "credit" in a Two Coconut build
- [ ] Pipeline status not updated to "Offer Sent" until Boy confirms

---

## Reference Files

- `~/.claude/skills/dushi-week-builder-v2/references/lessons-learned.md` — Section 2 (liability), Section 3 (One/Two Coconut pricing framing), Section 9 (voice)
- `~/.claude/skills/dushi-week-start/SKILL.md` — STEP 10 (original source of this skill), STEP 6 (offer block fields for the microsite — keep expiry in sync)
- `~/.claude/skills/dushi-week-letter/SKILL.md` — if the letter was already written, reuse the motivation hook from it rather than rewriting
