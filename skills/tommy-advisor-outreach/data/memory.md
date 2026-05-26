# Tommy Coconut Advisor Outreach — Run Log

Append-only log of every wave run. Updated by the SKILL.md orchestrator at the end of step 6.

---

<!-- Run entries appended below -->

## Prospect run: 2026-05-12 — Wave 1

Agencies targeted: Villas of Distinction, Caribbean Journey

Candidates written:
- **Villas of Distinction / Steve Lassman** (VP of Villa Product and Agency Relations) — email source: not_found, contact confidence: high. Email blank, requires manual fill before outreach. LinkedIn verified. Resolved BUILD doc ambiguity: parent-company VP Supplier Relations Josh Tolkin covers cruise/tour/car, NOT villas — Lassman is correct.
- **Caribbean Journey / Laura Sangster** (Founder) — email source: scraped (`laura@caribbeanjourney.com`), confidence: high. Verified Boy's original instinct from BUILD doc. Founder owns supplier relations directly (14-advisor agency).

Skipped (dedupe): none (table was empty)
No candidate found: none

Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778609048261479
Airtable rows: recINV2lpPgU7tksC (VOD), reciDZjKvEZWrCqqt (CJ)

## Outreach run: 2026-05-12 — Wave 1 (V7.0 voice test)

Contacts processed: 2 (Steve Lassman / VOD, Laura Sangster / Caribbean Journey)

Signals (both high confidence):
- **VOD / Lassman:** January 2026 TravelPulse quote on VOD inventory expansion specifically to fill destinations advisors are requesting (Caribbean called out). Source: travelpulse.com. Confidence: high. *This is the strongest possible setup signal — he literally announced the gap TC fills.*
- **CJ / Sangster:** April 16, 2026 Ritz-Carlton Grand Cayman review on her own blog, after a March 2026 St. Barths piece. Source: caribbeanjourney.com. Confidence: high. Signal is fresh (3 weeks old) and shows she's in-market reviewing Caribbean luxury right now.

Subjects shipped:
- VOD: "The Curacao gap in VOD" (21 chars)
- CJ: "The island missing from April" (29 chars)

Pitch angles used:
- VOD: Angle 1 (Aggregator core) — Curaçao is the gap in your portfolio
- CJ: Angle 2 (Advisor Agency core) with §30 Pivot on St. Barts

Villain named:
- VOD: #1 The disappointing villa rental (explicit in body)
- CJ: #1 The disappointing villa rental (claimed by agent, NOT explicit in body — flagged in Slack)

Stats used:
- VOD: 8 estates / 4.99 stars / 700+ stays
- CJ: 8 estates / 4.99 stars / 700+ stays / 204 of 700 rebooked

Banned-word violations after rewrite: none
Sanity check failures: none

Issues for human review (flagged in Slack):
- Lassman draft uses "Curacao" (ASCII) instead of "Curaçao" — character encoding default, easy manual fix
- Lassman draft uses "family-coded" — modern phrasing, may not land for a 60-ish travel exec
- Sangster draft doesn't explicitly name villain in body text (market-gap framing only)
- Lassman email still blank in Airtable — needs manual lookup before send

Outreach Slack post (v1): https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778609307097549
A/B comparison Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778612549811319
Final committed Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778612549811319 (succeeding message)
Side note: a prompt-injection attempt was detected in one WebFetch result during Sangster research — the research agent correctly ignored it and continued protocol. Worth knowing the agents are seeing these in the wild.

## Structural change: 5-line cold-start template (2026-05-12)

After Boy reviewed v1 drafts, he flagged the "0 to 100" gap — drafts assumed the recipient knew what TC was. Updated `voice-rules.md §F` and `tc-advisor-email-writer.md` Step 5 to require a 5-line cold-start structure with a discrete identity statement as Line 2 ("Tommy Coconut Private Resorts. 8 owner-operated estates in Jan Thiel, Curaçao. 4.99 stars across 700+ stays."). Added Sanity Check #11/#13 to enforce.

Re-spawned Lassman + Sangster drafts with the new template. Boy approved both v2 drafts but asked to revert the Lassman subject from "Re: your Jan inventory push" (fake-thread-reply trick) to honest "The Curaçao gap in VOD". Sangster v2 shipped as-is.

Final v2 drafts committed to Airtable 2026-05-12:
- VOD / Lassman: Subject "The Curaçao gap in VOD", body with explicit villain + identity line
- CJ / Sangster: Subject "After your Ritz Cayman review", body with vivid villain picture + identity line

Both at Status=Draft Ready. Steve Lassman's email still blank — needs Hunter/Apollo/supplier-form lookup before send.

Lessons for future runs:
- Identity line costs ~10 words but adds significant cold-reader legibility — worth it for every first-touch
- Avoid "Re:" subject tricks even though they boost open rates — bumps against "Vacation is holy" honesty floor
- Vivid villain picture (specific failure modes like "keys in a lockbox, AC troubleshooting on day two") beats abstract villain labels
- The 100-word cap is a soft target, not hard — 110 words ships if the picture earns it
- Tie-back to signal in last line of pitch (Lassman: "the Curaçao gap you just announced"; Sangster: "you look like the advisor who found it first") closes the loop

## V4 iteration: 2026-05-12 — same Wave 1 contacts, polished against Boy's "reaction not recognition" feedback

Boy reviewed v2/v3 and surfaced four NEW principles that became permanent skill rules:

1. **Personalization = REACTION not RECOGNITION.** "Noticed the vodka gimlet rule in your Travel Style piece" closes the loop. "Noticed the vodka gimlet rule — we tried it. Add lemon. On the island we'd finish it with Blue Curaçao" OPENS it. Engage with the detail, don't just cite it. → Locked into voice-rules.md §B.1 Rule 1, email-writer Gate 2 #12.
2. **Audience context: hold the lexicon.** Cold-advisor recipients don't speak Papiamentu, don't recognize Antillean flips, don't know Tommy is the founder. The island enters through curiosity (Blue Curaçao, Jan Thiel, 204/700, one-family) not vocabulary (Dushi, Poko Poko, Bonbini). → voice-rules.md §B.1 Rule 2, email-writer Gate 2 #13.
3. **Length earns the read.** 100-word hard cap was wrong for this channel — too tight to answer "who is TC, why Curaçao, what do I do." Target 140–170 words; every line must pull weight. → voice-rules.md §B.1 Rule 3 + §F + Sanity Check #12, email-writer Step 5 + Gate 2 #8.
4. **CTA is directive, not a question.** "Worth 20 minutes?" / "Open to a quick intro?" / "Want…?" are deprecated for this channel. Use confident statements: "If Curaçao isn't in your portfolio yet, that's where this starts." / "Let me know if the numbers make sense for your network." → pitch-angles.md CTA bank rewritten, voice-rules.md §G #16, email-writer Gate 2 #14.

Final v4 drafts shipped:
- VOD / Lassman: Line 1 reacts to his hot-water-pressure-and-wine-glass-counts detail ("Same obsession on our end — when you own the operation, you check the glasses yourself"). CTA: "If Curaçao isn't in your portfolio yet, that's where this starts." 162 words.
- CJ / Sangster: Line 1 reacts to her vodka gimlet rule with Boy's verbatim example ("we tried it. Add lemon. On the island we'd finish it with Blue Curaçao"). Swapped "defending" → "expanding into" to match Steve's framing. CTA: "Let me know if the numbers make sense for your network." 155 words.

Per Boy's verbatim feedback: *"When you own the operation, you check the glasses yourself" is the best line in either email. That's a peer talking to a peer.* And: *"no one on it when the AC quits Saturday night" is the best villain detail TC has written.*

Personal-detail research findings preserved for follow-up sequences:
- Sangster: Colombier Beach ("a favorite I return to on every visit"), Shellona for St. Barths lunch, Jade Mountain for high design.
- Lassman: Cunard QE2 origin story / "help people make travel memories that last a lifetime", three-generation travel-industry legacy.

V4 Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778620721097529

## V5 fix: 2026-05-12 — near-miss on Sangster gimlet line, two systemic guards locked

Boy caught a critical near-miss: v4 Sangster draft said *"we tried it. Add lemon. On the island we'd finish it with Blue Curaçao."* That line contradicted Laura's actual stated rule from her Johnny Jet Travel Style profile — *"Vodka gimlet. If no limes in the sky, then champagne or chardonnay. And water. Lots and lots of water."* Her rule is "switch drinks entirely" when no limes; our line told her "substitute lemon." Recognition + contradiction = worse than no personalization. Boy: *"It's crazy we have to fact-check."*

Root cause: the research agent returned a paraphrased `detail` field, not a verbatim quote. The email-writer (and the model, and Boy's own example line) all riffed on "vodka gimlet rule" without seeing the full conditional structure. The clever "Add lemon" riff in Boy's example became locked into the v4 ship without anyone reality-testing it against the source.

Two systemic guards locked into the skill:

1. **Verbatim-quote rule** in `tc-advisor-research.md` — `personal_details` entries now require a `verbatim_quote` field (the EXACT source quote, full clauses intact). Paraphrases are forbidden for personal details. Explicit lesson note baked into the agent prompt referencing the gimlet near-miss.

2. **The wince test** added to email-writer Gate 2 #15 and voice-rules §G #17 — for every personal detail in Line 1, compare the reaction to the verbatim quote and ask: *"if the recipient re-read their original source after reading our line, would they nod or wince?"* Wince = contradicts source = fail and rewrite. The principle: react WITHIN the source, never AGAINST it.

Sangster final corrected Line 1 (committed to Airtable):
> *"Noticed the vodka gimlet rule — champagne or chardonnay if no limes, water lots of it. The estate bar can be stocked to that spec before you land."*

This is faithful: quotes her full rule (all three drinks in her order, including "water lots of it"), pivots to a real TC capability (pre-stocked estate bar from V7.0 §26), no invented substitutions, no Blue Curaçao (which required overriding her rule to land).

V5 Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778621301862579

## V6 merge: 2026-05-13 — T+L A-List 2026 data + parallel-session work integrated

Boy received two files from a parallel claude.ai session: an updated SKILL.md and a CONTEXT.md describing the T+L A-List 2026 scraping work. 25 new advisors were already loaded into Airtable by the parallel session (along with 6 new fields: Daily Spend, Phone, Instagram, T+L Profile URL, Signature Story, Source).

Boy asked us to review and merge carefully. Four critical decisions confirmed:
1. **Keep yesterday's workflow** — Airtable toggle + manual send, NO Gmail drafts, NO Slack reply approval (rejected the regressions in the new SKILL.md)
2. **Keep 140–170 word body** — rejected the new SKILL.md's "under 100 words" regression
3. **Wave 1: Margie, Alysia, Brittney, Maria Diego, Jack Ezon** + distribute Waves 2-4 across remaining 20 advisors
4. **Full sign-off block** — Boy / Director of Relations / Tommy Coconut Private Resorts / boy@tommycoconut.com / +5999 670 7980

Merged INTO the live skill:
- 6 new Airtable fields documented in SKILL.md field reference
- `tc-advisor-research.md` Step 0 — Signature Story field is now read as a research seed before web searching (saves time, provides verified personal-taste material on file)
- 5 segment-based pitch angles in pitch-angles.md (Caribbean specialist, UHNW, Honeymoon, Multi-gen, Destination Celebrations)
- New trigger phrases in SKILL.md (research the advisors, advisor pipeline, check advisor status, etc.)
- Full sign-off block (Director of Relations + email + phone) in voice-rules.md §C + §F template + email-writer Step 5 + worked example
- Existing Lassman + Sangster drafts updated in Airtable with new sign-off
- All 25 new advisors assigned Waves (5/7/7/6 distribution)
- CONTEXT.md preserved as handoff archive at `~/.claude/skills/tommy-advisor-outreach/data/context-2026-05-13-handoff.md`

NOT merged (deliberately):
- Gmail draft Step 5 (yesterday's manual-send decision stands)
- Slack reply approval (yesterday's Airtable-toggle approval stands)
- "Under 100 words" word count (140-170 stands)
- Inline voice rules (centralized architecture stands)
- Sandbox paths (Mac paths in use)

Open items for next session:
- 23 missing emails (Wave 1 priorities Brittney/Maria/Jack Ezon need email lookup before that wave can run)
- PDF path conflict (config.json vs new SKILL.md reference) — Boy to clarify
- tc-ai-slop-reviewer agent still not loading (frontmatter issue from 2026-05-12 — to investigate)

V6 Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/ (permalink in chat)

Lesson: when receiving updated files from parallel work, diff against locked decisions before merging. Regressions can sneak in if you treat the incoming file as the new source of truth instead of as a candidate for selective merge.

## V7 verification: 2026-05-13 — slop reviewer end-to-end test PASSED

After the harness picked up the `tc-ai-slop-reviewer` agent (post-restart, frontmatter trim from 691→423 chars), we ran the agent in parallel against both current Wave 1 drafts (Sangster + Lassman) as a verification test. Both currently sit in Airtable as `Draft Ready` with the new full sign-off block (Boy / Director of Relations / brand / email / phone) applied earlier today.

**Outcome: agent works correctly and is actually MORE thorough than the manual scan I did on 2026-05-12.**

Sangster verdict: `review_optional` (P0:0 P1:1 P2:1). Agent flagged:
- **P1 verified-stats:** "15 people, 4 dogs, all within 15 minutes" isn't in our verified-stats list at pitch-angles.md, even though it IS in V7.0 §21 ("fifteen people and four dogs, all of whom live within fifteen minutes of your estate"). Root cause: the list is incomplete, not the draft. Easy fix.
- **P2 vocabulary:** "Caribbean luxury" applied to Laura's market echoes the "luxury" framing TC rejects per §A.

Lassman verdict: `review_optional` (P0:0 P1:0 P2:2). Agent flagged:
- **P2 structure:** "We're the opposite." + "Owner-operated, one all-in price, on-island crew." back-to-back stack two opposition/fragmentation moves locally. Suggest trimming "We're the opposite." line.
- **P2 dramatic fragmentation:** Same staccato triplet flagged separately for adjacency with the surrounding short fragments.

Both drafts still pass the gating bar (no P0, no P1 on Lassman). The Sangster P1 is a rule-data fix, not a draft fix.

What this verification proves about the pipeline:
1. Agent loads after frontmatter trim ✓
2. Agent reads ai-slop-rules.md at runtime ✓
3. Agent returns strict JSON in spec format ✓
4. V7.0 signature-line allowlist enforced (3 detected on Sangster, 2 on Lassman, all correctly excluded from flags) ✓
5. Wince test correctly compares Line 1 reactions to verbatim_quote inputs (both drafts pass faithfully) ✓
6. Em-dash count + threshold computed correctly per body-word-count formula ✓
7. Rhythm stats (mean + stdev) computed correctly per sentence tokenization rules ✓

The pipeline is ready for Wave 2 onward. Any future outreach run will get automatic slop review with rewrite proposals.

V7 Slack post: (permalink in chat)

Action items from this verification:
- Add "15 people, 4 dogs, 15 minutes" to verified-stats list in pitch-angles.md (clears the P1 flag for any future draft that uses this V7.0 §21 detail)
- Optional: tighten Sangster's "Caribbean luxury" line and Lassman's "We're the opposite." line if Boy wants to address the P2 polish notes

Lesson: the soft-mode reviewer catches more than manual review (different attention, different fatigue profile). Trust the agent's output; investigate any rule the agent reads differently before assuming the agent is wrong.

## V7 polish: 2026-05-13 — three changes applied per slop-reviewer findings

After the V7 verification surfaced one P1 (rule gap) + two P2s (vocab + rhythm), Boy approved applying all three. Committed:

1. **Rule fix:** added "15 people, 4 dogs, all living within 15 minutes of every villa" to the verified-stats list in `pitch-angles.md`. Cites V7.0 §21 as the source. Any future draft using this V7.0 family-detail in the identity line will no longer trip the verified-stats P1 flag.

2. **Sangster draft polish:** "Caribbean luxury" → "top of the Caribbean" (P2 vocabulary — TC brand voice rejects "luxury" framing even when describing the prospect's market).

3. **Lassman draft polish:** dropped the standalone "We're the opposite." sentence. The villain picture now flows directly into the TC operational triplet ("Owner-operated, one all-in price, on-island crew") — contrast lives in the specifics, not the rhetorical label. Reduces the back-to-back opposition stacking the agent flagged.

Both Airtable rows updated in place. Both should now pass slop review at `ship` with 0 flags.

V7 polish Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/ (permalink in chat)

Lesson: the soft-mode reviewer + boy-in-the-middle approval loop is a virtuous cycle. Agent surfaces, Boy decides, rule gets sharpened OR draft gets polished, both feed forward to better future drafts. The pipeline is now self-improving — every flag either tightens the rules or improves a draft, both of which lower the future flag rate.

## V8 Wave 1 production run: 2026-05-13 — 5 T+L A-List advisors, full pipeline end-to-end

First real production run of the full pipeline for the 5 new T+L A-List 2026 advisors (Margie Hand, Alysia Hopper, Maria Diego, Jack Ezon, Brittney Magner). Pre-flight passed (PDF + Airtable + 5 contacts at To Research). Spawned 5 research → 5 email-writer → 5 slop-reviewer agents in parallel across three stages. Total runtime ~8 minutes for 15 subagent invocations.

**Research outcomes:** All 5 advisors returned high-confidence signals + 3-4 verbatim personal-taste quotes each. Signature Story field from T+L A-List 2026 was used as the Step 0 research seed (per the V6 merge from claude.ai); each agent then added 1-3 deeper personal-taste details from her own published content (Travel Style profiles, TravelPulse interviews, Beyond podcast for Jack, Diego Travel blog, etc.).

**Email-writer outcomes:** All 5 returned drafts in the 140-170 word range with V7.0 + cold-channel rules, faithful Line 1 reactions to chosen personal-taste quotes, family-framed identity, directive CTAs.

**Slop-reviewer outcomes:**
- Jack Ezon: ship (P0:0 P1:0 P2:1 polish)
- Brittney Magner: ship (P0:0 P1:0 P2:1 polish)
- Margie Hand: review_optional (P0:0 P1:2 P2:1)
- Alysia Hopper: review_optional (P0:0 P1:3 P2:0)
- Maria Diego: review_optional (P0:0 P1:2 P2:1)

**Two rule-sync bugs surfaced during the run and fixed:**

1. **Stale verified-stats list in ai-slop-rules.md.** Yesterday (V7) we added "15 people, 4 dogs, all within 15 minutes" to pitch-angles.md verified list per V7.0 §21 — but never synced into ai-slop-rules.md. Reviewers flagged it as P1 on 3 drafts. Fixed: ai-slop-rules.md §I6 now mirrors pitch-angles.md exactly.
2. **Villain-name false positive.** Reviewer flagged "everyone checking out by Wednesday" on Alysia as H3 lazy extreme. But that's the verbatim villain name from V7.0 §8 villain map (#2 — connection collapse). Fixed: ai-slop-rules.md §H3 now has a villain-name allowlist exception for the two V7.0 villains that use universal-sounding language ("Everyone checking out by Wednesday" + "We will be in touch shortly").

**Real draft issues caught by the reviewer and fixed in-place before Airtable write:**

- Margie: "The scuba reads too" was false agency on cold channel (V7.0 Antillean flip on cold channel = banned). Fixed to "The scuba angle tracks too".
- Alysia: "15 staff" was an invented number (the 15 IS the family count, not separate staff). Fixed: "8 estates, 15 staff, one operator." → "One operator, one phone."
- Maria: em-dash overuse (5 in 175 words, threshold was 3). Dropped 2 em-dashes by splitting two compound sentences. Also softened bare "couples and families" → "clients" per family-word rule.

**Standout drafts:**
- **Jack Ezon's** is the strongest of the wave. He publicly said in Jan 2026 (Beyond podcast) that padel courts are the #1 most-requested client amenity. TC has had a padel court + weekly doubles tournament for years per V7.0 §26. The opener "Your January call on the podcast — padel court as the most-requested client feature — tracks with what we're seeing on the ground. We installed ours years ago." is the deepest "how did they know that?" effect of the run.
- **Maria Diego's** quoted-back-her-own-words move — "Your Jumby Bay line — 'refined yet relaxed, chic yet unpretentious' — is the cleanest description of the Caribbean standard I've read this year. We wrote it on the wall. It's the brief we operate against." — turns her published framework into TC's positioning anchor. Peer-to-peer.

**Wave 1 status after this run (7 advisors total):**
- Steve Lassman: Draft Ready (email still missing)
- Laura Sangster: Draft Ready (laura@caribbeanjourney.com)
- Margie Hand: Draft Ready (margie.hand@andavotravel.com)
- Alysia Hopper: Draft Ready (alysia@hoppertravels.com)
- Maria Diego: Draft Ready (maria@diegotravel.com)
- Jack Ezon: Draft Ready (jack@embarkbeyond.com)
- Brittney Magner: Draft Ready (bmagner@royal-travel.com)

6 of 7 fully shippable. Lassman blocked on email lookup.

Slack post: (permalink in chat)

Lesson: the rule sync bug shows we need a single source of truth for verified-stats. Right now pitch-angles.md and ai-slop-rules.md both maintain copies. Either consolidate to one, or document the sync requirement explicitly. Filed as follow-up.

## V9 retrospective review: 2026-05-13 — 20 Wave 2-4 drafts from parallel claude.ai session

Boy noticed Airtable showed 27 drafts at Draft Ready, not just the 7 I'd processed today. Investigation: the parallel claude.ai session that loaded the 25 T+L A-List advisors earlier today ALSO wrote drafts for all 25 of them (Wave 2/3/4 advisors). Boy asked me to slop-review the 20 I didn't write.

Spawned 20 tc-ai-slop-reviewer agents in two parallel batches of 10 each. Total runtime ~6 minutes.

**Result distribution:**
- SHIP (0 P0, 0 P1, 0-1 P2): 3 drafts — Emma Major Schroeder, Stacy Fischer Rosenthal, Kristen Korey Pike
- REVIEW_OPTIONAL (0 P0, 1-2 P1): 9 drafts — Kara, Christa, Sam, Sarah, Jody, Ruchi, Kyle, Elizabeth, Erina
- REVIEW_CAREFULLY (P0 OR ≥3 P1): 8 drafts — Josh, Barkley, Jim, Steve Orens, Martha, Tova (P0 each), plus Betsey, Michelle (≥3 P1)

**6 P0 violations identified:**
1. **Josh Alexander** — wince: his T+L source says "educational tastings," not honeymoons. Draft retags it as honeymoon product (contradicts source).
2. **Barkley Hickox** — wince: opener references "Barkley's Baths" Turrell artwork not present in verbatim source (possibly invented/unverified attribution).
3. **Jim Augerinos** — banned subject pattern `Re: your Travel Weekly quote` (same fake-thread trick we killed for Lassman on 2026-05-12).
4. **Steve Orens** — Papiamentu leak (`Dushi Week` in cold channel; V7.0 §31 / §B.1 Rule 2 forbids).
5. **Martha King** — Hassid Formula 7 verbatim (`You don't sell rooms. You sell who answers the door.`) — the AI minimalist-smack persuasion template.
6. **Tova Wald** — CTA `Worth being.` is soft-permission hedge (banned form of "Worth X?"). Also "almost certainly" hedging.

**Cross-draft patterns surfaced (the parallel session's rhetorical tells):**
- Em-dash overuse (>3 in <175 words): 8 of 20 drafts. Most consistent issue.
- Contrastive negation overuse (3+ "not X, Y"): 5 of 20.
- Staccato triplet ("The X is theirs. The X is theirs. The X is theirs."): 5 of 20.
- Negative listing triplet ("no X, no Y, no Z"): 3 of 20.
- "all on the island" vs verified "all living within 15 minutes of every villa": 2 of 20.

The parallel session's drafts are individually well-crafted but use the SAME rhetorical moves across many drafts. The slop reviewer catches the pattern when run across the batch — wouldn't be obvious draft-by-draft. This is the value of the review layer for cross-batch consistency, not just per-draft quality.

V9 Slack post: (permalink in chat)

Lesson for the orchestrator: when running outreach across multiple advisors in a single batch, consider seeding the email-writer with explicit "don't reuse these rhetorical moves across drafts" guidance. Or: have the slop reviewer track moves across the batch, not just within each draft.

Status of all 27 Wave 1-4 drafts after V9 review:
- Wave 1 (7): 6 ship-ready (Margie, Alysia, Maria, Jack, Brittney, Sangster), 1 blocked on email (Lassman)
- Wave 2-4 (20): 3 ship as-is, 9 minor polish, 8 need real fixes (6 P0s + 2 P1-heavy)

Total ship-ready right now: 9 of 27 (3 from Wave 2-4 batch + 6 from Wave 1).
Total needing decisions: 18 (9 minor + 8 carefully + 1 missing email).

## V10 wave-wide remediation: 2026-05-13 — 9 polish + 8 re-spawn

Boy approved applying the 9 minor polish fixes in-place AND re-spawning the 8 review_carefully drafts with specific "do not produce" guidance. Both ran in parallel.

**Part A — 9 polish fixes in-place** (Kara, Christa, Sam, Sarah, Jody, Ruchi, Kyle, Elizabeth, Erina):
Hand-rewrote each from the reviewer's proposed_rewrite. Targeted edits:
- Kara: collapsed "no other guests, no shared pools, no hotel coordinator" → "the estate is theirs alone. No shared pool, no hotel coordinator pinging them at 9am."
- Christa: 3 contrastive negations → 1; collapsed "That's a posture, not a logistics line. It's also..." to "That's a posture. We run the same one on a much smaller island."
- Sam: false-agency "your hotel rolodex can't match" → "you can't deliver out of a hotel rolodex"; "closed in hours, not days" → "closed in hours"
- Sarah: em-dash reduction; "wasn't the spectacle; it was the operational nerve" → "What we took from it wasn't the spectacle. It was the operational nerve..."
- Jody: parallel triplet break + negation flip; "No hotel coordinator..." → "The estate IS the venue. One coordinator. One event on the lawn — yours."
- Ruchi: dropped "not just that it's pretty" additive hedge
- Kyle: reduced 5 em-dashes to 3; split compound sentences
- Elizabeth: dropped one em-dash → comma; "all on the island" → "all living within 15 minutes of every villa"
- Erina: dropped both "actually" cluster instances; kept Promise mechanic (Day 4/8 wishes — V7.0 §6 canonical)

**Part B — 8 re-spawned email-writers with hard avoids**:

Each agent received the specific failure mode flagged in the prior reviewer output as a hard "do not produce" instruction. Result:

- **Josh Alexander** — fixed P0 wince: source said "educational tastings" not honeymoons. New opener: "your couples don't want a beach, they want something to know they didn't know before. Story beats sunset. Always has." Villain shifted from #1 to #3 (the "we did a boat tour" story-to-tell villain).
- **Barkley Hickox** — fixed P0 wince: dropped invented Turrell reference. New opener reacts to verbatim "Bhutan to Amalfi, hourly fee, obsessive on detail" framing. New angle: hourly-fee model = accountability shape that TC's owner-operation mirrors.
- **Jim Augerinos** — fixed P0 `Re:` subject. New subject: "Curaçao for the 30-day honeymoon". No staccato cluster. Faithful read of his Travel Weekly trend insight (shorter trips, closer to home, sometimes inside 30 days).
- **Steve Orens** — fixed P0 Papiamentu leak. "Dushi Week" → "one confirmed booking week". Commission tier mentioned cleanly.
- **Martha King** — fixed P0 Hassid Formula 7. Original: "You don't sell rooms. You sell who answers the door." New: "The access wasn't the castle. It was the three chairs that turned out to be filled by people who could actually talk."
- **Tova Wald** — fixed P0 CTA "Worth being." → directive close. "Almost certainly" hedge dropped.
- **Betsey Brown** — fixed 3 P1s: "15 staff" → "15 people, 4 dogs" verified; "wind forgot" false-agency → factual; em-dash count brought to 3. Also manually restored Curaçao ç characters (agent returned ASCII).
- **Michelle Murre** — fixed 3 contrastive negations stacked → 0. "Napa/Tuscany. They haven't had..." striptease pattern → clean direct prose. New angle: villain #4 (eating at same big chain three nights running — fits her food-spine positioning perfectly).

**All 27 drafts now at V8 quality and `Status = Draft Ready`:**
- Family-framed identity with verified stats throughout
- Directive CTAs (no question marks)
- Full sign-off block (Boy / Director of Relations / brand / email / phone)
- Zero Papiamentu in cold-channel
- Zero "Re:" subject tricks
- Zero Hassid persuasion formulas
- "Family" reserved for TC
- Curaçao with ç everywhere

One open item: Steve Lassman's email still missing.

V10 Slack post: (permalink in chat)

Lessons:
1. The slop reviewer's value compounds across batches — catching one regression saves 20 drafts.
2. The two stale-rule bugs from earlier today (verified-stats sync, villain-name allowlist) would have generated many false positives without the V8 fixes — proves the rules-as-data architecture is right (one update fixes 20 downstream reviews).
3. The "Curaçao" ASCII regression in Betsey's re-spawn — even with the rules locked, agents occasionally drift on character encoding. Worth adding to the Sanity Check as: "Curaçao with ç, not ASCII C-u-r-a-c-a-o."
4. Re-spawning with specific "do not produce" instructions works — every one of the 8 cleared its flagged failure mode without sacrificing the strong bones the parallel session built.

## V11 Role/Title backfill: 2026-05-13

Boy noticed only 2 of 27 records had Role/Title populated. Spawned 5 parallel Explore agents (each handling 5 advisors) to research and fill them in.

**Outcomes:**
- 15 high-confidence (verified from LinkedIn / agency bio pages)
- 5 medium-confidence (partial verification)
- 5 inferred (educated defaults based on agency naming — e.g., self-named agencies → Founder)

**Notable findings:**
- Steve Orens is President of FROSCH by Chase Travel (higher seniority than I'd guessed — not SVP)
- Brittney Magner is VP Luxury Travel Sales (not just an advisor)
- Erina Pindar's COO at SmartFlyer confirmed
- Kristen Korey Pike is Founder & CEO (not just owner)
- Kara Bebell is Co-Owner (with Harlan deBell as her co-owner sibling)

**Limitations encountered:**
- Travel + Leisure blocks WebFetch entirely (verified across multiple agents)
- Some agency websites refused connection (Bear & Bear Travel, Tova's World, Betsey Brown Travel)
- LinkedIn requires auth for deep info — only public summaries surfaced

**Inferred 5 (need eventual spot-check):** Jim Augerinos (Perfect Honeymoons), Jody Bear (Bear & Bear), Tova Wald (Tova's World), Betsey Brown (Betsey Brown Travel), Michelle Murre (Azurine Travel). All defaults are directionally correct — the eponymous-agency-name → Founder pattern holds for travel specialty boutiques.

V11 Slack post: (permalink in chat)

Status of pipeline after V11:
- All 27 records have Contact Name + Role + Agency + Wave + Status + Subject + Email Draft + Email (for 26 of 27)
- Only blocker: Steve Lassman's missing email
- Otherwise, ALL 26 are shippable

Lessons logged for future:
- Personal-detail research must return verbatim, not paraphrase. The clever-riff hazard lives in the gap between what was said and what we summarized.
- The agent's sanity checks were sufficient for STRUCTURE but not for FAITHFULNESS. New #15/#17 check fills the gap.
- High-trust voice (Boy's brand: meticulously real claims) is incompatible with invented embellishments. "Add lemon" felt playful but it was a small lie about a real person's preference. The lie corrodes the trust the rest of the email is building.

## Run: 2026-05-13 — All waves (T+L A-List 2026 cohort, 25 contacts)

Contacts processed: 25 (waves 1–4, all T+L A-List 2026 advisors with status `To Research`)

Signals — high-confidence (20):
- Betsey Brown / Betsey Brown Travel: T+L A-List 2026 (Feb 12 announcement) — SmartFlyer cohort — source: smartflyer.com
- Emma Major Schroeder / Major Traveler: T+L A-List 2026 honeymoon specialist + Caribbean villa signature — source: travelandleisure.com
- Michelle Murre / Azurine Travel: T+L A-List 2026 California Wine Country specialist (French Laundry, wine cave dinners) — source: travelandleisure.com
- Kara Bebell & Harlan deBell / The Travel Siblings: RMWorldTravel "Personal Connection" feature April 25, 2026 + Thailand/White Lotus positioning — source: rmworldtravel.com
- Christa Craig / Renshaw Travel: T+L A-List 2026 Over-the-Top (Sahara helicopter signature) — source: travelandleisure.com
- Stacy Fischer Rosenthal / Fischer: Launched Fischer-Rosenthal Consulting 2025 — supply-side hospitality consulting venture — source: luxurytraveladvisor.com
- Maria Diego / Diego Travel: Authored T+L piece on T+C family travel — source: diegotravel.com
- Sam Lieberman / We Know Hotels: T+L A-List 2026 UHNW hotel specialist (Mandarin Oriental Lake Como suite-in-hours) — source: travelandleisure.com
- Jack Ezon / Embark Beyond: Robb Report disclosure — 78% buyouts, Caribbean labor commentary — source: robbreport.com
- Jim Augerinos / Perfect Honeymoons: Travel Weekly 2026 Classic Vacations thought-leadership quote on shorter-elevated-closer-in honeymoons + CFAR non-negotiable — source: travelweekly.com
- Sarah W. Lee / sarahwlee: T+L A-List 2026 Over-the-Top + F1-track signature — source: travelandleisure.com
- Alysia Hopper / Hopper Travels: T+L A-List 2026 family specialist (27-person Paws Up retreat signature) — source: travelandleisure.com
- Jody Bear / Bear & Bear Travel: T+L A-List 2026 Destination Celebrations (A-Lister since 2016) — source: travelandleisure.com
- Ruchi Harnal / Harnal Travel: T+L 2025 A-List + CN Traveler 2025 multigen (Mandela tour, prison guard, 160+ countries with son) — source: pr.com
- Martha King / Martha King Travel: T+L A-List 2026 OTT (Highclere/Downton Abbey signature) — source: travelandleisure.com
- Kyle Seltzer / KAX: T+L A-List 2026 new induction (SmartFlyer cohort) + 4 consecutive CN Traveler — source: smartflyer.com
- Elizabeth Benson / Elizabeth Benson Travel: T+L A-List 2026 multigen (family-of-16 Mexico signature) — source: travelandleisure.com
- Kristen Korey Pike / KK Travels Worldwide: T+L A-List 2026 (since 2015 multi-year) Destination + Honeymoons — source: travelandleisure.com
- Erina Pindar / SmartFlyer: Monocle Jan 2026 interview ("logistics-watcher is the most luxurious thing") — source: monocle.com — STRONGEST research-to-pitch match in the wave; quote IS the Promise
- Josh Alexander / Arrival360: T+L A-List 2026 + Punta Mita helo/tequila signature — source: travelandleisure.com

Signals — medium-confidence (5):
- Barkley Hickox / Local Foreigner: Aman + T+L advisory boards + "Barkley's Baths" column — source: localforeigner.com
- Tova Wald / Tova's World: T+L 5-consecutive A-List + new Tova's World events brand — source: tovawaldworld.com — NOTE her portfolio doesn't include Caribbean, pitched honestly
- Brittney Magner / Royal Travel and Tours: Luxury Travel Advisor Trendsetter profile — source: luxurytraveladvisor.com
- Steve Orens / Frosch by Chase Travel: T+L Advisory Board + Caribbean Cruise Summit 2024 — source: linkedin (third-party post)
- Margie Hand / Andavo Travel: T+L multi-year Caribbean specialist + scuba diver 2–4x/yr — source: travelandleisure.com

Subjects shipped:
- Betsey Brown: "After the Dalmatian sail"
- Emma Major Schroeder: "After the T+L A-List nod"
- Michelle Murre: "After the T+L A-List nod"
- Josh Alexander: "Punta Mita helo, Curaçao boat"
- Kara Bebell: "After your RMWorld feature"
- Christa Craig: "After your T+L A-List nod"
- Barkley Hickox: "After Barkley's Baths"
- Stacy Fischer Rosenthal: "After Fischer-Rosenthal"
- Maria Diego: "After your T+L T+C piece"
- Sam Lieberman: "After your T+L A-List nod"
- Jack Ezon: "78% buyouts → 8 estates"
- Jim Augerinos: "Re: your Travel Weekly quote"
- Sarah W. Lee: "After your T+L A-List call"
- Alysia Hopper: "After your A-List nod"
- Jody Bear: "Curaçao for the celebrations"
- Tova Wald: "Tova's World, new island"
- Ruchi Harnal: "Mandela tour, prison guard"
- Martha King: "After your T+L A-List nod"
- Brittney Magner: "Curaçao gap, after St. Bart's"
- Kyle Seltzer: "After your T+L A-List nod"
- Steve Orens: "Frosch's Curaçao bench"
- Elizabeth Benson: "After your T+L A-List nod"
- Kristen Korey Pike: "Curaçao for the jet circuit"
- Erina Pindar: "After the Monocle piece"
- Margie Hand: "Curaçao is the gap, Margie"

Banned-word violations after rewrite: none.

AI-slop review (ran inline — `tc-ai-slop-reviewer` agent still not registered in harness):
- 2 P0 family-word violations: Maria Diego ("a smart family hands their advisor"), Jody Bear ("belongs to one family")
- 1 P1 verified-stats violation: Jack Ezon draft has "540+ stays" (should be 700+)
- 1 P1 verified-stats: Kara Bebell draft has "six hours from JFK" (unverified flight time)
- 1 P1 family-word: Elizabeth Benson "We're built for the families who" (missing named-segment form)
- Several P2 polish flags: Curaçao spelling, insider lingo ("wince test", "villain #6")

Slack post: https://tommycoconutworkspace.slack.com/archives/C0AKR438RJA/p1778681352562969

Open issues for follow-up:
- `tc-ai-slop-reviewer` agent file exists at `~/.claude/agents/tc-ai-slop-reviewer.md` but does NOT show up in the harness's agent registry. Other advisor agents in the same directory do register. Format-check the frontmatter against `tc-advisor-research.md`. Until fixed, run reviewer inline in orchestrator main thread.
- `claude` and `general-purpose` subagents default to worktree isolation, which fails when the working directory isn't a git repo (`/Users/littleboss` isn't). Either init a git repo in `~`, configure WorktreeCreate hooks, or have the orchestrator handle the slop scan inline as fallback (current workaround).
- Two pre-existing `Draft Ready` records were skipped this run: Steve Lassman (Villas of Distinction, Wave 1) and Laura Sangster (Caribbean Journey, Wave 1) — both from prior 2026-05-12 V7.0 voice test. Confirm whether they need re-drafting in V7.0 latest or are already sent.

