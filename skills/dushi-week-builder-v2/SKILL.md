---
name: dushi-week-builder-v2
description: "V2 — Airtable-first itinerary builder for Tommy Coconut Private Resorts. Use this skill whenever building, editing, or updating a Dushi Week itinerary for any TC guest. Content (day blocks, activity copy) is pulled live from Airtable Itinerary Items V2 — Airtable is the single source of truth. The HTML shell provides structure only. Personalization (letter, cover, tokens, closing) is written per guest. Output is a complete HTML itinerary ready for microsite handoff. Triggers: 'itinerary', 'Dushi Week', 'guest week', 'trip plan', 'schedule their week', any reference to planning a TC guest stay in Curaçao."
---

# Dushi Week Builder — V2 (Airtable-First)

## ⚠️ STEP ZERO — Read Before Anything Else

**Before writing a single word — read `references/lessons-learned.md`.** This document is the institutional memory of every Dushi Week ever built. It contains every mistake, correction, dangerous pattern, liability rule, and hard-won insight from real builds. Read it first. Every time. No exceptions.

Then follow the Pre-Build Checklist in Section 16 of lessons-learned.md.

---

## STEP 0.5 — Look Back (Dushi Week Registry)

Every Dushi Week is logged in Airtable. Check it BEFORE you build, update it AFTER you ship.

- **Where:** base `appFRLV1H76ohiIQS` → table **"Dushi Weeks"** (`tblGHUrF6PGkqrnn3`)
- **Before building:** search by guest email (dedupe), find nearest prior build by Estate + Variant, take `max(Build #) + 1`, check for returning guest (Departed/Alumni row)
- **After shipping:** log Microsite URL + Pipeline ID + itinerary file path, set Status, keep All-in price in sync with Pipeline.Total Amount

---

## Architecture — Three Layers

Every itinerary is built from three distinct layers. Understanding this is the foundation of the V2 workflow.

### Layer 1 — Structure (HTML Shell)
The HTML shell provides the visual container: CSS design tokens, page layout, class names, typography, color palette. It does **not** contain day content. It lives in `references/itinerary-standard-sat-to-sat--couple.html` (couple variant) and is the starting point for all HTML output. The shell barely changes between builds — only the structure matters here, not the words inside it.

### Layer 2 — Content (Airtable — Single Source of Truth)
Day content lives in **Airtable Itinerary Items V2** (base `appFRLV1H76ohiIQS`). Six segment templates exist, each containing the complete day-by-day activity blocks for that guest type. When Ray or Britt update a block in Airtable, that update flows into every future build automatically — no file needs to be re-uploaded or re-synced.

**Never invent day content from memory. Always pull from Airtable.**

### Layer 3 — Personalization (Per-Guest Writing)
Cover page, personal letter, philosophy page, Week at a Glance, closing page, and any guest-specific inserts/swaps. This is the only layer that gets written fresh each build. Everything else comes from Layers 1 and 2.

---

## The Six Segment Templates

| Segment | Airtable Guest Record ID | Items | Notes |
|---|---|---|---|
| Couple | `rec7QFzJ2s342F0IZ` | 19 | Complete. HTML shell available. |
| Friends | `rec2R9SiqXz5VUQVX` | 19 | Complete. Airtable only. |
| Family teens | `recX78q5CWqslAm1e` | 17 | Complete. Airtable only. |
| Family young kids | `recjG9FwdBH0683UX` | 16 | Complete. Airtable only. |
| Family young adults | `recptPrA2LnvarKhu` | 17 | Complete. Airtable only. |
| Multi gen | `reczs1Jiwbh6BVMQO` | 12 | ⚠️ Days 7–8 missing — flag to Ray before starting. |

To pull template items for a segment: `list_records_for_table` on Itinerary Items V2, filter by the Guest Record ID above (field `fldjwBB7eAU9BPa8j`), sort by day number (`fldPlg98rFGiaCCSH` asc) then time-of-day.

---

## Build Workflow — Four Steps

### Step 1 — Identify & Pull
1. Confirm guest segment (Couple / Friends / Family teens / etc.)
2. Check Dushi Week Registry for dedupe + returning guest flag
3. Pull all template items for that segment from Itinerary Items V2 (sorted by day → time-of-day)
4. Pull the HTML shell from `references/itinerary-standard-sat-to-sat--couple.html`

### Step 2 — Personalize Tokens
Replace all tokens in the shell. Do not touch day content yet.

| Token | Replaces With |
|---|---|
| `{Basecamp}` | Villa name (e.g., "Dushi Hideaway") |
| `{First Name}` | Primary guest first name |
| `[Crew name]` | Cartel name (e.g., "The Wyand Cartel") |
| `[Guest first names]` | All guests (e.g., "Lori & Scott") |
| `[Hometown]` | City they're from |
| Dates on cover | Arrival and departure dates |

### Step 3 — Write Personal Sections
Write fresh for this guest (use tommy-coconut-voice skill):
- **Cover page** — tokens only, no prose
- **Philosophy page** — standard text + one personalized paragraph connecting their life to the POKO POKO philosophy. Add a returning-guest sentence if 2CCM+.
- **Personal letter** — the heart of the build. Research the guest, write from real facts only (no hallucinated backstory). See lessons-learned.md Section 1.
- **Week at a Glance** — update if the day schedule was adjusted from the template
- **Closing page** — short, emotional, personalized H2

### Step 4 — Apply Guest-Specific Inserts/Swaps
Any changes the user requested beyond the template (new breakfast block, upsell box, venue swap on one day). For each change:
1. Check Activity Catalog first (`fldJx3o8AKlPzFQSv` = couple variant copy, `fldtIcAZltENxFR4U` = pro tip)
2. Check Itinerary Items V2 for this guest's specific records
3. If not in either table, write in the same style as a comparable block in the template
4. Restaurant-about card: first occurrence only

**Never rewrite day blocks that weren't explicitly requested.**

---

## Copy Rules

### Copy 1 vs Copy 2
- **Copy 1** — First-visit framing. "Brisa Do Mar. Pop's Place. Caracasbaai waterfront..."
- **Copy 2** — Return-visit framing. Used when: (a) venue appears twice in the same week, OR (b) guest is returning (2CCM+) and has visited before. "You know this table already..."

### Pricing Framing
- **One Coconut** → Culinary Pass, $35/person/dinner, "CP X of 5"
- **Two Coconut** → "Included — Two Coconut" everywhere. Search draft for "$35" and "credit" — delete any instance found.

### Restaurant-About Cards
`<div class="restaurant-about">` appears on the FIRST occurrence of a restaurant in the week only. If adding a restaurant to an earlier day than its existing card, move the card to the earlier day and remove it from the later one.

---

## What You Need From the User

### Required
1. **Guest names** — Full names, children's ages if applicable
2. **Trip dates** — Arrival and departure, flight numbers if available
3. **Villa assignment** — Which TC villa
4. **Guest segment** — Determines which Airtable template to pull (see The Six Segment Templates above)
5. **Package** — One Coconut or Two Coconut (drives pricing framing throughout)
6. **Dietary restrictions / allergies** — Critical for every restaurant mention
7. **Cruise ship calendar** — For their week (drives beach vs. city scheduling)

### Highly Valuable
8. **Guest backstory** — Work, life situation, how long since last real vacation, hobbies. The letter is only as good as the real details behind it.
9. **Crew name** — TC gives every group a name ("The Wyand Cartel"). Suggest one if not chosen.
10. **Returning guest context** — Prior stay details, what they loved, what they mentioned in WhatsApp
11. **Special requests** — Extra massages, excursions, romantic additions, kid-specific needs

### Defaults
- **Sunset Club**: Always Wednesday (fixed TC event)
- **Flamingo Hike**: Any weekday 7 AM, suggest Monday
- **8th Night Buffer**: Always included — late checkout on departure day
- **Private Chef BBQ**: All-In package ONLY — confirm with Ray before including

---

## Guest Segments — Rhythm & Language Guide

### Couple (no kids)
- **Rhythm**: Fully flexible. Build in POKO POKO time. Couples need unscheduled hours, not a packed agenda.
- **Language**: Intimate, warm. "This week belongs to the two of you."
- **Highlights**: Booker's massage, Sunset Club, romantic dinner at De Gouverneur, Boat Day, golden hour photos
- **Template**: `rec7QFzJ2s342F0IZ`

### Friends Group
- **Rhythm**: Flexible, social, higher energy. Later nights viable.
- **Language**: Crew energy. Banter-friendly. "Nobody remembers the quiet vacation."
- **Highlights**: Boat Day, Line Fishing (Day 3 PM), Mei Mei salsa night, Mambo nightlife, west coast adventure
- **Template**: `rec2R9SiqXz5VUQVX`

### Family — Teens (10–17)
- **Rhythm**: No nap. Teens sleep in — morning activities from 10 AM. Some activities split parents/teens.
- **Language**: Acknowledge the teens directly. "This isn't a parent trip you're dragged along on."
- **Highlights**: Snorkeling, Flamingo Hike, Boat Day, Mambo Beach Boulevard, Culture Walk as "urban exploration"
- **Template**: `recX78q5CWqslAm1e`

### Family — Young Kids (under 10)
- **Rhythm**: Nap window SACRED for under-5 (~1 PM, 60–90 min). Bedtime 8 PM. Every activity works around this.
- **Language**: Warm, grounding. Kid-specific section in Good to Know.
- **Highlights**: Flamingos, Papagayo shallow water, Boat Day with life jacket, Sea Aquarium, early dinners
- **Template**: `recjG9FwdBH0683UX`

### Family — Young Adults (18–25)
- **Rhythm**: Fully flexible. Everyone is an adult. Some activities split (parents one thing, adult kids another).
- **Language**: Peer energy. Adult kids are vacation partners, not dependents. Name them individually.
- **Highlights**: Guided Snorkel, Boat Day, nightlife options for adult kids, adventurous food, intro dive
- **Template**: `recptPrA2LnvarKhu`

### Multi Gen (grandparents + parents + kids)
- **Rhythm**: Complex — balance multiple generations. Grandparents may need rest. Split options are key.
- **Language**: Acknowledge each generation. "Three generations. One island. Zero agendas."
- **⚠️ Note**: Days 7–8 missing from template. Flag to Ray before starting.
- **Template**: `reczs1Jiwbh6BVMQO`

---

## The Obligation Rule

**TC community activities go in the "What's Happening at Tommy Coconut Today" info box ONLY — never in the main day timeline.**

Main timeline = activities built FOR this guest (their boat day, their dinner, their Sunset Club).
TC Today box = things the TC family is doing today. Guests opt in via WhatsApp if interested.

Activities always in TC Today box only:
- Line Fishing with Boy & Britt (Mondays, Caracas Bay ~4 PM)
- Reef Snorkeling with Raymonde (Tuesdays, 9 AM, Tugboat Beach)
- Give Back Locally (Fridays, 10–11:30 AM)
- Padel (Saturdays, 09:00–11:00 AM)

Exception: Private Boat Day with Captain Mike IS in the main timeline — it's built for the guest.

---

## The Cruise Ship Rule

The cruise ship calendar drives the entire week's scheduling. This is non-negotiable.

- **Zero-ship days** → Beach hopping, west coast, popular beaches
- **Heavy-ship days (5,000+ pax)** → Willemstad (cruise energy makes the city alive), Mambo Boulevard, Caracasbaai, estate day
- **Light-ship days (<2,000 pax)** → Flexible, most spots are fine
- **Always include cruise intel** at the top of each day block

Source: CruiseTimetables.com. Verify day-of-week labels against an actual calendar — web snippets mislabel days. See lessons-learned.md Section 12 for verification method.

---

## New / Unknown Activities — Operator Research Protocol

For any activity not run by the TC crew and not documented in `references/island-database.md`, **never invent an operator, location, hours, price, or contact.** Protocol:

1. **Detect & batch** — collect all unverified activities into one list, don't ask one-by-one
2. **Ask the user** (one pass) — "Do you have a preferred operator for any of these?"
3. **If named** → forensic research: official source + 2 independent corroborations, real location/hours/contact/price, cross-check every fact
4. **If not named** → research to find the best option, then same forensic check
5. **Report with source attribution**, mark verified vs. unconfirmed, get approval before writing into the itinerary
6. **Save to island-database.md** — so the next build doesn't re-research

TC-crew-run activities (flamingo hike, reef snorkel, boat day, Sunset Club, culture walk) are already verified — no research needed.

---

## Writing Voice

Load the `tommy-coconut-voice` skill before writing any content. Key rules:
- POKO POKO is always in caps, always with K (never C)
- Never use banned hospitality words (nestled, pampered, tranquil, exclusive, etc.)
- Objects have feelings ("The pool doesn't care what time it is")
- Tommy leads, doesn't serve ("The island already threw your calendar away")
- Specific over generic (real names, real places, real times)
- One Papiamentu word per section is enough
- **Never invent backstory.** Every claim in the letter must be traceable to source data (WhatsApp chat, booking form, Airtable record, verified research)

---

## Output

The output is a single HTML file: `itinerary-[cartel-name].html`, saved to the guest's working folder.

Structure:
1. Cover page (tokens)
2. Philosophy page (standard + personalized paragraph)
3. Personal letter
4. Week at a Glance (table)
5. Day pages 1–8 (from Airtable, with guest inserts applied)
6. Crew page (standard)
7. Closing page (personalized H2 + body)

After delivery, the HTML is the source document for the microsite build (`dushi-week-microsite` skill).

---

## Reference Files

Read in this order — lessons-learned corrects errors in island-database:

1. **`references/lessons-learned.md`** — MANDATORY FIRST READ. Every mistake, correction, liability rule, crew fact correction, completed build reference, and the full segment template registry (Section 20).
2. **`references/island-database.md`** — Restaurants, experiences, beaches, crew bios, scheduling constraints, add-on prices. Some entries outdated — lessons-learned.md Section 13 lists corrections that override this file.
3. **`references/itinerary-standard-sat-to-sat--couple.html`** — HTML shell for Couple builds. Structure and CSS reference for all other segments.

---

## Delivery Checklist

Before handing off:

- [ ] Correct segment template pulled from Airtable (not invented from memory)
- [ ] All tokens replaced (Basecamp, First Name, Crew name, Dates)
- [ ] Personal letter sourced from real data only — no hallucinated backstory
- [ ] Pricing framing correct: One Coconut = $35/person/CP; Two Coconut = "Included — Two Coconut"
- [ ] Dietary flags at every restaurant mention (never "it's handled" — guest tells the server)
- [ ] Obligation Rule: community activities in TC Today box only, never main timeline
- [ ] Cruise calendar applied — west coast on best zero-ship day
- [ ] Day content not rewritten beyond explicitly requested inserts/swaps
- [ ] All new copy sourced: Activity Catalog → Itinerary Items V2 → comparable item (in order)
- [ ] Restaurant-about cards on first occurrence only
- [ ] Copy 1/2 correct for returning guests and repeat venues
- [ ] New/third-party activities ran through Operator Research Protocol
- [ ] Dushi Week Registry updated (Airtable log, Status, file path)
- [ ] HTML file saved to guest's working folder, path logged in registry
