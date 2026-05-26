---
name: tommy-advisor-outreach
description: Researches travel-advisor contacts in the Tommy Coconut Travel Advisor Pipeline Airtable, drafts hyper-personalized cold emails on TC brand voice, writes drafts back to Airtable, and posts a Slack review package. Trigger phrases include "run advisor outreach for wave X", "draft emails for wave X", "research [agency] and draft the email".
---

# Tommy Coconut Advisor Outreach

End-to-end orchestrator: pulls advisor contacts from Airtable → parallel research subagents → parallel email-writer subagents → writes drafts back to Airtable → posts Slack review.

Boy reviews in Slack, manually toggles status to `Reviewed` in Airtable for approved drafts, then copies the body and sends manually from `boy@tommycoconut.com` with the local PDF attached.

---

## Triggers

This skill has TWO modes — **prospect** and **outreach**.

### Prospect mode (find contacts, write to Airtable as candidates)

- "prospect Wave [1|2|3|4]"
- "prospect contacts for [agency name]" (one-off)
- "find contacts for Wave [X]"
- "seed Wave [X]"

Use when the table is empty for the requested wave, or when Boy wants to find a contact at a new agency.

### Outreach mode (research + draft emails for existing contacts)

- "run advisor outreach for wave [1|2|3|4]"
- "run advisor outreach" (all waves with `To Research` status)
- "research [agency name] and draft the email" (single-contact dry run)
- "draft emails for wave [X]"
- "research the advisors" / "advisor pipeline" / "work the advisor list"
- "write emails for wave [X]" / "draft the advisor emails" / "build the advisor emails"
- "who should we email first" / "prep the travel agent emails"
- "check advisor status" / "how many advisors are To Research" / "update the advisor pipeline"

Use after prospect mode (or manual seeding) has put contacts in the table with status `To Research`.

If the user says any of these without specifying a wave, ask which wave before proceeding. If the user says "run advisor outreach" and the wave has no `To Research` contacts but DOES have agencies in `config.wave_to_agencies`, suggest running prospect mode first.

---

## Load before every run

Read `~/.claude/skills/tommy-advisor-outreach/data/config.json` first — paths, IDs, send-from, wave→agency map.

Then, based on mode:
- **Outreach mode:** also read `voice-rules.md`, `pitch-angles.md`, `fallback-hooks.md` in parallel
- **Prospect mode:** only config.json is needed; the prospector subagent handles its own logic

---

# === OUTREACH MODE ===

## Step 1 — Pre-flight checks

Before spawning any subagents, hard-abort if ANY of these fail:

1. **PDF exists.** Verify the file at `config.pdf_path` resolves on disk (Bash `test -f`). If missing → post to Slack: *"PDF attachment missing at [path]. Cannot run outreach without the leave-behind. Fix the path in `~/.claude/skills/tommy-advisor-outreach/data/config.json` or move the file."* — and STOP.
2. **Airtable accessible.** A single read against base `appgvTQA2jmr63R4G`, table `Travel Advisor Pipeline`. If it errors, surface the error and STOP.
3. **Contacts to process.** Filter records where `Status = "To Research"` AND (`Wave = [requested wave]` OR no wave specified). If empty → post to Slack: *"No contacts with status 'To Research' in [Wave X]. Check Airtable: appgvTQA2jmr63R4G."* — and STOP.

---

## Step 2 — Spawn research subagents (parallel)

For each contact returned in step 1, spawn `tc-advisor-research` via the Agent tool. **All spawn in a single message — never sequentially.**

Pass each agent:
- Contact name
- Agency name + agency type
- Website URL + LinkedIn URL
- Specialization tags
- **T+L Profile URL** (if non-empty) — Travel + Leisure A-List profile, gives the agent a verified bio page to scan
- **Instagram URL** (if non-empty) — for additional taste-detail mining
- **Signature Story** (if non-empty) — the pre-scraped T+L "Epic Escape" / standout trip. Agent reads this in Step 0 as a research seed before web searching (see tc-advisor-research.md Step 0).

Returns from each agent:
- `signal_text` (the one specific finding)
- `signal_source_url`
- `confidence` — `high` | `medium` | `low`
- `no_signal` — boolean (true if all 5 searches yielded nothing usable)
- `personal_details[]` — verbatim quotes for taste-detail reactions (Step 0 Signature Story counts as one of these)

Hard cap: 5 web searches per contact. Agent prompt enforces this.

---

## Step 3 — Spawn email-writer subagents (parallel)

Once all research agents return, spawn `tc-advisor-email-writer` for every contact in a single message.

Pass each agent:
- Contact first name (greeting)
- Agency name + agency type (Aggregator | Advisor Agency | Independent)
- Signal text + signal source URL + confidence (OR `no_signal=true` flag)
- The full `personal_details` array from research (with `verbatim_quote` fields intact) — for Line 1 reaction + wince test
- Verbatim copies of `voice-rules.md` and `pitch-angles.md` (the agent re-reads them but inline pass guarantees fresh state)

Returns from each agent:
- `subject_line` (under 33 characters)
- `email_body` (V7.0 + cold-channel rules — see voice-rules.md §B.1 + §F + §G)

If the agent reports a banned-word violation after its rewrite attempt → log to memory, mark the record with confidence `low` in Airtable, post the offending draft to Slack flagged for manual rewrite.

---

## Step 3.5 — Spawn AI-slop reviewers (parallel, after writers return)

Added 2026-05-12 per Boy's anti-AI-slop skill build. **Soft-mode** review — never blocks the pipeline, always surfaces flags to Slack for Boy's decision.

For each contact whose email-writer returned a draft, spawn `tc-ai-slop-reviewer` via the Agent tool in a single message.

Pass each agent:
- `subject_line` (from writer)
- `email_body` (from writer)
- `channel` = `"cold_advisor_outreach"`
- `verbatim_quote` (from research's `personal_details[0].verbatim_quote` if any — used for the wince test)
- `signature_lines_used` (from writer's output, if reported)

Returns from each reviewer (per `ai-slop-rules.md`):
- `overall_recommendation` — `ship` | `review_optional` | `review_carefully`
- `flags` — array of per-line flags with severity, category, rule cited, offending line, why, and proposed rewrite
- `rhythm_stats` — sentence-length mean / stdev / verdict
- `em_dash_count` + verdict
- `v7_signature_lines_detected`
- `summary` — one-paragraph human-readable read

**The reviewer never blocks.** Even if `overall_recommendation = review_carefully`, the orchestrator proceeds to Step 4 (write to Airtable). The reviewer's flags + rewrites are surfaced to Boy in the Slack post (Step 5) so he can decide whether to edit before sending.

---

## Step 4 — Write back to Airtable

For each contact, update its record in `tblAYeEEElaubtW06`:

| Airtable field | Value |
|---|---|
| Signal | `signal_text` (or empty if `no_signal=true`) |
| Signal Source URL | `signal_source_url` |
| Signal Confidence | `confidence` (or `no signal`) |
| Email Subject | `subject_line` |
| Email Draft | `email_body` |
| Status | `Draft Ready` |

---

## Step 5 — Post Slack review package

One message per wave run (not per contact) to `#ops-updates` (channel ID in `config.json`).

Format:

```
*Advisor Outreach — Wave [X] ready for review*

[For each contact, separated by ━━━━━ lines:]

*[Agency Name]* — [Contact Name] ([Agency Type])
Signal: [signal text] ([source URL]) — confidence: [high|medium|low]
Subject: [subject line]

[email body]

— AI-slop review: [overall_recommendation] · P0:[n] P1:[n] P2:[n]
[If any flags, list them inline:]
  ⚠️ [severity] [category] — [why]
     Line: "[line_text]"
     Suggested rewrite: "[proposed_rewrite]"
[Reviewer summary one-line:]
  [summary]

━━━━━━━━━━━━━━━━━━━━

[End:]
To approve: toggle Status to `Reviewed` in Airtable for the ones you want to send.
If a reviewer flagged something, decide whether to apply the suggested rewrite by editing the Email Draft field directly in Airtable.
Then copy the body, paste into your email client, attach the PDF, send from boy@tommycoconut.com.

Airtable: https://airtable.com/appgvTQA2jmr63R4G/tblAYeEEElaubtW06
PDF: [config.pdf_path]
```

Mention Boy at the end so he sees it.

**Reviewer surfacing rules:**
- If `overall_recommendation = ship` → mention the review verdict but don't expand the flags list (there shouldn't be any).
- If `overall_recommendation = review_optional` → expand only P1 + P2 flags inline.
- If `overall_recommendation = review_carefully` → expand ALL flags inline (P0, P1, P2). Make sure each P0 is visually prominent (use a 🚨 prefix or bold).

---

## Step 6 — Append to memory

Append a run entry to `~/.claude/skills/tommy-advisor-outreach/data/memory.md`:

```markdown
## Run: [YYYY-MM-DD] — Wave [X]

Contacts processed: [count]

Signals:
- [Agency] / [Contact]: [signal] — confidence: [high|medium|low] — source: [URL]
- [Agency] / [Contact]: NO SIGNAL — used fallback hook

Subjects shipped:
- [Agency]: "[subject]"

Banned-word violations after rewrite: [list, or "none"]
```

---

## What this skill does NOT do

- Does not send emails. Boy sends manually from his own client.
- Does not create Gmail drafts. Output is Airtable only.
- Does not auto-detect Slack approval. Boy toggles status in Airtable.
- Does not add contacts to the pipeline. Boy seeds the table manually.
- Does not chase follow-ups. Future iteration.

---

## Fallback behavior

| Situation | Behavior |
|---|---|
| No contacts to process | Post to Slack and stop |
| Research agent finds no signal | Email-writer uses the agency-level hook from `fallback-hooks.md`, confidence = `no signal` in Airtable |
| Banned-word violation after rewrite | Flag in Slack, mark `low` confidence, do NOT block the rest of the wave |
| Airtable write fails | Post the full output to Slack anyway with a "WRITE FAILED" header so Boy can copy manually |
| Slack post fails | Write full output to memory file with a "SLACK POST FAILED" header, surface the error to Boy in the terminal |
| PDF path missing at runtime | Hard abort before any subagent spawns |

---

## Airtable field reference

Base: `appgvTQA2jmr63R4G` · Table: `tblAYeEEElaubtW06` ("Travel Advisor Pipeline")

| Field | ID | Notes |
|-------|-----|-------|
| Agency Name | `fldusGiG4bZMyjeJn` | Primary field |
| Contact Name | `fldk0dd7lnZCVLm3n` | Person receiving the email |
| Role / Title | `fldGdC5DtyScEJY99` | Their job title |
| Agency Type | `fldtRcmkPlqQNyvUD` | Aggregator / Advisor Agency / Independent |
| Website URL | `fld5DLSFW8bybqYhm` | Agency website |
| LinkedIn URL | `fldLGZjTRQXUwy1ee` | Contact's LinkedIn |
| Contact Email | `fldKfGd1DVLy8D5mR` | Direct email if known |
| Specialization | `fldLsQHX342nQioZP` | Caribbean, UHNW, Multi-gen, Luxury Villa |
| Wave | `fldZ6REch6Uiy0CmQ` | Wave 1/2/3/4 |
| Status | `fld8SOPwEDme7z6ia` | Current pipeline stage |
| Signal | `fldAc04dWiFWWvk1Z` | Research hook found |
| Signal Source URL | `fldkp2dbKbGgqrmOS` | Where the signal came from |
| Signal Confidence | `fldYqQoZ3oEGT3VFe` | high / medium / low / no signal |
| Email Subject | `fldQdrWt40iEpxzuY` | Generated subject line |
| Email Draft | `flddEok88t9HGSIGy` | Full email body |
| Date Contacted | `flduGXs4u7VcdQDaY` | When sent |
| Last Reply Date | `fldXLIiwF51PYGLYv` | Most recent reply |
| Commission Tier | `fldYASgPOUFy29gu4` | Standard 10% / Dushi Week 12% / Preferred 15% |
| Notes | `fldooSGdoyv6Yy53U` | Freeform notes / prospector audit trail |
| **Daily Spend ($/person)** | `fldVXpKCelXAPLZH3` | Client spend tier from T+L profile (added 2026-05-13) |
| **Phone** | `fld259CTyu032WVcv` | Direct phone (added 2026-05-13) |
| **Instagram** | `fld3iFOREnVItkY2i` | Instagram profile URL (added 2026-05-13) |
| **T+L Profile URL** | `fldLAOUtyHqig6eOi` | Travel + Leisure A-List profile (added 2026-05-13) |
| **Signature Story** | `fldnPIfjhfkeTq8WI` | Their standout trip / "Epic Escape" from T+L (research seed — see tc-advisor-research.md Step 0) |
| **Source** | `fldybHEzn9cKG8clL` | Where the contact came from (T+L A-List 2026, manual, etc.) |

The bottom 6 fields were added 2026-05-13 when 25 T+L A-List 2026 advisors were loaded into the table. The research agent reads `Signature Story` as a research seed before running web searches — this is the verified personal-taste material already on file.

---

## Configuration (read from config.json)

- `pdf_path` — absolute path to the local advisor PDF
- `send_from` — boy@tommycoconut.com
- `airtable_base_id` — appgvTQA2jmr63R4G
- `airtable_table_id` — tblAYeEEElaubtW06
- `airtable_table_name` — Travel Advisor Pipeline
- `slack_channel_id` — channel for review posts
- `slack_channel_name` — for display only
- `wave_to_agencies` — map of `Wave N` → array of `{name, type, website?}` agencies to prospect

---

# === PROSPECT MODE ===

Use when Boy triggers any of: `prospect Wave [X]`, `prospect contacts for [agency]`, `find contacts for Wave [X]`, `seed Wave [X]`.

This mode discovers candidate contacts at the target agencies and writes them to Airtable in `Status = To Research`. Boy then verifies in Airtable before outreach mode runs.

## Step P1 — Pre-flight checks

1. **Config has agencies for the wave.** If trigger is `prospect Wave X`, look up `config.wave_to_agencies["Wave X"]`. If missing or empty: post to Slack: *"No agencies configured for Wave X. Edit `~/.claude/skills/tommy-advisor-outreach/data/config.json` to add them under `wave_to_agencies`."* and STOP.
2. **Single-agency triggers** (`prospect contacts for Caribbean Journey`): build an ad-hoc agency list with just that one entry. Type/website may be unknown — the prospector handles discovery.
3. **De-dupe check.** Read existing records from `tblAYeEEElaubtW06` with `Agency Name` matching any in the target list. Build a set of `(agency_name, contact_name)` pairs already in Airtable. The prospector results will be filtered against this set before writing.

## Step P2 — Spawn prospect subagents (parallel)

For each agency in the target list, spawn `tc-advisor-prospector` via the Agent tool. **All spawn in a single message — never sequentially.**

Pass each agent:
- `agency_name`
- `agency_type` (Aggregator | Advisor Agency | Independent, if known)
- `wave` (e.g. "Wave 1")
- `website_url` (optional)

Returns from each agent: a single JSON candidate object (see `~/.claude/agents/tc-advisor-prospector.md` for the strict format) — or `no_candidate_found: true` if nothing surfaced.

## Step P3 — Write candidates to Airtable

For each returned candidate where `no_candidate_found` is false AND `(agency_name, contact_name)` is NOT in the dedupe set:

Create a NEW record in `tblAYeEEElaubtW06` with:

| Airtable field | Value |
|---|---|
| Agency Name | `agency_name` |
| Contact Name | `contact_name` |
| Role / Title | `role_title` |
| Agency Type | `agency_type` |
| Website URL | `website_url` |
| LinkedIn URL | `linkedin_url` (mark in Notes if `linkedin_url_predicted=true`) |
| Contact Email | `email` (may be null — leave blank for Boy to fill) |
| Wave | `wave` |
| Status | `To Research` |
| Notes | Auto-generated audit line — see template below |

**Notes field template:**
```
Prospected by Claude on YYYY-MM-DD.
Contact confidence: [high/medium/low]
Email source: [scraped | predicted_pattern | generic_inbox | not_found]
[If predicted] Pattern evidence: [email_pattern_evidence]
[If generic_inbox] Fallback email: [fallback_email]
Source URLs:
- [source_url_1]
- [source_url_2]
Why this contact: [notes from prospector]
```

If a candidate's `(agency_name, contact_name)` IS in the dedupe set, skip the write and add to the "already present" count for the Slack post.

If a prospector returned `no_candidate_found=true`, add to the "no candidate found" list with `what_you_tried` for Boy's visibility.

## Step P4 — Post Slack review

One message per prospect run to `#ops-updates` (channel ID from config).

Format:

```
*Advisor Outreach — Prospect run for Wave [X]*

New candidates written ([N]):

━━━━━━━━━━━━━━━━━━━━

*[Agency Name]* — [Agency Type]
Contact: [Contact Name] ([Role/Title])
LinkedIn: [linkedin_url] [PREDICTED if linkedin_url_predicted]
Email: [email or "BLANK — fill manually"] (source: [email_source], confidence: [email_confidence])
Confidence: [contact_confidence]
Notes: [first line of notes]

━━━━━━━━━━━━━━━━━━━━

[If any duplicates:]
Already present in Airtable, skipped: [list]

[If any no-candidate-found:]
No candidate found for: [list of agency names — what was tried]

NEXT STEPS:
1. Open Airtable: https://airtable.com/appgvTQA2jmr63R4G/tblAYeEEElaubtW06
2. Verify each candidate (right person? right role?)
3. Fill any blank Contact Email cells
4. Trigger: "run advisor outreach for Wave [X]"
```

Mention Boy.

## Step P5 — Append to memory

Append a prospect run entry to `~/.claude/skills/tommy-advisor-outreach/data/memory.md`:

```markdown
## Prospect run: [YYYY-MM-DD] — Wave [X]

Agencies targeted: [list]

Candidates written:
- [Agency] / [Contact] ([Role]) — email source: [source], confidence: [c/m/l]

Skipped (dedupe): [list, or "none"]
No candidate found: [list, or "none"]
```

---

## What prospect mode does NOT do

- Does not draft emails — that's outreach mode.
- Does not research signals — that's outreach mode.
- Does not auto-trigger outreach mode after writing — Boy reviews first.
- Does not validate emails (no Hunter/Apollo integration in v1).
- Does not pick more than ONE candidate per agency — re-trigger for alternates if needed.
