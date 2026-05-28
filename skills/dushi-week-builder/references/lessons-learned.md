# Dushi Week Builder — Lessons Learned & Build Intelligence

**MANDATORY READING.** This document must be read BEFORE any other reference file, BEFORE writing any content, BEFORE generating any output. It contains every mistake, correction, insight, and technical lesson learned from real builds. Ignoring this document leads to hallucinated content, dangerous liability language, factual errors, and wasted time.

Last updated: 2026-05-27 (Lafrance Cartel build #67 — added Build #67 section at end: map pin audit rule, email/microsite expiry sync, no-names standard, pipeline record double duty, pull-main-before-hotfix rule. Prior: 2026-05-26 Moons Cartel build — added Captain Mike boat trip types to Section 14, CP counter grep to Section 3, pre-PR microsite audit to Section 19, and expanded Build #7 corrections in Section 17. Prior: Sagar Cartel build — first Family Young Adults prospect build. Added checklist items 16–18: breakfast audit, upsell audit, bookingUrl token rule. Added Build 6 reference. Added pre-PR breakfast+upsell pass to Section 19.) Prior: 2026-05-25 (Fairburn Cartel build — first HTML-template-skeleton couple build. Added Section 20: Template-First Rule.) Prior: 2026-05-23 (skill change: output is now **text-only Markdown** — photo/HTML/PDF/DOCX pipeline retired — and a new **Operator Research Protocol** for new/unknown activities). Prior: 2026-05-22 (Adams "Traveling Trio" — first two-coconut all-inclusive LEAD build). Prior: 2026-04-16 (King Cartel build)

---

## Table of Contents

1. [The Hallucination Problem](#1-the-hallucination-problem)
2. [Dangerous Liability Language](#2-dangerous-liability-language)
3. [Booking Packages & Value Stack](#3-booking-packages--value-stack)
4. [Crew Facts — Corrections](#4-crew-facts--corrections)
5. [Activity Scheduling Rules](#5-activity-scheduling-rules)
6. [Restaurant Deep Knowledge](#6-restaurant-deep-knowledge)
7. [Info Boxes — Mandatory Structure](#7-info-boxes--mandatory-structure)
8. [The Obligation Rule](#8-the-obligation-rule)
9. [Voice and Letter Writing](#9-voice-and-letter-writing)
10. [Technical: Output Is Text-Only](#10-technical-output-is-text-only)
11. [Retired: HTML / PDF / DOCX Pipeline](#11-retired-html--pdf--docx-pipeline)
12. [Technical: Common Failures](#12-technical-common-failures)
13. [Island Database Corrections](#13-island-database-corrections)
14. [Places & Experiences Deep Knowledge](#14-places--experiences-deep-knowledge)
15. [Nightlife Deep Knowledge](#15-nightlife-deep-knowledge)
16. [Pre-Build Checklist](#16-pre-build-checklist)
17. [Completed Builds — Reference Templates](#17-completed-builds--reference-templates)
18. [Airtable Field Reference](#18-airtable-field-reference)
19. [Process & Workflow Lessons](#19-process--workflow-lessons)
20. [Template-First Rule — HTML Skeleton Builds](#20-template-first-rule--html-skeleton-builds)

---

## 1. THE HALLUCINATION PROBLEM

This is the single biggest issue found across builds. The AI repeatedly fabricated backstory, discovery narratives, and emotional moments that had zero basis in the provided data.

### What Happened (King Cartel Build)
The letter claimed: "Jesica scrolled past a thousand rental houses with drone shots and infinity pools — and something about this one made her stop." Completely invented. The booking application showed they found TC through **ChatGPT** (#1 recommendation for family vacations in Curaçao).

Ray's exact feedback: *"my insight is that you hallucinate a lot of stuff, you take a lot of tokens and a lot of my time with that."*

### The Rule
**NEVER invent backstory, discovery narratives, personality details, or emotional moments that are not explicitly sourced from the provided data.** If the WhatsApp chat, booking application, Airtable record, or user input doesn't contain a specific detail — DO NOT WRITE IT.

### What You CAN Write
- Facts from the WhatsApp chat transcript (actual messages, actual words)
- Facts from the booking application (how they found TC, payment method, dates)
- Facts from Airtable records (booking channel, guest status, guest notes)
- Facts from guest research (Apollo, web search, LinkedIn — fact-checked with source attribution)
- TC voice applied to TRUE facts — make real things sound beautiful

### What You CANNOT Write
- How they found TC if you don't have that data ("scrolled past a thousand rental houses")
- Emotional reactions you weren't told about ("something about this one made her stop")
- Dialogue or interactions that didn't happen ("You called me Tony")
- Personality traits not supported by evidence
- Assumptions about family dynamics without source data

### How to Handle Missing Context
If the personal letter needs a "how they found us" paragraph and you don't have that data:
1. ASK Ray: "How did the Kings find TC?"
2. Check the booking application data
3. Check the WhatsApp chat for clues
4. If nothing: write something generic but honest: "You found us. However you got here — the island was ready."

### 1A. NEW / UNKNOWN ACTIVITIES = HIGHEST FABRICATION RISK — RESEARCH, DON'T INVENT

The most dangerous place to hallucinate is a **new or third-party activity** that isn't already documented with a verified operator — horseback riding, ATV/UTV, private wine tasting, cooking class, deep-sea charter, kite-surf lessons, off-site spa, etc. (Several add-on entries in `island-database.md` are *names only*, with no operator, hours, price, or contact.) It's tempting to fill the gap with a plausible-sounding operator name, address, or price. **Never do this.**

The full procedure lives in **SKILL.md → "New / Unknown Activities — Operator Research Protocol."** In short:
1. **Detect & batch** every activity with no verified operator.
2. **Ask the user** (one batched pass) for a preferred operator per activity.
3. **If they name one** → wide, deep, *forensic* research on that operator (official source + 2 independent corroborations; real location/hours/contact/price/constraints; cross-check every fact).
4. **If they don't** → research to find the best option, then forensically fact-check the option you chose.
5. **Report with per-fact source attribution**, mark verified vs. unconfirmed, get user approval before it enters the itinerary. Unverifiable facts get left out or marked "to confirm."
6. **Save the verified operator** into `island-database.md` so the next build doesn't re-research.

TC-crew-run experiences (flamingo hike, reef snorkel, boat day, Sunset Club, culture walk) are already verified — no research needed.

---

## 2. DANGEROUS LIABILITY LANGUAGE

This is a legal and business risk. Zero tolerance.

### What Happened (King Cartel Build)
The letter said about Grace and Mary Kate's gluten-free needs: "Every restaurant, every chef, every dinner has been flagged. You don't have to ask. You don't have to explain. It's handled."

Ray flagged this as **dangerous**: by writing "it's handled," TC becomes legally responsible if a restaurant serves gluten. TC does not control restaurant kitchens. TC cannot guarantee what a chef puts on a plate.

### The Rule
**NEVER claim TC has "handled," "flagged," "briefed," or taken responsibility for any dietary restriction or allergy at any restaurant.** The guest is always the one who tells the server. TC provides information about which restaurants have options — that's it.

### What TO Write
- "Every restaurant in this itinerary offers gluten-free options. When you sit down, just let the server know — the island is used to it."
- "GF options available — let server know."
- "Naturally gluten-free options — fresh fish, salads."
- "Sushi rice is naturally gluten-free, and the poke bowls work perfectly."

### What NEVER to Write
- ~~"It's handled."~~
- ~~"The kitchen knows."~~
- ~~"Every restaurant has been flagged."~~
- ~~"You don't have to ask. You don't have to explain."~~
- ~~"Every chef has been briefed."~~
- ~~"We've taken care of it."~~

The GF badge `<span class="dietary-flag">GF</span>` is fine — it's informational. The accompanying text must always put the action on the GUEST ("let the server know") not on TC ("we've handled it").

---

## 3. BOOKING PACKAGES & VALUE STACK

The skill's default description doesn't clearly distinguish between packages. This caused errors in the King build where Private Chef BBQ was initially included for a guest on the "Easy" payment path.

### The Three Packages

**Dushi Week Full (All-In):**
- EVERYTHING included
- 5 Culinary Pass dinners ($35/person/dinner)
- Sunset Club + BBQ
- **Private Chef BBQ at the estate** (BONUS — ONLY for all-in)
- **Massages INCLUDED** (booker first, then others at $200/person)

**Tommy Coconut Standard:**
- Everything EXCEPT dinners
- No Culinary Pass — restaurant recommendations are suggestions only, NOT "Dinner X of 5"
- Welcome dinner at Brisa do Mar IS included ($35/person credit including kids)
- Sunset Club may or may not be running — check per week
- NO Private Chef BBQ
- NO included massages (available as add-on at $200/person)
- When Sunset Club not running → boat day upgraded with +2 hours + private beach BBQ

**"Easy" Payment Path:**
- A PAYMENT METHOD, not a package level
- Guest gets Dushi Week Full — all inclusions apply
- BUT: "Easy" ≠ "All-In" for the Private Chef BBQ bonus
- **ALWAYS confirm with Ray** which bonuses apply

### The Value Stack — READ EVERY BUILD
File location: `tc-guest-confirmation/references/value-stack.md` (in the skills directory)

One price from $7,450/week includes: private villa (7 nights + 8th Night Buffer), iCar EV-SUV (8 days), boat charter with Captain Mike (half-day, BBQ included), Wednesday Sunset Club (VIP + hosted BBQ), Flamingo Hike with Happy & Lucky, reef snorkeling with Raymonde, culture walk with Tcam, line fishing with Boy & Britt, Give Back Locally with Kim & Ray, Discovery Dive (intro or guided), 7 dinners total (5 restaurant at $35/person + 1 onboard BBQ + 1 Sunset Club BBQ), WhatsApp concierge, airport transfers (Jeremiah), 60-min massage for the booker, Data Freedom SIM, housekeeping (final + mid-stay), fridge stocked + restocked, photo session at Sunset Club Golden Hour, custom hardcover photo album, beach kit (chairs, safe, snorkels, SUP, cooler), Jan Thiel beach access + parking.

### One Coconut / Standard Dushi Week Full — Culinary Pass framing (added 2026-05-26, Moons build)

The standard All-In package includes 5 Culinary Pass restaurant dinners ($35/person credit). Here is where that information lives and where it NEVER appears:

- **Printable itinerary HTML** — **NEVER** use "$35/person", "Culinary Pass", "credit", or "house account" anywhere: not in `restaurant-about` cards, not in time-block body copy, not in info boxes. The template has zero such language. The `restaurant-about` cards are description-only (restaurant vibe, hours, tips). Run "grep for $35 and credit, delete all" before delivering — same rule as Two Coconut.
- **Microsite** — Culinary Pass belongs ONLY in `offer.includes` (e.g. "5 Culinary Pass dinners ($35/person credit)") and `goodToKnow` (explain what the pass means and which restaurants it covers). Never in `days[].schedule` titles or body.
- **Microsite schedule titles** — use venue name only (`"Villa Vis"`, not `"Dinner 1 of 5 — Villa Vis"`). No counters, no credit labels.
- **PRE-PR GREP (mandatory):** Before opening any One Coconut microsite PR, run:
  ```
  grep -n "Culinary Pass Dinner" apps/web/src/features/dushi-microsite/content/<family>.ts
  ```
  Must return zero results. The pattern `<strong>Culinary Pass Dinner X of 5...</strong>` appears in schedule bodies on multiple builds and is ALWAYS wrong. Delete every instance found.

### Two Coconut / Double Dushi — all-inclusive (added 2026-05-22, Adams build)

A fourth offer shape exists beyond the three above, and it CAN apply to the printable itinerary (not just the microsite). The `dushi-week-microsite-two-coconut` skill owns the web/booking side; this is how it shows up in the *document*:

- **Every breakfast, every lunch, every dinner + open bar at the estate** — the richest tier. NO $35/person credit anywhere.
- **Never** use "$35/person", "Culinary Pass", "house account", or "CP X of N" framing/badges. In the **printable itinerary** body copy you may reference the dinner count (e.g. "Dinner 3 of 7"). In the **microsite** schedule item `title` field, **never use "Dinner X of 7" counters** — use the venue name only (e.g. `"Villa Vis"`, not `"Dinner 1 of 7 — Villa Vis"`). Search the draft for "$35" and "credit" and delete.
- **Breakfast** is a standing line every day: **Coffee Bike OR Brisa do Mar** ("both right around the corner from the estate"). This is **absolute** — even on days anchored at a specific venue (Mambo, west coast, boat day), breakfast is still Coffee Bike or Brisa do Mar. Never substitute a venue-specific option (e.g. Bliss the Berry) for breakfast regardless of where the day is based.
- **Lunch** every day, sited by where the day puts them (beach club, boat, west-coast stop, estate). Don't invent a venue — pull it from the day's plan. **Mambo day lunch = a named beach club** (e.g. Mood Beach, Cabana Beach) — not an açaí/smoothie bar like Bliss the Berry.
- Tone: "no credit to track, no receipts to sign. You just show up and live." Gifts, not line items.
- Dinner count still resolves to **5 restaurants + 2 BBQs = 7** — the welcome dinner being a *restaurant* (e.g. Villa Vis, owner-pickup) is what makes the 5 work.
- **HTML CSS classes:** use `.tc-badge` and `.tc-line` (not `.cp-badge` / `.cp-line`) — those names leaked internal "CP" framing. Kluginbill build corrected this.

---

## 4. CREW FACTS — CORRECTIONS

These correct errors in `island-database.md`. Use THESE descriptions, not the ones in the database.

**Boy**: "The host who cares the most." NOT "the vibe" or "shows up late." The island database says "shows up late. Everyone loves him anyway." — **WRONG.** Boy is the welcoming presence. He does the rum toast at check-in (rum for adults, virgin for kids). "The treasure is out there!"

**Happy**: Male. Former street dog who decided TC was his family. **NOT a dachshund.**

**Lucky**: Male. Dachshund. Runs the Flamingo Hike.

**Christmas**: Female. Retired dachshund. 14 years old. Mostly sleeps, still has opinions. Can arrange meet-and-greet for guests who love dogs or who lost a dog.

**The Flamingo Hike is ALWAYS Happy AND Lucky together.** Never mention Lucky alone running the hike. "Happy and Lucky run point." Both dogs. Always.

**Culture walk with Tcam**: Starts from **Brion Plein**, not "Pietermaai."

**Padel**: Always describe as "with Tommy Coconut family members and guests." Day/time: **SATURDAYS, 09:00–11:00 AM** (moved from Sundays 4 PM — for good, per Ray, Windy City build, May 2026). Not generic "afternoon."

---

## 5. ACTIVITY SCHEDULING RULES

These OVERRIDE the generic scheduling in island-database.md and the main SKILL.md.

### Fixed Activity Days
- **Line Fishing**: MONDAYS ONLY, Caracas Bay, ~4 PM with Boy & Britt. OPTIONAL. Never schedule as mandatory.
- **Reef Snorkeling**: TUESDAYS ONLY, 9 AM, walk-in at Tugboat Beach (#1 snorkel spot in Curaçao). If boat day is also Tuesday, Captain Mike takes them by boat.
- **Give Back Locally**: FRIDAYS ONLY, 10-11:30 AM. NEVER in main itinerary.
- **Sunset Club**: WEDNESDAYS (when running)
- **Flamingo Hike**: ANY weekday, 7 AM. Suggest early in the week. Always moveable.
- **Culture Walk (Tcam)**: Normally THURSDAYS, 5 PM from Brion Plein. Can sometimes move — always confirm.
- **Punda Vibes**: THURSDAYS, 6-10 PM, fireworks at 8:15 PM
- **Padel**: SATURDAYS, 09:00–11:00 AM (moved from Sundays 4 PM — for good, per Ray May 2026)

### West Coast Day
- Schedule on the **BEST zero-ship day** — not locked to any specific day of the week
- **Heavy-cruise-day exception (the sunrise mitigation):** if Ray pins the west coast to a heavy cruise day anyway, START AT SUNRISE (~8 AM at Piskado). Cruise day-trippers reach the west coast ~10 AM+; arriving at dawn means turtles + Grote Knip nearly to yourselves before the crowd. Frame the cruise alert around "we beat the ships." Used on the Adams build (Wed = west coast + Sunset Club, with both ships in port).
- Route order: **Playa Piskado → Grote Knip → Kleine Knip (3-min stop) → Porto Mari**
- NOT Piskado → Porto Mari → Grote Knip (wrong order in earlier builds)
- Recommend: bring the cooler, stop for **pastetchi** (crispy fried pastry pockets), stop for **batido** on the way back
- **Kleine Knip** (Kenepa Chiki): "The most overlooked beach on the island." Just south of Grote Knip. Usually empty. DO NOT SKIP.
- Beach Gear Set: snorkels for everyone, beach safe, two beach chairs, cooler, portable SUP/kayak

### Arrival Day
- Early check-in can be arranged — mention it
- Pro tip: put kids' swimwear on TOP of suitcase
- Drive from airport crosses **Queen Juliana Bridge** with Handelskade view — NOT along the coast
- **White noise machines NOT available** on the island — guests must bring their own
- If arriving Saturday: recommend Zanzibar Saturday Happy Hour (5 PM, live band, half-price drink buckets, families welcome)

### Departure Day (Day 8)
- Explain the 8th night: "Your Dushi Week is 7 nights, but we booked an extra night so your departure day has zero checkout stress. No 'please vacate by 10 AM.'"
- Note: "vacate by 10 AM" (NOT "11 AM") when describing what other places do
- Jeremiah pickup: 3 hours before flight

---

## 6. RESTAURANT DEEP KNOWLEDGE

### Preferred Dinner Schedule
- **Welcome dinner: Villa Vis** — owner personally picks guests up. Check closed days (Tue+Wed) first. If guests don't want fish-only, use Brisa do Mar or Mei Mei.
- **Monday: Mei Mei** — salsa lesson at 9:15 PM as dessert. For adults/young adults. If small children, schedule Wed-Sun so kids can do 30 min mini golf + playground before dinner.
- **Thursday: De Gouverneur** — combine with culture walk (Tcam 5 PM) and Punda Vibes (6-10 PM, fireworks 8:15 PM). The perfect Willemstad evening.
- **Friday: Brisa do Mar** — live music on Fridays. Always try to schedule here on Friday.
- **Last dinner: Pasawa Eatery** — authentic local soul food. Emotional close.

### Restaurant Details

**Brisa do Mar (Pop's Place)**
- **Open 7 days a week** (island-database may say closed Tuesdays — WRONG)
- Near Bayside Hill and Jan Thiel villas
- Tommy's table — only person on the island who has his own table
- $35/person credit including kids
- Website: brisadomarpopsplace.com
- Full menu: brisadomarpopsplace.everyorder.io
- Kids menu: Chicken Tenders, Ribs, Cheeseburger (all with fries)

**Landhuis Brakkeput Mei Mei**
- 18th-century plantation house. Charcoal grill. Ribs and steaks.
- Weekly specials: Paella (Wed), Lobster (Thu), Red Snapper (Fri), Big 'S' Steak (Sun)
- **Monday: FREE salsa lesson at 9:15 PM** with instructor Heinrich Provence
- Mini golf + large playground on artificial grass
- Open **Wed-Sun, 5 PM-11 PM.** CLOSED Mon+Tue.
- NOTE: Ray has scheduled Mei Mei on Tuesday for the King build. ALWAYS defer to Ray on restaurant hours — he knows when places will make exceptions.
- NOTE: Ray confirmed Mei Mei IS open MONDAY for the salsa-lesson dinner (Windy City build, May 2026). The Monday salsa lesson (~9:15 PM, Heinrich Provence) is the reason to put dinner there on a Monday — frame it as "dessert is the dance floor."
- Website: brakkeputmeimei.com / meimeicuracao.com

**Villa Vis**
- Jan Thiel. Fish/sushi/poké ONLY.
- Owner personally picks up guests — why it's preferred for welcome dinner
- Open **Thu-Mon, 12-9 PM.** CLOSED Tue+Wed.
- Phone: +5999 524 0026
- NOT for families where kids don't eat seafood

**Grand Café Gouverneur de Rouville (De Gouverneur)**
- Otrobanda, Anna Bay, view over Handelskade. Building dates to 1737.
- Keshi Yena (national dish). Cuban Banana Soup (legendary).
- Open daily. Lunch 9 AM-4 PM, Dinner 5:30-10 PM.
- GF options available. Website: de-gouverneur.com

**Pasawá Box Eatery**
- Caracasbaaiweg 177. Opened July 2023.
- Shipping containers, hand-painted by local artists. Multiple vendor stalls.
- Vendors: Piská Swa (seafood), Pão e Carne (Portuguese grilled), Funchi Ku (fried polenta), Everything Between Buns (smashburgers)
- Best as last dinner or any authentic night

**Boca 19**
- End of Santa Barbara Beach Resort. Barefoot dining.
- Pairs with El Capitano day — moor at Santa Barbara, walk to Boca 19.
- Website: boca19.com

**Zest Beach Café**
- Great for families — picnic tables in the sand, space for kids to run, visibility
- The go-to family dinner spot after a big adventure day

### Captain Magic Mike — Two Distinct Boat Trips (added 2026-05-26, Moons build)

Captain Mike runs **two different trips**. They are NOT interchangeable — check the itinerary to see which one the guest has, then use that label everywhere (slug, name, offer.includes, letter, closing).

| Trip | Time | Label to use | Experience |
|---|---|---|---|
| **Private Boat Day** | 10 AM – 2 PM | "Private Boat Day with Captain Magic Mike" | Snorkeling (Tugboat Beach, Spanish Water), hidden coves, private beach BBQ |
| **Private Sunset Cruise** | 3 PM – 7 PM | "Private Sunset Cruise with Captain Magic Mike" | On-water sunset, onboard BBQ, drinks flowing as the light turns |

**Never** label the 10 AM trip a "sunset cruise" — it ends at 2 PM. Check `<h4 class="time-label">` in the approved itinerary HTML for the departure time, then match all microsite references accordingly: experiences slug, experiences name, `offer.includes` line, letter paragraph, closing paragraph, and schedule item title + body.

### El Capitano (Experience, not restaurant)
- Luxury self-drive tender boats on Spanish Water. NO license needed.
- For 8+ people, book 2 boats.
- Isla Capitano: Private floating island exclusive to El Capitano guests.
- Safety: GPS, waterproof radio, speed limiter, escort boat nearby.
- Website: elcapitanocuracao.nl
- Pairs with Boca 19 lunch → Zanzibar Happy Hour → Jan Thiel dinner

---

## 7. INFO BOXES — MANDATORY STRUCTURE

Every day page must have THREE info boxes at the bottom. No exceptions.

### Box 1: WHAT'S HAPPENING AT JAN THIEL BEACH TODAY
- Monday: No special events
- Tuesday: Live at the Beach @ Zest, 7:30 PM
- Wednesday: Unplugged Beach Sessions @ Zanzibar, 7:30 PM
- Thursday: Sangria & Beats @ Zest, 3-7 PM
- Friday: Zest Happy Hour, 6 PM
- Saturday: Zanzibar Happy Hour 5 PM (live band)
- Sunday: Zanzibar 3-4 PM + Tinto 7:30 PM

### Box 2: WHAT'S HAPPENING IN CURAÇAO TODAY
- Always state cruise ship count + total passenger count
- "Zero cruise ships" on empty days
- Mention Punda Vibes (Thursday), Koningsdag (April 27), or other cultural events
- Source: CruiseTimetables.com (specific month pages, e.g., /willemstadcuracaoschedule-jun2026.html)
- Always verify day-of-week labels against actual calendar — web snippets sometimes have wrong days

### Box 3: WHAT'S HAPPENING AT TOMMY COCONUT TODAY
- Monday: Line fishing with Boy & Britt, Caracas Bay ~4 PM
- Tuesday: Reef snorkeling with Raymonde, Tugboat Beach 9 AM
- Wednesday: Sunset Club (if running), otherwise no special events
- Thursday: Culture walk with Tcam, 5 PM from Brion Plein
- Friday: Give Back Locally 10-11:30 AM
- Saturday (Arrival): "Pool is clean. Hot tub filled with fresh water, getting to 37°C (98.6°F)."
- Saturday (Departure): "Already thinking about next time"
- Saturday: Padel with TC family & guests, 09:00–11:00 AM
- Sunday: No special TC events (crew around)

---

## 8. THE OBLIGATION RULE

This is UNIVERSAL across all builds. If putting something in the itinerary would make a guest feel they need to say YES or NO — it goes in the "What's Happening at Tommy Coconut Today" info box ONLY. NEVER in the main day timeline.

**Main timeline** = things BUILT FOR THIS GUEST. Their boat day. Their dinner. Their beach hopping. Their Sunset Club. Things they booked.

**TC Today info box** = things WE (Tommy Coconut) are doing today. Guests browse it. If something catches their eye, THEY message the WhatsApp group. No pressure. No decision required.

Activities that are ALWAYS TC Today box only:
- Line fishing with Boy & Britt (Mondays)
- Reef snorkeling with Raymonde (Tuesdays)
- Give Back Locally (Fridays)
- Padel (Saturdays, 09:00–11:00 AM)
- Any other "join us" community activity

Framing: "Boy & Britt are fishing at Caracas Bay this afternoon. If you feel like joining, drop a message in the group." — NOT "4:00 PM Line Fishing with Boy & Britt" as a scheduled event.

**Exception**: The private boat trip with Captain Mike IS in the main timeline — it's built for the guest.

---

## 9. VOICE AND LETTER WRITING

### Letter Rules
- TC Voice Stage 3 (Relationship register) — load the tommy-coconut-voice skill
- Sign off: `T` (bold, navy) in the itinerary. NOT full name, NOT "Tommy"
- Theme: "The treasure is out there" where appropriate
- At least one Antillean English flip in the letter
- One Papiamentu word (dushi, POKO POKO, bonbini, etc.)
- Objects have feelings: "The rum has been waiting longer than you have."
- Never use banned hospitality words (nestled, pampered, tranquil, exclusive, etc.)
- Deep research the primary guest before writing
- **Every claim in the letter must be traceable to source data**

### Voice Corrections
- Never use "Tico Time" — correct term is "Dushi Time" or just "POKO POKO"
- "all our energy goes into the week" NOT "every dollar goes into the week" (less transactional)
- "Every Experience Is an Invitation" — not "Gift" (updated from earlier builds)

### Sign-off Rules by Context
- Public Airbnb reply: `Vacation is holy.\n— Tommy 🥥`
- WhatsApp (first-time guests): `Vacation is holy.\nT 🥥\nTommy Coconut Private Resorts`
- WhatsApp (repeat guests): `Vacation is holy.\nRay & the entire Tommy Coconut family 🥥\nTommy Coconut Private Resorts`
- Google/Facebook ask (first-time): `Dushi,\nT 🥥\nTommy Coconut Private Resorts`
- Itinerary letter: `T` (bold, navy color)

---

## 10. TECHNICAL: OUTPUT FORMAT — TWO PATHS

### Path A: HTML Template Skeleton (preferred for couple and returning-guest builds)
When a standard HTML template exists for the variant (estate + coconut count + guest type), **use it as the skeleton**. See Section 20 for the full rule set. The template is the authoritative day schedule — personalize tokens and insert/swap specific blocks only.

Standard template locations:
- **Sat-to-sat couple (any estate):** `itinerary-standard-sat-to-sat--couple 2.html` — save a durable copy in `~/.claude/skills/dushi-week-builder/references/` or the claude-toolkit repo. Do NOT rely on the `~/Downloads` copy.

Deliverable: the edited HTML file, renamed `itinerary-[cartel-name].html`. Save to the guest's working folder.

### Path B: Text-Only Markdown (fresh builds with no HTML template for the variant)
As of 2026-05-23 the fresh-build produces **one clean Markdown file** — no HTML, no PDF, no DOCX, no photos. See `output-pipeline.md` for layout (day-block format, Week-at-a-Glance table, sign-offs, file naming).

**Which path to use:** Check the Dushi Week Registry (STEP 0.5) for nearest prior build by Estate + Variant. If an HTML file is linked → Path A. If only a Markdown exists or nothing exists → Path B.

The single biggest workflow simplification: **there is no longer a "three-file sync."** Edit the Markdown, save it, deliver it. When the user wants a change, change the one file. No copy-to-workspace, no PDF regeneration, no DOCX-script update.

File name: `Dushi-Week-[CrewName].md`.

---

## 11. RETIRED: HTML / PDF / DOCX PIPELINE

The HTML + WeasyPrint-PDF + Node-`docx` pipeline (Cloudinary hero photos, font embedding, photo picker, crop-gravity iteration, three-file sync) is **retired** — it consumed the most time, focus, and tokens for the least guest value, and every photo swap forced a regenerate. The old `scripts/create-docx.js` generator has been deleted. Do **not** resurrect this pipeline unless the user explicitly asks to bring photos/visual export back. If they do, the V8 brand tokens and font details in the `tommy-coconut-voice` skill (PART X) are the starting point.

---

## 12. TECHNICAL: COMMON FAILURES

- **One file, no sync**: the build is a single Markdown file (Section 10). There is no HTML source-of-truth, no PDF/DOCX to keep in sync. Edit the one file.
- **Don't pass the whole itinerary to a sub-agent**: a full itinerary is large. Don't try to pass it as context to a sub-agent — work on it directly.
- **Context window exhaustion**: Large builds can run out of context across sessions. The CLAUDE.md working memory preserves corrections across sessions. The lessons-learned document (this file) preserves them across builds.
- **Cruise calendar verification**: Always verify day-of-week labels against an actual calendar. **Concrete method (Adams build):** the WebFetch summary of cruisetimetables.com mislabeled EVERY weekday (claimed Aug 10 2026 = Sunday; it's Monday) AND a single summarizing fetch dropped a ship (missed Allure on Aug 11). So: (1) compute the weekday yourself from a known anchor — e.g. Jul 4 2026 = Saturday, 2026 is NOT a leap year — never trust the fetch's day-of-week; (2) do a SECOND, detailed fetch ("list ships per date, do not compute weekday") and reconcile against the first.

---

## 13. ISLAND DATABASE CORRECTIONS

These OVERRIDE `references/island-database.md`. The database was written before real builds corrected it:

1. **Boy's bio**: Database says "shows up late." → CORRECT: "The host who cares the most."
2. **Brisa do Mar hours**: Database may say closed Tuesdays. → CORRECT: **Open 7 days.**
3. **Happy**: Database groups Happy & Lucky as "Two dogs." → CLARIFY: Happy is a former street dog (NOT a dachshund). Lucky IS the dachshund.
4. **Culture walk start**: → CORRECT: Brion Plein (not "Pietermaai")
5. **"Every Experience Is a Gift"**: → CORRECT: "Every Experience Is an Invitation"
6. **Padel**: → CORRECT (May 2026): SATURDAYS, 09:00–11:00 AM (was Sundays 4 PM — moved for good per Ray)
7. **Schooner Bar**: Ray removed from a build. Verify before including.
8. **Cloudinary / photos**: N/A — the build is text-only (Sections 10–11). No images are embedded, so cloud names and crop gravity no longer matter.

---

## 14. PLACES & EXPERIENCES DEEP KNOWLEDGE

### TC Add-On Prices (Ray-confirmed, Windy City build, May 2026)
These are TC's OWN prices for paid upgrades on top of a Dushi Week — use these, not third-party online rates. Present as optional upgrades ("your call"), arranged via the WhatsApp group.
- **Horseback ride on the beach** — **$300 per person.** Guided coastal ride, all levels, helmets/water sorted. (A "must-do" guests often name; it's a paid add-on, not included.)
- **Frankie's Beach / Playa Franki** (private secluded beach, Landhuis San Nicolas, Santa Martha) — **$250 per person** (supersedes the Adams "$1,500 for the group"). Beach beds, cooler, picnic lunch, total privacy; rocky seafloor = snorkel-and-lounge, not swim. Morning or afternoon slot, ~4 hrs.
- **Touriffic guided jet ski tour** (operator: Touriffic Curaçao, @tourrific_curacao) — **$350 per jet ski (2 riders).** Launches from **Santa Cruz on the WEST coast (Westpunt area), NOT Caracas Bay/Jan Thiel** (Ray correction, May 2026). Guided run up the wild coast to the **Blue Room** sea cave and the western coves. Pairs with the around-the-island / west-coast day, not an east-side day.
- **Extra beach cabana** (when 1 is already included for 2 people): **$125 / 2 persons at Jan Thiel**; **$150 / 2 persons on a west-coast beach day.**
- **Swim with dolphins** — third-party (Dolphin Academy at the Sea Aquarium, Mambo): **Dolphin Swim ≈ $194 p.p.** (30 min in-water + all-day Sea Aquarium access, Tue–Sat; spectators $20). This is the venue's online price, not a TC price — quote as "about $194."
- **Estate wellness add-ons** (clinic comes to the estate): massage (booker's included, others extra), manicure, pedicure, private yoga, vitamin-drip IV. No fixed prices captured yet — "just ask in the group."

### Mambo Beach Boulevard (heavy-cruise-day move)
Near the Sea Aquarium; thrives ON cruise days (lean into the buzz). **Cabana Beach** = reserved daybeds, beach access, sports bar, Blush boutique (7 AM–6 PM). **Mood Beach** = Bohemian-vibe lunch, daybeds/cabanas, cocktails to your spot. Two-story boardwalk of shops (10 AM–6 PM). Dolphin Academy is right here.

### Far-west beaches (a SECOND west-coast day, distinct from the Piskado/Knip loop)
- **Playa Kalki** (Westpunt, ~75 min from Jan Thiel) — divers' "Alice in Wonderland" reef offshore (coral, turtles, fish); small calm cove, palapas, snorkel-from-shore.
- **Natural Jacuzzi (Suplado)** — natural rock pool on the rugged coast near Westpunt; surf surges into a churning pool; short rocky scramble; distinct from Boka Pistol's blowholes.
- **Daaibooi (Daaibooibaai)** — quiet local mid-west beach between cliffs; calm clear water, good swim/snorkel.
- **Playa Forti** — ~40-ft cliff jump into turquoise water (jump or watch); cliff-top restaurants with panoramic views; snorkel along the cliff edge.
- ⚠️ Far-west beaches + a 5 PM Willemstad culture walk on the same day is geographically tight (opposite ends) — flag the drive and treat the culture walk as moveable.

### Tugboat Beach
- #1 snorkel spot in Curaçao. Sunken tugboat just offshore — now a thriving reef.
- Walk-in from beach. Shallow depth. All skill levels. Kids with PFDs can do it.
- Open daily 9 AM-6 PM. Small quirky beach bar (BBQ, cold drinks).
- **Bring cash** (guilders or dollars). Off the grid. Unpaved road (iCar handles it).
- Not a sunbathing beach — you come for what's under the water.
- Activities: "Be the Artist" workshop, intro dives, guided dives, PADI courses.

### Jan Thiel Beach — Deep Knowledge
- 4 beach clubs: Papagayo (shallowest, infinity pool, best for kids), Zest Beach Café (picnic tables, cabanas), Zanzibar (energy, happy hours, live music), Koko's (smoothies, açaí bowls, most relaxed)
- 5 restaurants: Zest Restaurant, Zanzibar, Tinto Bar y Cocina, Agave Bar y Taquería, Koko's
- iCar opens gate automatically. No cash needed.
- Daybeds bookable via WhatsApp concierge (guest pays direct to club)
- Do NOT mention "Beach entry free after 4:30 PM" — skip this detail.

### Diving
- Available for BOTH Standard and Dushi Week Full packages
- Resident divemaster **Julian** (+599 9 665 7276)
- NOT an add-on — included for all guests
- Kids under 8 cannot dive. Ages 8-10: Bubblemaker (shallow only).
- For young families: "If Mom and Dad want to try an intro dive, Boy hangs out with the kids."

### Batido
- Creamy fruit shake — more than a drink. It's the taste of stopping, of pulling over.
- Mango, papaya, passion fruit, tamarind. Stands and trucks everywhere.
- Recommend on west coast day drive back.

### Fort Bekkenburg
- 5 minutes from Palm Breeze. 17th-century harbor defense.
- Quick detour (20 min enough). Cannons. History. Good for toddler families near Caracasbaai.

---

## 15. NIGHTLIFE DEEP KNOWLEDGE

### Pietermaai District
Trendiest neighborhood. Restored colonial mansions. Weekend starts Thursday. Upscale, conversational — not "party and get crazy."

**VERIFIED OPEN (April 2026):**
- **Mundo Bizarro** — 12 Nieuwestraat. Cuban-style. Salsa on Thursday nights. THE go-to.
- **Saint Tropez Ocean Club** — Infinity pool, daybeds, trendy bar. Day + evening.
- **Mr. Porter Street Cafe** — 42 Nieuwestraat. Replaced Miles Jazz Cafe. Premium bar.
- **Café Old Dutch** — Since 2001. Casual pub.
- **Blackjack** — Sports bar + dining. Air-conditioned.
- Also: BKLYN, Bluebird, Café George, Soi95, Oliva, Kome, BijBlauw

**CLOSED — DO NOT RECOMMEND:**
- ~~Bar 27~~ — CLOSED since ~2021
- ~~Miles Jazz Cafe~~ — CLOSED since 2020. Now Mr. Porter.

### Mambo Beach Boulevard
- **Wednesday**: Cabana Nights (DJs Carlito, Alain, Alex Sargo, after-party 9 PM-midnight)
- Madero Ocean Club, Hemingway Beach Bar
- Rileks Beach Bar (Live Music Fri, Sunset Sessions Sat, Sunday Vibes)

### By Night (for older kids 18+)
- Recommend Pietermaai District
- Offer to arrange driver for pickup/dropoff (safety + convenience — parents love this)
- Thursday = Mundo Bizarro salsa night or Punda Vibes
- Friday/Saturday = Mundo Bizarro, Mr. Porter, Saint Tropez, Mambo Boulevard

---

## 16. PRE-BUILD CHECKLIST

Do this EVERY TIME before writing a single word:

0. ✅ **Check the Dushi Week Registry** (SKILL.md → "STEP 0.5") — Airtable base `appFRLV1H76ohiIQS`, table "Dushi Weeks" (`tblGHUrF6PGkqrnn3`). Search the guest's email (dedupe), find the nearest template by Estate + Variant, take `max(Build #) + 1` for the new slug, and check for a prior stay. Log/update the row after you ship.
0a. ✅ **Identify the correct segment template.** Match the guest type to one of the 6 templates in Section 20 (Couple / Friends / Family teens / Family young kids / Family young adults / Multi gen). This determines both (a) which Airtable items to pull and (b) which HTML file to use (if any). ⚠️ Multi gen template is incomplete — days 7–8 missing.
0b. ✅ **Determine output path.** Only Couple has an HTML skeleton. All others → pull template items from Itinerary Items V2 by segment Guest Record ID (Section 20) and use as authoritative day schedule. Do NOT invent a schedule from memory.
0c. ✅ **If using HTML skeleton (Couple, Path A): open the template, identify all tokens, list what changes.** Do NOT touch day copy until you have a complete token + insert/swap list.
1. ✅ Read this document (you're doing that now)
2. ✅ Read the value stack: `tc-guest-confirmation/references/value-stack.md`
3. ✅ Confirm booking package with Ray: Full (All-In), Full (Easy), or Standard
4. ✅ Get ALL pre-booking communication — WhatsApp, phone notes, Airbnb messages, emails, DMs
5. ✅ Pull Airtable records: Guest table + Pipeline table
6. ✅ Check booking channel (Pipeline field `fld2Jvct0z6acihYS`)
7. ✅ Check Coconut Cartel status (Guest field `fld3tAQ67vKgxbeB1`): `1CCM` = first-time. NOT returning.
8. ✅ Research primary guest: Apollo, web search, LinkedIn. Fact-check everything.
9. ✅ Get cruise ship calendar: CruiseTimetables.com for their week
10. ✅ Identify best zero-ship day for west coast beach hopping
11. ✅ Load tommy-coconut-voice skill before writing content
12. ✅ Confirm restaurant hours against the actual dates
13. ✅ Check group size — groups of 5+ need two iCars
14. ✅ Ask Ray: "Anything special about this guest I should know?"
15. ✅ List any new / third-party activity with no verified operator (horseback riding, ATV, wine tasting, cooking class, etc.) and run the Operator Research Protocol (Section 1A / SKILL.md) — ask Ray for a preferred operator, then research + forensically fact-check before writing it in.
16. ✅ **Breakfast audit** — Every non-arrival day must open with Coffee Bike OR Brisa del Mar. No other breakfast venue. Go day by day before shipping. Coffee Bike is closed Monday → use Brisa del Mar on Mondays.
17. ✅ **Upsell audit** — Before shipping, verify: (a) west-coast day has Frankie's Beach + Touriffic jet ski; (b) Mambo/Sea Aquarium day has dolphin swim + Mood cabana; (c) Jan Thiel beach days have Papagayo daybed. These are the standard upsell slots — don't leave them empty.
18. ✅ **bookingUrl token** — Use the Pipeline Airtable record ID (`recXXX...`) as the `t=` parameter, NOT the short token from `fldZIAV3Qr8RaTixS`. Confirmed: portal reads record ID.
19. ✅ **Cover hero image** — Two steps, every build:
    1. **Set the Basecamp** on the Pipeline record: update field `fld15SzszbTcHufZT` (linked record) to the correct Basecamp record ID from `tblGc7g7uBedgS3Ui`.
    2. **Fetch the hero Cloudinary ID** from the Basecamp record: field `fldwENhluLhDMIhdG` returns a slug (e.g. `dushi-hideaway`, `palm-breeze`, `hh-hero-people`).
    3. **Build the cover URL**: `https://res.cloudinary.com/tommy-coconut/image/upload/w_1600,h_800,c_fill,g_auto,q_auto:best/<slug>`
    ⚠️ Do NOT use the old `dhschyq40` cloud or the hardcoded versioned Palm Breeze URL from the template skeleton — those are wrong for any estate that isn't Palm Breeze.

---

## 17. COMPLETED BUILDS — REFERENCE TEMPLATES

### Build 1: The Wyand Cartel (THE OG BUILD — Voice Benchmark)
- **Who**: Heather, Brent, Evie (2.5 years old)
- **Villa**: Palm Breeze | **Package**: Dushi Week Full (All-In) | **Dates**: Mar 19-26, 2026
- **Guest type**: Young Family with Toddler
- **Key insight**: NAP WINDOW IS SACRED (1 PM every day as a scheduled event). Massages during nap. Private Chef BBQ after bedtime ("This one's on us. Once Evie is asleep, the deck becomes yours."). West coast on last full day paired with Sunset Club.
- **Voice benchmark**: "Five months of Vermont winter. The marina wrapped up in shrink wrap." / "The pillow already misses her." / "No bill. No catch. Just a dushi night you didn't see coming."

### Build 2: The Phelan Cartel
- **Who**: Josh, Julia, Eleanor (8), Benji (5)
- **Villa**: Bayside Hill | **Package**: Tommy Coconut Standard | **Dates**: Apr 18-25, 2026
- **Guest type**: Family with Small Children (5-8)
- **Key insight**: No naps but bedtime 8-9 PM. Early dinners (6-6:30 PM). Mini golf at Mei Mei = energy burn. Zest Beach Café = go-to family dinner. Tree nut allergy flagged everywhere.

### Build 3: The Hernandez Island Hoppers Cartel
- **Who**: Michael, Roxie, Reagan, Samantha
- **Villa**: Tropical Haven | **Package**: Dushi Week Full | **Dates**: Apr 4-11, 2026
- **Guest type**: Family with Adult Children (18-25)
- **Key insight**: No bedtime constraint. Nightlife viable. Split activities. Intro dive real option. Easter Sunday was a factor. Pietermaai nightlife for adult kids.

### Build 5: The Fairburn Cartel (First HTML-Template Skeleton Build)
- **Who**: Lori & Scott Francisco-Fairburn (fairburnloriscott@gmail.com)
- **Villa**: Dushi Hideaway | **Package**: Two Coconut (All-Inclusive, 2CCM) | **Dates**: Feb 6–13, 2027
- **Guest type**: Returning Couple (second trip)
- **Build type**: HTML template skeleton — `itinerary-standard-sat-to-sat--couple 2.html` used as base
- **Working folder**: `~/Desktop/lorifairburn 22cm hot leadf/itinerary-fairburn-cartel.html`
- **Key insights from this build:**
  1. **Template is the skeleton.** Day copy is NEVER rewritten from scratch. Only tokens and specific insert/swap blocks change. Rewriting days was the single biggest error in prior sessions.
  2. **Airtable is the copy bank.** Activity Catalog (`fldJx3o8AKlPzFQSv` = couple variant copy) and Itinerary Items V2 are source of truth before writing any new copy. Check both before inventing anything.
  3. **Write from comparables when Airtable is empty.** Same word count, same rhythm, same time-block → pro-tip → restaurant-about structure.
  4. **Copy 1 vs Copy 2.** Copy 1 = first-visit framing. Copy 2 = return-visit framing — used when (a) venue appears twice in the same week OR (b) returning guest (2CCM+) has visited the venue on a prior trip.
  5. **Restaurant-about on first occurrence only.** If a restaurant appears on Day 1 and again on Day 3, only Day 1 gets the restaurant-about card.
  6. **Two Coconut label.** "Included — Two Coconut" everywhere. Never "$35/person", never "Culinary Pass", never "CP X of N."
  7. **Returning couple letter.** "You came back" framing. Reference the specific moment that proved they'd return (snowstorm, booking before photos were sent). Contrast last trip (full family) with this trip (just the two of them). Closing H2: "[Names] — you came back. That means everything."
- **Token map for this build:** `{Basecamp}` → Dushi Hideaway · `{First Name}` → Lori · `[Crew name]` → The Fairburn Cartel · `[Guest first names]` → Lori & Scott · Dates → Feb 6–13, 2027

### Build 7: The Moons Cartel (First-Timer Couple, Dates TBD, One Coconut Prospect)
- **Who**: moons123@icloud.com (no real names at build time)
- **Villa**: Happy Hideaway | **Package**: Prospect (One Coconut, $10,250) | **Dates**: TBD
- **Guest type**: Couple, first time in Curaçao
- **Build #**: 62 | **Slug**: Moons123DushiWeek62 | **Microsite**: tommycoconutprivateresorts.com/Moons123DushiWeek62
- **Pipeline record**: `recPyHqxX9AtZIFDw`
- **Key corrections made during this build (don't repeat):**
  1. **$35/person Culinary Pass in restaurant-about** — added "Culinary Pass credit applies here" to the Brisa do Mar `restaurant-about` card. WRONG. Template has zero credit language. All tiers: `restaurant-about` = description only. Culinary Pass info goes in the microsite only.
  2. **No real guest names** — guest only had a username. Adapted letter salutation to "You two," and massage block accordingly. Don't invent names.
  3. **Dates TBD** — guest had no confirmed dates. Used generic labels ("Your Arrival Saturday", "Day 1 · Sunday") + placeholder ISO dates `2026-01-01`–`2026-01-08`. Update `arrivalDate`, `departureDate`, `dateRangeLabel` in the microsite once dates are confirmed.
  4. **CP Dinner counter strings in microsite schedule bodies** — `<strong>Culinary Pass Dinner X of 5 — $70 tonight.</strong>` appeared in all 5 dinner schedule bodies. WRONG — the rule says CP language goes ONLY in `offer.includes` and `goodToKnow`. Pre-PR: grep for "Culinary Pass Dinner" in the content file — must return zero results.
  5. **Boat day mislabelled as sunset cruise** — the approved itinerary was the 10 AM–2 PM Private Boat Day, but the microsite used "sunset cruise" everywhere (slug, experiences card, letter, closing, offer.includes). Always check the time-label in the itinerary to determine which trip type, then match all references. See Section 14 for the two trip types.
  6. **Invented content in beaches[] card** — Porto Mari's `vibe` and `description` contained "double reef" and "wild pigs" that were not in the Moons itinerary. All `beaches[]` and `experiences[]` card fields must trace to the approved itinerary or verified facts — not invented.
  7. **Redundant offer.includes lines** — two separate lines described the same boat trip. Pre-PR: read `offer.includes` top-to-bottom and remove logical duplicates.
  8. **Timing descriptor mismatch in offer.includes** — said "last-night Pasawá" when Pasawá was actually on Day 1. Any timing label ("last-night", "welcome", etc.) in `offer.includes` must match the actual schedule position.
  9. **Internal ops notes in schedule body** — text intended for TC operations ("confirm dietary specifics with Kelly first", "details not yet shared with the crew") appeared in guest-facing body copy. Scan every body field for any text that implies TC crew action or internal coordination — delete it.

### Build 6: The Sagar Cartel (First Family Young Adults Prospect Build)
- **Who**: Sagar (lead — full name unknown at build time)
- **Email**: sagar.ram4@hotmail.com | **Phone**: +1 2182341857
- **Villa**: Dushi Hideaway | **Package**: Prospect (All-In, $18,060) | **Dates**: May 31–Jun 7, 2026
- **Guest type**: Family Young Adults (3 adults, adult kids, first time in Curaçao)
- **Build #**: 59 | **Slug**: SagarDushiWeek59 | **Microsite**: tommycoconutprivateresorts.com/SagarDushiWeek59
- **Key corrections made during this build (don't repeat):**
  1. **Breakfast venues**: Days 1, 3, 5 had no breakfast at all. Days 2 and 4 had wrong venues (Zanzibar, Mood). Required full passthrough after shipping. Run the breakfast audit (checklist #16) before opening the PR.
  2. **Mood Beach = lunch, not breakfast.** It's a daybeds/cabana lunch spot on the boulevard. Coffee Bike is breakfast on Mambo day.
  3. **Disfruta Más is retired.** Do not use it. Coffee Bike or Brisa del Mar only.
  4. **bookingUrl token = Pipeline record ID** (`recLjOD9MLgs3bAUy`), not short token from `fldZIAV3Qr8RaTixS`. Portal validates by record ID.
  5. **Dolphin swim upsell was missing** from the Mambo day. Always add it (Dolphin Academy, ~$194/person, Tue–Sat).
  6. **Frankie's Beach + Touriffic missing** from west-coast day. Always include both as upsells.
  7. **Touriffic price**: $350/jet ski (2 riders), launches from west coast (Santa Cruz/Westpunt), NOT Caracas Bay.
  8. **Coffee Bike closed Monday**: Day 2 was Monday — use Brisa del Mar instead.

### Build 4: The King Cartel (Most Corrections)
- **Who**: Andy (54), Jesica (54), Grace (22), John (20), Mary Kate (18), Andrew (15)
- **Villa**: Bayside Hill | **Package**: Dushi Week Full ("Easy") | **Dates**: Jun 16-23, 2026
- **Guest type**: Family with Young Adults + One Teen
- **Key insight**: "Easy" ≠ "All-In" for BBQ bonus. Found TC via ChatGPT. GF for Grace + Mary Kate — NEVER claim "handled." Day 1 dinner = Mei Mei with salsa. Friday fully blocked. Two iCars needed. Wednesday nightlife = Cabana Nights at Mambo Beach.
- **Problems caught**: Hallucinated narrative, liability language, Lucky without Happy, wrong restaurant.

### Key Differences by Guest Type

| Factor | Toddler (<3) | Small Kids (5-8) | Adult Kids (18-25) |
|---|---|---|---|
| Nap | SACRED 1 PM | None | None |
| Bedtime | 8 PM hard | 8-9 PM | None |
| Dining | Early 6:30. High chair. | Early 6-6:30. Kids menu. | 7:30-8 PM. Adventurous food. |
| Private Chef BBQ | After bedtime (All-In only) | Not in Standard | Date night potential |
| Nightlife | None | None | Pietermaai, Mambo |
| Activities | Sea Aquarium, flamingos | Snorkeling w/ parents, mini golf | Intro dive, split activities |
| Beach | Papagayo (shallow) only | Papagayo + more | Full range |

---

## 18. AIRTABLE FIELD REFERENCE

- Base ID: `appFRLV1H76ohiIQS`
- Guests table: `tblmo3rRjUKrrWix0`
- Pipeline table: `tblb7gP5D3NYND9a0`
- Guest notes: `fldexJE4il2hgL5aW`
- Full name: `fld3Gn1jGcjea8gwf` (**COMPUTED — never set directly**)
- First name: `fldqXcezylqkGBpDB`
- Last name: `fldGqfbAthxS4d0wi`
- Phone: `fld68nXHUC9xcTLUH`
- Booking channel (Pipeline): `fld2Jvct0z6acihYS`
- Coconut Cartel status (Guest): `fld3tAQ67vKgxbeB1` (e.g., `1CCM`)
- Captain's Briefing: `tblaSSj38XFPI255j`
- Family Briefing: `tblHJVwI8syL297zF`

### Marketing-leads "Pipeline" base (for building from a LEAD, not a booked guest)
Funnel / landing-page lead submissions live in a SEPARATE base named **"Pipeline"** — base `appiQO2iMCRjdMe0F` (NOT the main `appFRLV1H76ohiIQS`, and unrelated to the main base's Pipeline *table*).
- **Sessions table** `tbl7T49CVkrGv5HNe` — one row per funnel STEP. To reconstruct a lead: find rows by email, pull ALL rows sharing the same **Session ID** (`fldAzOSgOjESk95H2`), then merge the **Answers** JSON (`fldKXXBN6Ywrz0uPg`, a `[{q,a}]` array) across steps. The `Step = complete` row usually holds the full combined payload.
- Email `fldmvNVTCy5ESMsDZ` · Submitted At `fldxKI8aZfQeG4aeB` · Lead Status `fldmjDJNDZEt2WNFn` · plus geo + UTM + Campaign fields.
- Other tables in this base: Campaigns, Landing Pages, LP Versions, Annotations, Web Sessions, **Itinerary Sessions** (microsite behavioral telemetry), Leads Activity, Hermes.

### Google Review Direct Link
`https://g.page/r/CZLeACxdzFq3EBM/review`

### Facebook Review Link
`https://www.facebook.com/TommyCoconut/reviews`

---

## 19. PROCESS & WORKFLOW LESSONS

### Ask for Pre-Booking Communication FIRST
Before building, ALWAYS ask Ray for all communication prior to booking. Phone notes, WhatsApp, Airbnb messages, DMs, emails. This is where the gold is — how they found TC, what excited them, what worried them, their tone, their personality.

### Two iCars for Groups of 5+
Always check group size. Mention "Two iCars charged and ready" when applicable.

### Friday Blocking
If Ray says a day is "fully blocked" — respect it completely. Morning AND afternoon cleared. Only schedule the evening dinner.

### Private Chef BBQ — Ask Before Including
This bonus varies by payment path. When in doubt, ASK Ray. Don't assume.

### Cruise Calendar — Verify Days
Web snippets sometimes label wrong days of the week. Cross-reference with an actual calendar.

### One File — Text Only (or One HTML File)
The deliverable is either a single Markdown file (fresh builds) or the edited HTML template file (skeleton builds). No PDF/DOCX, no photos, no three-file sync. Edit the one file, save it, deliver it. See Section 10 for which path to use.

### Template → Airtable → Comparable (The Copy Priority Order)
This is the single most important build discipline. When any copy is needed:
1. **Template first.** Is the copy already in the HTML skeleton? If yes, leave it alone.
2. **Airtable second.** Check Activity Catalog (couple variant: `fldJx3o8AKlPzFQSv`) and Itinerary Items V2. Use catalog copy verbatim.
3. **Comparable last.** Only write fresh copy if both Airtable tables come up empty. Match word count, rhythm, and structure of the nearest comparable item in the same template.
Writing from scratch without checking Airtable first is what caused the most rewrites and errors.

### Copy 1 / Copy 2 — Always Check Before Writing a Venue Twice
If a venue appears more than once in the same week, the second occurrence uses Copy 2 (return-visit framing: "You know this table already..."). Returning guests (2CCM+) get Copy 2 even on first appearance if they've visited on a prior trip. Copy 1 framing on a return visit breaks the immersion.

### Restaurant-About Cards — First Occurrence Only
A restaurant-about card (the white card with h3 + description + URL) appears only the FIRST TIME a restaurant shows up in the week. Subsequent appearances = time-block only, no card. If adding a restaurant on an earlier day, remove the card from the later day.

### Breakfast + Upsell Pass — Do This Before Opening the PR
Before opening the PR for any microsite build, do a 30-second pass:
1. Open every day's schedule. Does it start with Coffee Bike or Brisa del Mar? If not, add it.
2. Open every day's upsells. Is the west-coast day missing Frankie's or Touriffic? Add them. Is the Mambo day missing dolphin swim or Mood cabana? Add them. Are Jan Thiel beach days missing a Papagayo daybed? Add it.
This takes 2 minutes and saves a full re-deploy cycle.

### Pre-PR Microsite Content Audit (added 2026-05-26, Moons build)

Run these checks on the content file before opening the PR. Every item on this list caused a post-PR fix on a real build.

1. **CP counter grep** (One Coconut builds only): `grep -n "Culinary Pass Dinner" content/<family>.ts` → must return 0 results.
2. **Boat day type**: check the itinerary's departure time. 10 AM → "Private Boat Day". 3 PM → "Private Sunset Cruise". Verify the experiences slug, experiences name, offer.includes line, letter paragraph, and closing paragraph all use the same label.
3. **offer.includes deduplication**: read the array top-to-bottom. Each activity appears once. Remove logical duplicates (e.g., two boat lines, two massage lines).
4. **offer.includes timing descriptors**: any label like "last-night X" or "welcome X" must match the actual schedule position. Cross-check against the days array.
5. **Beaches/experiences cards vs itinerary**: every `beaches[].description`, `beaches[].vibe`, and `experiences[].blurb` must trace to the approved itinerary or verified facts. No invented menus, reef names, or animal sightings.
6. **Internal ops notes**: grep schedule bodies for phrases like "confirm with", "not yet shared", "internal", "ops note". Delete any found.
7. **expiresAtISO**: set to 48 hours from the deploy time you're about to trigger — not from when the build started.

### Debrief → Booking Channel Check
Before writing any Airbnb review in a debrief, pull the Pipeline record. Airbnb booking → write Airbnb review. Non-Airbnb → SKIP Airbnb review, ask for Google review instead.

---

### Tommy Portal — Booking URL Token Is the Pipeline Record ID
The tommy-portal payment page (`/payments/pay?t=`) uses the **Airtable Pipeline record ID** as the token — NOT the short payment token stored in Pipeline field `fldZIAV3Qr8RaTixS`. Use `recXXXXXXXXXXXXXX` (the record ID, 17 chars starting with `rec`) as the `t=` parameter in `bookingUrl`. Confirmed: Sagar build 2026-05-26.

---

### Building from a LEAD (not a booked guest) — Adams build, 2026-05-22
Leads arrive via the funnel (Section 18's marketing "Pipeline" base), so you'll have rich PREFERENCE data but be MISSING booking facts. Workflow:
- Reconstruct the profile from the Sessions table first; present it back to Ray before building anything.
- ASK for what the funnel can't give: villa, guest first names, exact package, flight #/landing time. If a lead has no booking yet, there IS no flight — write the arrival block flight-agnostic ("Wheels down at Hato") rather than shipping raw `⟨ ⟩` placeholders. NEVER invent a flight number (hallucination rule, Section 1).
- A lead asking for the all-inclusive offer = two-coconut framing (Section 3). The full lead-conversion path (offer countdown + payment page) is the `dushi-week-microsite-two-coconut` skill — flag it if they want the web/booking version, not just the printable document.
- The funnel captures gold for the letter: how they found us (Facebook/ChatGPT/etc.), prior-visit count, "what made you decide to do this now", vacation DNA, must-dos. Use ONLY what's there.
- Save reusable external-system pointers (the lead base ID, any verified third-party operators) to memory / `island-database.md` so the next lead build is faster.

---

---

## 20. TEMPLATE-FIRST RULE — HTML SKELETON BUILDS

**This section exists because the single biggest failure mode across early builds was rewriting day copy that did not need to be touched.** The day schedules, activity descriptions, time blocks, pro tips, and info boxes in the standard HTML template represent months of iteration and real-guest feedback. They are not a starting point — they are the answer. The only question is what personalization goes on top.

### The Rule

When a standard HTML template exists for the build variant, **use it as the skeleton**. Day content is READ-ONLY. You touch:
- **Tokens** (cover page, letter, philosophy page, closing page, Week at a Glance)
- **Specific insert/swap blocks** explicitly requested (a new breakfast, an upsell box, a venue swap on one day)
- **Nothing else**

You do NOT:
- Rewrite day descriptions because you think the copy could be better
- Replace time blocks with "improved" alternatives from memory
- Add activities that weren't requested, even if they seem like good ideas
- Remove blocks that weren't mentioned as removals

If in doubt: **leave it alone and ask.**

### Token Map — Sat-to-Sat Couple Template

| Token | Replace With |
|---|---|
| `{Basecamp}` | Villa name (e.g., "Dushi Hideaway") |
| `{First Name}` | Primary guest first name |
| `[Crew name]` | Cartel name (e.g., "The Fairburn Cartel") |
| `[Guest first names]` | Both names (e.g., "Lori & Scott") |
| `[Hometown]` | City they're from |
| Dates on cover | Arrival and departure dates |
| Cover hero image URL | Look up from Basecamps table (`tblGc7g7uBedgS3Ui`, field `fldwENhluLhDMIhdG`) → build as `https://res.cloudinary.com/tommy-coconut/image/upload/w_1600,h_800,c_fill,g_auto,q_auto:best/<slug>`. Also set `fld15SzszbTcHufZT` on the Pipeline record first. See checklist item 19. |

### Copy Source Priority (When a Block Needs New or Changed Content)

1. **Activity Catalog** (Airtable, base `appFRLV1H76ohiIQS`): Field `fldJx3o8AKlPzFQSv` = couple variant copy. Field `fldtIcAZltENxFR4U` = pro tip / operational note. Search by venue/activity name first.
2. **Itinerary Items V2** (same Airtable base, 785 records): Per-trip confirmed itinerary items. Check this if Activity Catalog comes up empty.
3. **Write from comparable**: If neither table has the copy, write fresh copy that matches the word count, rhythm, and structure of the nearest comparable item in the template. A breakfast block should read like other breakfast blocks. An upsell box should read like other upsell boxes.

**Never write from memory or training data when Airtable is available.** Catalog copy has been approved by Ray. Memory copy has not.

### Copy 1 vs Copy 2

- **Copy 1** = First-visit framing. Guest is encountering this venue for the first time (in this trip or ever). Lead with place identity: "Brisa Do Mar. Pop's Place. Caracasbaai waterfront..."
- **Copy 2** = Return-visit framing. Use when: (a) the same venue appears twice in the same week, OR (b) the guest is returning (2CCM+) and has visited the venue on a prior trip. Lead with familiarity: "You know this table already..."

The Activity Catalog labels these entries "Copy 2" — search for the venue name + "copy 2" in the catalog description or title field.

### Two Coconut (All-Inclusive) Framing

- **NEVER** mention "Two Coconut" anywhere in the guest-facing printable itinerary. It is internal TC terminology only.
- Never: "$35/person", "Culinary Pass", "CP X of N", "credit", "house account", "Included — Two Coconut"
- Do NOT add any dinner counter label (cp-line, tc-line, or similar) under dinner time blocks. Remove those CSS classes entirely.
- In the Week at a Glance table: no badges next to dinner venue names.
- Good to Know section header: "Your Included Dinners" (no package name)
- Before delivering: search the HTML for "$35", "credit", "Two Coconut", "Culinary Pass", "CP " — all must return zero results.

### Restaurant-About Cards — Placement Rule

The `<div class="restaurant-about">` card appears **only on the first occurrence** of a restaurant in the week. Logic:
- Adding a restaurant to an earlier day than its existing card → move the card to the earlier day, remove from the later day
- Restaurant appears only once → card on that day
- Restaurant appears twice (two different days) → card on the earlier day only, time-block only on the later day

### Standard Template File Location

The canonical `itinerary-standard-sat-to-sat--couple 2.html` should be saved at:
`~/.claude/skills/dushi-week-builder/references/itinerary-standard-sat-to-sat--couple.html`

Do NOT rely on the `~/Downloads` copy — it can be overwritten or lost. If the references copy doesn't exist yet, save it there now.

### Sections That ARE Personalised (Not Read-Only)

| Section | What Changes |
|---|---|
| Cover page | Crew name, guest names, dates, villa name |
| Philosophy page | Add one returning-guest sentence if 2CCM+ |
| Personal letter | Everything — full personalisation, TC voice |
| Week at a Glance | Update day themes/dinners if schedule changes |
| Day pages | Only specific requested inserts/swaps |
| Closing page | H2 personalised ("Lori & Scott — you came back."), body adjusted for returning guest |
| Crew page | No changes (crew is the same) |

---

### Template Registry — All Six Segment Types (Reviewed 2026-05-25)

All six templates live in **Itinerary Items V2** (base `appFRLV1H76ohiIQS`), linked to "Template" guest records. To find the correct template for a build: filter Itinerary Items V2 by the guest's segment name (below). Each template's Guest record ID is listed for direct lookup.

| Segment | Guest Record ID | Items | HTML File Exists? | Notes |
|---|---|---|---|---|
| Couple | `rec7QFzJ2s342F0IZ` | 19 | ✅ `itinerary-standard-sat-to-sat--couple.html` | **Complete. HTML is the primary skeleton for couple builds.** |
| Friends | `rec2R9SiqXz5VUQVX` | 19 | ✅ Use Kluginbill Cartel as skeleton | Trip record ID in Itinerary Items V2 = `recahcqUFxVBCIjfE` (NOT the Guest Record ID). HTML built Kluginbill build #67. |
| Family teens | `recX78q5CWqslAm1e` | 17 | ❌ Airtable only | Content in Itinerary Items V2; no HTML file yet |
| Family young kids | `recjG9FwdBH0683UX` | 16 | ❌ Airtable only | Content in Itinerary Items V2; no HTML file yet |
| Family young adults | `recptPrA2LnvarKhu` | 17 | ❌ Airtable only | Content in Itinerary Items V2; no HTML file yet |
| Multi gen | `reczs1Jiwbh6BVMQO` | 12 | ❌ Airtable only | **INCOMPLETE — Days 7 & 8 are missing. Do not use without flagging this gap.** |

**For builds without an HTML file:** pull all items for the segment template from Itinerary Items V2, sorted by day number, and use them as the authoritative day schedule. Do not invent a schedule from memory.

---

### Day-by-Day Structure — All Templates

All templates share the same core skeleton for Days 1, 5, 6: Airport Pickup + Villa Vis (Day 1), West Side Day + Sunset Club (Day 5), Jan Thiel + Culture Walk + Punda Vibes (Day 6). The differences below are the only things that change between segments.

**COUPLE** — 19 items, all 8 days complete
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard + Hemingway's (Sunday)
- Day 3: Flamingo Hike + Mei Mei salsa
- Day 4: Guided Snorkel + Booker's Massage + Landhuis dinner
- Day 5: West Side Day + Sunset Club
- Day 6: Jan Thiel + Culture Walk + Punda Vibes
- Day 7: Boat Day (AM + PM) + Pasawá
- Day 8: Airport + De Gouverneur (1737 / Otrobanda)

**FRIENDS** — 19 items, all 8 days complete
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard + Hemingway's
- Day 3: Flamingo Hike + Line Fishing (PM) + Mei Mei salsa
- Day 4: Booker's Massage + Landhuis dinner *(no Guided Snorkel)*
- Day 5–6: same as Couple
- Day 7: Boat Day (AM + PM) + Pasawá
- Day 8: Airport + De Gouverneur

**FAMILY TEENS** — 17 items, all 8 days complete
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard *(no Hemingway's — teens, late night dropped)*
- Day 3: Flamingo Hike + Line Fishing + Mei Mei salsa
- Day 4: Booker's Massage + Landhuis dinner
- Day 5–6: same as Couple
- Day 7: Boat Day (AM only) + Pasawá *(afternoon boat slot dropped)*
- Day 8: Airport + De Gouverneur

**FAMILY YOUNG KIDS** — 16 items, all 8 days complete
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard
- Day 3: Flamingo Hike + Line Fishing *(Mei Mei salsa dropped — no late night for young kids)*
- Day 4: Booker's Massage + Landhuis dinner
- Day 5–6: same as Couple
- Day 7: Boat Day (AM) + Pasawá
- Day 8: Airport + De Gouverneur

**FAMILY YOUNG ADULTS** — 17 items, all 8 days complete
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard
- Day 3: Flamingo Hike + Line Fishing *(Mei Mei dropped)*
- Day 4: Guided Snorkel + Booker's Massage + Landhuis dinner
- Day 5–6: same as Couple
- Day 7: Boat Day (AM) + Pasawá
- Day 8: Airport + De Gouverneur

**MULTI GEN** — 12 items, ⚠️ DAYS 7–8 MISSING
- Day 1: Airport + Villa Vis
- Day 2: Mambo Beach Boulevard
- Day 3: Flamingo Hike + Mei Mei salsa *(Line Fishing dropped)*
- Day 4: Booker's Massage + Landhuis dinner
- Day 5–6: same as Couple
- Days 7–8: **NO RECORDS IN AIRTABLE** — must be built manually or flagged to Ray before starting

## 23. STRUCTURAL OVERLOAD RULES — Chrissymag Cartel Review

Added 2026-05-27 after reviewing the Chrissymag Cartel itinerary (Build #67, Friends segment, 10 guests, Feb 26–Mar 5 2027). The build packed too many events into single days and created physically impossible timing. These rules prevent recurrence.

### 23.1 Anti-Overload Rule
If a day contains an "All Day" anchor block (Mambo Beach Boulevard, West Side Day, Jan Thiel Beach all day, Boat Day), that day may have at most **ONE additional major evening event**. Never pair an all-day beach block with both a happy hour AND a private dinner on the same day. If a Private Chef BBQ is confirmed by Ray, it replaces — not supplements — any other evening event.

### 23.2 Boat Day Isolation Rule
Boat Day with Captain Magic Mike is a full-day anchor. If the itinerary shows a 10 AM–2 PM Private Boat Day, the day may have **ONE relaxed evening event** (e.g., Pasawá). Never schedule Boat Day on the same day as Culture Walk + Punda Vibes — the drive timing is impossible (2 PM return + rest + 4:15 PM Culture Walk at Brion Plein = minimum 90 min shortfall). Boat Day demands its own day or a completely free evening.

### 23.3 Timing Realism Pass
Before shipping, scan every day for a "Rest until X" block followed by an off-estate activity at X+15 minutes or less. If found, flag it: a "Rest until 4:00 PM" block preceding a 4:15 PM Culture Walk in Willemstad (45 min drive) is physically impossible. Minimum buffer: rest end time + 90 minutes + drive time before the next off-estate commitment.

### 23.4 Breakfast Grep Enhancement
Add to post-build verification (Pre-Build Checklist #16):
```bash
# Every non-arrival day must have Coffee Bike or Brisa del Mar
grep -n "Day [2-8]" your-file.html | xargs -I {} grep -A 20 "{}" | grep -i "coffee\|brisa"
# Count must equal number of non-arrival days. Days with zero hits = missing breakfast.
```

### 23.5 V8 Token Migration Reminder
If the approved original or skeleton predates May 2026, run the V8 design-token migration (Cormorant Garamond + Inter, `#0A2330` → `--color-ink`, `#FAF6EF` → `--color-cream`, `#6CE3DF` → `--color-turq`) before any token personalization. Do not ship pre-V5 CSS.

---

*This document is a living record. Update it after every build with new corrections, insights, and technical lessons. The goal: zero hallucinations, zero liability language, zero wasted tokens.*

---

## Build #67 — The Lafrance Cartel · May 2026

**Guest:** jlafrance1@outlook.com · Couple, no names shared · Dushi Hideaway · Two Coconut All-Inclusive · $14,350 · Dates TBD
**Slug:** LafranceDushiWeek67 · **Mode:** prospect · **Pipeline:** `recDuK6yOIHKtAYPD`

### Lesson 1 — Map pins must be updated when restaurants are swapped

When Day 3's dinner was changed from Komé → Pasawá Box Eatery during a hotfix, the schedule and `restaurants[]` were updated but the `mapPins` array was not. The Komé pin (wrong restaurant, wrong location) shipped to production and required a third PR.

**Rule:** After any restaurant swap, grep `mapPins` for the old restaurant name and update the pin. Add this to the pre-PR map pin audit (see pre-PR checklist in `dushi-week-microsite-from-itinerary/SKILL.md`).

### Lesson 2 — Offer email expiry and microsite expiresAtISO must match

The offer email was written with "3:00 PM island time" and the microsite `expiresAtISO` was set to `16:00` (4 PM). One hour difference. Neither value was wrong in isolation; they just weren't checked against each other. Required another PR to align.

**Rule:** After setting `expiresAtISO`, convert it to island time (UTC-4) and verify it matches the expiry text in the offer email HTML. If you're building the email and the microsite in the same session, set the time in one place first and copy it to the other.

### Lesson 3 — No-names builds: use cartel name throughout

This guest never shared real names. Correct approach (confirmed during build):
- `family.members: []`, `primaryGuest: ""`, `bookerGuest: ""`
- Letter salutation: `"You two,"` (not a placeholder — leave it exactly like that)
- Crew `whatsappMessage` starters: `"Hi Boy — it's the Lafrance family. "` (use family surname, not Cartel name)
- `offer.whatsappMessage`: `"Hi Britt — it's the Lafrance family. We want to lock the Dushi Week (Dushi Hideaway). Send the payment link."`
- Do NOT use placeholder text like `[Guest Names]` — write the cartel/family name directly

### Lesson 4 — Pipeline record may serve double duty as payment record

The skill previously warned "if you paste the lead pipeline ID the pay page won't work." In this build, the user gave the lead pipeline record ID and confirmed it was also the payment record — and it worked. Britt doesn't always create a separate offer record.

**Rule:** Don't assume two records exist. Ask the user: "Is there a separate offer/payment pipeline record, or is `recXXX` the one Britt wants?" If they confirm it's the same record, use it for both `bookingUrl` and `bookingPipelineId`.

### Lesson 5 — Pull main before opening each hotfix branch

When three hotfix PRs were merged in sequence (PRs #399, #401, #402), the branch for #402 was created before #401 merged to main. The result was a merge conflict on the same line. Always pull `origin/main` and create a fresh branch from HEAD after each PR merges — never reuse a stale base.

```bash
git checkout main && git pull && git checkout -b fix/<next-fix>
```

### Lesson 6 — Activity Catalog record ID verification (added from skill-audit session)

**Pitfall:** When batch-fetching Activity Catalog records by `recordIds`, it is easy to mislabel records in your local mapping because the Airtable `Name` field may not match your mental model.

**Real example:** Record `recUN2t3VRfmi848x` was labeled `"playa-piskado"` in fetch code → Airtable `Name` field returned **"Flamingo Hike"**. Record `rec62Y92QXnp3dPHt` was labeled `"flamingo-hike"` → Airtable returned **"De Gouverneur"**. The result: day copy would have been inserted into the wrong days, corrupting the entire itinerary.

**Rule:** Always verify the `Name` field against your expectation before trusting the block. Query by `filterByFormula` with the activity name first, fetch, dump to JSON, read back and print `Name` fields, then ask the user to verify each name matches the activity they expect. Only after all names match expectations may you proceed to insert blocks into the itinerary.

---

## Build #57 — The Fairburn Cartel · May 2026

**Guest:** Lori & Scott Fairburn · Returning couple · Dushi Hideaway · Feb 6–13, 2027
**Slug:** FairburnDushiWeek57 · **Mode:** prospect (Two Coconut)

### Lesson 1 — Booking URL uses Pipeline record ID, not the short token

The portal payment page (`/payments/pay?t=`) expects the **Pipeline record ID** (e.g. `recHq43qTtZAyFIUq`) as the `?t=` parameter. The Pipeline table has a separate field (`fldZIAV3Qr8RaTixS`) with a short token (e.g. `e4mZktpLilkJ`) — this is NOT what the portal uses. Using the short token produces "Invalid payment link" on the live site. Always build the booking URL as:
```
https://portal.tommycoconutprivateresorts.com/payments/pay?t=<PIPELINE_RECORD_ID>
```

### Lesson 2 — Derive mode from Pipeline status, never guess

We initially shipped in `mode: "guest"` because it wasn't explicit in the itinerary. The book button was missing entirely. Always read the Pipeline status field (`fldvNoCtn1157G37W`) and derive:
- `Lead` or `Offer Sent` → `mode: "prospect"` (book button, countdown, sticky CTA)
- `Booked` / `On Island` / `Departed` / `Alumni` → `mode: "guest"` (no offer mechanics)

### Lesson 3 — Reset offer expiry after every hotfix deploy

Set `expiresAtISO` to 48 hours from the **latest deploy**, not from when the build started. We extended the Fairburn timer twice because hotfixes (broken pay link, wrong mode) pushed new deploys after the initial window was set. Any time you push a fix, recalculate and update `expiresAtISO`.

### Lesson 4 — Skills must be in the shared repo or co-workers get inconsistent output

At the start of this build, 5 of 7 skills existed only on Boy's local machine. Co-workers had a frozen, incomplete toolkit. All skills are now in `TommyCoconutIT/claude-toolkit`. After every skill update: commit + push. Co-workers run `git pull` to stay current.
