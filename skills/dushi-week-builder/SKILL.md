---
name: dushi-week-builder
description: "Build personalized Dushi Week itineraries for Tommy Coconut Private Resorts guests. Use this skill whenever the user asks to create, edit, or update a guest itinerary, trip plan, Dushi Week schedule, or vacation week for any Tommy Coconut guest — whether from scratch or modifying an existing one. Also trigger when the user mentions 'itinerary', 'Dushi Week', 'guest week', 'trip plan', 'schedule their week', or any reference to planning a guest's stay in Curacao at a TC villa. This skill contains the full island knowledge database, guest type intelligence, scheduling logic, cruise ship awareness, and a verified-operator research protocol for new activities. TWO OUTPUT PATHS: (A) HTML template skeleton — when a standard HTML template exists for the variant, use it as the authoritative skeleton and only personalize tokens + specific requested blocks; (B) fresh Markdown — for new variants with no HTML template. See lessons-learned.md Section 10 and Section 20."
---

# Dushi Week Builder

## ⚠️ STEP ZERO — Read Before Anything Else

**Before writing a single word, before reading any other reference file, before asking the user anything — read `references/lessons-learned.md`.** This document contains every mistake, correction, dangerous pattern, and hard-won insight from real builds. It exists because real builds produced hallucinated content, dangerous liability language, and factual errors that cost time and created business risk. The lessons-learned document is the institutional memory of every Dushi Week ever built. Read it first. Every time. No exceptions.

After reading lessons-learned.md, also read the value stack at `tc-guest-confirmation/references/value-stack.md` (in the skills directory) — this contains the complete offer breakdown that you must understand before building any itinerary.

Then follow the Pre-Build Checklist in Section 16 of lessons-learned.md before proceeding.

---

## ⚠️ STEP ZERO POINT FIVE — Run the Pre-Build Checklist BEFORE every GATE 1

The Section 16 checklist is **not** "before you write the first word" — it's "before you ever ask Boy to review." Every time you're about to say "itinerary is ready" / "GATE 1," **literally scan**:

- **Section 16 #16 — Breakfast audit.** Every non-arrival day opens with Coffee Bike OR Brisa do Mar. No other venue. No exceptions. Coffee Bike closed Monday → Brisa.
- **Section 16 #17 — Upsell audit.** West-coast day = Frankie's + Touriffic. Mambo/Sea Aquarium day = Dolphin Swim + Mood cabana. Jan Thiel beach day = Papagayo daybed + Zest cabana. **Upsells are geography-locked — when a day's anchor changes, audit the upsells immediately.**
- **Section 16 #17a + Section 5 + Section 8 — Optional activities in info-box only.** Reef snorkel with Raymonde (Tue), line fishing (Mon), padel (Sat), Give Back Locally (Fri) go **only** in the TC Today info box, **never** in a main schedule time-block. If you see any of these in a `time-block` — delete.
- **Section 20 Token Map — Day-page h2 dates.** When arrival/departure are confirmed, every `<h2 class="day-date">` includes the real date (`Saturday · August 29, 2026`), not just the weekday.
- **Section 2 — Liability language.** No "we've handled it," "kitchen knows," "chef has been briefed," "every restaurant has been flagged." Dietary action always lives with the guest.

**Show Boy what you checked as part of the GATE 1 message** — e.g. "Audit clean: ✅ breakfast (Coffee Bike or Brisa, all 6 non-arrival days) · ✅ upsells geography-locked · ✅ optional activities info-box only · ✅ no liability language · ✅ real dates on all 8 day-page h2s." If you can't tell Boy what you checked, you didn't check it, and Boy ends up doing the audit for you. Don't.

---

## ⚠️ STEP ZERO POINT SIX — The Anti-Freelance Gate (HARD RULE, added 2026-05-28 after Build #70 Momajaa)

**You are not the writer. The voice has already been written, approved, and stored in two places: the HTML template skeleton and the Airtable Activity Catalog. You are a transcriber + personaliser. Personalisation is limited to: guest names, crew/cartel name, dates, basecamp tokens, dietary lines, and the personal letter (where the rules still apply — only sourced facts).**

### Every word in the deliverable must trace to one of four sources

Every time-block, every restaurant-about card, every info-box body, every letter paragraph, every closing line, every day subtitle, every banner title must be one of:

- **(a) Template-verbatim** — already exists in `references/itinerary-standard-sat-to-sat--couple.html` or another HTML skeleton for the segment. Copy `<h4>` and `<p>` text byte-for-byte. Swap basecamp / name / date tokens, nothing else.
- **(b) Airtable-verbatim** — pulled from Activity Catalog (couple variant field `fldJx3o8AKlPzFQSv`, pro tip field `fldtIcAZltENxFR4U`) or Itinerary Items V2 (base `appFRLV1H76ohiIQS`). Use the catalog text without paraphrasing.
- **(c) Pre-approved comparable** — only when (a) AND (b) return empty for that exact activity. Match word count, rhythm, and structure of the nearest similar template block. Flag as `[FRESH-COMP]` in the GATE 1 source table.
- **(d) Explicitly user-approved** — Boy or Ray told you in this session: "use this exact wording." Quote it back to confirm before writing.

**Nothing else is allowed in the deliverable. If a block doesn't have a source from (a), (b), (c), or (d) — leave it out.**

### If a sentence is forming in your head that isn't from one of those four sources — STOP. That sentence does not go in the deliverable.

This includes the small stuff. "Coffee Bike pulls up at the estate. Espresso, pastries, on the deck." is not in the template. "The wellness clinic comes to the estate" is — but the price you remember for additional massages probably isn't. Day subtitles like "Under the water, on the sand, on the deck" are not. Closing lines like "the kind of quiet that only POKO POKO gives you" are not. None of it goes in.

### Common failure modes the gate catches (from Build #70 Momajaa)

- **Inventing prices.** Wellness add-on prices are *not yet captured* per Section 14 of `lessons-learned.md`. "$200/person for additional massages" is unsourced. The only acceptable copy is "drop a message in the group, the wellness clinic comes to the estate." Same for any other price not in the value stack or catalog.
- **Repeating a freelance one-liner.** "Coffee Bike pulls up at Dushi Hideaway. Espresso, pastries, on the deck." appeared on multiple days in Build #70. Coffee Bike copy lives in the Activity Catalog. Pull it once and use it; vary only what the catalog varies.
- **Training-data poetry.** "The turtles came back for the fish guts. You came back for the turtles." "Cooler out. Sandwich. Repeat." "Snorkel out, look down, lose track of time." "You'll have an opinion by the bottom of the cup." "Dessert is the dance floor." All invented. Pull Piskado / Knip / Porto Mari / Pastetchi+Batido / Mei Mei copy from the template's Day 5 West Side Day and Day 3 Monday blocks.
- **Day subtitles + banner titles invented.** The template has its own subtitles. Use them or leave them blank — do not write "Water, Sun, Hands, Table" or "The long day. The best day to put it on."
- **Closing-page emotion.** "Four other people you already love, on an island that already knows your name." "One full memory card on Cameron's camera, one hardcover album in the mail." The template has a closing block. Pull it.

### MANDATORY pre-GATE-1 source attribution table

Before saying "itinerary is ready," generate this table and include it in the GATE 1 message. Every block in the file gets one row.

```
| Page | Block | Source |
|---|---|---|
| Cover | Crew name + dates | TOKEN (build inputs) |
| Philosophy | Three-options framing | template L132-139 |
| Letter | Salutation + body | LETTER-PERSONAL (drafted from sourced facts only — list every sentence not traceable to funnel/Airtable below the table) |
| Sat Arrival | Wheels Down | template L150-155 |
| Sat Arrival | Jeremiah at Hato | template L157-162 |
| Sat Arrival | Welcome at Estate | template L164-169 |
| Sat Arrival | Welcome Dinner Villa Vis | template L170-176 |
| Sat Arrival | After-dinner Zanzibar | template L184-189 |
| Sun Day 1 | Intro Dive | template L<X> (couple Day 2) |
| Sun Day 1 | Welcome Massage | template L<Y> (couple Day 2) |
| ... | ... | ... |
```

**If any row reads `FRESH (no source)` — do not call GATE 1. Re-pull from template or Airtable. If the activity genuinely has no template or catalog copy, stop and ask the user before writing fresh.**

### The principle, stated plainly

If you can't point to a line number in the template or a field in Activity Catalog for any given sentence in the deliverable — that sentence is invented, and inventions burn the user's credits on rewrite cycles. The skill exists to prevent that. Use it.

---

## STEP 0.5 — Look Back (Dushi Week Registry)

**Every Dushi Week we generate is logged in one Airtable table. Check it BEFORE you build, and update it AFTER you ship.** This is how we avoid re-research, duplicate builds, and slug-number collisions — and how we honor returning guests.

- **Where:** base `appFRLV1H76ohiIQS` → table **"Dushi Weeks"** (`tblGHUrF6PGkqrnn3`). Access via the Airtable MCP (`search_records` / `list_records_for_table` / `create_records_for_table` / `update_records_for_table`).
- **Fields:** Cartel · Build # · Email · Estate · Arrival · Departure · Nights · Guest type · Variant (🥥 One Coconut / 🥥🥥 Two Coconut) · Status (Lead → Offer Sent → Booked → On Island → Departed → Alumni) · All-in price · Microsite (URL) · Pipeline ID · Itinerary doc (path/link) · Built on · Notes.

**Before you build, run these four lookups:**
1. **Dedupe** — `search_records` the table for the guest's **email**. If a row already exists, you're continuing/updating an existing week, not starting fresh. (This is exactly the trap the Mrikaucki build hit — a half-built lead record already existed in Airtable.)
2. **Nearest template** — filter by **Estate + Variant** to find the closest prior build to copy. Same estate + same coconut count = the fastest, most accurate start.
3. **Next Build #** — use `max(Build #) + 1` for the new slug N. (Watch for collisions — #45 was used twice already.)
4. **Returning guest?** — a Departed/Alumni row for the same email/surname means prior-stay context to honor in the letter.

**After you ship, log it.** Append a new row (or update the existing one) with every field you know: link the Microsite URL + Pipeline ID + the path to the printable itinerary doc, and set Status. Keep `All-in price` in sync with `Pipeline.Total Amount`. If a lead later converts, **update** Status (Offer Sent → Booked) rather than adding a second row.

> **C-lite — don't orphan the itinerary doc.** The printable `.md` defaults to `~/Downloads`, which is machine-local and unretrievable later. At minimum record its path in the `Itinerary doc` field; better, save a copy somewhere durable (a repo dir or shared drive) and link that.

---

## What This Skill Does

This skill generates personalized 7-night itineraries for Tommy Coconut Private Resorts guests staying in Curaçao. Each itinerary is a **clean, well-structured text (Markdown) document** that reads like an invitation — not a hotel printout. It combines deep island knowledge, guest-specific personalization, cruise ship calendar awareness, and the Tommy Coconut voice.

**The deliverable is text only.** No photos, no Cloudinary, no photo picker, no HTML/PDF/DOCX export. Present the writing well — strong headings, scannable day blocks, clear time entries — but the value is in the *words and the plan*, not in image work. Skipping the photo/visual pipeline is deliberate: it used to burn the most time, focus, and tokens for the least guest value.

The itinerary is the guest's first real touchpoint with the island. It sets the tone for the entire trip. It should feel like a letter from someone who already knows them.

---

## Before You Start — What You Need from the User

To build an itinerary, you need these inputs. Ask for anything missing:

### Required
1. **Guest names** — Full names of all adults and children, with ages for kids
2. **Trip dates** — Arrival and departure dates, flight numbers if available
3. **Villa assignment** — Which TC villa they're staying at
4. **Guest type** — See [Guest Types](#guest-types) below. This fundamentally shapes the itinerary's rhythm, language, and activity mix
5. **Dietary restrictions / allergies** — Critical for restaurant and chef briefings
6. **Cruise ship calendar** — For the week of their stay (user should provide or you search for it). This drives which days get beach activities vs. city activities

### Highly Valuable (ask if not provided)
7. **Guest backstory** — What do they do for work? How long since their last real vacation? Kids' personalities? Hobbies? This is what makes the letter personal, not generic
8. **Guest nickname / crew name** — TC gives guest groups a name (e.g., "The Wyand Cartel"). If the user hasn't chosen one, suggest they create one
9. **Special requests** — Extra massages, excursions, romantic experiences, kid-specific needs
10. **Provisioning preferences** — Fridge stocking preferences, bar preferences, specific brands

### Defaults (use if not specified)
- **Culinary Pass**: 5 dinners included (standard Dushi Week package). **Pricing: $35 per person per dinner.** Calculate the total per dinner for the group (e.g., family of 3 = $105/dinner). Include this in Good to Know.
- **Nap window**: ~1 PM for toddlers, flexible for older kids, skip for adults-only and adult children
- **Date Night at the House / Private Chef BBQ**: ONLY for "All-In" payment path. Confirm with Ray before including. See lessons-learned.md Section 3.
- **Sunset Club**: Always Wednesday evening (it's a fixed TC event)
- **Flamingo Hike**: Schedule Mon-Fri, suggest Monday, note it can be moved to any weekday morning
- **8th Night Buffer**: Included — late checkout on departure day

---

## Guest Types

The guest type fundamentally shapes the itinerary — the rhythm of the day, the language used, activities suggested, and what gets emphasized or skipped. Read `references/island-database.md` for detailed scheduling variants per type.

### 1. Young Family (kids under 5)
- **Rhythm**: Nap window is SACRED (~1 PM, 60-90 min). Bedtime ~8 PM. Every activity must work around this.
- **Language**: Warm, grounding. Kid-specific section in Good to Know ("Evie's Rhythm"). Gear checklist (crib, high chair, car seat, life jacket).
- **Activities**: Flamingos (kids love them), Sea Aquarium touch tanks, shallow beach at Papagayo side of Jan Thiel, boat day with life jacket sized for child. Skip nightlife. Date Night at the House = couples' evening after kid bedtime.
- **Dining**: Flag kid-friendly restaurants. Note high chair availability. Organic milk/specific brands in provisioning.

### 2. Teen Family (kids 10-17)
- **Rhythm**: More flexible. No nap window. Teens sleep in — schedule morning activities for 10 AM, not 7 AM (except flamingos, which are optional for teens).
- **Language**: Acknowledge the teens directly. "This isn't a parent trip you're dragged along on."
- **Activities**: Snorkeling, paddleboard, ATV/UTV for older teens, boat day, padel. Sea Aquarium if younger teens. Culture walk framed as "urban exploration" not "tour."
- **Dining**: Teens eat constantly. Note lunch options everywhere.

### 3. Family with Young Adults (kids 18-25)
- **Rhythm**: Fully flexible. No nap. No bedtime. Everyone is an adult — the itinerary respects that. Some activities the whole group does together, some are split (parents do one thing, adult kids do another).
- **Language**: Peer energy. The adult kids are vacation partners, not dependents. Name them individually, write to them directly. "This is the trip where you're all just... people who love each other on a beach."
- **Activities**: Full range. Boat day, beach hopping, culture walk, reef snorkeling, padel, intro dive (adult kids may want this even if parents don't). Nightlife options for adult kids (Pietermaai strip, Mambo Boulevard evening scene). Parents might want a quieter evening while kids go out — build that optionality in.
- **Dining**: Adult kids can handle spice, adventurous food, street food. Plasa Bieu is a hit. Number 10 brunch is their scene. Culinary Pass dinners are family-together moments.
- **Special considerations**: This group often hasn't had a real family vacation since the kids were small. The emotional arc is reunion + reconnection. The personal letter should lean into this. "When was the last time all of you were in the same place with nowhere to be?"

### 4. Couple (no kids)
- **Rhythm**: Fully flexible. Romantic arc. Build in POKO POKO time — couples need unscheduled hours, not a packed agenda.
- **Language**: Intimate, warm. "This week belongs to the two of you."
- **Activities**: Boat day, beach hopping, culture walk, Date Night at the House (private chef BBQ), golden hour photos, reef snorkeling. Sunset Club is the highlight.
- **Dining**: Lean into De Gouverneur for romance. Brisa del Mar for ocean views. Pasawa for soul.

### 5. Multi-Gen (grandparents + parents + kids)
- **Rhythm**: Complex. Multiple rhythms to balance. Grandparents may need rest. Kids need naps. Parents are in the middle.
- **Language**: Acknowledge each generation. "Three generations. One island. Zero agendas."
- **Activities**: Split options are key. Some activities for everyone (flamingos, Sunset Club, boat day). Some for the active crew only (reef snorkeling, padel). Grandparents get "POKO POKO at the villa" as a real option, not a consolation prize.
- **Dining**: Dietary needs multiply. Flag everything.

### 6. Friends Group
- **Rhythm**: Flexible and social. Higher energy. Later nights.
- **Language**: Crew energy. Banter-friendly. "Nobody remembers the quiet vacation."
- **Activities**: Full adventure slate. Boat day, beach hopping, reef snorkeling, padel, nightlife. Culture walk framed as discovery + drinks.
- **Dining**: Group-friendly restaurants. Communal eating. Plasa Bieu for the experience.

---

## The Structure of a Dushi Week Itinerary

Every itinerary follows this exact structure. Don't skip sections, don't reorder them.

### Page 1: Cover
- "DUSHI WEEK™" title
- Guest crew name (e.g., "The Wyand Cartel")
- Individual names
- Trip dates
- Villa name + address (Kaya Karamele 18, Jan Thiel, Curaçao)
- "Vacation is holy. ◆"

### Page 2: The Tommy Coconut Philosophy
This page is the same for every guest, with light personalization:
- "We believe that vacation is holy."
- Explain what TC is (not a hotel, not a resort, not a rental company with a logo and a cleaning fee)
- The Dushi Life vs. The Must Life
- POKO POKO philosophy (always caps)
- Personalized paragraph connecting THEIR life to the philosophy (use guest backstory)
- "This itinerary is a proposal, not a rule" — mention they can add excursions, massages, swap days
- "Vacation is holy. ◆"

### Page 3: Personal Letter
Write a personal letter from Tommy to the guests. This is the heart of the itinerary. Rules:
- Address them by first names
- Reference their specific life situation (work, kids, how long since last trip)
- Name the crew members who are waiting for them
- Use the TC voice (load the tommy-coconut-voice skill for this)
- End with "Vacation is holy. ◆"
- Mention crew members in the letter closing (Raymonde, Boy, Britt, Jeremiah, Captain Magic Mike, Tcam, Happy & Lucky)

### Page 4: Week at a Glance
A grid/table showing all 8 days with columns: Day, Highlight, Dinner, Vibe. Keep it scannable.

### Pages 5-12: Daily Itineraries (Day 1 through Day 8)
Each day block includes:
- **Day number + date + title** (e.g., "DAY 1 — Thursday, March 19 — THE LANDING")
- **Cruise Intel alert** — Ship count, passenger count, what it means for the day
- **Time blocks** — Each activity with time, title, and rich description
- **Pro Tips** — Insider knowledge boxes
- **Alt Options** — "Not feeling it? Here's what else you could do"
- **Culinary Pass markers** — "Culinary Pass Dinner X of 5" with pricing note
- **Dietary reminders** — Flag allergies at every restaurant mention
- **Website URLs** — Include restaurant/attraction websites in italics where available

### Page 13: Good to Know
Standard sections (customize details per guest type):
- Every Experience is an Invitation, Not an Obligation
- Your Culinary Pass (pricing: $35/person/dinner, calculated total for the group)
- This is a Proposal, Not a Rule
- Dietary & Allergies (guest-specific)
- Kid's Rhythm (if applicable — nap times, bedtime, gear setup). Skip for adult-only groups.
- Scheduling Flags (what was moved/adjusted and why — e.g., "Beach hopping moved to Sunday because zero cruise ships")
- Your Wheels (iCar details)
- Beach Intel (Jan Thiel, Caracasbaai, beach kit)
- Diving (optional intro dive or guided dive — mention as available via WhatsApp group)
- The 48-Hour Guarantee (if in 48 hours it's not what we said or you expected, 100% refund)

### Page 14: Your Crew
Two tiers, written as short character intros (not job titles):
1. **Main crew** (8 members): Raymonde, Boy, Jeremiah, Captain Magic Mike, Tcam, Britt, Happy & Lucky, Cameron
2. **Founders** (separate, smaller block): Tommy Coconut (never show or describe his face — describe him by his presence), Kim (Queen of Clean), Ray (Right Hand Man)

Pull each member's bio from `references/island-database.md` (corrected by `lessons-learned.md` Section 4). In a text document, just use a clear heading per tier — no cards, borders, or color tokens.

### Page 15: Closing
Final letter. Short. Emotional. References the week's highlights. Names the crew again. Ends with:
- "Vacation is holy. ◆"
- "The treasure is out there. ◆"
- Tommy Coconut Private Resorts / Kaya Karamele 18, Jan Thiel, Curaçao

---

## New / Unknown Activities — Operator Research Protocol

**This is a hard anti-hallucination rule. It extends `lessons-learned.md` Section 1.**

Most of what goes in a Dushi Week is run by the TC crew (flamingo hike, reef snorkel, boat day, Sunset Club, culture walk, etc.) — those have *known, verified operators* (the crew) and need no research. The danger zone is anything **new or third-party** that the plan calls for or the guest requests and that does **not** already have a verified operator documented in `references/island-database.md`. Examples: **horseback riding, ATV/UTV tours, private wine tasting, cooking class, deep-sea fishing charter, kite-surf lessons, off-site spa, dolphin swim outside Sea Aquarium** — and anything a guest asks for that isn't in the database. Several entries in the add-on list are *names only* with no operator, hours, price, or contact — treat those as unknown.

For any such activity, **never invent an operator, location, hours, price, phone, website, or booking detail.** Follow this protocol instead:

### Step 1 — Detect & batch
While planning, flag every activity that lacks a verified operator. Collect them into one list. Do **not** ask one-by-one mid-build.

### Step 2 — Ask the user (one batched pass)
Before finalizing the itinerary, present the list and ask, per activity:

> "These need an operator before I can write them up — do you have a preferred operator for any of these? (e.g. horseback riding, cooking class.) If not, say so and I'll research and recommend the best one."

### Step 3a — If the user names an operator
Run **wide, deep, forensic research on THAT specific operator**:
- Confirm it actually exists and is currently operating (not closed/seasonal/defunct).
- Find the **official source** (their own website / verified social), plus 2+ independent corroborating sources.
- Pull the real facts: exact location, hours/days, contact (phone / WhatsApp / email), price, what's actually included, age & safety constraints, recent reviews/reputation.
- **Forensic fact-check:** cross-check every fact across sources. If sources disagree or you can't confirm something, say so explicitly. Never smooth over a gap with a plausible-sounding detail.

### Step 3b — If the user has no preferred operator
- Do **wide research to find the best option** — reputable, well-reviewed, appropriate for the guest type, and sensibly located relative to the villa / that day's route.
- Then run the **same deep forensic fact-check** from Step 3a on the option you chose.
- Bring back a clear recommendation **with the evidence**, not just a name.

### Step 4 — Report with sources, get approval
Present findings with **source attribution per fact** (links). Mark each fact **verified** or **unconfirmed**. Do not write the activity into the itinerary until the user approves the operator. Anything you couldn't verify gets left out or written as "to confirm" — never stated as fact.

### Step 5 — Save it so we never re-research
Once an operator is verified and approved, add it to `references/island-database.md` (with the verified details + date checked) so the next build reuses it instead of burning tokens researching again.

**Tools:** use `WebSearch` / `WebFetch` for the research. This is exactly the kind of high-risk-for-fabrication moment the hallucination rule exists for — slow down and verify.

---

## The Cruise Ship Rule — This Is Critical

The cruise ship calendar drives the entire week's scheduling. This is non-negotiable.

**The principle:** Popular tourist beaches (Playa Piskado, Grote Knip, Mambo Beach, Blue Bay) get overwhelmed on heavy cruise days. TC guests should never be sent to these spots when thousands of cruise passengers are there. Instead:

- **Zero-ship days** → Schedule beach hopping, west coast adventures, popular beaches
- **Heavy-ship days (5,000+ pax)** → Schedule downtown Willemstad (the cruise energy makes the city "flamazing"), pool days, or go to non-touristy spots like Caracasbaai. Sea Aquarium + Mambo Boulevard works great on heavy days — the boulevard thrives on the buzz.
- **Light-ship days (<2,000 pax)** → Flexible, most spots are fine
- **Always mention cruise intel** at the top of each day so guests understand why their week is scheduled the way it is

Read `references/island-database.md` for the full scheduling logic and cruise calendar integration approach.

---

## Writing Voice

The itinerary is written in the Tommy Coconut voice. Before writing any content, load the `tommy-coconut-voice` skill (V8 — The Arc + The Tokens). The voice IS the deliverable now — there are no photos or styling to lean on, so the words carry everything. Key reminders:
- POKO POKO is always in caps, always with K (never C)
- Never use banned hospitality words (nestled, pampered, tranquil, exclusive, etc.)
- Objects have feelings ("The pool doesn't care what time it is")
- Tommy leads, doesn't serve ("The island already threw your calendar away")
- Specific over generic (real names, real places, real times)
- One Papiamentu word per section is enough

---

## Output Format

**Two paths. Check the Dushi Week Registry before choosing.**

### Path A — HTML Template Skeleton (preferred for couple and returning-guest builds)

When a standard HTML template exists for the variant, open it and use it as the skeleton. **The day content in the template is the authoritative schedule — do not rewrite it.** You personalize tokens (cover, letter, philosophy, closing) and make only the specific insert/swap/remove changes explicitly requested.

- Standard template (sat-to-sat couple): `~/.claude/skills/dushi-week-builder/references/itinerary-standard-sat-to-sat--couple.html`
- Save output as `itinerary-[cartel-name].html` in the guest's working folder
- Copy source: Activity Catalog → Itinerary Items V2 → write from comparable (in that order)
- See `references/lessons-learned.md` Section 20 for the full rule set

### Path B — Fresh Markdown (new variants with no HTML template)

For guest types or variants with no existing HTML template. One deliverable: a single, clean Markdown text document. No HTML, no PDF, no DOCX, no photos. Read `references/output-pipeline.md` for how to lay the text out well.

- Strong, scannable headings (`#`, `##`, `###`) for cover, philosophy, letter, Week at a Glance, each day, Good to Know, Crew, Closing
- Week at a Glance as a Markdown table (Day | Highlight | Dinner | Vibe)
- Each day as a clear block: title line, cruise intel line, time entries, three info boxes, pro tips
- Save as `Dushi-Week-[CrewName].md`

---

## Reference Files

Read these in this order. The order matters — lessons-learned corrects errors in island-database.

1. **`references/lessons-learned.md`** — **READ FIRST. MANDATORY.** Every mistake, correction, insight, and technical lesson from real builds. Corrects errors in all other reference files. Contains the pre-build checklist, restaurant deep knowledge, crew corrections, liability rules, and completed build templates.

2. **`references/island-database.md`** — Restaurants (with URLs), experiences, beaches, crew bios, scheduling constraints, activity hours, cruise ship rules, villa details, provisioning lists, guest type scheduling variants. **Note: Some entries in this file are outdated — lessons-learned.md Section 13 lists specific corrections that override this file.**

3. **`references/output-pipeline.md`** — How to lay out the text (Markdown) itinerary so it reads beautifully: document structure, day-block format, tables, sign-offs, file naming, and the delivery checklist.

*(The old `scripts/create-docx.js` DOCX generator has been deleted — the build is text-only.)*

---

## Personalization Checklist

Before finalizing any itinerary, verify:

- [ ] Guest type identified and itinerary rhythm matches (nap windows for young families, nightlife options for adult kids, split activities for multi-gen, etc.)
- [ ] Guest names used throughout (never "Dear Guest")
- [ ] Crew name used on cover and throughout
- [ ] Backstory referenced in personal letter and woven into day descriptions
- [ ] Dietary allergies noted at every restaurant mention — but NEVER claim TC has "handled" or "flagged" it with the restaurant. The guest tells the server. See lessons-learned.md Section 2.
- [ ] Kid gear mentioned (crib, high chair, car seat, life jacket) if applicable
- [ ] Nap windows built into every day if kids are under 5
- [ ] Cruise calendar drives beach vs. city scheduling
- [ ] **Pricing framing correct for package:** One Coconut → Culinary Pass ($35/person × group, CP X of 5); Two Coconut → "Included — Two Coconut" everywhere (never "$35", never "Culinary Pass")
- [ ] Restaurant/attraction website URLs included where available
- [ ] Every TC experience marked as "included — an invitation, not an obligation"
- [ ] The Obligation Rule applied: "join us" activities in TC Today info box ONLY, never main timeline. See lessons-learned.md Section 8.
- [ ] Flexibility notes for moveable experiences (Tcam walk can sometimes move from Thursday, flamingo hike any weekday)
- [ ] Diving mentioned in Good to Know as optional add-on
- [ ] "Proposal not a rule" mentioned in philosophy AND Good to Know
- [ ] 48-hour guarantee included
- [ ] WhatsApp group referenced as the communication channel
- [ ] All crew members listed: main crew (8) + founders (Tommy, Kim, Ray)
- [ ] Tommy Coconut described by presence, never show his face
- [ ] Villa address: Kaya Karamele 18 (not Kaya Lèter C6)
- [ ] Flight numbers and times are accurate
- [ ] Culinary Pass dinners numbered correctly (X of 5)
- [ ] Any new / third-party activity (horseback riding, ATV, wine tasting, etc.) ran through the Operator Research Protocol — operator verified with sources and user-approved, nothing invented
- [ ] **Output path confirmed:** HTML template skeleton if template exists for this variant (Path A); fresh Markdown if not (Path B). See lessons-learned.md Section 10.
- [ ] **If Path A (HTML template):** Day copy not rewritten — only tokens + explicitly requested inserts/swaps. Every copy change sourced from Activity Catalog → Itinerary Items V2 → comparable item (in that order).
- [ ] **Restaurant-about cards:** Each restaurant card appears on its FIRST occurrence in the week only.
- [ ] **Copy 1 / Copy 2 checked:** Returning guests and repeat venues in the same week use Copy 2 (return-visit framing).
