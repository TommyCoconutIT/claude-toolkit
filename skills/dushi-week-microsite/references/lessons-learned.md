# Lessons Learned — Dushi Week Microsite

These are real production incidents from the microsite builds (King, Bama, Wyand, Friends, Adams Trio, Reunion Cartel, …). Each one cost time and at least one shipped a broken hero to prod. Read this before editing. Lessons 1–22 are the King-era core; 23+ are later additions (most recent: the Reunion Cartel two-coconut **lead** build — #53, Dushi Hideaway, 2026-05-25). The canonical list of every page/build ("pages made") is the Airtable **Dushi Weeks** registry — see lesson #35.

---

## 1. The Cloudinary `CLOUD` env-var trap

**What happened.** Several microsite components built Cloudinary URLs with a hard guard on `process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME`. When the env var wasn't set (local dev), those helpers silently returned `""` — so the video, day-card photos, and section heroes all rendered nothing. We spent a debugging cycle on each of `HeroCountdown`, `DayCard`, and others before realizing they all had the same bug.

**The fix.**
```ts
const CLOUD = process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME ?? "tommy-coconut";
function cldUrl(publicId: string, w = 1600) {
  if (!publicId) return "";
  return `https://res.cloudinary.com/${CLOUD}/image/upload/f_auto,q_auto,w_${w}/${publicId}`;
}
```

**The rule.** Every Cloudinary URL builder in `features/dushi-microsite/` falls back to `"tommy-coconut"`. Other components in the codebase (`SectionExperiences`, `CrewGallery`) already did this — match them. Production still has the env var set, so the fallback only matters for local dev, but missing local dev rendering means you can't catch issues before shipping.

---

## 2. iOS Safari hero autoplay isn't automatic

**What happened.** Desktop hero video played fine; on mobile it stayed on the poster forever. The video had all the "right" attributes — `autoPlay muted loop playsInline` — but iOS Safari still refused to autoplay.

**Why.** Two iOS gotchas:
1. The JSX `muted` prop sometimes isn't honored after hydration. The DOM element ends up with `muted = false` even though the JSX said `muted`.
2. A `<source>` child element occasionally fails to register on first paint in iOS Safari.

**The fix.** All three together:
```tsx
const videoRef = useRef<HTMLVideoElement | null>(null);

useEffect(() => {
  const v = videoRef.current;
  if (!v || !videoUrl) return;
  v.muted = true;                 // force-mute via DOM, not JSX
  const tryPlay = () => {
    const p = v.play();
    if (p && typeof p.catch === "function") p.catch(() => {});
  };
  tryPlay();
  // If autoplay was blocked, kick it off on first touch.
  const onTouch = () => {
    tryPlay();
    window.removeEventListener("touchstart", onTouch);
  };
  window.addEventListener("touchstart", onTouch, { passive: true, once: true });
  return () => window.removeEventListener("touchstart", onTouch);
}, [videoUrl]);

return (
  <video
    ref={videoRef}
    src={videoUrl}                {/* src directly, NOT a <source> child */}
    autoPlay muted loop playsInline preload="auto"
    poster={bgImg || undefined}
    aria-hidden="true"
  />
);
```

**The rule.** Any autoplay-muted hero video in this repo gets this exact pattern. Test by resizing the preview to 375px and checking `video.paused === false` after a few seconds.

---

## 3. Squash-merge can silently drop a prop

**What happened.** PR #277 (homepage hero video + scrim fix) added a `posterPublicId` prop to `HeroCountdown`. PR #278 (a larger refactor) was opened before #277 merged. When #278 got squash-merged, the `posterPublicId` prop on `HeroCountdown` disappeared — even though `MicrositeShell` still passed it in. PR #279 (the next change) failed to build on Vercel:

```
Type error: Property 'posterPublicId' does not exist on type 'IntrinsicAttributes & Props'.
```

Vercel kept the previous successful deploy live, so production still served the **wrong** hero video for ~10 minutes after I told the user "shipped." The user had to point out the wrong video was still showing.

**The rule.**
- After any squash-merge that depended on another PR, **immediately** `npm run typecheck` (from `apps/web`) against the new `origin/main`. If it fails, you have an orphan change to restore.
- Watch the Vercel deploy status:
  ```bash
  gh api repos/TommyCoconutIT/tommy-os/deployments --jq \
    '.[] | select(.environment=="Production – tommy-web") | {sha:.sha[0:7], created_at, id}' | head -3
  # then for the newest id:
  gh api repos/TommyCoconutIT/tommy-os/deployments/<id>/statuses --jq '.[0:1]'
  ```
- Confirm prod actually serves the change:
  ```bash
  curl -sL -A "Mozilla/5.0" "https://www.tommycoconutprivateresorts.com/KingDushiWeek42" \
    | grep -oE 'res\.cloudinary\.com[^"]+\.mp4' | head -1
  ```
  Compare the public ID to what `content/<family>.ts` says.

---

## 4. `npm run build` clobbers the dev server

**What happened.** Mid-debug I ran `npm run build` in the same worktree where the dev server was running. The production build overwrote `.next/` artifacts that the dev server's HMR depended on. Dev started throwing `Cannot find module './vendor-chunks/@sentry.js'` and `Cannot find module './5321.js'` errors on every request.

**The fix.**
```bash
# Stop dev server first:
preview_stop <serverId>
rm -rf apps/web/.next
preview_start Web
```

**The rule.** Don't run `npm run build` in the dev tree. If you need to verify a production build will work, either:
- Trust the type check (`npm run typecheck` from `apps/web`) for type-level errors, OR
- Run `npm run build` in a separate worktree.

---

## 5. Vercel build failures don't roll back — they freeze prod

**What happened.** PR #279's prod build failed. Vercel's behavior in that case is "keep the last successful deploy live." So prod kept serving the old hero video. The PR was marked merged in GitHub. The deploy status said `failure`. The user saw the wrong video and asked why nothing changed.

**The rule.** "Merged" ≠ "deployed". Always check the deployment state, not the PR state. If the build failed, the previous deploy is still live and your "shipped" claim is wrong.

---

## 6. Worktree breaks `gh pr merge --delete-branch`

**What happened.** Inside the worktree, `gh pr merge <n> --squash --delete-branch` errors out with `fatal: 'main' is already used by worktree at '/Users/raybongers/Claude 4.6/tommy-os'`. The squash-merge itself succeeds (with `--admin`); only the local-branch-delete step fails. GitHub usually deletes the remote branch server-side anyway.

**The fix.** Use `--admin`, then delete the remote branch via the API if needed:
```bash
gh pr merge <num> --squash --delete-branch --admin   # squash succeeds; delete-branch may partial-fail
gh pr view <num> --json state                        # confirm "MERGED"
gh api repos/TommyCoconutIT/tommy-os/git/refs/heads/marketing/<topic> -X DELETE  # cleanup
```

`422 Reference does not exist` from the cleanup call is fine — it means GitHub already deleted it.

---

## 7. Stash + branch-off-main with conflict resolution

**Setup.** While editing on branch A, you want to open a fresh PR off `origin/main`. The flow:

```bash
git fetch origin main
git stash push -m <topic> -- apps/web/src
git checkout -b marketing/<topic> origin/main
git stash pop
```

**When conflicts happen.** If a sibling PR is open and touches the same files, `git stash pop` will leave conflict markers. Your stashed version is "theirs" in stash-pop terminology (because the working tree is "ours"). To take the stashed (your) side:

```bash
git checkout --theirs <conflicted-file>
git add <conflicted-file>
```

Verify no leftover markers:
```bash
grep -rl '<<<<<<<' apps/web/src
```

---

## 8. Spotify silently refuses programmatic playback for non-Premium

**What happened.** Multiple attempts to make music autoplay on landing (IFrame API, gesture listeners, ref-based `.play()` calls) all failed for anonymous (non-Premium) Spotify visitors. The audio just never started.

**The fix.** Use Spotify's own iframe embed and let the user press Spotify's own play button. We can pin a specific track via `music.pinnedTrackId` ("Slice of Paradise"). The bottom-menu Music button just toggles the iframe's visibility.

**The rule.** No matter how clever the workaround, Spotify will block programmatic playback for free-tier users. Show their UI and let them click.

---

## 9. Cross-component state via window events

**Pattern.** The bottom-menu Music button needs to toggle the floating Spotify pill that lives elsewhere in the tree. Instead of lifting state up through MicrositeShell:

```ts
// In BottomMenu:
function toggleMusic() {
  window.dispatchEvent(new CustomEvent("ms-music-toggle"));
}

// In MusicPlayerPill:
useEffect(() => {
  function onToggle() { setClosed((c) => !c); }
  window.addEventListener("ms-music-toggle", onToggle as EventListener);
  return () => window.removeEventListener("ms-music-toggle", onToggle as EventListener);
}, []);
```

This kept MicrositeShell clean and didn't require a context provider. Use for similar 1:1 sibling-component toggles, but don't overuse — for anything more than a binary flip, lift state up.

---

## 10. Soft-fail Airtable canonical fetches

**Pattern.** The server page wraps every canonical fetch in `safe<T>(fn, fallback)`:

```ts
async function safe<T>(fn: () => Promise<T>, fallback: T): Promise<T> {
  try { return await fn(); }
  catch (err) {
    console.warn("[king-dushi-week] marketing fetch failed:", (err as Error).message);
    return fallback;
  }
}

const [beaches, cartel, stories, ...] = await Promise.all([
  safe<BeachRow[]>(() => getBeachMarketing(), []),
  safe<CartelMember[]>(() => getCoconutCartel(), []),
  safe<GuestStoryRow[]>(() => getGuestStories(), []),
  // ...
]);
```

Without this, missing Airtable env vars throw and the entire page errors out. With this, sections that depend on Airtable show their static fallback (or nothing) and the rest of the page still renders. Local dev becomes possible without secrets.

---

## 11. "Mirror live page" pattern — what to drop, what to keep

When mirroring a live brand page (`/family`, `/guest-stories`, `/who-is-tommy`) into a microsite section:

**Keep**:
- All copy, headlines, sub-copy verbatim
- Image / video Cloudinary IDs
- The same Airtable getter calls
- The same CSS class names (`page-header`, `family-grid`, `longread`, `story-item`, `wall-card`, `divider-line`, `longread-emphasis`, `figure wide`) — they all exist in `globals.css` already

**Drop**:
- `<SiteHeader>` and `<SiteFooter>` — the microsite has its own chrome
- `<DualApplyCta>` — the microsite has its own I-Want CTA
- `<JsonLdScript>` — the microsite is `robots: noindex`, no need for structured data
- The whole-page `<main>` wrapper

The result looks pixel-identical to the live page but slots into the microsite's nav model.

---

## 12. PascalCase routes are fine

Next.js routes are case-sensitive but PascalCase works. `/KingDushiWeek42` is a real route. If the user wants a kebab alias for shareability, add a sibling page that does `redirect("/KingDushiWeek42")`. Don't try to "fix" the PascalCase — it's intentional.

---

## 13. WhatsApp group invite `?mode=gi_t` param — behavior is INCONSISTENT, don't pick a fixed rule

**What happened (and kept happening).** The `?mode=gi_t` query param on Dushi Week group invites has **flipped** between required and broken across guests and dates:
- **2026-05-21, Bama Famjam:** the *stripped* URL did NOT open the group; adding `?mode=gi_t` back fixed it.
- **2026-05-22, Hernandez Island Hoppers** (and the King build): the URL *with* `?mode=gi_t` did NOT open the group; stripping it to the bare form fixed it.

**Why.** The param doesn't control *correctness* — a WebFetch of both the clean and param URLs resolves server-side to the same group. The real failure is in the WhatsApp app's universal-link hand-off, which is **device / client / version dependent** and can't be reproduced from the dev environment. So neither "always strip" nor "always keep" is right.

**The rule (verify, then match the user's latest report):**
1. When a group link "won't open", WebFetch `https://chat.whatsapp.com/<code>` (and the `?mode=gi_t` variant) and confirm the `og:title` is the expected group name with a working "Join Chat" — that proves the code is valid and which group it opens.
2. Then **ship whichever variant the user's own-phone test says works** right now. If they report the param version broken → ship the bare canonical link. If they report the bare version broken → add `?mode=gi_t` back. Do **not** argue from this lesson or from memory — defer to their latest device test.
3. The native mobile path (`BottomMenu.tsx`) builds a `whatsapp://chat?code=<code>` deep-link (param stripped) with the full `groupInviteUrl` as the ~1.4s fallback — so the param only affects the desktop/fallback href, not the native scheme.

This matches the reconciled persistent-memory note `feedback_whatsapp_invite_param.md` (the canonical source — keep them in sync).

---

## 14. Group + pre-filled WhatsApp text is impossible via URL — do BOTH

**What happened.** The user wanted the upsell ("Yes, count us in") to open WhatsApp with the message already in the input. We tried opening the group invite URL with the message — WhatsApp **ignored** the text. We switched to `wa.me/?text=…` — on the user's iOS WhatsApp it opened the most-recent chat (the group) and **still** dropped the text.

**Why.** WhatsApp's URL scheme genuinely has no "open this group AND pre-fill text" form:
- `chat.whatsapp.com/<id>` → opens group, **always** ignores `text=`
- `wa.me/<PHONE>?text=…` → 1:1 chat, text reliably pre-filled (but it's a phone, not a group)
- `wa.me/?text=…` → *documented* as a share-with picker, but some iOS versions silently open the recent chat and drop the text

**The fix (updated 2026-05-22 — use the recipient when there is one).** `wa.me/?text=` (no recipient) was the original compromise, and it's genuinely broken on iOS (opens the most-recent chat, drops the text) — a user flagged that upsells "don't open Tommy's number and the message is gone." The fix: when the invite is a **1:1 number** (`wa.me/<phone>` — every *prospect* page has no group yet, so `whatsapp.groupInviteUrl` points at Tommy's mobile), open **that** chat with the text reliably pre-filled. Only true group invites (`chat.whatsapp.com`) fall back to clipboard + share-picker, because WhatsApp can't pre-fill a group.
```ts
export async function openGroupWithMessage(groupInviteUrl: string, message: string) {
  let copied: WhatsAppOpenResult = "opened-only";
  try {
    if (navigator?.clipboard) { await navigator.clipboard.writeText(message); copied = "copied-and-opened"; }
  } catch { /* rare iOS clipboard block — fall through */ }
  if (typeof window !== "undefined") {
    const phone = extractWaMePhone(groupInviteUrl);              // /wa\.me\/(\d{6,15})/ → digits or null
    const url = phone
      ? `https://wa.me/${phone}?text=${encodeURIComponent(message)}`   // 1:1, text reliably pre-filled
      : `https://wa.me/?text=${encodeURIComponent(message)}`;          // group → share picker fallback
    window.open(url, "_blank", "noopener,noreferrer");
  }
  return copied;
}
```
Used by `UpsellCard` ("Yes, count us in") **and** `CrewGallery` ("Message …"). For a number-invite, the message lands pre-filled in Tommy's chat (no paste needed); the clipboard copy stays as a harmless backup. Toasts must be family-agnostic — "Opening WhatsApp to Tommy Coconut — your message is ready" — NOT "paste in the King Cartel group" (that hardcoded "King Cartel" string was a stale bug on every family's fallback crew gallery).

**The rules.**
- **Prospect pages set `whatsapp.groupInviteUrl: "https://wa.me/<tommyNumberE164NoPlus>"`** (e.g. `https://wa.me/59996968263`). There's no group until the guest books, so the number IS the right target — and it's the only form that pre-fills text reliably.
- **Booked-guest pages** keep a real `chat.whatsapp.com/<id>` group → clipboard + picker (group + pre-filled text is still impossible via URL; see the channel table above).
- The offer "Questions first?" button (`IWantThisWeek`) already used `buildWaMeLink(fallbackTcPhone ?? "59996968263", msg)` → it was always correct; its label is now "WhatsApp Tommy Coconut now".

---

## 15. `overflow-x: auto` clips absolutely-positioned dropdowns

**What happened.** On mobile, tapping the **Days** dropdown did nothing visible — the panel rendered but never appeared. It worked fine on desktop.

**Why.** The Days trigger lived inside `.ms-topmenu-left`, which has `overflow-x: auto` for horizontal scrolling. A container with `overflow` set on *one* axis effectively clips the *other* axis too (browsers force `overflow-y` to `auto`/`hidden` when `overflow-x` is `auto`). The absolutely-positioned dropdown panel dropping *below* the bar got clipped.

**The fix.** Render the dropdown trigger **outside** the `overflow-x` container. We moved the Home button + Days dropdown to be direct children of `.ms-topmenu-inner`, leaving only the scrollable section links (`Beaches → Estate`) inside `.ms-topmenu-left`.

**The rule.** Never put a dropdown/popover trigger inside an `overflow-x: auto` (or `overflow: hidden`) scroll container. Move it out, or render the panel via portal/`position: fixed`.

---

## 16. `text-align: center` centers contents, not constrained blocks

**What happened.** We set `text-align: center` on the hero `<section>` for Family / Stories / Tommy. The eyebrow centered, but the **headline and lead stayed left**.

**Why.** `globals.css` gives `.page-header h1` a `max-width: 20ch` and `.page-header .lead` a `max-width: 55ch`. `text-align: center` aligns the *text inside* a block; it does nothing about *where the block itself sits* when the block is narrower than its parent. With no auto margins, the constrained block hugs the left edge.

**The fix.** Add `margin-inline: auto` to every `max-width`-constrained element you want centered:
```tsx
<h1 className="display" style={{ marginInline: "auto" }}>…</h1>
<p className="lead" style={{ marginInline: "auto" }}>…</p>
```

**The rule.** To center a block both ways: `text-align: center` (for inline content) **plus** `margin-inline: auto` (for the block itself) **plus**, on the flex container, `align-items: center` + `justify-content: center` + a `min-height`.

---

## 17. Microsite-only content overrides — don't edit Airtable for microsite tweaks

**What happened.** Twice the user wanted to change canonical content *only on the microsite*: "Memory 02 · One Full Day" → "One Half Day", and hide the "Top-shelf rum… Restocked through the week." line on the Bayside Hill estate. Both strings live in **Airtable** and are shared with the live `/dushi-memories` and `/estates/bayside-hill` pages.

**The fix.** Override at the **microsite render layer**, not in Airtable — so the live brand pages stay untouched:
```tsx
// String replace (Memory eyebrow):
{m.public_eyebrow.replace("One Full Day", "One Half Day")}

// Filter out one story line (Estate):
{block.lines
  .filter((line) => line.trim() !== "Top-shelf rum, tequila, vodka, gin. Restocked through the week.")
  .map((line, j) => <p key={j}>{line}</p>)}
```

**The rule.** When a microsite-specific content change touches Airtable-sourced copy, ask: "should the live page change too?" If no → filter/replace in the microsite component. If yes → it's an Airtable edit (and tell the user it lives in Airtable, not code).

---

## 18. Scroll-affordance chevrons for overflowing menus

**Pattern.** When the top/bottom menus overflow on narrow viewports, users didn't realize there was more — the cut-off items just looked clipped. The `HorizontalScroller` component wraps `.ms-topmenu-left` / `.ms-bottommenu-left` and shows `‹` / `›` chevrons **only when** that side has hidden content:

```ts
function update() {
  setCanScrollLeft(el.scrollLeft > 4);
  setCanScrollRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 4);
}
// listen on: el "scroll", ResizeObserver(el), MutationObserver(el, {childList,subtree})
// click chevron → el.scrollBy({ left: ±200, behavior: "smooth" })
```

Hidden chevrons get `opacity: 0; pointer-events: none; tabIndex: -1` so they're fully inert. Reuse `HorizontalScroller` for any horizontally-scrollable strip.

---

## 19. Mobile nav unified with desktop — MobileTabBar deleted

**What happened.** The microsite originally had a separate `MobileTabBar` (Days · Map · Family · Chat) on phones and a `BottomMenu` on desktop. The user wanted the **same** bottom menu on both. We deleted `MobileTabBar` entirely, removed the `@media (max-width:760px){ .ms-bottommenu{display:none} }` hide rule, and added tighter mobile padding + iOS safe-area inset to `.ms-bottommenu-inner`. The bottom nav now horizontally-scrolls (with chevrons, see #18) on phones.

**The rule.** One nav component, responsive — not two parallel ones to keep in sync. If a phone bar feels cramped, make the shared bar responsive rather than forking it.

---

## 20. Forward navigation everywhere, not just "back"

**What happened.** Section views and day cards only offered "← Back to the week". Users hit a dead end at the bottom of each section.

**The fix.** Every section view ends with a `‹ Back` + `Next: <next section> →` pager (`SECTION_LABELS` maps the order). Day cards keep their day-to-day prev/next **and** also get a "Next menu section: Beaches →" link (Beaches is the first top-menu section after Days). Linear browsing through the whole menu now never dead-ends.

**The rule.** Any "page-like" view in the microsite should offer a forward step, not just a way back.

---

## 21. Embedding a shared component in compact mode

**Pattern.** The Estate "Where you are" block needed the same interactive map that lives at `#map`. Rather than duplicate Mapbox markup, `CuracaoMap` got a `compact` prop: when true it renders **only** the map canvas (no heading, no day-filter chips, no legend) wrapped in `.ms-map-embed`. The full `<CuracaoMap days={days} />` and the embedded `<CuracaoMap days={days} compact />` share the exact same marker/popup code via an extracted `canvas` constant.

**The rule.** When a section needs a slice of an existing component, add a `compact`/`variant` prop and extract the shared inner JSX into a constant — don't fork the component.

---

## 22. The full PR cadence that worked

Every change this session followed the same loop, and it kept prod safe:
1. `git fetch origin main`
2. `git stash push -m <topic> -- apps/web/src` (if mid-edit on another branch)
3. `git checkout -b marketing/<topic> origin/main` → `git stash pop`
4. Edit → `npm run typecheck` from `apps/web` (exit 0; NOT `npx tsc`) → verify (running preview mobile+desktop, or curl the served HTML — see #27)
5. `git add` the specific files → commit with a `feat|fix(marketing/king-dushi-week-42): …` message + `Co-Authored-By` trailer
6. `git push -u origin marketing/<topic>` → `gh pr create`
7. On "ship it": `gh pr merge <n> --squash --delete-branch --admin` → confirm `state: MERGED` → delete remote ref (422 = already gone)
8. Only claim "live" after the **Vercel Production deploy** for that commit shows `success` (see #5).

One PR per logical change. The user reviews each Vercel preview and says "ship it" before merge — never merge unprompted.

---

## 23. `.microsite a { color: inherit }` clobbers single-class link colors

**What happened.** The offer-banner "Reserve this week →" CTA rendered navy-on-navy — invisible. A user flagged it ("can't read it, same color as the background").

**Why.** `globals.css` has `.microsite a { color: inherit; }` — specificity **(0,1,1)**. The CTA's own rule was `.ms-offer-banner-cta { … color: var(--ms-gold) }` — specificity **(0,1,0)**. (0,1,1) beats (0,1,0), so the link ignored its gold color and inherited the banner's navy. (The main `.ms-iwant-submit` RESERVE button survived only by luck: gold background + inherited dark text happened to be readable.)

**The fix.** Scope the button's color rule under `.microsite` so it wins: `.microsite .ms-offer-banner-cta { … }` (0,2,0).

**The rule.** Any `<a>`-based button inside the microsite that sets its own text color must be scoped under `.microsite` (or use a non-`<a>` element). A bare `.ms-*` class (0,1,0) will lose to `.microsite a` (0,1,1) and inherit instead. When adding a colored link-button, check it against this rule or it'll render the wrong color.

---

## 24. `referralCreditUsd: 0` prints "$0" — keep it at 500

**What happened.** The two-coconut skill said "two-coconut = no credit, set `referralCreditUsd: 0`." But `ShareSection` renders on **every** home view (prospect AND guest) and prints *"When they book, **$\<credit\>** lands in your account and **$\<credit\>** lands in theirs"* using `content.offer?.referralCreditUsd ?? 500`. Because `0` is not nullish, the `?? 500` fallback doesn't fire — the page literally shows **"$0 lands in your account."** (wyand.ts shipped with `0` — a latent broken-copy bug.)

**The rule.** Keep `referralCreditUsd: 500` on every microsite. The referral credit is a standing share-the-week feature, unrelated to the "no $35 meal credit" two-coconut promise. The only valid reasons to change it are a real different referral amount — never 0.

---

## 25. The reserve section (`IWantThisWeek`) — current shape + copy conventions

**Added 2026-05-22 (Adams Trio), updated through #323.** The reserve card, top to bottom:
1. Heading **"Book {Cartel}'s week."** (the primary CTA verb is **Book**, not Reserve)
2. **Prominent per-person-per-night price** (`.ms-iwant-price`, ~24px serif) + an all-inclusive sub-line
3. **"What's included" list** from the optional **`offer.includes: string[]`** content field (`.ms-iwant-includes`, gold ✓ bullets)
4. The **"BOOK THIS WEEK →"** button (`href={offer.bookingUrl}`)
5. Fineprint: **a confirmation email lands the moment payment clears** + the hold deadline
6. A "Questions first?" card → **"WhatsApp the Tommy Coconut family now"** (the secondary path)
7. The full **Tommy Coconut Promise** as a navy full-width block (`.ms-iwant-promise`, gold accents, 🥥 bullets) below the cards

**Copy conventions (the user is specific about these):**
- **Primary CTA = "Book"** (heading, card title, button). The lede keeps the softer verb **"Tap reserve …"** — yes, "Book" and "reserve" coexist on purpose; don't "fix" it to match.
- **Never name "Britt" in the reserve card.** It's **"the Tommy Coconut family"** — the "knows your week" line, the WhatsApp button, and the toast all say "the Tommy Coconut family", not Britt.
- `priceLabel` **leads with the per-person-per-night figure**, e.g. `"$860 per person, per night · $18,060 all-in (3 guests · 7 nights)"`.
- `offer.includes` is per-family (lives in content; absent → generic trust bullets show).

**Everything except `offer.includes` is hardcoded in the shared `IWantThisWeek`** → edits hit **every** prospect page (intended — the Book language, the email note, the Promise block are all universal). The Promise here is in addition to the Good-to-Know Promise; both can coexist on one page (the user confirmed they want both).

---

## 26. The pay-page "Nights" count is the Pipeline / portal — NOT the web microsite

**What happened.** The portal pay page showed "8 nights" for a 7-night Dushi Week. The user thought it was a microsite bug.

**Why / scope.** The `/payments/pay` page lives in **`apps/portal`** and reads `Nights` from the **Pipeline record's dates** (Airtable). Nothing in `apps/web` (the microsite, `offer.priceLabel`, `paymentAmountUsd`) affects it. An 8-vs-7 mismatch is either (a) the Pipeline's departure date being a day late / the complimentary bonus night baked into the contracted dates (per the bonus-night model, Pipeline dates should be the real 7 nights), or (b) the portal counting the bonus night in its display.

**The rule.** Anything on the portal pay page (nights, installments, the "$X/mo" math, the gateway) is a **Pipeline-data fix (Britt, Airtable)** or a **portal-code fix (TCam)** — out of scope for the marketing-site task. Diagnose and hand off; don't try to fix it from `apps/web`.

---

## 27. Worktree + verification reality (the stuff that wastes cycles)

- **You're in a separate worktree checkout** (`apps/web/.claude/worktrees/<name>/`). Create/edit files **inside the worktree path**, not the main tree at `/Users/.../tommy-os/apps/web/…` — absolute paths to the main tree write to the wrong checkout (and the worktree's working tree stays empty). If you catch this, `cp` the files into the worktree and clean up the main tree.
- **Fresh worktrees have no `node_modules`.** Run `npm install` at the **worktree root** once before typechecking or previewing (it can take a few minutes).
- **Typecheck = `npm run typecheck` from `apps/web`** (runs `tsc --noEmit`). `npx tsc` does NOT work — it tries to self-install and bails.
- **The home `/` route 500s without `AIRTABLE_MARKETING_BASE_ID`** (it doesn't wrap that fetch). The microsite route DOES (`safe()` wrappers) → **navigate straight to `/<Slug>DushiWeek<N>`**, never `/`. `/api/web-session/*` 500s and the `dushiweek/80` fallback image 404s in dev too — all env/template artifacts, not regressions.
- **The preview browser is flaky** — it pins to the launch.json server's registered port and intermittently resets to `/`. For reliable verification, prefer **`curl` of the dev server's served HTML** (the content config is serialized into the SSR payload, so even Good-to-Know / reserve copy is greppable) + **computed styles via `preview_eval`** over screenshots. Screenshots of below-the-fold content frequently capture the wrong region here.
- **Day hero images are CSS background-images** that only render on the single-day view (not the home/week-glance). Verify a swapped hero by **loading its Cloudinary URL directly** (`…/upload/f_auto,q_auto,w_1600/<publicId>` → 200), not by screenshotting.

---

## 28. Slug number isn't always sequential

King 42 → Bama 43 → Wyand 44 → Friends 45 looked sequential, but the Adams build used **the arrival week-of-year** (Aug 10 2026 = ISO week **33** → `AdamsTrioDushiWeek33`). The number is symbolic/owner's-choice — **confirm with the user** rather than assuming "next integer." It can be a birthday, the arrival week, or just the counter.

---

## 29. The section pager order MUST equal the menu order (and it's prev/next, not back-home)

**What happened (#321).** On the **Letter** section the bottom pager showed *"Back to the week / Next: Beaches"* and on **Estate** it showed *"Next: Map"* — neither matched the order the user navigates by. The user expected Letter → `← Estate / Map →` and Estate → `← Memories / Letter →`.

**Why.** Two bugs in `MicrositeShell`:
1. `SECTION_VIEWS` had `philosophy` (Letter) **first**, but Letter lives in the **BottomMenu**, visually after the TopMenu sections. The pager's `idx`/`next` used that wrong order.
2. The pager's left button was always **"← Back to the week"** (home), not the previous section.

**The fix.** `SECTION_VIEWS` order must be **the combined nav order**: TopMenu trip sections first (`beaches, icar, restaurants, memories, estate`), then BottomMenu brand pages (`philosophy/Letter, map, family, stories, who-is-tommy, good-to-know`). The pager then renders **previous section (left) / next section (right)** off that order, with `onBackHome` only as the fallback at the **first** section's prev and the **last** section's next.

**The rule.** `SECTION_VIEWS` is the single source of truth for **both** hash routing **and** the pager order — and it must mirror the TopMenu (`MENU_ITEMS`) + BottomMenu (`BOTTOM_ITEMS`) sequence. **When you add/reorder a menu item, reorder `SECTION_VIEWS` to match**, or the pager's prev/next will point at the wrong neighbours. (Days are not in `SECTION_VIEWS` — the day pager links forward to the first section, Beaches.)

---

## 30. The video hero needs a GUARANTEED scrim — white text dies without it

**What happened (#326).** A guest reported the hero "broken on mobile": "DUSHI WEEK", the family name, and the countdown were invisible. Root cause: the hero renders `<video class="ms-hero-bg"> <div class="ms-hero-scrim"> <div class="ms-hero-inner">`, but **`.ms-hero-scrim` had no CSS**, and the old video-scrim rule used an adjacent-sibling selector (`video.ms-hero-bg + .ms-hero-inner::before`) that the scrim div itself breaks — so it silently **never matched**. The video hero had **no dark backing**. The white hero text was only legible because the *local-dev* fallback (the trio video) is dark.

**Why it bites on real devices, not in dev.** On the live site the hero uses the **canonical Airtable hero video**, which is bright; and **iOS Low Power Mode disables video autoplay**, freezing the video on its (bright) poster frame. Bright media + white text + no scrim = invisible.

**The fix.** Give the dedicated scrim div the gradient, with explicit stacking — never rely on sibling adjacency:
```css
.ms-hero-scrim {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;   /* video = z auto (0), .ms-hero-inner = z 2 */
  background: linear-gradient(180deg, rgba(0,45,66,0.5) 0%, rgba(0,45,66,0.85) 100%);
}
```

**The rule.** The hero's white text must sit on a scrim that's present regardless of media type (video/div/img), brightness, or play state. Test by *imagining a bright frozen poster*, not the dark dev video — the dev video hides this class of bug.

---

## 31. "Mobile looks broken / unstyled" → diagnose CSS LOAD, not layout

**What happened.** A guest reported the microsite "off on mobile." Two long detours (overflow audits, the hero scrim) before the screenshots showed the truth: the **whole page was rendering with no author CSS** — default serif font, blue underlined link-buttons, disc bullets, a giant unsized WhatsApp `<svg>`, a bare HTML table. That is **not a layout bug**; it's the render-blocking CSS failing to load/apply.

**The triage — first question:** is custom styling *present but mis-arranged* (a real layout/CSS bug) or *absent entirely* (default browser styling)? Absent = CSS didn't load. Don't debug layout.

**Verify the site is serving CSS correctly (it almost always is):**
```bash
page=https://www.tommycoconutprivateresorts.com/<Slug>
curl -s "$page" | grep -oE '/_next/static/css/[^"?]+\.css'        # the stylesheet hrefs
curl -sI "$page/../_next/static/css/<hash>.css" | grep -i content-type   # expect: text/css; 200
curl -s ".../<hash>.css" | grep -c ms-hero                        # rules actually present
```
If the CSS is `200 · text/css` and contains the `ms-*` rules → the build/delivery is fine. The unstyled view is a **client-side load failure** (a dropped render-blocking request — iOS Low Power Mode, weak signal, or a mid-deploy moment).

**The clincher.** Load a *different* microsite (e.g. `/KingDushiWeek42`) on the **same phone**. If it renders styled with the **identical** CSS files (compare: same `<link>` hrefs, same `<head>`, same `data-precedence`), the broken page has no page-specific defect — it just failed to fetch the CSS that visit. The CSS is `cache-control: immutable`, so once any page fetches it, a **hard reload** of the broken page renders it from cache.

**Also rule out (quickly):** the site is Tailwind v4 → requires **Safari 16.4+ / iOS 16.4+** (`@layer`, `color-mix()`, `@property`). An ancient iOS would drop the styles too — but a same-phone sibling page rendering fine disproves the version theory.

**Tooling caveat.** The preview screenshot tool gives misleading artifacts here (it once showed a "cream gutter on the right" that the DOM proved was full-width) and **cannot navigate to external/live URLs** (it stays pinned to localhost). For mobile diagnosis trust `curl` + `getBoundingClientRect`/`getComputedStyle`, not screenshots.

---

## 32. Reusing the worktree branch for sequential PRs after a squash-merge — rebase to keep the diff clean

**Context (Reunion Cartel, 2026-05-25).** In a Claude Code worktree you're pinned to one feature branch (e.g. `claude/<name>`), and `main` is checked out in the *primary* worktree — so you can't `git checkout main` or branch off it locally (the #6 error). Across one session you open **several sequential PRs from the SAME branch**. After each squash-merge, `origin/main` gets a new single commit whose *content* equals your branch's but with a different SHA. If you just commit the next change and open a PR, GitHub's three-dot (merge-base) "Files changed" re-shows **all** prior changes as new (the merge base is still the pre-squash commit) — a huge, confusing diff.

**The fix — rebase your one new commit onto the squashed main:**
```bash
git fetch origin main
git add <files> && git commit -m "…"                       # your new change
git rebase --onto origin/main <branch-tip-before-this-commit>   # drops already-merged commits, replays only the new one
git diff origin/main HEAD --stat                            # TWO-dot: should show ONLY your new change
git push -u origin <branch>                                # remote branch was deleted on the prior merge; this recreates it
gh pr create --base main --head <branch> …
```
`<branch-tip-before-this-commit>` = the commit your branch sat at before this new commit (i.e. the already-merged tip). Verify with the **two-dot** `git diff origin/main HEAD` (NOT three-dot `...`) — that's the true content delta.

**Also:** `gh pr view <n> --json merged` **errors** ("Unknown JSON field: merged"). Use `--json state,mergedAt,mergeCommit`; `state == "MERGED"` confirms the merge even when `--delete-branch`'s local step failed (#6). Clean up the remote ref with `git push origin --delete <branch>` (or the `gh api … -X DELETE` in #6). After merging, the **Production deploy lags the merge by ~1–2 min** — the listed "Production – tommy-web" deploy may briefly still be the *prior* commit, so **poll** until a deploy whose `ref` startswith the new merge commit shows `state: success` before claiming "live."

---

## 33. Verify the offer Pipeline BEFORE wiring it into a live pay button (two-coconut)

**What happened (Reunion Cartel).** Britt handed over the offer Pipeline `rec…` ID to drop into `offer.bookingUrl`/`bookingPipelineId`. Wiring a **live payment link** blind is risky — so read the Pipeline first (Airtable MCP, main base `appFRLV1H76ohiIQS`, Pipeline table `tblb7gP5D3NYND9a0`) and confirm:
- **`Payment_Gateway === "Stripe"`** (field `fldSva0Yxmr3QA7xq`) — EXACTLY the string "Stripe". Anything else → the lead lands on the **ungated CX Pay form** (the gotcha in the two-coconut SKILL).
- **`Status === "Offer Sent"`** (field `fldvNoCtn1157G37W`) — required for the cold-lead Stripe gate.
- **`Total Amount`** set to the offer price (fields `fldCkP5EaAocQfUeU` / `fldPF9OiriBCkRmC4` — both held `24990`). This is what the pay page actually charges; `offer.paymentAmountUsd` in the content config is **display-only**.
- **`Primary Guest`** (field `fldd9fzwjjktigoIg`) links the **real** lead Guest record. If it's blank or a placeholder (name renders as `" "`), the pay-page billing form **won't prefill** name/email/phone — flag it for relink. ⚠️ Watch for **duplicate Guest records** for the same email (the Reunion lead had ≥3); the Pipeline can end up linked to the wrong/blank one.

`list_records` omits empty fields, so query by **field ID** or read the whole record — don't trust a name-keyed fetch that returns "nothing" to mean the field is empty.

---

## 34. The offer hold is ALWAYS 48 hours

TC lead offers carry a **fixed 48-hour** countdown — not "typical," always. Set `offer.expiresAtISO` = the **actual send moment + 48h**, in Curaçao time (AST = UTC−04:00, no DST). It's send-time-relative, so confirm when they're sending before locking it:
```bash
TZ=America/Curacao date -v+48H '+%Y-%m-%dT%H:%M:%S-04:00'   # 48h from now, AST
```
The prospect **"DATES BLOCKED FOR …"** banner reads from `expiresAtISO`. In the outreach email/WhatsApp, state the 48h hold **plainly and calmly** — never "hurry / limited availability." (Mirrors persistent memory `feedback_tc_offer_hold_48h` and the two-coconut SKILL offer block.)

---

## 35. Dushi Weeks registry — field-ID reference ("pages made"; check before, log after)

Base `appFRLV1H76ohiIQS` → **"Dushi Weeks"** `tblGHUrF6PGkqrnn3` (Airtable MCP). This table IS the canonical list of every itinerary + microsite built. **Before:** `search_records` by the guest email to dedupe; take `max(Build #) + 1` for the slug. **After ship:** `create`/`update` the row. Field IDs:

| Field | ID | Notes |
|---|---|---|
| Build # | `fldgT8XqFQj1sqJMb` | number |
| Cartel | `fldxIghKQfJ4IwSd7` | "The Reunion Cartel" |
| Microsite URL | `fldFXPQyAm1Mwjiy2` | live URL |
| Variant | `fldORYKyCywXOyg8i` | "🥥 One Coconut" / "🥥🥥 Two Coconut" |
| Estate | `fldHL6DdMX64gBWNs` | options incl. "Dushi Hideaway", "Palm Breeze", "Bayside Hill", "Happy Hideaway", "Tropical Haven", "Castaway Beach", "Sailaway Beach", "Sunshine Bay" |
| Guest type | `flddU3VYa1kp1g0qN` | "Friends"/"Couple"/"All-Adult"/"Young Adults"/"Young Family"/"Teen Family"/"Multi-Gen"/"Other" |
| Status | `fldorTqskBJLu6f47` | "Lead"/"Offer Sent"/"Booked"/"On Island"/"Departed"/"Alumni" |
| Price (all-in) | `fld27l7OutGB5iqUF` | number |
| Nights | `fldBNnYlsPC8msLJH` | number |
| Arrival / Departure | `fldgbCN2bocNp9csC` / `fldiNX3g8emNAyamI` | ISO date |
| Pipeline ID | `fldgaE8IwWo48trMU` | the offer Pipeline `rec…` |
| Email | `fldmR0EH5pSLGZbKK` | lead email |
| Source itinerary | `fldG9MqTKPOS2uxph` | e.g. `Dushi-Week-<Crew>.md` |
| Notes | `fldFZfJwXl08g15Ik` | placeholders / open items |

Live microsites use Status **"Offer Sent"** even with placeholder/pending pieces (the convention; the Notes field carries the open items). Build numbering isn't strictly sequential (#28). Reunion Cartel = **#53** (row `reczSqI85HBmJY4is`).

---

## 36. Building from a funnel LEAD — where the data lives + the "Failed" auto-build signal

A two-coconut microsite is usually built for a **lead**, not a booked guest. The lead's funnel data lives in the marketing **"Pipeline"** base `appiQO2iMCRjdMe0F` → **Sessions** `tbl7T49CVkrGv5HNe` (one row per quiz step; merge the `Answers` JSON across rows sharing a **Session ID**; the `complete`-step row holds the full combined payload). The **main** base also has an itinerary **auto-build job** table `tblomZtSy0qeghyPE` keyed off those sessions — a row with **Status "Failed"** (tags `research-incomplete` / `anchor-overlap` / `assembly-failed`) means the automated build choked and a **manual build is needed** (that's usually why a lead lands with you). The quiz answers are the gold for the letter + day plan (must-dos, who's coming, budget, "how did you find us") — use **only** what's there, never invent (hallucination rule). A lead has **no fixed dates/flight** → write the page date-agnostic or with a clearly-labelled **example week**, and set `mode: "prospect"`. (Mirrors memory `reference_marketing_leads_pipeline_base`.)
