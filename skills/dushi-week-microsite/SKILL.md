---
name: dushi-week-microsite
description: "Build and edit personalized interactive Dushi Week microsites (web pages) for Tommy Coconut Private Resorts guests at /<FamilySlug>DushiWeek<N>. Use whenever the user wants to create a new family microsite, edit the hero video/photos, add or modify menu sections, mirror brand pages (Family / Stories / Who's Tommy / Beaches / iCar / Estate / Map), wire the music or WhatsApp, fix day-card photos, restyle the closing block, change navigation, or tune iOS autoplay behavior. Triggers on phrases like 'King microsite', 'Dushi Week page', 'KingDushiWeek42', 'hero video', 'day cards', 'bottom menu', 'estate map', 'interactive microsite', 'mirror /family / /guest-stories / /who-is-tommy', 'mirror the live page', 'family microsite for <name>', or any work on the Next.js page at apps/web/src/app/[locale]/<Slug>/page.tsx and its `features/dushi-microsite/` components. Distinct from the dushi-week-builder skill which produces the printable HTML/PDF/DOCX itinerary document — this skill is for the live interactive page on tommycoconutprivateresorts.com."
---

# Dushi Week Microsite

A skill for building and editing the interactive **web microsite** that each Tommy Coconut family gets at `tommycoconutprivateresorts.com/<FamilySlug>DushiWeek<N>` (e.g. `/KingDushiWeek42`). This is the close-of-sale + during-trip + share-with-friends page — not the printable itinerary (that's the `dushi-week-builder` skill).

## ⚠️ Read this first

Before editing, read `references/lessons-learned.md`. It captures the real production incidents from the first build (Vercel build failures hiding live, squash-merge dropping props, iOS hero autoplay silently failing on mobile, dev-server `.next` getting clobbered, etc.). Every gotcha is something that already happened — not theoretical.

Then for big jobs, read `references/architecture.md` for the file map.

---

## What lives where

```
apps/web/
├── src/app/[locale]/
│   ├── KingDushiWeek42/page.tsx        ← per-family route (server component)
│   └── king-dushi-week-42/page.tsx     ← optional kebab alias (301 → PascalCase)
├── src/features/dushi-microsite/
│   ├── content/king.ts                 ← ONE typed config per family
│   ├── types.ts                        ← DushiMicrositeContent, DayCard, etc.
│   ├── lib/
│   │   ├── today.ts                    ← pre-trip / today / post-trip mode
│   │   └── whatsapp.ts                 ← group invite + clipboard helper
│   └── components/
│       ├── MicrositeShell.tsx          ← client root: hash routing, view switch
│       ├── HeroCountdown.tsx           ← cinematic hero w/ video + countdown
│       ├── TopMenu.tsx                 ← sticky top nav (in-trip pages)
│       ├── BottomMenu.tsx              ← sticky bottom nav (brand pages + Music + WA)
│       ├── DayCard.tsx                 ← single day card
│       ├── SectionBeaches.tsx          ← mirror of /beaches (canonical + static)
│       ├── SectionIcar.tsx
│       ├── SectionRestaurants.tsx
│       ├── SectionExperiences.tsx      ← Dushi Memories
│       ├── SectionEstate.tsx           ← mirror of /estates/bayside-hill
│       ├── SectionFamily.tsx           ← mirror of /family
│       ├── SectionStories.tsx          ← mirror of /guest-stories
│       ├── SectionWhoIsTommy.tsx       ← mirror of /who-is-tommy
│       ├── CuracaoMap.tsx              ← Mapbox; has `compact` prop
│       ├── MusicPlayerPill.tsx         ← Spotify iframe + window-event toggle
│       ├── MobileTabBar.tsx            ← phone-only bottom bar
│       ├── ShareSection.tsx, IWantThisWeek.tsx, OfferCountdown.tsx,
│       ├── ExitIntentModal.tsx, MobileStickyCTA.tsx, etc.
└── src/app/globals.css                 ← `.ms-*` styles all live here
```

**Hard rule**: only edit inside `apps/web/`. Never touch `apps/portal/`, `apps/web/`, or `packages/` (per `apps/web/CLAUDE.md`).

---

## How a microsite works (one breath)

1. The server page (`[locale]/<Slug>/page.tsx`) calls a bundle of Airtable getters in `Promise.all`, each wrapped in a `safe<T>(fn, fallback)` so missing creds fail soft → static fallback.
2. It passes the family content config (`kingContent`) plus a `canonical` object (Airtable rows) into `<MicrositeShell>`.
3. `MicrositeShell` is a client component. It owns:
   - `activeView` (one of: `home`, `philosophy`, `beaches`, `icar`, `restaurants`, `memories`, `estate`, `map`, `family`, `stories`, `who-is-tommy`, `good-to-know`)
   - `activeDayId` (when set, single-day view takes priority over `activeView`)
   - URL hash sync (`#beaches`, `#day-3`, etc.)
4. Based on `activeView` + `activeDayId`, it renders one of three layouts: **HomeView** (week glance + share + closing), **SingleDayView** (one DayCard + prev/next/home), or **SectionView** (one section like SectionFamily).
5. The hero + mode/offer banners only show on home view. Other views go straight from the top nav into content.

---

## Building a new family microsite (Phase 1 — 1 day)

**Steps:**

1. **Copy `content/king.ts` → `content/<family>.ts`.** Rename the export, change `slug`, `family.*`, `trip.*`, `whatsapp.groupInviteUrl`, `hero.cloudinaryVideoId` (if pinned), `closing.*`. Keep the structural shape identical.

2. **Create the route.** Add `apps/web/src/app/[locale]/<PascalCaseSlug>/page.tsx`. Copy `KingDushiWeek42/page.tsx` verbatim and only change two things:
   - `import { kingContent } from "@/features/dushi-microsite/content/king"` → your new config
   - `metadata`: title, description, `path`, `ogImageCloudinaryId`
   - **Keep `robots: { index: false, follow: false }`** — these pages stay personal.

3. **Optional kebab alias.** Add `[locale]/<kebab-slug>/page.tsx` that does `redirect("/<PascalCaseSlug>")`. Both URLs then work.

4. **Curate day photos.** Each `DayCard.heroCloudinaryId` is a Cloudinary public ID (no `.jpg` / `.png` extension — `f_auto` handles format). The full URL Cloudinary builds is `https://res.cloudinary.com/tommy-coconut/image/upload/f_auto,q_auto,w_1600/<publicId>`.

5. **Run the dev server, navigate to the new slug, walk every section.** Type check is not enough — actually click through.

6. **Open a PR.** Match the established commit-message style: `feat(marketing/<family>-dushi-week-<n>): <one line>`.

Estimate: a fresh microsite for a new family that reuses everything = ~half a day if their content is ready.

---

## Common one-off edits

### Change the hero video
Set `content.hero.cloudinaryVideoId` in `content/<family>.ts`. The fallback chain in `MicrositeShell` is: `content.hero.cloudinaryVideoId` → `canonical.homepage?.heroVideoCloudinaryId` → `canonical.estate?.heroVideoCloudinaryId` → image fallback (`content.hero.cloudinaryFallbackImageId`).

**The order matters** — if you remove the `content.hero.cloudinaryVideoId ||` part of the chain, microsite-specific overrides stop working and you inherit whatever the marketing homepage row in Airtable says.

### Change a day's hero photo
Edit the `heroCloudinaryId` for that day inside `content/<family>.ts`. Use the subtitle as a unique anchor for the edit — the Cloudinary public IDs are sometimes shared across days, so `heroCloudinaryId: "X"` is not unique by itself.

### Change a section's headline text
- "Your island, mapped" / "The island is the resort" → `components/CuracaoMap.tsx`
- Memory eyebrows ("One Full Day", etc.) → these come from **Airtable** (`getMemoriesMarketing`), not code. If you must override one for a single microsite, do a `.replace()` inside `SectionExperiences.tsx`'s render and add a one-liner comment explaining why.

### Add a section photo hero
Use the reusable primitive — see "Style primitives" below. Render `<section className="ms-section-photohero" style={{backgroundImage: "url(...)"}}>...</section>` at the top of any section component.

### Add a new menu section
1. Extend the `ActiveView` union in `TopMenu.tsx`.
2. Add it to `SECTION_VIEWS` in `MicrositeShell.tsx`.
3. Add a `case "<name>":` in `SectionView`'s switch with the body.
4. Decide top or bottom bar: keep TopMenu focused on in-trip pages (Philosophy → Estate); push brand-story pages (Family, Stories, Who's Tommy, Good to Know) into `BottomMenu.tsx`'s `BOTTOM_ITEMS`.

### Mirror a live brand page inside the microsite
Pattern (used for Family, Stories, Who's Tommy, Beaches, iCar, Estate, Memories):

1. **Find the live page**: `apps/web/src/app/[locale]/<page>/page.tsx`.
2. **Identify its Airtable getters** (e.g. `getCoconutCartel`, `getCartelHeroBg`, `getCartelCtaBg`).
3. **Add them to the server page's `Promise.all`**, each wrapped in `safe<T>(() => fn(), <fallback>)`.
4. **Extend the `CanonicalData` type** in `MicrositeShell.tsx` and the `EMPTY_CANONICAL` constant.
5. **Create `Section<X>.tsx`** that takes the canonical data + bg props. Copy the live page's JSX, drop `<SiteHeader>` / `<SiteFooter>` / `<DualApplyCta>` / `<JsonLdScript>`. Reuse the same CSS classes (`page-header`, `family-grid`, `longread`, `story-item`, `wall-card`, etc.) — they already exist in `globals.css`. The microsite section then matches the live page automatically.
6. **Provide a static fallback** for local dev without Airtable env vars (or accept that this section won't render locally).

### Integrate the music + WhatsApp into the bottom menu (already done)
Music is a button in `BottomMenu` that dispatches `window.dispatchEvent(new CustomEvent("ms-music-toggle"))`. `MusicPlayerPill` listens for that event and flips its open/closed state. WhatsApp is just an `<a href={groupInviteUrl} target="_blank">` button in the same bar. **Do not bring back the floating circular FABs** — the user explicitly asked to integrate them into the bar.

---

## Style primitives in `globals.css`

These are scoped under `.microsite` and meant to be reused. Look at the King microsite for live examples.

- `.ms-section-photohero` — dark photo with a scrim + gold eyebrow + serif heading. Background image is set inline via `style={{ backgroundImage: "url(...)" }}`. Has a sibling `.ms-section-photohero-scrim` and `.ms-section-photohero-inner` for content. Used by Beaches, iCar, can be reused for any cinematic section open.
- `.ms-section-videohero` — same as above but the background is an autoplay muted looping `<video>` element instead of a `background-image`. Used by SectionEstate for the Bayside Hill walk-through. See HeroCountdown for the iOS-safe video setup pattern.
- `.ms-hero-scrim` — sibling div placed after the hero `<video>` so the gradient sits between the video and the headline. Without this, the video washes the text out.
- `.ms-closing` — navy block with the message-in-a-bottle background, gold serif heading, "VACATION IS HOLY. T 🥥" sign-off. Uses `.ms-closing-bg`, `.ms-closing-scrim`, `.ms-closing-inner`.
- `.ms-topmenu` + `.ms-bottommenu` — both navy bars; top is sticky-top, bottom is sticky-bottom; both use the same `.ms-*menu-link` / `.is-active` styling. Bottom adds `.ms-bottommenu-actions` (Music + WhatsApp on the right).
- `.ms-music` — Spotify compact iframe (280×80) bottom-left, with `.ms-music-close` × button.
- `.estate-map-frame` — 4:3 ratio box. When CuracaoMap is dropped inside with `compact`, the embed fills via `.estate-map-frame .ms-map-embed { position: absolute; inset: 0 }`.

---

## Verification before claiming "shipped"

1. **TypeScript clean**: from `apps/web`, run `npm run typecheck` (NOT `npx tsc` — it self-installs and bails). Must exit 0. In a fresh worktree, `npm install` at the worktree root first.
2. **Local preview**: navigate to `/<Slug>` on `localhost:3002`. Walk every section + every day card. The static fallbacks should all render even without Airtable env vars.
3. **Mobile viewport**: resize the preview to 375×812. Hero video must autoplay; the MobileTabBar replaces the BottomMenu.
4. **`gh pr create`**, then **wait for the Vercel production deploy to go `success`** before telling the user it's live:
   ```bash
   gh api repos/TommyCoconutIT/tommy-os/deployments --jq '.[] | select(.environment=="Production – tommy-web") | {sha:.sha[0:7], created_at, id}' | head -3
   gh api repos/TommyCoconutIT/tommy-os/deployments/<id>/statuses --jq '.[0:1] | .[] | {state, target_url}'
   ```
5. **Confirm the prod HTML actually serves the change**:
   ```bash
   curl -sL -A "Mozilla/5.0" "https://www.tommycoconutprivateresorts.com/<Slug>" \
     | grep -oE 'res\.cloudinary\.com[^"]+\.mp4' | head -1
   ```

If the Vercel deploy state is `failure`, **prod is still serving the previous successful deploy** — your "merged" PR is invisible. Diagnose, push a fix, re-verify.

---

## Worktree + PR workflow (the one that works)

Inside the worktree at `apps/web/.claude/worktrees/<branch>/`:

```bash
# Branch off latest main, even mid-edit:
git fetch origin main
git stash push -m <topic> -- apps/web/src
git checkout -b marketing/<topic> origin/main
git stash pop
# If a conflict arises (because a sibling PR isn't merged yet), prefer the
# stashed (your) side — git checkout --theirs is "their" stashed change here:
git checkout --theirs <conflicted-file>
```

To merge after approval:

```bash
gh pr merge <num> --squash --delete-branch --admin
```

`--admin` is needed because `main` is checked out in the parent worktree. The squash-merge itself succeeds; the `--delete-branch` step *partially* fails with `fatal: 'main' is already used by worktree at ...`. The remote branch is usually deleted anyway (GitHub does that server-side); if not, run:

```bash
gh api repos/TommyCoconutIT/tommy-os/git/refs/heads/marketing/<topic> -X DELETE
```

---

## Voice + content rules

- The microsite is a letter, not a sales page. First-person, no "discover", no "experience our luxury".
- The Dushi Life vocabulary is sacred: *dushi* (sweet, good), *cartel* (the family group), "the treasure is out there", "VACATION IS HOLY. T 🥥". Don't rewrite these.
- Tommy is **never photographed** — the live `/who-is-tommy` page renders his bio card with `class="family-card no-photo"`. The mirror in `SectionWhoIsTommy.tsx` follows the same rule.
- Every section that has a live brand-page equivalent should pull from the same Airtable rows so updates propagate automatically. **Don't hardcode copy that lives in Airtable.**
- For personalization (family names, dates, dinner picks, vibe lines), it's `content/<family>.ts`. That's the only file that should differ between microsites.

---

## Phase 2 ideas (after the family approves Phase 1)

These were scoped out of the initial King build. Don't volunteer them; propose only if the user asks "what's next":
- Voice notes from Boy / Captain Magic Mike / Jeremiah (audio clips with play button)
- Father's Day Sunday modal (Dad-only surprise on Day 5)
- Photo carousels per day
- Soundscape ambient toggle
- Easter-egg pirate-map closing card
- PWA "Add to Home Screen"
- iCal export
- Tide/moon data on the boat day
- Memory Mode (post-stay) — gallery + rebook CTA

---

## What this skill is NOT

- Not the printable itinerary document → use `dushi-week-builder` instead
- Not the guest portal (`apps/portal/`) → totally different app
- Not the WordPress site (archived in `apps/web/`) → ignore it
- Not for editing Airtable directly — when you need a content change that lives in Airtable (e.g. "Memory 02 · One Full Day" copy), tell the user it's an Airtable edit, not a code edit
