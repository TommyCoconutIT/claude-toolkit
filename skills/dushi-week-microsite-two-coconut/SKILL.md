---
name: dushi-week-microsite-two-coconut
description: "Build the TWO COCONUT 🥥🥥 (Double Dushi) version of a Dushi Week microsite from an itinerary — the lead-conversion variant. Unlike the one-coconut 🥥 microsite (already-booked guests, Share button), the two-coconut page is sent to LEADS to convert them: it carries the richer all-inclusive offer (every lunch + every breakfast + open bar, no $35 credit), and its primary CTA is an OFFER / BOOK button that opens a payment page instead of a Share button. Use whenever the user says 'two coconut', '🥥🥥', 'Double Dushi', 'the booking version', 'the offer version', 'the version we send to leads', 'make the offer page', 'add the payment / book button to the itinerary', or hands you an itinerary for an UN-booked prospect they want to convert. Do NOT use for: the one-coconut already-booked guest page (use dushi-week-microsite-from-itinerary), producing the printable itinerary document (dushi-week-builder), or generic edits to an existing microsite (dushi-week-microsite). Read the one-coconut skill first — this skill is the delta on top of it."
---

# Dushi Week Microsite — TWO COCONUT 🥥🥥 (Double Dushi / Offer + Booking)

> **Read `dushi-week-microsite-from-itinerary` (the one-coconut 🥥 skill) first.** Everything there applies: the typed content config, the route shell, the `MicrositeShell` view machine, the verify-then-ship cadence, the voice rules, the WhatsApp lessons. **This skill is only the delta** — what makes the two-coconut version different.

---

## One coconut 🥥 vs Two coconut 🥥🥥 — the whole difference

| | 🥥 One Coconut | 🥥🥥 Two Coconut (this skill) |
|---|---|---|
| **Audience** | Already-**booked** guest | **Lead** we're converting |
| **`content.mode`** | `"guest"` | `"prospect"` (requires the `offer` block) |
| **Primary CTA** | **Share my week** | **OFFER / Book this week** → payment page |
| **Meals** | 5 dinners + 2 BBQs | 5 dinners + 2 BBQs **+ every lunch + every breakfast + open bar** |
| **Breakfast** | — | Choice of **Coffee Bike** *or* **Brisa do Mar** (both around the corner from every estate) |
| **Lunch** | — | **Every day**, based on where the itinerary has them that day |
| **Open bar** | — | **Yes**, at the estate |
| **$35 credit** | mentioned | **Never mentioned** — they just sign the receipt |
| **Beaches / Restaurants / Memories / iCar** | same | **same** (identical content, canonical Airtable) |
| **Family / Stories / Who's Tommy** | same | **same** |
| **Estate + Map** | the booked estate | the **chosen** estate (pulled by slug — see below) |

Everything not in this table is identical to the one-coconut build. Don't re-derive it; copy it.

---

## Meal inclusions — the two-coconut additions

The itinerary's day schedules and the "what's included in the week" copy must reflect the all-inclusive upgrade. When transcribing into `content/<family>.ts`:

- **Every dinner** (5) + **two BBQs** — same as one-coconut.
- **Every lunch** — add a lunch block to each day's `schedule`, sited by where the itinerary puts them that day (beach club, boat, west-coast stop, estate). Pull the venue from the day's plan; don't invent one.
- **Every breakfast** — each day notes the breakfast choice: **Coffee Bike** *or* **Brisa do Mar**, "both right around the corner from the estate." This is a standing line, same every day.
- **Open bar at the estate** — include in the estate's "in the week" inclusions and wherever the one-coconut version mentioned the bar.
- **No $35 credit** — search the transcribed content for any "$35", "credit", "sign for", "house account" language and **remove it**. Two-coconut guests "just sign the receipt" — no credit mechanic, don't mention one.

The `goodToKnow` / estate "in the week" lists are where these inclusions live. Keep the Tommy voice — these are gifts, not line items.

---

## Estate + Map — pull by slug

The estate section already renders from canonical Airtable via `getMergedEstateBySlug("<slug>")` in the server page — so picking the right estate is just passing the right slug. The map pins follow the estate. Confirm the estate from the itinerary, then use its slug:

| Estate | Slug (`getMergedEstateBySlug` arg + `/estates/<slug>`) |
|---|---|
| Happy Hideaway | `happy-hideaway` |
| Dushi Hideaway | `dushi-hideaway` |
| Bayside Hill | `bayside-hill` |
| Palm Breeze | `palm-breeze` |
| Castaway Beach | `castaway-beach` |
| Sailaway Beach | `sailaway-beach` |
| Sunshine Bay | `sunshine-bay` |

In the server page (`apps/web/src/app/[locale]/<Slug>/page.tsx`), change the one hard-coded estate fetch:
```ts
safe<MergedEstate | null>(() => getMergedEstateBySlug("<chosen-slug>"), null),
```
The Estate section then mirrors exactly how that estate is listed at `tommycoconutprivateresorts.com/estates/<slug>` — story blocks, skim box, amenities, reviews, the lot. The map view re-centers to the chosen estate (set the estate pin + day pins in `content/<family>.ts` to that estate's coordinates).

The static fallback (`content.estate`) should still describe the chosen estate for local dev, but production uses the canonical Airtable data.

---

## The booking model — OFFER button replaces Share

The one-coconut page ends every flow at "Share my week." The two-coconut page is a **conversion** tool, so the CTA changes to **OFFER / Book this week** and routes to a payment page.

### 1. Set prospect mode + offer block

> **⚠️ This doc drifted from the code. Current `Offer` shape (verified 2026-05-22 on the Adams Trio build):** the field is **not** `pipelineId`. The type already carries `bookingUrl`, `bookingPipelineId`, `paymentAmountUsd`, and an optional `includes: string[]`. Use those — you do **not** need to add anything to `types.ts`.

In `content/<family>.ts`:
```ts
mode: "prospect",
offer: {
  expiresAtISO: "2026-05-24T18:00:00-04:00",         // ALWAYS send-moment + 48h (fixed TC convention — see microsite lessons #34). TZ=America/Curacao date -v+48H
  priceLabel: "$860 per person, per night · $18,060 all-in (3 guests · 7 nights)", // LEAD with per-person/night
  includes: [                                        // NEW (optional): bulleted "what's included" at the reserve point
    "Every dinner (7) — Villa Vis, Pasawá, …",
    "Every lunch and every breakfast (Coffee Bike or Brisa do Mar)",
    "Open bar at the estate, all week",
    // …the experiences, the iCar + transfers, the estate
  ],
  shareTokenSlug: "<family>-<primary>",              // attribution token
  referralCreditUsd: 500,                            // ⚠️ KEEP 500 — see the ShareSection trap below (0 prints "$0")
  whatsappMessage: "…",                              // fallback "questions?" path, not the primary CTA
  bookingUrl: "https://portal.tommycoconutprivateresorts.com/payments/pay?t=recXXXX", // ← the OFFER button href
  bookingPipelineId: "recXXXX",                      // reference metadata (the Pipeline the charge posts against)
  paymentAmountUsd: 18060,                           // reference metadata only — pay page charges Pipeline.Total Amount
},
```

> **The actual charge amount does NOT live in the content config.** It lives on **`Pipeline.Total Amount`** in Airtable (a single per-itinerary number Britt sets when she creates the Pipeline). `priceLabel` + `paymentAmountUsd` here are display/informational only — keep them in sync with `Total Amount` by hand. **The OFFER button reads `offer.bookingUrl`** (already wired in `IWantThisWeek`); `bookingPipelineId` + `paymentAmountUsd` are reference metadata.

> **⚠️ `referralCreditUsd` — the ShareSection trap.** `ShareSection` renders on **every** home view (prospect AND guest) and prints *"When they book, **\$\<referralCreditUsd\>** lands in your account…"* via `?? 500`. Setting `0` literally prints **"\$0"** (broken copy). The referral credit is a standing microsite feature, not a per-itinerary thing — **keep it at 500**. (The old "two-coconut = NO credit, set 0" line was wrong; "no credit" only ever meant the $35 meal / Culinary-Pass credit, never the referral credit.)

`mode: "prospect"` already flips `MicrositeShell` into the close-of-sale layer (offer countdown banner, the I-WANT section, mobile sticky CTA, exit-intent modal). The two-coconut work is repointing those CTAs from WhatsApp/Share to the OFFER/booking page.

### 2. The CTAs are ALREADY wired — a new build needs NO component edits

> **✅ Done in the shipped codebase (Friends #45 onward). Do NOT re-wire.** For a new two-coconut build you touch only **`content/<family>.ts` + the route + the estate slug** — never the components.

How it actually works (verified 2026-05-22): every conversion CTA funnels to the **`#i-want`** section, and **`IWantThisWeek` holds the single outbound link to `offer.bookingUrl`** (the portal pay page). The rest are anchors:
- `IWantThisWeek` "BOOK THIS WEEK" → `href={offer.bookingUrl}` — the only real outbound link
- `OfferCountdown` CTA → `#i-want`
- `MobileStickyCTA` → `#i-want`
- `ExitIntentModal` "Lock my week" → `#i-want`
- `TopMenu` BOOK button (shown when prospect via `showIWantCta`) → `#i-want`

So `mode: "prospect"` + a valid `offer.bookingUrl` IS the entire wiring. Keep the **WhatsApp-to-Tommy** option ("Questions first?") as the secondary fallback — its button reads **"WhatsApp the Tommy Coconut family now"** and opens Tommy's number with the message pre-filled (see lessons-learned #14 + #25, updated). The reserve section also uses **"Book"** for the primary CTA and carries the full Tommy Coconut Promise block — see lessons-learned #25.

### 3. The OFFER / booking page = the portal's public payment page

**Do not build a card form inside `apps/web`.** Card capture is PCI-sensitive and already solved, tested, and compliant in `apps/portal`. The OFFER button links **out** to the portal's existing public payment route:

```
${PORTAL_BASE_URL}/payments/pay?t=<pipelineId>
```

See "Payment infrastructure" below for the full contract — the cold-lead gap is **resolved** (Option A, owned by TCam).

---

## Payment infrastructure (researched from `apps/portal` — read-only)

> **Scope rule (CLAUDE.md):** payment processing lives in `apps/portal`. The `apps/web` microsite must **not** replicate Collect.js or Stripe Elements. Link out to the portal page. Any change *inside* `apps/portal` is cross-app work that needs the user's explicit go-ahead.

### The public pay page (the reuse target)
- **Route:** `apps/portal/src/app/payments/pay/page.tsx` → `/payments/pay?t=<pipelineId>`
- **Server fetch:** `fetchPayPageData(token)` (`features/payments/lib/fetch-pay-page-data.ts`) returns `{ guestName, propertyName, payments[], suggestedAmount, gateway: "cxpay"|"stripe", + billing defaults }`. Validates the Pipeline exists.
- **Client form:** `pay-form-client.tsx` (`PayFormClient`) — an editable **amount** input (prefilled with `suggestedAmount`) + a modal that renders **one of two gateways**:

**Stripe path (public, no login):**
1. `createPublicStripeIntent({ pipelineId, amount })` → `clientSecret` (`features/payments/actions/create-public-stripe-intent.ts`)
2. `<StripePaymentForm clientSecret … onSuccess={pid => …}>` — Stripe Elements, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
3. `recordPublicStripeCharge({ pipelineId, paymentIntentId, amount })` records it.

**CX Pay path (public, no login):**
1. `<CollectJsForm amount … onPayment={…}>` tokenizes the card client-side (NMI Collect.js, PCI-safe)
2. `processOneOffCharge({ pipelineId, paymentToken, amount, billing, threeDsData })` (`features/payments/actions/process-one-off-charge.ts`) charges via CX Pay + records it.

**Gateway choice** is per-booking via `Pipeline.Payment_Gateway` ("cxpay" | "stripe"). New flows generally use Stripe.

### The amount-per-itinerary lever — `Pipeline.Total Amount`
The charge amount is a **single per-itinerary number on `Pipeline.Total Amount`** (Airtable), set by Britt when she creates the offer Pipeline. TCam's `fetch-pay-page-data.ts` change makes the pay page's amount input **fall back to `Total Amount`** when the Pipeline has no scheduled installments yet (the cold-lead case). The input stays editable so a lead can pay a negotiated half-down. The web content config does **not** carry the charge amount — it carries `offer.bookingUrl` (the pay-page URL) + `offer.bookingPipelineId`; `paymentAmountUsd` is informational only.

### The cold-lead gap — RESOLVED (Option A, Stripe, TCam owns it)
The public Stripe intent gated on `status === "Booked"`; a fresh lead's Pipeline is `"Offer Sent"`. **Decision locked: Option A + Stripe.** Why Stripe over CX Pay: the Stripe public path already status-gates (we just widen it), Stripe Elements does 3DS automatically, and `/api/webhooks/stripe` already syncs PaymentIntents → Payment records. The CX Pay one-off path (`process-one-off-charge.ts`) has **no status gate at all** — extending it for cold leads would let any holder of any Pipeline ID charge a card against it. So Stripe only.

**TCam's portal PR (3 files, ~30 lines):**
1. `create-public-stripe-intent.ts` — accept both `"Booked"` and `"Offer Sent"` as eligible statuses.
2. `record-public-stripe-charge.ts` — on success: flip `Pipeline.Status` `"Offer Sent"` → `"Booked"`; fire PostHog `offer_converted` `{ pipelineId, amount }`; prepend `"💳 OFFER → Booked"` to the existing Slack alert.
3. `fetch-pay-page-data.ts` — `suggestedAmount` falls back to `Total Amount` when there are no scheduled installments.

On success it does **not** auto-send the confirmation email or WhatsApp group invite — Britt does those manually for now (a small follow-up PR may automate the email after the first 1–2 conversions land in prod).

### ⚠️ The `Payment_Gateway` gotcha
The pay page reads `Pipeline.Payment_Gateway` and **defaults to CX Pay unless the field is exactly the string `"Stripe"`** (`rawGateway === "Stripe" ? "stripe" : "cxpay"`). Every offer Pipeline MUST have `Payment_Gateway = "Stripe"` set explicitly, or the lead lands on the CX Pay form (which has no status gate). This is part of Britt's Pipeline checklist below.

### Britt's offer-Pipeline checklist (Airtable, at offer-send time — manual for now)
Creating the offer Pipeline is **manual** (auto-creation deferred until the flow is proven). Britt sets:
- `Status` = `"Offer Sent"`
- `Total Amount` = `<numeric offer price>` (e.g. `24500`)
- `Payment_Gateway` = `"Stripe"` ← do not forget (see gotcha above)
- `Primary Guest` linked to the lead's Guest record (so the billing form prefills name/email/phone/address)
- `Email` + `Phone` filled

Then she copies the `rec…` ID to you → you put it in `offer.bookingUrl` (`https://portal…/payments/pay?t=<rec…>`) and `offer.bookingPipelineId`.

### Division of labor — TCam owns the portal PR
- **In `apps/web` (ours):** ✅ the offer/CTA plumbing is **already shipped** (Friends #45 onward). The `Offer` type already has `bookingUrl`/`bookingPipelineId`/`paymentAmountUsd`/`includes`, and `IWantThisWeek` already links to `offer.bookingUrl` with the other CTAs anchoring to `#i-want`. So a new build's web work is just **content + route + estate slug** — no `types.ts` edit, no CTA wiring. Set `offer.bookingUrl` to the full `https://portal…/payments/pay?t=<rec…>` URL (the portal base default is `https://portal.tommycoconutprivateresorts.com`).
- **In `apps/portal` (TCam's lane):** the 3-file change above. **He delivers it as its own portal PR, which we pull / integrate later** once merged + deployed. Do NOT edit `apps/portal` from the web side.
- **Integration point:** the web side can ship its CTAs immediately (the route exists). The **end-to-end booking flow only works once TCam's portal PR is deployed** (until then, an "Offer Sent" Pipeline gets rejected by the un-widened status gate). Test together after his deploy.

---

## Recipe (delta over the one-coconut recipe)

0. **Registry first.** Check the **Dushi Weeks** table (base `appFRLV1H76ohiIQS` / `tblGHUrF6PGkqrnn3`, via the Airtable MCP): dedupe by the lead's email, grab the nearest two-coconut template by estate, and take `max(Build #) + 1` for the slug. After you ship, log/update the row (Microsite URL, Variant 🥥🥥, Pipeline ID, Status — Offer Sent → Booked when it converts). Full protocol: `dushi-week-builder` SKILL → "STEP 0.5".
1. Run the **one-coconut recipe** as the base (copy `king.ts` — or, faster, the most recent two-coconut at the same estate — fill family/trip/days, create the route).
2. **Flip to prospect:** `mode: "prospect"` + the `offer` block — `expiresAtISO` (real deadline), `priceLabel` (lead with per-person/night), `includes` (the what's-included list), `shareTokenSlug`, `referralCreditUsd: 500`, `whatsappMessage`, **`bookingUrl`** + `bookingPipelineId` + `paymentAmountUsd`. **No `types.ts` edit** — the fields already exist (see §1). The charge amount is `Pipeline.Total Amount` (Britt sets it); `paymentAmountUsd` is informational.
3. **Meal upgrades — often already done.** A two-coconut itinerary is usually *generated* all-inclusive (every lunch + breakfast, open bar, "no receipts to sign", 🥥🥥). If so, just transcribe faithfully. Only add upgrades / strip "$35 credit" language if the source itinerary is a one-coconut draft.
4. **Set the estate slug** in the server page's `getMergedEstateBySlug("<slug>")` and point the map pins at that estate.
5. **CTAs need no work** — already wired (see §2). `mode: "prospect"` + a valid `offer.bookingUrl` is the whole thing.
6. **Coordinate the dependency:** Britt creates the offer Pipeline (`Status="Offer Sent"`, `Total Amount`, `Payment_Gateway="Stripe"`, Primary Guest link, Email+Phone) and hands you the `rec…` ID → put it in `offer.bookingUrl` + `bookingPipelineId`. **TCam's portal PR** (Stripe-gate-widen, Option A) must be deployed before booking works end-to-end — the web page ships first, but an "Offer Sent" Pipeline is rejected at the pay page until his gate-widen lands. (The page + price + WhatsApp all work regardless; only the card charge is gated.)
7. **Verify + ship** per the one-coconut cadence (`npm run typecheck` from `apps/web` — NOT `npx tsc`; local preview or curl-the-served-HTML; PR; wait for green Vercel **prod** deploy before saying "live").

---

## After you ship — the page is step one of a conversion flow

Shipping the two-coconut page isn't the end of the job — it's the asset you send a lead. The natural next two asks (the user reaches for both):

1. **The outreach that delivers the link.** Write the **email + WhatsApp** that sends the lead their page — **invoke the `tommy-coconut-voice` skill** and write it as **Stage 2 (Consideration / advisor register)**: warm, proof-loaded.
   - **Lead angle = EASE (locked by the user).** Position TC as the **easiest, most seamless, frictionless vacation they'll ever have**. The villain is the *work / mental load of planning and running the trip themselves* (the 47 reservations, the "did we book the boat day?" texts at midnight). Hooks that landed: *"you plan nothing," "we already built the week," "the only job left is showing up," "you walk in, Boy hands you a rum, and the week just runs."* **Do NOT frame it as "the tourist island vs the real island" / us-vs-the-tourist-version** — even for a returning-island guest, the user explicitly rejected that angle.
   - **Pull proof from the real guest stories**, don't invent it: the live `/guest-stories` page or the canonical Airtable guest-stories data. Well-traveled guests sell the ease for you — *"the most impressive experience I've ever had" (Aubrey), "everything super arranged" (Amber), "the best vacation of my life" (Yara).* Quote 2–3 verbatim with first-name attribution. (Plus the headline receipts if you want: 700+ stays, 4.99.)
   - Reference **The Tommy Coconut Promise** (day-four money-back), state the **all-in price** plainly ($X pppn / $X all-in), and frame the **hold deadline calmly** — honest, never "book now / hurry / limited availability." Reserve "family" for the TC crew — the lead is "the three of you" / their cartel name. Channel sign-offs: email & WhatsApp → *"Vacation is holy. Just say when. T🥥"*. (See the persistent memory `feedback_tc_lead_outreach_positioning`.)

2. **A follow-up reminder anchored on `offer.expiresAtISO`.** The hold-release datetime is the obvious trigger for a nudge. Offer to schedule a one-time reminder (via the `/schedule` skill / `RemoteTrigger`) to fire a few hours **before** the hold releases, drafting a short follow-up nudge (WhatsApp + email) pointing back at the page. Convert the hold time (Curaçao = UTC−04:00) to UTC for the schedule.

> These are separate skills (`tommy-coconut-voice`, `/schedule`) — don't reinvent their rules here; hand off to them. This note just flags that the microsite build usually leads straight into them.

---

## Same as one coconut — do not re-derive

Beaches, Restaurants, Memories, iCar, Family, Stories, Who's Tommy: **identical**. Same components, same canonical Airtable, same copy. The microsite codebase (`features/dushi-microsite/components/`, `globals.css`, helpers, nav) is unchanged. Per-family work is still just `content/<family>.ts` + the route shell + (for two-coconut) the estate slug and the offer/payment wiring.

For every gotcha — Cloudinary env fallback, iOS hero autoplay, squash-merge prop drops, overflow-clipped dropdowns, centering, WhatsApp param inconsistency, the PR cadence — read `~/.claude/skills/dushi-week-microsite/references/lessons-learned.md`. They all apply here too.

---

## Quick reference

| Artifact | Path |
|---|---|
| One-coconut skill (read first) | `~/.claude/skills/dushi-week-microsite-from-itinerary/SKILL.md` |
| Architecture + lessons | `~/.claude/skills/dushi-week-microsite/references/` |
| Microsite content config (template) | `apps/web/src/features/dushi-microsite/content/king.ts` |
| Microsite route (template) | `apps/web/src/app/[locale]/KingDushiWeek42/page.tsx` |
| **Public pay page (reuse target)** | `apps/portal/src/app/payments/pay/page.tsx` + `pay-form-client.tsx` |
| Public Stripe intent | `apps/portal/src/features/payments/actions/create-public-stripe-intent.ts` |
| Public Stripe record | `apps/portal/src/features/payments/actions/record-public-stripe-charge.ts` |
| CX Pay one-off charge | `apps/portal/src/features/payments/actions/process-one-off-charge.ts` |
| Pay-page data fetch | `apps/portal/src/features/payments/lib/fetch-pay-page-data.ts` |
| Card forms | `apps/portal/src/features/payments/components/{stripe-payment-form,collect-js-form}.tsx` |
| Prospect/offer UI (already in web) | `apps/web/src/features/dushi-microsite/components/{OfferCountdown,IWantThisWeek,MobileStickyCTA,ExitIntentModal}.tsx` |
