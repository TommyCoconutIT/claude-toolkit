---
name: dushi-week-microsite-from-itinerary
description: "Take a finished Dushi Week itinerary (HTML, DOCX, PDF, or pasted text) and turn it into a personalized interactive web microsite at tommycoconutprivateresorts.com/<FamilySlug>DushiWeek<N>. Use whenever the user hands you a guest's itinerary and asks you to 'turn this into a landing page', 'build the microsite', 'create the interactive page', 'make a personalized page for the <Family> family', or pastes/attaches a Dushi Week itinerary document with the intent of getting a live page out. Triggers on phrases like 'give the itinerary and you create the landing page', 'turn this itinerary into a microsite', 'build the <Family> microsite from this itinerary', 'create a personal landing page from this Dushi Week', or 'I have the itinerary, now I want the website'. Do NOT use this skill for: producing the printable itinerary document itself (that's the dushi-week-builder skill — totally separate, totally different deliverable), generic edits to an already-existing microsite (use dushi-week-microsite instead), or any work outside apps/web/."
---

# Dushi Week Microsite — From Itinerary

## Inputs and outputs

```
INPUT                                OUTPUT
─────────────────────────────────    ─────────────────────────────────────────────
A finished Dushi Week itinerary  →   apps/web/src/features/dushi-microsite/
  (HTML, DOCX, PDF, or pasted          content/<family>.ts          ← typed config
  text. Sometimes the file               (the only file that differs per family)
  produced by the                    apps/web/src/app/[locale]/
  dushi-week-builder skill,            <FamilySlug>DushiWeek<N>/page.tsx
  sometimes a Google Doc the           <kebab-slug>/page.tsx        ← optional 301 alias
  user pastes.)                      A PR opened against main.
```

The microsite codebase (`features/dushi-microsite/components/`, `globals.css`, route layout, helpers) is **not modified by this skill**. It's the personalization that's new each time. Only one TypeScript file per family + the route shell.

For codebase-level questions ("how does the section pager work", "how do I add a new menu section", "the iOS hero video doesn't autoplay"), use the **`dushi-week-microsite`** skill instead. That sibling skill is the architecture playbook + lessons-learned reference; this one is the create-pipeline.

## When NOT to use this skill

- Producing the printable HTML/PDF/DOCX itinerary document → that's **`dushi-week-builder`**, which runs first. This skill picks up *after* the itinerary exists.
- Editing an existing microsite (text tweaks, photo swaps, nav changes) → that's **`dushi-week-microsite`**.
- Anything outside `apps/web/` → out of scope per `apps/web/CLAUDE.md`.

---

## Dushi Week Registry — check first, log after

Every Dushi Week (itinerary + microsite) is tracked in Airtable: base `appFRLV1H76ohiIQS` → table **"Dushi Weeks"** (`tblGHUrF6PGkqrnn3`), via the Airtable MCP. Full protocol is in the **`dushi-week-builder` SKILL → "STEP 0.5"**; the microsite-specific parts:

- **Before building:** `search_records` by the guest's email (dedupe — a lead may already have a row), and take **`max(Build #) + 1`** as the slug `<N>` instead of guessing it.
- **After shipping:** update the family's row — set **Microsite** (the live URL), **Variant** (🥥 / 🥥🥥), **Pipeline ID**, and **Status**. If a lead converts, move Status Offer Sent → Booked (don't add a second row).

---

## Required inputs from the itinerary

Read the itinerary first. You're looking for these fields. Most will be present; ask the user only for what's truly missing.

### Family identity
- Cartel name (e.g. "The King Cartel", "The Wyand Cartel"). If the itinerary doesn't have one, suggest one and confirm before locking in.
- Member names with ages for kids (the names ride across the hero — get the spelling right)
- Primary guest (the booker / the head of trip)
- Booker guest (sometimes the same person, sometimes the partner who handled payment)

### Trip
- Estate / basecamp name (Bayside Hill, Castaway Beach, Palm Breeze, Happy Hideaway, …)
- Arrival date (ISO yyyy-mm-dd)
- Departure date
- Arrival flight: code + local landing time
- Departure flight: code + local departure time (sometimes blank — that's fine)
- Date-range label for display ("June 16 to 23, 2026")

### Hero
- Tagline (1–2 lines, the family-specific "this year, the island built it for him" energy)
- Optional pinned hero video Cloudinary public ID. Default to `hero-drone-waterfront` (King's choice — works for any family).
- Hero eyebrow ("DUSHI WEEK" is the locked default)
- Fallback image Cloudinary public ID (defaults to `dushiweek/80` for the bottle/beach still)

### Letter from Tommy
The itinerary usually has a multi-paragraph opening letter addressed to the booker. Lift it verbatim. Don't rewrite. The Tommy Coconut voice is sacred — see the `tommy-coconut-voice` skill if you're tempted to edit.

### Philosophy block
One short heading + a 2–3 paragraph block on what the Dushi Life means. Usually identical across families with one or two name swaps.

### Days array (8 entries — Arrival + Day 1–6 + Departure)
For each day:
- `id` ("arrival", "day-1" … "day-6", "departure")
- `label` ("Arrival Day", "Day 1", "Departure Day")
- `date` (ISO)
- `dateLabel` ("Tuesday, June 16")
- `subtitle` (one-line emotional read of the day)
- `heroCloudinaryId` (curated photo — pick from the itinerary or use the King defaults as a guide)
- `vibe` (1–4 words: "The Landing", "Dive & Golden Hour", "On the Water")
- `cruise` (passenger count + ship names + optional advisory — itinerary usually has this in the day's intel block)
- `schedule` (time-blocks: time + title + body. Body may contain inline `<strong>`/`<em>` via dangerouslySetInnerHTML)
- `restaurants` (1–2 per day, with about-copy + GF notes + IG handle if available)
- `upsells` (optional paid add-ons: name, blurb, priceLabel, whatsappMessage)
- `infoBoxes` (beach / curacao / tc — optional contextual snippets the itinerary calls out)
- `mapPins` (array of `{ id, name, coords: [lng, lat], category }` — coords from the itinerary's location refs)

### Week-glance table
One row per day for the home-view glance table: `dayId`, `day`, `date`, `highlight`, `dinner`, `vibe`. Usually derivable from the days array.

### Crew (CrewMember[])
Static fallback list. In production this is **superseded by Airtable** via the `family` Section's canonical fetch — but the static list still ships in case Airtable env vars are missing. Mostly identical across families (Boy, Britt, Captain Magic Mike, etc.); only personalize the `whatsappMessage` starter phrases ("Hi Boy — it's the King family. ") to use the new family's name.

### Closing
- Heading ("The treasure is out there.")
- 2–3 paragraphs
- Sign-off ("VACATION IS HOLY. T 🥥" is the locked default)

### Mode
- `"guest"` if booked (no urgency / no offer countdown)
- `"prospect"` if un-booked (requires an `offer` block: price, expiry, share token, referral credit, WhatsApp message)

**Derive mode from the Pipeline status field (`fldvNoCtn1157G37W`) — do not guess:**
- Status `Lead` or `Offer Sent` → `mode: "prospect"`
- Status `Booked`, `On Island`, `Departed`, `Alumni` → `mode: "guest"`
If you don't have the Pipeline record, ask the user before defaulting.

### Booking URL
The `bookingUrl` in the `offer` block uses the **Pipeline record ID** as the `?t=` parameter — NOT the short token in `fldZIAV3Qr8RaTixS`.

```typescript
bookingUrl: "https://portal.tommycoconutprivateresorts.com/payments/pay?t=<PIPELINE_RECORD_ID>"
// e.g. "https://portal.tommycoconutprivateresorts.com/payments/pay?t=recHq43qTtZAyFIUq"
```

The field `fldZIAV3Qr8RaTixS` exists in the Pipeline table but is NOT the token the portal uses. Using it will produce an "Invalid payment link" error. Always use the `rec...` record ID.

### Offer expiry
Set `expiresAtISO` to 48 hours from the moment you deploy — not from when you started the build.
If you push a hotfix after the initial deploy, reset the expiry to 48 hours from the fix deploy time.
Format: ISO with Curaçao offset (`-04:00`), e.g. `"2026-05-28T17:00:00-04:00"`.

### WhatsApp
- `groupInviteUrl` — the real WhatsApp group invite URL for the family. Default to the **bare** form `https://chat.whatsapp.com/<id>`, but know that the `?mode=gi_t` param's behavior is **inconsistent across guests/devices** (it fixed Bama, it broke Hernandez + King). Don't treat either state as absolute: if the guest reports the link won't open, WebFetch both variants to confirm the group, then ship whichever one their own-phone test says works. See lessons #13 and the memory note `feedback_whatsapp_invite_param.md`.
- `fallbackTcPhone` — optional concierge phone (E.164, no `+`)
- **Upsell messages**: each `upsells[].whatsappMessage` is what gets pre-filled when the guest taps "Yes, count us in". Write them in the family's voice — e.g. *"The King Cartel would like to reserve a Papagayo daybed for Wed Jun 17 — as mentioned in the Dushi Week itinerary."* The microsite copies the message to the clipboard AND opens `wa.me/?text=…`; group + pre-fill isn't guaranteed by WhatsApp, so the message must read well as a paste. See lessons #14.

### Music
- `spotifyType` + `spotifyId` (defaults: Tommy Coconut artist top-tracks)
- Optional `pinnedTrackId` — when set, the embed plays that specific song first (King family uses "Slice of Paradise")

---

## Recipe

1. **Read the itinerary in full** before writing any code. Get the voice and the rhythm before you start mechanically extracting fields. A microsite that has the right field values but the wrong *voice* feels off.

2. **Decide the slug**: `<PascalCaseFamily>DushiWeek<N>` where `<N>` is a monotonically increasing counter across families. The King family was #42 (King's 42nd birthday year of the Dushi Week tradition — sometimes it's symbolic, sometimes just the next number; confirm with the user).

3. **Copy `apps/web/src/features/dushi-microsite/content/king.ts` to `content/<family>.ts`**. This is the reference implementation — every field is filled out and shows the right shape. Rename the export to `<family>Content`.

4. **Walk the file top-to-bottom**, replacing King-specific values with the new family's. Keep King's content as a reference for what "good" looks like. Specifically:
   - `slug`, `mode`
   - `family.*`
   - `trip.*`
   - `hero.tagline` and `hero.cloudinaryVideoId` (only change the latter if the user pins a different video)
   - `music.pinnedTrackId` (optional — only if they pick a specific track)
   - `whatsapp.groupInviteUrl` (use a `REPLACE_WITH_<FAMILY>_GROUP_INVITE` placeholder if the user hasn't shared one yet — DON'T leave it blank, the rendering depends on the field existing)
   - `philosophy.*`, `letter.*`, `closing.*`
   - `weekGlance` (re-derive from the new days)
   - `days` (this is the bulk — every day card)
   - `crew` (re-personalize the `whatsappMessage` starters)
   - `goodToKnow` (mostly stable; tweak family-specific notes)
   - `beaches`, `experiences`, `iCar`, `estate` (static fallbacks — almost identical across families, only swap if the family is at a non-Bayside-Hill estate)

5. **Create the route**: copy `apps/web/src/app/[locale]/KingDushiWeek42/page.tsx` to `[locale]/<FamilySlug>DushiWeek<N>/page.tsx`. Two changes:
   - `import { kingContent } from "@/features/dushi-microsite/content/king"` → import the new family's content
   - `metadata`: title, description, `path`, `ogImageCloudinaryId`. Keep `robots: { index: false, follow: false }` — these stay personal.

6. **Optional kebab alias**: add `[locale]/<kebab-slug>/page.tsx` that does `redirect("/<FamilySlug>DushiWeek<N>")`. Useful if anyone might type the URL.

7. **Run TypeScript check** from `apps/web/`: `npm run typecheck` (NOT `npx tsc` — it self-installs and bails; in a fresh worktree run `npm install` at the worktree root first). Must exit 0. Catch missing fields or shape mismatches before they hit Vercel.

8. **Verify locally**: open `localhost:3002/<FamilySlug>DushiWeek<N>` and walk every section + every day card. The static fallbacks should render even without Airtable env vars. Test the WhatsApp upsell buttons (they should copy + open `wa.me/?text=…`).

9. **Open a PR** with title `feat(marketing/<family-slug>-dushi-week-<n>): create personalized microsite from itinerary`. Body should list what came from the itinerary verbatim (letter, philosophy, days) and what's defaulted (hero video, music, fallback crew copy).

Half-day estimate for an experienced run — most of the time is in faithful copy transcription (don't rewrite the Tommy voice), not code.

---

## What's already provided by the codebase (do not re-implement)

| Need | Reuse | Notes |
|---|---|---|
| Routing, hash sync, view switching | `MicrositeShell.tsx` | Don't touch. |
| Top + bottom navigation | `TopMenu.tsx` + `BottomMenu.tsx` | Don't touch unless asked. |
| Day card layout | `DayCard.tsx` | Don't touch. |
| Mirrored brand sections | `SectionFamily / SectionStories / SectionWhoIsTommy / SectionBeaches / SectionIcar / SectionEstate / SectionExperiences / SectionRestaurants` | Pull from canonical Airtable. Don't duplicate copy in your new content file. |
| Hero countdown + iOS-safe video | `HeroCountdown.tsx` | Don't touch. |
| Music pill (Spotify embed) | `MusicPlayerPill.tsx` | Don't touch. Use `music.pinnedTrackId` from your content file to pin a track. |
| WhatsApp deep-linking | `lib/whatsapp.ts` | Don't touch. Your `upsells[].whatsappMessage` strings are the only thing you write here. Clipboard + `wa.me/?text=` dual path is already built. |
| Menu scroll chevrons | `HorizontalScroller.tsx` | Wraps both nav bars. Don't touch — it auto-shows `‹`/`›` when items overflow. |
| Tracking (per-session attribution) | `microsite-referral` POST in MicrositeShell | Wires automatically — no work on your side. |

> **Nav is unified.** There's one `BottomMenu` on every viewport (no `MobileTabBar`, no floating WhatsApp FAB — both deleted). The Music + WhatsApp buttons live inside BottomMenu. Top bar = trip pages; bottom bar = brand-story pages. Every section/day view offers forward navigation, not just "back".

---

## Sensible defaults when the itinerary doesn't say

- **Hero video**: `hero-drone-waterfront`
- **Music**: Tommy Coconut top tracks, pinned to "Slice of Paradise" (the family will tell you if they want a different track)
- **Mode**: `"guest"` unless this is being built for a prospect (un-booked lead) — confirm with the user
- **Hero eyebrow**: `"DUSHI WEEK"`
- **Closing sign-off**: `"VACATION IS HOLY. T 🥥"`
- **WhatsApp group**: placeholder `REPLACE_WITH_<FAMILY>_GROUP_INVITE` — get the real URL from the user before final ship
- **Estate**: Bayside Hill unless the itinerary says otherwise
- **Crew**: copy the King's crew list verbatim, then personalize the WhatsApp starter messages ("Hi Boy — it's the <Family> family. ")

---

## Voice rules (the part that ruins a microsite if you get it wrong)

- **Do not rewrite the letter from Tommy.** Lift it verbatim from the itinerary. Punctuation, line breaks, italics — all of it.
- **Do not rewrite the Dushi-Life vocabulary.** "Dushi", "Cartel", "Vacation is holy", "The treasure is out there", "Tommy Coconut" — these are sacred phrases. Don't make them more corporate, don't simplify them, don't translate them.
- **Tommy is never photographed.** When rendering the crew + Family section, his card is bio-only (`has_photo: false`). The microsite codebase already enforces this — just don't add a Cloudinary image for him in your content.
- **Days have a vibe and a rhythm, not a checklist.** The `subtitle` field carries the emotional read of the day; the `schedule` carries the activities. Don't merge them.
- **The microsite is a letter, not a sales page.** First-person, no "discover", no "experience our luxury", no "world-class". Match the itinerary's voice exactly — it was already written in the right voice.

If in doubt, invoke the `tommy-coconut-voice` skill before writing copy.

---

## Verification before claiming "shipped"

1. **TypeScript clean**: `npm run typecheck` from `apps/web/` exits 0 (NOT `npx tsc`).
2. **Local preview**: every section + every day renders. Day cards show their photos (the cldUrl fallback should make this work even without `NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME` set).
3. **Mobile (375×812)**: hero video autoplays; bottom menu's `‹` / `›` chevrons appear when items overflow; Days dropdown opens on tap.
4. **Vercel production deploy succeeds**: `gh api repos/TommyCoconutIT/tommy-os/deployments` → newest "Production – tommy-web" deploy → state `success`. **Don't tell the user "live" until this is green** — failed builds keep the previous deploy serving.
5. **Curl the prod URL**: confirm the hero video URL contains the right Cloudinary public ID.

For everything you might trip on, read `~/.claude/skills/dushi-week-microsite/references/lessons-learned.md`. Every gotcha is something that already happened on the King build.

---

## Phase 2 add-ons (do not include unless the user asks)

These are out of scope for the initial create-from-itinerary pass. Mention them only if the user says "what's possible next":
- Voice notes from crew (audio clips with play buttons)
- Father's Day / surprise modal on a specific day
- Photo carousels per day
- Ambient soundscape toggle
- Easter-egg pirate-map closing card
- PWA "Add to Home Screen"
- iCal export
- Tide/moon data on the boat day
- Memory Mode (post-stay gallery + rebook CTA)

---

## Quick reference — the King build

| Artifact | Path |
|---|---|
| Content config | `apps/web/src/features/dushi-microsite/content/king.ts` |
| Route | `apps/web/src/app/[locale]/KingDushiWeek42/page.tsx` |
| Live URL | `https://www.tommycoconutprivateresorts.com/KingDushiWeek42` |
| Source itinerary (the input that produced it) | `~/Downloads/King-Dushi-Week.html` |

Use the King microsite as the canonical reference for "what the output looks like". When you're stuck on a content shape question, look at king.ts first.
