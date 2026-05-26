# Architecture — Dushi Week Microsite

Deep dive on how the King microsite is wired. Read after SKILL.md when you need to add a major feature (new section type, new view, new offer mechanic).

---

## The three-view state machine

`MicrositeShell.tsx` owns the entire page state. There are only three top-level views, picked by these two pieces of state:

```ts
const [activeView, setActiveViewState] = useState<ActiveView>("home");
const [activeDayId, setActiveDayIdState] = useState<DayId | null>(null);

const isSingleDay = activeDayId !== null;            // takes priority
const isHome     = activeView === "home" && !isSingleDay;
// else: section view (one of philosophy / beaches / icar / restaurants /
//                     memories / estate / map / family / stories /
//                     who-is-tommy / good-to-know)
```

| View | When | Renders |
|---|---|---|
| **Home** | `activeView==="home"` && no day picked | Hero + mode banner + glance table + share + closing |
| **SingleDay** | `activeDayId !== null` | One `<DayCard>` + prev/next/back-to-week pager |
| **Section** | `activeView` is one of SECTION_VIEWS | Section component (e.g. `<SectionFamily>`) + prev/next-section pager (follows SECTION_VIEWS = menu order; home only at the first/last ends) |

The hero is **only on Home**. When the user clicks "Beaches" or a day, they jump straight into that content with no hero scrolled through.

---

## URL hash routing (one-way)

`MicrositeShell` listens for `hashchange` and translates:

- empty / `#home` → `home` view
- `#arrival`, `#day-1` ... `#departure` → SingleDay
- `#beaches`, `#family`, etc. → Section view

Hash updates flow **one-way** (hash → state). When state changes from a button click, we call `history.replaceState` to keep the URL in sync without firing another hashchange.

`window.scrollTo({ top: 0, behavior: "instant" })` on every view change so each view starts from the top.

---

## Server page contract

```ts
// apps/web/src/app/[locale]/<Slug>/page.tsx
export default async function Page({ params }) {
  const { locale } = await params;
  setRequestLocale(locale);

  const [
    beaches, dining, memories, baysideHill, homepage,
    cartel, cartelHeroBg, cartelCtaBg,
    stories, storiesHeroBg,
    tommyHeroBg, tommyCtaBg, tommySuerte, tommyTreasure,
  ] = await Promise.all([
    safe<BeachRow[]>(() => getBeachMarketing(), []),
    safe<DiningRow[]>(() => getDiningMarketing(), []),
    safe<MemoryRow[]>(() => getMemoriesMarketing(), []),
    safe<MergedEstate | null>(() => getMergedEstateBySlug("bayside-hill"), null),
    safe<HomepageContent | null>(() => getHomepageContent(), null),
    safe<CartelMember[]>(() => getCoconutCartel(), []),
    safe<string | null>(() => getCartelHeroBg(), null),
    safe<string | null>(() => getCartelCtaBg(), null),
    safe<GuestStoryRow[]>(() => getGuestStories(), []),
    safe<string | null>(() => getGuestStoriesHeroBg(), null),
    safe<string | null>(() => getTommyHeroBg(), null),
    safe<string | null>(() => getTommyCtaBg(), null),
    safe<string | null>(() => getTommySuerte(), null),
    safe<string | null>(() => getTommyTreasure(), null),
  ]);

  return (
    <MicrositeShell
      content={kingContent}
      canonical={{
        beaches, dining, memories,
        estate: baysideHill, homepage,
        cartel, cartelHeroBg, cartelCtaBg,
        stories, storiesHeroBg,
        tommyHeroBg, tommyCtaBg, tommySuerte, tommyTreasure,
      }}
    />
  );
}
```

`safe<T>` is defined locally inside the page file. It catches Airtable failures and returns the fallback so the page still renders.

---

## CanonicalData type (in MicrositeShell)

When adding a new mirrored section, extend both the type AND `EMPTY_CANONICAL`:

```ts
type CanonicalData = {
  beaches: BeachRow[];
  dining: DiningRow[];
  memories: MemoryRow[];
  estate: MergedEstate | null;
  homepage: HomepageContent | null;
  cartel: CartelMember[];
  cartelHeroBg: string | null;
  cartelCtaBg: string | null;
  stories: GuestStoryRow[];
  storiesHeroBg: string | null;
  tommyHeroBg: string | null;
  tommyCtaBg: string | null;
  tommySuerte: string | null;
  tommyTreasure: string | null;
};

const EMPTY_CANONICAL: CanonicalData = {
  beaches: [], dining: [], memories: [], estate: null, homepage: null,
  cartel: [], cartelHeroBg: null, cartelCtaBg: null,
  stories: [], storiesHeroBg: null,
  tommyHeroBg: null, tommyCtaBg: null, tommySuerte: null, tommyTreasure: null,
};
```

Keep them in lockstep — if the type has a key, `EMPTY_CANONICAL` must too.

---

## Adding a new menu section — checklist

1. **`TopMenu.tsx`** — extend the `ActiveView` union with the new id.
2. **`MicrositeShell.tsx`** — add the id to `SECTION_VIEWS` so hash routing recognizes it. **Insert it at the position that matches its menu placement** — `SECTION_VIEWS` is also the section-pager order, so it must mirror the TopMenu→BottomMenu sequence (TopMenu trip sections first, then BottomMenu brand pages). Wrong position = wrong prev/next pager links (see lessons #29).
3. **`MicrositeShell.tsx`** — add a `case "<id>":` to `SectionView`'s switch, returning the section's JSX.
4. **`TopMenu.tsx` or `BottomMenu.tsx`** — add a `{ id, label }` to the appropriate menu items array. Top bar is for trip pages, bottom bar is for brand-story pages. Keep `SECTION_VIEWS` (step 2) in the same relative order.
5. If mirroring a live brand page, follow the mirror pattern in SKILL.md "Common one-off edits → Mirror a live brand page".

---

## DushiMicrositeContent shape (the per-family config)

The full shape lives in `types.ts`. Key fields a new family microsite must set:

```ts
{
  slug: "<PascalCaseSlug>",
  mode: "guest" | "prospect",          // guest = booked, no urgency; prospect = with offer countdown
  family: { cartelName, members, primaryGuest, bookerGuest },
  trip: {
    estate: "Bayside Hill",            // basecamp name
    arrivalDate, departureDate,         // ISO yyyy-mm-dd
    arrivalDateTimeISO,                 // for the countdown
    arrivalFlight: { code, arrivalLocalTime },
    departureFlight?: { code, departureLocalTime },
    timezone: "America/Curacao",
    dateRangeLabel,                     // human-readable
  },
  offer?: { ... },                      // required when mode === "prospect"
  hero: {
    cloudinaryVideoId?: string,         // pinned video, overrides homepage fallback
    cloudinaryFallbackImageId: string,  // poster + image fallback
    tagline, eyebrow,
  },
  music: { spotifyType, spotifyId, label, pinnedTrackId? },
  whatsapp: { groupInviteUrl, fallbackTcPhone? },
  beaches: BeachClub[],                 // static fallback (Airtable supersedes)
  experiences: Experience[],            // static fallback
  iCar: { tagline, paragraphs },
  estate: { name, tagline, paragraphs, amenities },  // static fallback
  philosophy: { heading, paragraphs },
  letter: { eyebrow, salutation, paragraphs, signOff },
  weekGlance: [{ dayId, day, date, highlight, dinner, vibe }, ...],
  days: DayCard[],                      // 8 entries: arrival + 6 + departure
  goodToKnow: [{ heading, body }],
  crew: CrewMember[],                   // static fallback (Airtable supersedes)
  closing: { heading, paragraphs, signOff },
}
```

For prospect mode (un-booked leads), `offer` is required:
```ts
offer: {
  expiresAtISO: string,
  priceLabel: "$24,000 · 7 nights · 7 guests",
  shareTokenSlug: "king-andy",
  referralCreditUsd: 500,
  whatsappMessage: "Hi team — the King family wants to book...",
}
```

---

## Component naming conventions

- `Section<X>.tsx` — full-page section rendered when its `ActiveView` is active
- `HeroCountdown.tsx`, `OfferCountdown.tsx` — sticky banners under the hero
- `*Pill` — chrome that floats over content (e.g. `MusicPlayerPill`)
- `HorizontalScroller.tsx` — generic wrapper that adds `‹` / `›` scroll chevrons to any overflow-x strip (used by TopMenu + BottomMenu)

CSS is `.ms-<component>-<part>` — flat, no nesting beyond modifiers. All in `globals.css`.

> **Nav is unified, not forked.** There is no longer a `MobileTabBar` or floating `WhatsAppFAB` — both were deleted. The single `BottomMenu` renders on every viewport (Letter · Map · Family · Stories · Who's Tommy? · Good to Know + ♪ Music + WhatsApp), scrolling horizontally with chevrons on narrow screens. The Music button and WhatsApp button live *inside* BottomMenu, not as floating circles.

---

## Navigation model (current)

- **Top bar** (`TopMenu.tsx`): Home · Days(dropdown) · Beaches · iCar · Restaurants · Memories · Estate + Share CTA. Home and the Days dropdown render OUTSIDE `.ms-topmenu-left` (the overflow-x scroll container) so the dropdown panel isn't clipped on mobile — see lessons #15. The section links sit inside `.ms-topmenu-left`, wrapped by `HorizontalScroller`.
- **Bottom bar** (`BottomMenu.tsx`): Letter · Map · Family · Stories · Who's Tommy? · Good to Know + ♪ Music + WhatsApp. Brand-story pages + the two action buttons. Also wrapped by `HorizontalScroller`.
- **Forward navigation**: section views end with `‹ Back to the week` + `Next: <next section> →`; day cards keep day-to-day prev/next AND add `Next menu section: Beaches →`. No view dead-ends. See lessons #20.

---

## State that lives outside React

| State | Where | How to interact |
|---|---|---|
| URL hash | `window.location.hash` | Set via `history.replaceState`; listen via `hashchange` |
| Music open/closed | `MusicPlayerPill` internal `useState` | Toggle via `window.dispatchEvent(new CustomEvent("ms-music-toggle"))` |
| Referral attribution | `localStorage["tcpr_ref"]` | Captured on mount from `?ref=` query param |
| Toast | `MicrositeShell` `useState` | Pass `showToast` callback down |

For everything else, lift state up to `MicrositeShell` and pass callbacks down.

---

## What you can safely change without touching MicrositeShell

- Section copy and visual layout — edit the section component file directly
- Day photos and copy — edit `content/<family>.ts`
- Hero video/photo — edit `content/<family>.ts`
- Bottom-menu labels — edit `BottomMenu.tsx`'s `BOTTOM_ITEMS`
- Style tokens — edit `globals.css` under `.ms-*`

## What requires touching MicrositeShell

- New `ActiveView` value
- New canonical data field
- New chrome (floating element, banner)
- View routing changes
- Page-level state

When you touch MicrositeShell, **also** check that the type extension propagates into the server page's `Promise.all` and into `EMPTY_CANONICAL`.
