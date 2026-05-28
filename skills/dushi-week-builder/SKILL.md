---
name: dushi-week-builder
description: "Build personalized Dushi Week itineraries for Tommy Coconut Private Resorts guests. Use this skill whenever the user asks to create, edit, or update a guest itinerary, trip plan, Dushi Week schedule, or vacation week for any Tommy Coconut guest — whether from scratch or modifying an existing one. Also trigger when the user mentions 'itinerary', 'Dushi Week', 'guest week', 'trip plan', 'schedule their week', or any reference to planning a guest's stay in Curacao at a TC villa. This skill contains the full island knowledge database, guest type intelligence, scheduling logic, cruise ship awareness, and a verified-operator research protocol for new activities. TWO OUTPUT PATHS: (A) HTML template skeleton — when a standard HTML template exists for the variant, use it as the authoritative skeleton and only personalize tokens + specific requested blocks; (B) fresh Markdown — for new variants with no HTML template. See lessons-learned.md Section 10 and Section 20."
---

# ═══════════════════════════════════════════════════
# CRITICAL RULES — ONE-PAGE QUICK REFERENCE
# ═══════════════════════════════════════════════════
# Read this FIRST, then the full skill below.

# 1. CHECK LOCAL ORIGINAL FIRST — ~/Desktop/Leads-dushi-week/[guest]/itinerary-*.html is Tier 1 (ALWAYS check before anything else)
# 2. NEVER REWRITE DAY COPY — Copy verbatim from Tier 1 or Tier 2 (Activity Catalog), only swap tokens (names, dates, estate)
# 3. HTML SKELETON = STRUCTURE ONLY — Not a content source, day copy is LOCKED
# 4. ACTIVITY CATALOG = CONTENT SOURCE — Airtable tblhqPOkdgvW2pnVY, use segment-variant fields verbatim
# 5. UNKNOWN ACTIVITIES → OPERATOR RESEARCH PROTOCOL — Never invent operator, hours, price, or location
# 6. DIETARY ALLERGIES → GUEST TELLS SERVER — NEVER claim "TC handled it" or "we've flagged it"
# 7. CRUISE CALENDAR DRIVES SCHEDULING — Zero-ship days = beach, Heavy-ship days = city/downtown
# 8. LOAD TOMMY-COCONUT-VOICE — Before writing any letters, philosophy, or closing
# 9. OUTPUT PATH — HTML if template exists (Path A), Markdown if not (Path B)
# 10. POST-BUILD VERIFICATION — Run grep checks + source audit table before delivering

# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# 🛑 STOP & ASK USER BEFORE PROCEEDING IF:
# ═══════════════════════════════════════════════════
# - AIRTABLE_API_KEY not set (check with: echo $AIRTABLE_API_KEY | head -c 10)
# - Guest email not provided
# - Arrival/departure dates not provided
# - Villa not assigned
# - Guest type unclear (Couple/Friends/Family/etc)
# - Cruise calendar not available for their week
# - Unknown activity with no verified operator (run Operator Research Protocol first)
# - Original itinerary exists but user says "don't touch it"
# - Build # collision in Airtable Dushi Weeks table
# - Microsite deployment method unclear
# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# STEP NEGATIVE THREE — VERIFY FOLDER PATH (MANDATORY)
# ═══════════════════════════════════════════════════
# The file-system trap: Two folders exist on your Desktop.
# Run this to see which ones exist:
#   ls -la ~/Desktop/ | grep -i leads
# 
# Canonical workspace (USE THIS ONE): ~/Desktop/Leads-dushi-week/ (NO SPACE)
# Legacy folder (DO NOT USE): ~/Desktop/Leads- dushi week/ (WITH SPACE)
#
# If both exist, CONFIRM WITH USER which folder to use before proceeding.
# Default to the no-space folder unless user explicitly directs otherwise.
# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# STEP NEGATIVE FOUR — VERIFY AIRTABLE AUTH (MANDATORY)
# ═══════════════════════════════════════════════════
# Before querying Airtable, verify the API key is set:
#   echo $AIRTABLE_API_KEY | head -c 10
#
# If empty, redacted, or returns nothing:
#   STOP — Ask user to set AIRTABLE_API_KEY in ~/.hermes/.env
#   DO NOT proceed with Airtable queries until auth is confirmed.
#
# If curl returns 401 even with key set, export the env var:
#   source ~/.hermes/.env 2>/dev/null || true
# Then retry the curl command.
# ═══════════════════════════════════════════════════

# ⚠️ CRITICAL RULE — READ BEFORE ANYTHING ELSE ⚠️

**THE SINGLE BIGGEST FAILURE MODE:** The AI treats the HTML skeleton as a "template to fill in" and rewrites day copy that should be **LOCKED**. This injects hallucinations, slop, and errors into approved content.

**THE THREE-TIER HIERARCHY — CONTENT AUTHORITY FLOWS IN THIS ORDER:**

| Tier | Source | When to Use | What You Can Change |
|------|--------|-------------|---------------------|
| **Tier 1** | **Local approved original** (`~/Desktop/Leads-dushi-week/[cartel]/itinerary-*.html`) | **ALWAYS CHECK FIRST** — if this exists, it is the ONLY source of truth **for content** | Segment variables, styling tokens, Cloudinary IDs, user-requested swaps. **Structural overloads must still be fixed — see Section 25.** |
| **Tier 2** | **Activity Catalog** (Airtable `tblhqPOkdgvW2pnVY`, base `appFRLV1H76ohiIQS`) | When NO local original exists (new leads, prospects) | Use segment-variant fields (`Variant — Couple`, `Base Description`) **verbatim** |
| **Tier 3** | **HTML Skeleton** (`itinerary-standard-sat-to-sat--couple.html`) | **STRUCTURE ONLY** — never use as content template | Layout, CSS, tokens. **DAY COPY IS READ-ONLY** |

**⚠️ NEVER:**
- Rewrite day copy because you think it could be "better"
- Replace time blocks with alternatives from memory
- Add activities that weren't requested
- Remove blocks that weren't mentioned
- **Redesign the HTML skeleton — use it verbatim, do not add/remove structural elements (e.g. upsell boxes, info boxes, restaurant cards) that don't exist in the canonical template**
- **Change the order of time blocks — the skeleton's sequence is the approved schedule**
- **Add time labels (e.g. "~7:00 PM") to dinner blocks unless they exist in the skeleton**
- **Use placeholder tokens like "{First Name}" — use "The booker" or generic references when names are unknown**

**✅ ALWAYS:**
- Check for local approved original FIRST (before reading any other file)
- If original exists: copy-paste day content verbatim, only swap tokens
- If no original: query Activity Catalog by exact activity name + segment variant
- If catalog is empty: ask user to paste approved block, accept verbatim
- **Preserve the skeleton's exact structure — day order, block sequence, element types**
- **If the skeleton doesn't have upsell boxes, don't add them**
- **If the skeleton has dinner without a time label, don't add one**

**The skeleton does NOT contain specific activities, times, or day copy.** The standard HTML skeleton has placeholder shapes like `Day 2 · Morning · [ACTIVITY]` and `Day 2 · Evening · [DINNER]`. The specific activities, times, and descriptions live in the **approved original** (Tier 1) or **Activity Catalog** (Tier 2). If the approved original contains structural overloads (too many events on one day, impossible timing), **the approved original still wins for content** — but the overloads must be fixed per lessons-learned.md Section 23.

---

# Dushi Week Builder

## ⚠️ STEP NEGATIVE TWO — Review Canonical Folder Startup Prompt (MANDATORY)

**Before any build action — even before checking for local originals — review the canonical folder's startup prompt.** It may contain session-specific rules that override general skill guidance (e.g., "never use the Friends HTML skeleton as content source," "comparison build must use parallel subfolder," or "approved source hierarchy for this session").

1. **Check the canonical folder first:**
   ```bash
   ls ~/Desktop/Leads-dushi-week/
   ```
2. **Read `DUSHI-WEEK-START-UP-PROMPT.md`** if it exists at the folder root:
   ```bash
   cat ~/Desktop/Leads-dushi-week/DUSHI-WEEK-START-UP-PROMPT.md
   ```
3. **Treat its rules as authoritative for this session.** If it conflicts with the skill's general guidance, the startup prompt wins.
4. **Only then proceed to Step Negative One.**

**The file-system trap:** The canonical lead workspace is `~/Desktop/Leads-dushi-week/` (**no space**). An older folder `~/Desktop/Leads- dushi week/` (**with space**) exists as legacy. Always use the no-space folder unless the user explicitly directs otherwise.

---

## ⚠️ STEP NEGATIVE ONE — Check for Local Canonical Template (MANDATORY)

**After reading the startup prompt (Step Negative Two), before reading lessons-learned.md, before asking the user anything — check if a canonical approved original already exists for this guest.**

Run this command:
```bash
ls -la ~/Desktop/Leads-dushi-week/
```

Then check inside the guest's folder (e.g. `~/Desktop/Leads-dushi-week/[cartel-name]/`) for:
- `itinerary-[cartel-name].html` — the approved original itinerary
- `Dushi-Week-[Cartel].md` — completed canonical MD
- `email-[family]-offer.html` — offer email

**If an approved original exists:**
1. **READ IT FIRST** — this is Tier 1, the ONLY source of truth
2. **Copy-paste day content verbatim** — do not rewrite, paraphrase, or "improve"
3. **Only change:** names, dates, estate, flight codes, Build #, styling tokens, Cloudinary IDs
4. **Write output to a parallel subfolder** (e.g. `…/[cartel-name]-ai-test/`) unless explicitly told to overwrite

**If NO approved original exists:**
1. Fall through to the lessons-learned.md workflow
2. Query Activity Catalog (Tier 2) for day copy by exact activity name + segment variant
3. Use HTML skeleton (Tier 3) for **structure only** — day copy from catalog or user-provided

---

## ⚠️ STEP ZERO — Read Before Anything Else

**After checking for local originals (Step Negative One), read `references/lessons-learned.md`.**

This document contains every mistake, correction, dangerous pattern, and factual error from real builds. It exists because real builds produced hallucinated content, dangerous liability language, and factual errors that cost time and created business risk. The lessons-learned document is the institutional memory of every Dushi Week ever built. Read it first. Every time. No exceptions.

After reading lessons-learned.mkd, also read the value stack at `tc-guest-confirmation/references/value-stack.md` (in the skills directory) — this contains the complete offer breakdown that you must understand before building any itinerary.

Then follow the Pre-Build Checklist in Section 16 of lessons-learned.md before proceeding.

**Also verify:** If the user references or attaches an existing HTML file (e.g. "review this html this is the skeleton"), do NOT create a new file. Ask first: "Do you want me to modify the existing file in place, or create a new one in the Leads folder?" Preserve originals unless explicitly told to overwrite.

---

## Pre-Flight Checklist — COMPLETE BEFORE WRITING ANY CONTENT

**Do not proceed to Step 1 until you can check every box below.** This checklist exists because the #1 failure mode is skipping Tier 1 discovery and treating the skeleton as a Mad Libs template.

### Tier 1 Discovery (MANDATORY — DO NOT SKIP)
- [ ] **Checked for local approved original:** Ran `ls ~/Desktop/Leads-dushi-week/` and confirmed the exact folder path (no space vs. space)
- [ ] **If original exists:** Read the entire file, identified all day blocks, confirmed which sections are locked vs. which need token swaps
- [ ] **If original exists:** Confirmed with user whether to modify in place or write to parallel test folder
- [ ] **If original does NOT exist:** Confirmed with user that this is a new lead/prospect build (Tier 2 → Activity Catalog)

### Copy Source Confirmation
- [ ] **For each day block:** Identified the source (Tier 1 original / Tier 2 Activity Catalog / Tier 3 skeleton fallback)
- [ ] **For Activity Catalog queries:** Used exact activity name (e.g. `"Distillery Morning"` not `"Distillery"`) + correct segment variant field (`Variant — Couple`, `Variant — Friends`, etc.)
- [ ] **For skeleton fallback:** Confirmed the block genuinely doesn't exist in Tier 1 or Tier 2 (not just "I didn't check")
- [ ] **For any pasted text from user:** Accepted verbatim, no rewording

### Guest Type + Segment Match
- [ ] **Identified guest type:** Couple / Friends / Family teens / Family young kids / Family young adults / Multi gen
- [ ] **Matched to correct template:** See Section 20 template registry — each type has different day structure
- [ ] **Confirmed Build # from Dushi Week Registry:** Airtable `appFRLV1H76ohiIQS` → table `tblGHUrF6PGkqrnn3` → `max(Build #) + 1`

### Voice + Liability Guardrails
- [ ] **Loaded tommy-coconut-voice skill** before writing any original content (letters, philosophy, closing)
- [ ] **Checked for dietary restrictions:** Will frame as "let the server know" NEVER as "TC has handled it"
- [ ] **Checked for new/unknown activities:** Will run Operator Research Protocol if no verified operator exists

### Technical Verification
- [ ] **Confirmed output path:** HTML template (Path A) if skeleton exists for this variant / Markdown (Path B) if no skeleton
- [ ] **Confirmed V8 design tokens:** Cormorant Garamond + Inter, `--color-ink` / `--color-cream` / `--color-turq`, heading weight 400
- [ ] **Confirmed booking URL token:** Pipeline record ID (`rec...`), NOT short token from `fldZIAV3Qr8RaTixS`
- [ ] **AIRTABLE_API_KEY verified:** Ran `echo $AIRTABLE_API_KEY | head -c 10` — confirmed set and not redacted
- [ ] **Folder path confirmed:** Ran `ls -la ~/Desktop/ | grep -i leads` — confirmed canonical folder (no space)
- [ ] **Step 10 ready:** Delivery & Deployment checklist reviewed (microsite, Airtable, Obsidian, follow-up)

---

## ⚠️ STEP 10: DELIVERY & DEPLOYMENT — RUN AFTER BUILD COMPLETE ⚠️

**After the itinerary document is built, complete these delivery steps before saying "done":**

### 10.1 Deploy Microsite (if applicable)
```bash
# Use the dushi-week-microsite skill to deploy
# Or run: hermes dushi-week-microsite --guest [guest-folder]

# Verify microsite is live:
curl -I https://www.tommycoconutprivateresorts.com/[GuestSlug]
# Should return HTTP 200

# Record microsite URL in Airtable:
# - Dushi Weeks table → Microsite field
# - Pipeline table → Microsite URL field (if exists)
```

### 10.2 Send to Guest
**Email path:**
```bash
# Use email-[guest]-offer.html template from guest folder
# Send via: send_message tool (if email connected) or manual send
# Subject: "Your Dushi Week at Tommy Coconut Private Resorts"
```

**WhatsApp path:**
```bash
# Use whatsapp-[guest]-send-message.md script from guest folder
# Send via: send_message tool (if Telegram/WhatsApp connected) or manual send
# Include microsite URL + hold expiry date
```

### 10.3 Update Airtable Pipeline
**Required field updates:**
- `Lead Stage` = "Offer Sent"
- `Status` = "Offer Sent"
- `Payment_Gateway` = "Stripe" (or as configured)
- `Offer Sent Date` = today's date (YYYY-MM-DD)
- `Microsite URL` = [deployed microsite URL]

**Optional but recommended:**
- `Lead Temperature` = "Hot" (if they engaged with the form)
- `QuotedRevenue` = [OfferWeeklyRate from Pipeline table]

### 10.4 Log to Obsidian
**Create/update guest log:**
```bash
# File: ~/Obsidian/TommyCoconut/07-Reports/Guests/[GuestName]-[MonthYear].md
# Include:
#   - Guest name, email, phone
#   - Stay dates, villa, guest count
#   - Status: "Offer Sent" or "Microsite Live"
#   - Microsite URL
#   - Hold expiry date
#   - Follow-up schedule (Day 3 check-in, Day 7 nudge, Hold expiry)
#   - Delivery checklist (what's done, what's pending)
```

**Update daily log:**
```bash
# File: ~/Obsidian/TommyCoconut/00-Inbox/Daily-Logs/[YYYY-MM-DD].md
# Add to "Completed" section:
#   - "[Guest Name] — Dushi Week built, microsite deployed, offer sent"
```

### 10.5 Schedule Follow-Up
**Add to Airtable or your task system:**
- **Day 3:** Check-in message ("Any questions?")
- **Hold Expiry (48 hours from deploy):** Final nudge before hold expires
- **Day 7:** Final nudge or archive as "Cold Lead"

**Or set a cron job:**
```bash
# Example: hermes cronjob create --schedule "3d" --prompt "Check in with [Guest Name] — Dushi Week follow-up"
```

### 10.6 Final Verification
**Before saying "done", confirm:**
- [ ] Microsite URL is live (curl returned HTTP 200)
- [ ] Airtable Pipeline updated (Lead Stage = Offer Sent)
- [ ] Airtable Dushi Weeks table updated (Microsite URL logged)
- [ ] Obsidian guest log created/updated
- [ ] Obsidian daily log updated
- [ ] Follow-up scheduled (Day 3, Hold Expiry, Day 7)
- [ ] Email/WhatsApp ready to send (or already sent)

**Present this summary to the user:**
```
═══════════════════════════════════════════════════
DELIVERY COMPLETE — [Guest Name]
═══════════════════════════════════════════════════
✅ Itinerary built: ~/Desktop/Leads-dushi-week/[guest]/itinerary-[guest].html
✅ Microsite deployed: https://www.tommycoconutprivateresorts.com/[Slug]
✅ Airtable updated: Lead Stage = "Offer Sent", Payment = Stripe
✅ Obsidian logged: 07-Reports/Guests/[GuestName].md + Daily Log
✅ Follow-up scheduled: Day 3 (May 31), Hold Expiry (May 30, 6 PM)
✅ Email/WhatsApp: Ready to send (script in guest folder)

NEXT STEPS:
- Send email/WhatsApp to guest (use script in guest folder)
- Wait for response (hold expires May 30, 6 PM Curaçao time)
- Day 3 check-in if no response (May 31)
═══════════════════════════════════════════════════
```

---

## ⚠️ COPY VERIFICATION — PRESENT THIS TABLE BEFORE BUILDING ⚠️

**Before writing any content, present this table to the user and get explicit confirmation:**

```
COPY SOURCE VERIFICATION
─────────────────────────────────────────────────────────────────────────
Section              │ Source                          │ Locked or Editable?
─────────────────────────────────────────────────────────────────────────
Cover page           │ [Tier 1 / Tier 2 / Tier 3]      │ [Tokens only / Full edit]
Philosophy page      │ [Skeleton / Original / Fresh]   │ [Locked / Editable]
Letter from Tommy    │ [Fresh write / Original]        │ [TC Voice / Verbatim]
Day 1 schedule       │ [Original / Catalog / Skeleton] │ [LOCKED / Token swap only]
Day 2 schedule       │ [Original / Catalog / Skeleton] │ [LOCKED / Token swap only]
Day 3 schedule       │ [Original / Catalog / Skeleton] │ [LOCKED / Token swap only]
... (repeat for all days)
Restaurant cards     │ [Original / Catalog]            │ [First occurrence only]
Upsell boxes         │ [Catalog / User-provided]       │ [Verbatim / Editable]
Crew bios            │ [island-database.md]            │ [LOCKED — use corrected bios]
Closing page         │ [Original / Fresh]              │ [TC Voice / Verbatim]
─────────────────────────────────────────────────────────────────────────

CONFIRMATION REQUIRED:
"Type 'locked' to confirm: I will NOT rewrite day copy that exists in Tier 1 or Tier 2.
 I will only swap tokens (names, dates, estate) and insert explicitly requested blocks."
```

**Do not proceed until the user confirms.** This explicit confirmation prevents the "I thought I was supposed to improve it" failure mode.

---

## ⚠️ POST-BUILD VERIFICATION — RUN BEFORE DELIVERING ⚠️

**Before saying "done", run this verification pass and present the results to the user:**

### Copy Integrity Check
```bash
# 1. Verify no day copy was rewritten from memory
# Compare your output against the Tier 1 original or Activity Catalog source
# Every day block should match source verbatim except for:
#   - Token swaps (names, dates, estate, flight codes)
#   - Explicitly requested insert/swap blocks

# 2. Verify restaurant-about cards appear on FIRST occurrence only
grep -n "restaurant-about" your-output.html
# Should return N cards where N = unique restaurants in the week

# 3. Verify no "$35/person" or "Culinary Pass" in Two Coconut builds
grep -n "\$35\|Culinary Pass\|credit\|house account" your-output.html
# Must return 0 results for Two Coconut builds

# 4. Verify no liability language about dietary restrictions
grep -in "handled\|flagged\|briefed\|we've taken care" your-output.html
# Must return 0 results

# 5. Verify crew bios match corrected versions (Section 4)
# Boy = "The host who cares the most" (NOT "shows up late")
# Happy = former street dog (NOT a dachshund)
# Lucky = dachshund
# Happy AND Lucky together on flamingo hike (never Lucky alone)
```

### Estate Name Consistency Check (CRITICAL — User catches mismatches)
```bash
# 6. Extract estate name from cover photo Cloudinary URL
grep -o 'Villa_[^"]*\|Dushi_[^"]*\|Palm_Breeze[^"]*' your-output.html | head -1
# This reveals the actual villa in the image filename (e.g., "Villa_Palm_Breeze-87")

# 7. Extract estate name from text references
grep -o 'Dushi Hideaway\|Villa Palm Breeze\|Villa [A-Za-z ]*' your-output.html | sort -u

# 8. COMPARE — They MUST match
# If cover photo says "Villa_Palm_Breeze" but text says "Dushi Hideaway" → MISMATCH
# Fix: Either swap the cover photo URL OR update all text references to match
```

**⚠️ PRE-DELIVERY REQUIREMENT:** Present this table to the user before delivering:

```
ESTATE NAME VERIFICATION
─────────────────────────────────────────────────────────────────────────
Cover Photo (Cloudinary URL)  │ Text References (Throughout)  │ Match?
─────────────────────────────────────────────────────────────────────────
[e.g. Villa_Palm_Breeze-87]   │ [e.g. Dushi Hideaway]         │ ❌ MISMATCH
─────────────────────────────────────────────────────────────────────────

ACTION REQUIRED:
- If photo is correct: Update all "Dushi Hideaway" → "Villa Palm Breeze" in text
- If text is correct: Replace cover photo URL with correct villa image
- Confirm with user which estate they're actually staying at
```

**This is a critical quality signal.** User catches estate name mismatches — verify before delivering.

### Copy Source Audit Table
**Present this table to the user before delivering:**

```
COPY SOURCE AUDIT
─────────────────────────────────────────────────────────────────────────
Day Block            │ Source Used                     │ Verbatim or Modified?
─────────────────────────────────────────────────────────────────────────
Day 1 schedule       │ [e.g. Tier 1 Original]          │ [Verbatim / Token swaps only]
Day 2 schedule       │ [e.g. Activity Catalog Couple]  │ [Verbatim]
Day 3 schedule       │ [e.g. Tier 1 Original]          │ [Verbatim / Token swaps only]
... (repeat for all days)
Letter from Tommy    │ [Fresh TC Voice write]          │ [Original — no source existed]
Restaurant cards     │ [Tier 1 Original]               │ [First occurrence only]
─────────────────────────────────────────────────────────────────────────

ANY "MODIFIED" ENTRIES MUST BE EXPLICITLY JUSTIFIED:
- "Token swaps only" = OK (names, dates, estate)
- "User-requested swap" = OK (e.g. "move distillery to Thursday")
- "Improved the copy" = NOT OK — revert to source verbatim
```

**If any day block shows "Modified" without a valid justification, revert it to the source verbatim before delivering.**

---

## Pre-Build Discovery — Map Existing Documents First

**BEFORE proceeding — complete Step Negative Three (folder path verification):**
```bash
ls -la ~/Desktop/ | grep -i leads
```

This shows which folders exist. You will see one or both:
- `Leads-dushi-week/` (NO SPACE) ← **CANONICAL — USE THIS ONE**
- `Leads- dushi week/` (WITH SPACE) ← Legacy from previous AI workflow

**If both exist:** CONFIRM WITH USER which folder to use. Default to no-space folder unless user explicitly directs otherwise.

**If user says "the other folder is from a different AI":** Honor that choice and work in the folder they specify.

Before writing a single word, check whether this guest already has a working folder on disk.

**The alternate-folder signal:** When the user says "the other folder is from a different AI" or specifically asks to work in `Leads-dushi-week/` (no space), honor that choice. Read the `DUSHI-WEEK-START-UP-PROMPT.md` inside **that** folder first — it may contain session-specific rules for comparison builds. For comparison/test builds, always use the canonical HTML skeleton + real data extracted from approved originals, and write output to a parallel subfolder such as `…/[cartel-name]-ai-test/`.

Run `ls ~/Desktop/Leads*` to verify the exact path before proceeding.

1. **Check for existing originals.** Look in `~/Desktop/Leads- dushi week/[cartel-name]/` for:
   - `Dushi-Week-[Cartel].md` — the completed canonical MD (may have real names, dates, villa, crew)
   - `email-[family]-offer.html` — offer email
   - Any pre-built `itinerary-*.html` — the existing styled render

2. **If originals exist with real guest data, extract from them.** Names, dates, villa, motivation, crew, dietary restrictions — the MD is the source of truth, not Airtable Q&A answers (which may be preliminary or simplified).

3. **Never overwrite originals.** If the user says "do not touch the originals," write new builds to a parallel subdirectory such as `…/[cartel-name]-ai-test/`. Copy the real data (not the HTML skeleton) into the test directory, then build fresh using the canonical template + real extracted data.

4. **Q&A data vs original data.** Booking-application Q&A JSONs can misstate duration (e.g., "5 nights" when the original booking is 7 nights Sat→Sat). The original completed MD always wins if it exists.

5. **Skill quality test workflow.** When the user asks to "test if the skill is good enough" or wants a "fresh build test," always use the canonical Friends/Couple/etc. HTML skeleton (not the pre-built itinerary HTML) and map real extracted data into it. Build in isolation, then compare test output to the pre-built original for parity. Do not copy the pre-built HTML.

---

## STEP 0.5 — Look Back (Dushi Week Registry)

**Every Dushi Week we generate is logged in one Airtable table. Check it BEFORE you build, and update it AFTER you ship.** This is how we avoid re-research, duplicate builds, and slug-number collisions — and how we honor returning guests.

**Prerequisite:** Airtable auth must be available. If `AIRTABLE_API_KEY` is not in `~/.hermes/.env`, stop and ask the user to save it before querying. Do not attempt to pass tokens through `write_file`/`execute_code` — platform redaction scrubbers will corrupt them and produce `401 Unauthorized`.

**Shell workaround:** If curl calls return 401 even after configuring the token, the env var may not be exported to the subprocess. Before any curl command, run: `source ~/.hermes/.env 2>/dev/null || true`

- **Where:** base `appFRLV1H76ohiIQS` → table **"Dushi Weeks"** (`tblGHUrF6PGkqrnn3`). Query via the `productivity/airtable` skill (`curl` + `filterByFormula`). There is no Airtable MCP — use plain REST.
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

**Check user-local templates first.** Before choosing Path A or B, check `~/Documents/Claude/Projects/Dushi Week Itinerary Builder/` (or whatever local project folder the user maintains) for `.html` template files matching the guest variant. If found, those are the canonical skeleton — not the skill directory copies. The user may have updated the skeletons since the last skill install.

**Two paths after template discovery:**

### Path A — HTML Template Skeleton (preferred when local canonical template exists)

When a standard HTML template exists for the variant (check user project folder first, then skill references dir), open it and use it as the skeleton. **The day content in the template is the authoritative schedule — do not rewrite it.** You personalize tokens (cover, letter, philosophy, closing) and make only the specific insert/swap/remove changes explicitly requested.

- **User local templates (canonical):** Check `~/Documents/Claude/Projects/Dushi Week Itinerary Builder/` first. These are the most current — the user may have updated them since skill install.
- **Skill reference templates (fallback):** `~/.hermes/skills/dushi-week-builder/references/`
- Save output as `itinerary-[cartel-name].html` in the guest's working folder
- Copy source: Activity Catalog → Itinerary Items V2 → write from comparable (in that order)
- See `references/lessons-learned.md` Section 20 for the full rule set

### Path AA — V8 Token Migration for HTML Skeletons

When using an HTML template that was built before V8 (May 2026), apply the V8 design token migration **before personalizing**:

| Legacy (V5–V7) | V8 / Live Site (May 2026+) |
|---|---|
| Playfair Display | Cormorant Garamond |
| Lato | Inter |
| `#002D42` Navy | `#0A2330` `--color-ink` |
| `#FDFBF7` / `#FAF7F1` Cream / Alabaster | `#FAF6EF` `--color-cream` |
| `#7EDCD5` Dushi Blue | `#6CE3DF` `--color-turq` (primary accent) or `#A7EDE9` `--color-turq-soft` (soft fill) |
| `#FFC125` Sunset Gold | **Retired from live system.** Replace with `--color-turq` for accent/CTA emphasis, `--color-ink` for text emphasis, or `--color-turq-soft` for badges/highlights. Do NOT use `#FFC125` or Gold on digital surfaces unless confirmed by Ray for print-only use. |

- Headline weight: **400** (not 700) with tight tracking (`letter-spacing: -0.01em`) — increase size, don't bold Cormorant headlines
- `<link>` tag for Google Fonts: `family=Cormorant+Garamond:ital,wght@0,400;1,400` (add `1,400` for italic)

**Execution steps (apply in this order):**
1. **Google Fonts link** — Replace the existing `<link>` tag with the V8 `Cormorant+Garamond:ital,wght@0,400;1,400&family=Inter:wght@400;500;600` link. Remove any separate Playfair or Lato links.
2. **Font-family declarations** — Templates use double-quoted font names in inline `<style>` blocks (e.g. `font-family: "Lato", Arial, sans-serif;`). Replace ALL occurrences, including quoted forms: `"Lato"` → `"Inter"`, `"Playfair Display"` → `"Cormorant Garamond"`.
3. **Hex colors** — Global replace: `#002D42` → `#0A2330`; `#FDFBF7`/`#FAF7F1` → `#FAF6EF`; `#7EDCD5` → `#6CE3DF`; `#FFC125` → `#6CE3DF`.
4. **CSS custom properties** — Add `--color-ink: #0A2330; --color-turq: #6CE3DF; --color-turq-soft: #A7EDE9;` to the `:root` block. V5 templates don't have these variables.
5. **Variable references** — Replace `var(--gold)` with `var(--color-turq)` and `var(--gold-soft)` with `var(--color-turq-soft)`.
6. **Headline weight normalization** — Cormorant headlines must be weight 400, NOT 700. Do **not** do a global `700 → 400` replace — that breaks body bold in `.time-label`, `<strong>`, etc. Scope to selectors using Cormorant: `.cover-title`, `.day-title`, `.letter-title`, `.philosophy-title`, `.day-badge`, `.crew-name`. Add `letter-spacing: -0.01em` to Cormorant H1/H2 rules if absent.

**Pitfall:** If a day-hero badge still uses `background: var(--gold)` or `background: #FFC125`, replace with `background: var(--color-turq)` (`#6CE3DF`). The turquoise badge on dark hero is the V8 pattern.

### Path B — Fresh Markdown (new variants with no HTML template)

For guest types or variants with no existing HTML template. One deliverable: a single, clean Markdown text document. No HTML, no PDF, no DOCX, no photos. Read `references/output-pipeline.md` for how to lay the text out well.

- Strong, scannable headings (`#`, `##`, `###`) for cover, philosophy, letter, Week at a Glance, each day, Good to Know, Crew, Closing
- Week at a Glance as a Markdown table (Day | Highlight | Dinner | Vibe)
- Each day as a clear block: title line, cruise intel line, time entries, three info boxes, pro tips
- Save as `Dushi-Week-[CrewName].md`

---

## Airtable Lead Search — Known Workflow Pitfalls

When looking for a lead by email in the Pipeline table, the basic list endpoint with `maxRecords=100` returned only records with non-empty emails (31 out of 100). The `filterByFormula` endpoint (`{Email}='email@address.com'`) was required to locate raw leads with minimal data. Use `filterByFormula` for reliable email matching.

**Two bases exist** — new funnel leads may be in either:
1. **Main base** (`appFRLV1H76ohiIQS`) — Pipeline (`tblb7gP5D3NYND9a0`) = bookings
2. **Marketing lead base** (`appiQO2iMCRjdMe0F`) — Sessions (`tbl7T49CVkrGv5HNe`) = landing-page submissions

When a Pipeline record is `Status: New Lead` with blank `FirstName`/`LastName`, no dates, and no villa — it's a raw funnel submission. Do not invent names, dates, or a villa. Ask the user.

---

## Reference Files

Read these in this order. The order matters — lessons-learned corrects errors in island-database.

1. **`references/lessons-learned.md`** — **READ FIRST. MANDATORY.** Every mistake, correction, insight, and technical lesson from real builds. Corrects errors in all other reference files. Contains the pre-build checklist, restaurant deep knowledge, crew corrections, liability rules, and completed build templates.

2. **`references/island-database.md`** — Restaurants (with URLs), experiences, beaches, crew bios, scheduling constraints, activity hours, cruise ship rules, villa details, provisioning lists, guest type scheduling variants. **Note: Some entries in this file are outdated — lessons-learned.md Section 13 lists specific corrections that override this file.**

3. **`references/output-pipeline.md`** — How to lay out the text (Markdown) itinerary so it reads beautifully: document structure, day-block format, tables, sign-offs, file naming, and the delivery checklist.

4. **`references/github-sync-status.md`** — GitHub sync status, local vs. remote feature comparison, lead lookup workflow, estate name verification checklist. **READ BEFORE SUBMITTING PRS OR SEARCHING FOR LEADS.** Updated 2026-05-28.

5. `references/segment-templates.md` — Day-by-day structures for all 6 guest segments (Couple, Friends, Family teens, Family young kids, Family young adults, Multi gen). Use when Activity Catalog queries fail — authoritative fallback, do not invent from memory. Added 2026-05-27.
6. `references/structural-review-checklist.md` — Post-build validation: skeleton comparison table, island-specific day events, trace technique for mystery content, overload pattern reminders. Added 2026-05-27.
7. `references/structural-overload-origin.md` — Why the HTML skeleton is structure-only and where overloads actually come from (the approved original, not the skeleton). Added 2026-05-27 after Chrissymag Cartel post-fix analysis.

8. **`references/lead-folder-layout.md`** — Filesystem conventions for the `~/Desktop/Leads- dushi week/` lead folder (note the space). How to check for existing originals, data precedence rules, and safe test-build subfolder naming.

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
- [ ] **Missing guest data handled:** No `{First Name}`, `{Guest Name}`, or other raw template tokens remain in the output. See Section 22.
- [ ] **Structural label alignment:** Every `time-label` heading matches its `time-desc` activity — label swaps in the skeleton (e.g., Flamingo Hike / De Gouverneur) must be caught and fixed. See Section 23.
