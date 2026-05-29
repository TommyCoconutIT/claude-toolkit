---
name: dushi-week-letter
description: "Writes or regenerates the 'A Letter From Tommy' personal letter for any Dushi Week lead. Fetches the segment-specific letter template from the Airtable Voice Templates table, personalizes it from the guest's quiz answers, and writes the finished letter back to the lead's Leads record as rich text. Use for first builds and letter rewrites. Triggers: 'write the letter', 'personalize the letter', 'regenerate the letter', 'letter for [guest name]'."
---

# Dushi Week Letter Writer

Writes the personal letter that opens every Dushi Week itinerary, sourced entirely from the guest's quiz answers. Writes the result directly back to the lead's record in Airtable.

---

## Step 1 — Fetch the Segment Template

Query the **Voice Templates** table:
- **Base:** `appFRLV1H76ohiIQS`
- **Table:** `tblwdtBAxzHDwLV2C` (Voice Templates)

Filter records for:
- `Segment` = the guest's segment (`couple`, `friends`, `family-young-kids`, `family-teens`, `family-young-adults`, or `multi-gen`)
- `Status` = `Approved`

Read the **Personal Letter Template** (`fldtExG9Kzn1KrYQp`) field. This is your structural skeleton — the voice scaffolding for this guest type, with `{{placeholder}}` tokens you will replace using the quiz answers.

---

## Step 2 — Fetch the Quiz Answers

Read the guest's quiz answers from the Leads record:

- **Base:** `appFRLV1H76ohiIQS`
- **Table:** `tblxw3UgaOTAmz4FQ` (Leads)
- **View:** `viwn8nJBWeXj37lKU`
- **Field:** `fldJgpYTgIENXmkOD` — Quiz Answers Raw

This is your only data source for personalization. Do not invent anything not present here.

### Name Handling — Two Modes

Determine the salutation mode from the quiz answers before writing.

**Mode A — Name in quiz answers**
Use first name(s) directly. "Lori and Scott," / "The Johnson family,"

**Mode B — Email only (no name in quiz answers)**
Try to extract a first name from the email address on the Leads record:
- Structured email (`lori.fairburn@gmail.com`) → extract "Lori". Flag it: `[UNVERIFIED — confirm with user]`
- Opaque email (`moons123@icloud.com`) → no extraction possible. Use a segment generic:
  - Couple → "You two,"
  - Friends → "Crew,"
  - Any family variant → "Friends," (until confirmed)

Never leave a `{{firstName}}` placeholder in the delivered output. Never invent a name.

---

## Step 3 — Write the Letter

Load the `tommy-coconut-voice` skill before writing.

### Structure — 5 to 8 paragraphs, no headers, no bullets

1. **Salutation** — first names (Mode A) or segment generic (Mode B)
2. **I know the week you came from** — the life they're arriving from. Use a real detail from the quiz if present. Fall back to something universally true for this guest type: "Two people who found seven days in the calendar and decided to use them."
3. **Why they're here** — ground the decision. How they found TC if in the quiz answers. What tipped them. One specific moment or signal if present.
4. **What this week is (and isn't)** — frame POKO POKO in their terms. Not a checklist. Not a schedule to keep up with. The itinerary is for once, then leave it.
5. **Named anchor moments** — optional. For milestone builds (anniversary, birthday, honeymoon), call out 2–4 moments from the actual itinerary by day. Only activities already in their week. See Milestone Rule below.
6. **The estate is ready** — "The estate is ready." Name Jeremiah and Boy where relevant.
7. **Sign-off** — VACATION IS HOLY. followed by T on its own line.

### Voice Rules

- TC Voice Stage 3 — Relationship register (warmest, most personal)
- Objects have feelings: "The rum has been waiting longer than you have."
- At least one Antillean English flip: "The island already threw your calendar away"
- One Papiamentu word (dushi, POKO POKO, bonbini) — one is enough
- POKO POKO always in caps, always with K — never "poco poco" or "Poko Poko"
- "all our energy goes into the week" — not "every dollar"
- "Every Experience Is an Invitation" — not "Gift"
- Never use "Tico Time" — say "Dushi Time" or just POKO POKO
- Banned words: nestled, pampered, tranquil, exclusive, curated, bespoke, journey, magical, unforgettable, immersive, elevated

### Liability Rules

- Never promise outcomes: "you'll feel recharged," "best vacation of your life"
- No "it's handled" or "you don't have to ask" for dietary needs — guest always tells the server
- No invented prices or add-on specifics

### Milestone Rule

For anniversary, honeymoon, or birthday builds:
- **In-person surprises (in-room champagne, flowers, airport greet, handwritten notes) NEVER appear in the letter.** These are Britt's unannounced moments — naming them destroys the surprise.
- **DO name the milestone moments the guest already chose** — call these out by day. That's how the milestone feels designed without TC making new promises.
- Pattern from Greene build: 4 anchor moments — Sunday [activity], Wednesday [Sunset Club portrait], Friday [boat trip], one guest-specific add-on. Two standard-week items + two guest-driven.

### Returning Guest Rule

When the quiz answers or context shows a prior stay:
- Lead with "You came back" framing
- Reference the specific signal that proved they'd return
- Contrast prior trip with this one if relevant
- Closing line: "[Names] — you came back. That means everything."

---

## Step 4 — Write Back to Airtable

Update the lead's record with the finished letter:

- **Base:** `appFRLV1H76ohiIQS`
- **Table:** `tblxw3UgaOTAmz4FQ` (Leads)
- **Field:** `fldpsqZHzDTqHfm3Z` — letterSuggestion (richText)

Format: plain rich text (markdown). No HTML tags. The sign-off:

```
VACATION IS HOLY.
T
```

Confirm the write succeeded before reporting done.

---

## Step 5 — Source Attribution Check

Before confirming delivery, verify every specific claim traces to the quiz answers. Flag anything assumed rather than sourced with `[UNVERIFIED — confirm with user]`.

Includes any first name extracted from an email address in Mode B.

Letters that ship with hallucinated backstory burn rewrite cycles. Section 1 of lessons-learned.md has the receipts.

---

## Reference Files

- `~/.claude/skills/dushi-week-builder-v2/references/lessons-learned.md` — Section 1 (hallucination), Section 2 (liability), Section 9 (voice + letter rules), Build #69 Greene (anniversary anchor pattern), Build #67 Lafrance (no-names salutation)
- Airtable base `appFRLV1H76ohiIQS` → **Voice Templates** table (`tblwdtBAxzHDwLV2C`) — segment letter templates (Step 1)
