# Dushi Week Build — Handoff SOP

One itinerary + one microsite per booked (or prospecting) family.
Two skills do the work. You review and approve at two gates.

---

## What you need before starting

| Tool | Access needed |
|---|---|
| Claude Code | Desktop app installed on your Mac — https://claude.ai/code |
| `claude-toolkit` repo | GitHub org member (TommyCoconutIT) — clone + run `./install.sh` |
| `tommy-os` repo | GitHub org member (TommyCoconutIT) — clone to `~/Code/tommy-os` |
| Airtable | Access to base `appFRLV1H76ohiIQS` (Dushi Weeks + Pipeline tables) |
| TC portal | To read the payment token from the Pipeline record |
| Vercel | Optional — deploys trigger automatically on merge |

**One-time setup after cloning `tommy-os`:**
```bash
cd ~/Code/tommy-os/apps/web
npm install
```
This is required once. The TypeScript check (Step 5) will fail without it.

---

## The 10 steps

### STEP 1 — Gather guest info
Open the guest's Pipeline record in Airtable. Note:
- Full names (spelling matters — it goes on the website)
- Arrival + departure dates
- Estate name (Dushi Hideaway, Bayside Hill, etc.)
- All-in price
- Payment token (the short code in the booking URL field)
- Flight codes if available

### STEP 2 — Check the Dushi Weeks registry
In Airtable → base `appFRLV1H76ohiIQS` → "Dushi Weeks" table:
- Search for the guest's email. If a row exists, you're updating — not starting fresh.
- Find the highest Build # and add 1. That's your slug number.

### STEP 3 — Build the itinerary
Open Claude Code. In any terminal or the desktop app, type:

```
/dushi-week-builder
```

Claude will ask for the guest info. Paste everything from Step 1.
It will produce a full printable itinerary document.

**⛔ GATE 1 — Do not proceed until Boy has read and approved the itinerary.**
The voice and the content are the product. This is non-negotiable.

### STEP 4 — Build the microsite
Once the itinerary is approved, type:

```
/dushi-week-microsite-from-itinerary
```

Point it at the itinerary file. Claude will build:
- `apps/web/src/features/dushi-microsite/content/<family>.ts`
- `apps/web/src/app/[locale]/<FamilySlug>DushiWeek<N>/page.tsx`

### STEP 5 — TypeScript check
Claude runs this automatically, but verify:

```bash
cd ~/Code/tommy-os/apps/web && npm run typecheck
```

Must exit with 0 errors before opening a PR.

### STEP 6 — Open a PR
Claude opens the PR automatically. The title format is:
```
feat(marketing/<family-slug>-dushi-week-<n>): create personalized microsite
```

**⛔ GATE 2 — Do not merge until Boy has reviewed the PR.**

### STEP 7 — Merge + wait for deploy
Boy merges. Vercel auto-deploys. Takes 3–5 minutes.
Check the Vercel dashboard or DM Boy to confirm green.

### STEP 8 — Update Airtable
In the Dushi Weeks row:
- **Status** → `Offer Sent` (or `Booked` if already confirmed)
- **Microsite** → the live URL (`https://www.tommycoconutprivateresorts.com/<slug>`)
- **Pipeline ID** → the `rec...` ID from Step 1

### STEP 9 — Write the WhatsApp message
In Claude Code, ask:

```
Write the WhatsApp message to send [Guest Names] their microsite link,
based on the dushi-week-builder skill's [guest type] framing.
```

Guest types: `couple`, `young family`, `teen family`, `family with young adults`,
`multi-gen`, `friends group`.

### STEP 10 — Boy sends it
Hand the message and link to Boy. He sends it from the TC number.
(Or Boy explicitly delegates this step in writing.)

---

## Two things that will break it if you skip them

**1. Getting Gate 1 approval before building the microsite.**
A wrong voice in the itinerary = wrong voice in the microsite = full rebuild.

**2. Getting the real WhatsApp group invite URL.**
The microsite file ships with a placeholder (`REPLACE_WITH_..._GROUP_INVITE`) until you have the real `https://chat.whatsapp.com/<id>` link. Get it from Boy before the guest is sent the link.

---

## If something goes wrong

| Problem | Fix |
|---|---|
| TypeScript errors | Claude fixes them. Don't push until typecheck passes. |
| Vercel deploy fails | Check Vercel dashboard, DM Boy. |
| Wrong content in the microsite | Fix in the `.ts` file, push a new commit. Vercel redeploys automatically. |
| Offer expiry date passed | Update `expiresAtISO` in the family's `.ts` file, push, tell Boy. |
| WhatsApp link won't open | Try the URL with and without `?mode=gi_t` — test on the guest's device if possible. |

---

## Key reference files (read before your first build)

All in `skills/dushi-week-builder/references/`:

| File | What it is |
|---|---|
| `lessons-learned.md` | Every mistake from every prior build. Read this first. Every time. |
| `island-database.md` | Restaurants, beaches, crew bios, cruise scheduling logic |
| `itinerary-standard-sat-to-sat--couple.html` | The couple template — fastest start for sat-to-sat couple builds |

---

## The two repos

| Repo | What it is |
|---|---|
| `TommyCoconutIT/claude-toolkit` | The skills and this SOP. Clone once, `git pull` to stay current. |
| `TommyCoconutIT/tommy-os` | The website. Microsite code goes here via PR. |
