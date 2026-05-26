# TC Advisor Outreach — Context Handoff Archive
### Imported 2026-05-13 from claude.ai session
### Source-of-record for the T+L A-List 2026 advisor loading work

This file is preserved as an archive of context that came in from a parallel Claude session that handled the T+L A-List 2026 scraping and Airtable load. **Live skill rules are in `~/.claude/skills/tommy-advisor-outreach/` and `~/.claude/agents/` — read those, not this.**

This document is for traceability: when someone asks "where did the 25 advisors come from" or "what's the Signature Story field for," this answers it.

---

## What was done in the parallel session

1. **Source identified:** T+L A-List 2026 (`travelandleisure.com/a-list/a-list-travel-advisors`) is publicly scrapeable via Apify. Each advisor profile contains name, agency, specialty, email (Cloudflare-encoded but decodable), phone, website, Instagram, and a "Signature Story" / "Epic Escape" / "Top Trip" field.

2. **25 advisors scraped and loaded** into `appgvTQA2jmr63R4G` / `tblAYeEEElaubtW06` ("Travel Advisor Pipeline"). All marked `Status = To Research`. 6 new fields added to the table to hold the T+L data: Daily Spend ($/person), Phone, Instagram, T+L Profile URL, Signature Story, Source.

3. **Emails decoded for 2 of 25:** Margie Hand (margie.hand@andavotravel.com), Alysia Hopper (alysia@hoppertravels.com). Remaining 23 need a second Apify RAG-browser pass or Hunter.io lookup.

4. **Apify actors recommended for future scraping:**
   - `apify/rag-web-browser` — fetches + decodes Cloudflare-protected emails on individual profile pages
   - `apify/website-content-crawler` — batch scrapes multiple URLs at once

5. **Notes for future scraping batches:**
   - Virtuoso's directory blocks scraping — don't try
   - Condé Nast Traveler Top Specialists list — publicly scrapeable, good Caribbean coverage, ~200 more advisors available
   - Agency websites (Brownell, SmartFlyer, Protravel) — most have public advisor directories

---

## Email approach (validated in the parallel session)

The parallel session converged on the same principles we'd already locked in this Mac-Mini session:

- **Personalization = reaction, not recognition** ✓ (matches our voice-rules.md §B.1 Rule 1)
- **No Papiamentu / no Antillean flips on cold advisor channel** ✓ (matches §B.1 Rule 2)
- **Sign-off: "Vacation is holy." (no emoji, no variant)** ✓
- **The island enters through curiosity, not vocabulary** ✓
- **Villain: the Lockbox Rental** — *"Not a villa rental with keys in a lockbox and no one on it when the AC quits Saturday night."* ✓
- **CTA: directive, never asks permission** ✓ (matches §G #16)
- **"Expanding into" not "defending"** ✓ (locked in our v4 ship)

**Two reference emails from the parallel session** matched (modulo wording variations) what we shipped locally for Steve Lassman and Laura Sangster on 2026-05-12. Final approved versions live in the Airtable Email Draft field for those two records.

---

## Bigger picture (long-term goal)

- **Short term:** 2–3 T+L A-List advisors reply and agree to a call
- **Medium term:** First FAM trip — 6–8 advisors visit Curaçao on TC's tab, Boy hosts, Magic Mike on the boat, Brisa Do Mar dinner, hour with Ray over rum
- **Long term:** 15–25% of TC bookings sourced through travel advisors; Virtuoso preferred supplier application

The FAM trip is the real closer. The emails open the door.

---

## What was MERGED into the live skill (2026-05-13)

Imported into the Mac skill:
- The 25 advisors are now in Airtable with Waves assigned (5/7/7/6 split across Waves 1–4)
- The 6 new Airtable fields documented in SKILL.md field reference
- Signature Story used as a research seed (tc-advisor-research.md Step 0)
- Segment-based pitch angles for the five segments (Caribbean specialist, UHNW, Honeymoon, Multi-gen, Destination Celebrations) added to pitch-angles.md
- Sign-off block expanded to full block: Boy / Director of Relations / Tommy Coconut Private Resorts / boy@tommycoconut.com / +5999 670 7980
- New trigger phrases added to SKILL.md

NOT imported (deliberately — yesterday's decisions stand):
- ❌ Gmail draft creation as Step 5 (Boy chose manual send via Airtable copy/paste)
- ❌ Slack reply-based approval ("approve [name]") — Boy chose Airtable status toggle
- ❌ "Under 100 words" body length — we kept 140–170 ("length earns the read")
- ❌ Inline voice rules in SKILL.md — kept centralized in voice-rules.md / pitch-angles.md / ai-slop-rules.md
- ❌ Sandbox paths (`/mnt/skills/user/...`, `/mnt/user-data/outputs/...`) — replaced with real Mac paths

---

*Last touched: 2026-05-13*
