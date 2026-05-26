# AI-Slop Rules — Cold Advisor Outreach Channel

Source of truth for the `tc-ai-slop-reviewer` agent. Also read by `tc-advisor-email-writer` at generation time so drafts try to avoid slop in the first place.

Distilled from four open-source frameworks (Stop Slop / Hardik Pandya; Avoid AI Writing / Conor Bronsdon; Hassid's "Ban"; Blake Stockton's "Don't Write Like AI") + TC's existing voice-rules. Banlist is the union of all four; severity is TC-tuned for cold advisor outreach.

**Channel scope:** these rules apply to **cold advisor outreach** specifically. Other TC channels (WhatsApp, social, long-form) have looser rules — Antillean flips and Tommy lexicon are core voice on warm channels, slop on cold ones.

---

## Severity tiers

| Tier | What it means | Reviewer behavior |
|---|---|---|
| **P0** | Always-fix. These are tells that ALWAYS scream AI. Single occurrence = flag. | Surfaces in Slack as a critical flag with rewrite. Per Boy's "soft" mode, never auto-rewrites — just flags strongly. |
| **P1** | Fix-before-send. Strong AI signal but context-dependent. | Surfaces in Slack with rewrite suggestion. Boy decides. |
| **P2** | Polish. Minor signals; flag for awareness. | Surfaces in Slack as optional polish notes. |

Reviewer's `overall_recommendation` is computed from flag counts:
- Any P0 → `review_carefully` (most important to address)
- ≥3 P1 → `review_carefully`
- 1–2 P1 + any P2 → `review_optional`
- 0 P0 / 0 P1 → `ship`

---

## V7.0 signature-line allowlist (DO NOT FLAG)

These constructions are deliberate TC brand voice. The reviewer must NOT flag them as AI tells, even though they technically match contrastive-negation / staccato-fragmentation / binary-contrast patterns.

Allowed (verbatim or near-verbatim):
- *"We don't sell bedrooms. We sell belonging."*
- *"You arrive as strangers. You leave as family."*
- *"They come tired. They leave knowing."*
- *"That's not marketing. That's the receipt."*
- *"I didn't say it. The guests said it."*
- *"The bank has never sent the wire."*
- *"Vacation is holy."* / *"Vacation is holy. We protect yours."*
- *"Three options. Most people only know about two."*
- The Three Options frame: *"Not the hotel, not the rental, the Private Resort."* (negative listing in service of the brand frame)

**Rule:** these phrases or close paraphrases (≥80% structural match) appearing ONCE in a draft are allowed. If they appear more than once, flag the duplicates as P2 polish.

**Pattern overuse threshold:** even with the allowlist, the same STRUCTURAL pattern (contrastive negation, binary contrast, staccato fragmentation) appearing **3+ times** in a single body is P1 — that's pattern overuse regardless of which exact phrases are used.

---

## Section A — Vocabulary banlist

### Tier 1 (P0 — single occurrence flags)

Already in TC voice-rules.md §A (TC-specific):
- nestled, pampered, tranquil, exclusive, unwind, indulge, curated, world-class, bespoke, opulent, prestigious
- fine dining experience, once-in-a-lifetime, unforgettable experience, paradise found, escape to
- Dear Valued Guest, journey, luxury vacation rental, All-inclusive resort, concierge

**ADD (open-source frameworks — same severity):**
- delve, tapestry, realm, paradigm, embark, beacon, testament to
- robust, comprehensive, cutting-edge, pivotal, seamless, watershed moment, game-changer
- leverage, utilize, harness (as verb)
- intricate, ever-evolving, enduring, daunting, holistic, actionable, impactful, learnings
- thought leader, best practices, synergy, interplay
- vibrant, thriving, bustling (esp. in tourism/luxury context)

### Tier 2 (P1 — flag in clusters of 2+ in same body)

Single occurrence may be okay if the surrounding context earns it. Two or more in the same body = AI pattern. Common promotional-AI words:

- harness, foster, elevate, unleash, streamline, empower, bolster, spearhead
- resonate, revolutionize, facilitate, underpin, nuanced, crucial, multifaceted
- ecosystem, myriad, plethora, encompass, catalyze, reimagine, galvanize, augment
- cultivate, illuminate, elucidate, juxtapose, transformative, cornerstone
- paramount, poised, burgeoning, nascent, quintessential, overarching, underpinning

### Tier 3 (P2 — flag by density > 3% of body)

Single occurrence fine, multiple instances signal AI:
- significant, innovative, effective, dynamic, scalable, compelling
- unprecedented, exceptional, remarkable, sophisticated, instrumental
- state-of-the-art

### Copula-avoidance verbs (P1)

AI's habit of giving verbs to inanimate things to sound more "literary":
- features, boasts, presents, showcases, serves as, represents
- "Our resort *features* 8 estates" → "We *have* 8 estates"
- "Curaçao *boasts* world-class beaches" → "Curaçao *has* beaches" (or skip the line — "world-class" is also banned)

### Adverb banlist (P1 in clusters)

All -ly intensifiers in cold B2B are P1 flags. Single use OK if it earns its weight, clusters are slop:
- really, just, literally, genuinely, honestly, simply, actually
- deeply, truly, fundamentally, inherently, inevitably
- interestingly, importantly, crucially, frankly

---

## Section B — Structural patterns

### B1. Contrastive negation (P1 if overused)

Pattern: *"It's not X, it's Y"* / *"Not X, but Y"* / *"The answer isn't X. It's Y."*

- **1 occurrence:** allowed (especially if it matches the V7.0 allowlist)
- **2 occurrences:** P2 polish flag
- **3+ occurrences:** P1 — pattern overuse
- Plus: *"It's not just X but also Y"* (additive hedge) is P1 always — different structure, lazier framing

### B2. Binary contrast / triple reveal (P1)

- Binary: *"Stop X. Start Y."* (Hassid formula 3) — P1
- Triple reveal: *"It's not X. It's not Y. It's Z."* (Hassid formula 4) — P0 — pure AI persuasion template

### B3. False agency (P1 on cold channel)

Inanimate things doing human verbs. Note: ALLOWED on warm/WhatsApp channel (V7.0 §12 Antillean flips), banned on cold advisor.

Examples:
- *"The decision emerges"* / *"The culture shifts"*
- *"The villa speaks for itself"* / *"The view captures you"*
- *"The data tells us"* / *"The market rewards"*

Fix: name the human actor.

### B4. Negative listing / rhetorical striptease (P1 if not in allowlist)

Pattern: *"Not a X… Not a Y… A Z."*

V7.0 Three Options frame is allowed (*"Not the hotel, not the rental, the Private Resort."*). Other negative lists → P1.

### B5. Dramatic fragmentation (P2 if overused)

*"[Noun]. That's it."* / *"[Noun]. Period."* / *"X. And Y. And Z."*

V7.0 Frank Lammers DNA uses staccato (*"They come tired. They leave knowing."*) — allowed in moderation. Threshold: ≥3 fragmented constructions in body = P1 overuse.

### B6. Em-dash overuse (P1 if over threshold)

TC voice uses em-dashes intentionally (V7.0 §C — em-dashes flip objects into agents). On cold advisor channel:

- **Threshold:** 1 em-dash per 50 words of body. So a 150-word body allows up to 3 em-dashes. A 200-word body allows up to 4.
- **Over threshold:** P1 flag.
- **8+ em-dashes in a single body:** P0 (AI rhythm signature).

---

## Section C — Hassid's 7 AI persuasion formulas (all P0 unless on V7.0 allowlist)

These are AI's default templates when asked to write persuasive copy. Each is a P0 flag if it appears:

1. **Drama setup:** *"In a world where [change], [virtue] becomes [currency]"*
2. **Status split:** *"Most people [lazy thing]. The few who win [disciplined thing]"*
3. **Binary switch:** *"Stop [old]. Start [new]"*
4. **Triple reveal:** *"It's not X. It's not Y. It's Z."*
5. **FOMO threat:** *"If you're not doing X, you're already behind"*
6. **Hidden truth:** *"The real work isn't [visible]. It's [invisible]"*
7. **Minimalist smack:** *"You don't need more X. You need Y"*

---

## Section D — Throat-clearing & meta-commentary (P0)

Always-flag (these are pure delay-the-actual-point patterns):

- *"Here's the thing,"* / *"Here's what,"* / *"It turns out,"* / *"The truth is,"*
- *"Let me be clear,"* / *"I'll be honest,"* / *"To be candid,"*
- *"Let's explore,"* / *"Let's take a look,"* / *"Let's break this down,"* / *"Let's dive in"*
- *"In this email, I'll …"* / *"What I want to share is …"*
- *"Hint:"* / *"Plot twist:"* / *"Spoiler:"*
- *"In a nutshell,"* / *"At the end of the day,"* / *"When all is said and done,"*

---

## Section E — Hedging & vague proof (P1)

- **Vague declaratives:** *"The reasons are structural,"* *"The implications are significant,"* *"The stakes are high"* — without naming the specifics. Name the thing or cut the line.
- **Vague attribution:** *"Studies show,"* *"Experts believe,"* *"Many in the industry agree"* — cite a specific source or strike it.
- **Hedging:** *"Perhaps,"* *"could potentially,"* *"may,"* *"might,"* *"tends to,"* *"often,"* *"sometimes,"* *"to a certain extent"*
- **Hollow intensifiers:** *"genuinely,"* *"truly,"* *"quite frankly,"* *"let's be clear,"* *"it's worth noting that"*

---

## Section F — Chatbot artifacts (P0 — always strip)

- *"Certainly!"* / *"Absolutely!"* / *"Great question!"* / *"I hope this helps!"*
- *"Feel free to reach out"* / *"Don't hesitate to"* (already banned in voice-rules §A)
- *"As an AI"* / *"As of my last update"* / *"I don't have access to"* (cutoff disclaimers)
- *"Step 1:" / "Let me think step by step"* / *"Breaking this down"* (reasoning-chain artifacts)
- *"In this section, we'll …"* / *"Let me walk you through …"* / *"As we'll see"*

---

## Section G — Rhythm tells (statistical)

### G1. Sentence-length uniformity (P1)

AI defaults to 15–25 words per sentence with low variance. Humans vary wildly.

Compute: mean and stdev of sentence-word-counts across the body.
- **Mean 15–25 AND stdev < 5:** flag as P1 — too uniform.
- **Mean 15–25 AND stdev 5–10:** P2 — borderline.
- **Mean outside 15–25 OR stdev > 10:** OK.

Target for TC cold-advisor: mix 3–8 word sentences with 20+ word sentences. Fragments and one-word "lines" count as their own sentences for this calculation.

### G2. Synonym cycling (P1)

AI rotates synonyms to avoid repeats. Humans repeat the clearest word.

Example flag: in the same paragraph, *"advisors,"* *"travel professionals,"* *"agents,"* *"specialists,"* *"practitioners."* If 3+ synonyms for the same referent appear in one paragraph → P1.

### G3. Paragraph length uniformity (P2)

Every paragraph the same length signals over-polish. Vary deliberately; include a 1-sentence paragraph somewhere.

---

## Section H — Proof & authority tells

### H1. Notability name-dropping (P1)

Stacking prestige references: *"as covered by The New York Times, BBC, FT, and The Hindu."* Use one with context, not four in a row.

### H2. Emotional flatline (P1)

*"What surprised me most was,"* *"I was fascinated to discover,"* *"What struck me was"* — announcing the emotion rather than showing it in the content.

### H3. Lazy extremes (P1)

*"everyone,"* *"nobody,"* *"always,"* *"never,"* *"every advisor knows,"* *"no client ever wants"* — sweeping universals as false authority. Replace with specifics.

**Exception (V7.0 villain-name allowlist):** the V7.0 §8 Villain Map names eight villains verbatim, and two use universal-sounding language as part of their canonical phrasing:
- *"Everyone checking out by Wednesday"* (villain #2 — connection collapse)
- *"We will be in touch shortly"* (villain #5 — trust)

When these appear verbatim or near-verbatim AS the villain-naming move in a draft, they are NOT lazy extremes — they are the brand's named villain. Do NOT flag. (Added 2026-05-13 after Wave 1 production run surfaced this false positive.)

### H4. Novelty inflation (P2)

*"a concept nobody's naming,"* *"the insight everyone's missing,"* *"what nobody tells you about."* Describe what was DONE with the concept, not that we discovered it.

---

## Section I — TC-specific brand-safety checks

### I1. Wince test (P0 — from voice-rules §G #17)

For every personal detail referenced in Line 1: compare the reaction to the `verbatim_quote` from research. Ask: *would the recipient nod or wince if they re-read their source?* Wince = the reaction contradicts the source. Always P0.

### I2. Identity-line check (P0 — from voice-rules §G #13)

Line 2 must include "Tommy Coconut Private Resorts" + geo anchor (Curaçao or Jan Thiel) + one verified stat. Missing → P0.

### I3. CTA-not-a-question (P0 — from voice-rules §G #16)

Final body line must not end in `?`. Must not ask permission. P0 if it does.

### I4. Family-word rule (P0 — from voice-rules §B)

The word "family" appears only in reference to Tommy Coconut, never to the advisor's pre-stay clients. *"the families you send"* → P0 rewrite to *"the couples / friends groups / families with kids you send"*.

### I5. No Papiamentu / no Antillean flips (P0 — from voice-rules §B.1 Rule 2)

Cold advisor channel only. *"Dushi,"* *"Poko Poko,"* *"Bonbini,"* *"the rum opened itself,"* *"I know where your house sleeps"* → P0 strip.

### I6. Verified-stats only (P1)

Any numeric claim must come from the verified list in `pitch-angles.md`:
- 4.99★ / top 1% rated in the world
- 700+ stays
- 204 of 700 booked again before they left
- 8 estates / Jan Thiel, Curaçao
- **15 people, 4 dogs, all living within 15 minutes of every villa** (per V7.0 §21 — the TC family count. Added 2026-05-13.)
- 7 years operating
- 65% occupancy cap by design
- $37,000 Bayside Hill (or $28,950 with 25% Summer Savings)

Invented numbers → P1. **"15 staff" is NOT verified** — the 15 is the family count, not a separate staff number. "X advisors" referring to the PROSPECT's network (e.g. "your 14 advisors") is allowed when the count came from their own published bio.

---

## Output format the reviewer must return

```json
{
  "overall_recommendation": "ship | review_optional | review_carefully",
  "p0_count": 0,
  "p1_count": 2,
  "p2_count": 1,
  "flags": [
    {
      "severity": "P0 | P1 | P2",
      "category": "vocabulary | structure | formula | throat-clearing | hedging | chatbot-artifact | false-agency | rhythm | proof | wince | identity | cta | family | lexicon | verified-stats",
      "rule_cited": "Section/subsection reference, e.g. 'Section A Tier 1' or 'Section C Formula 4 (triple reveal)'",
      "line_text": "the exact line from the draft containing the offense",
      "offense": "the specific word/phrase/pattern triggering the flag",
      "why": "one-sentence explanation",
      "proposed_rewrite": "the rewrite suggestion (preserve voice, address the specific offense)"
    }
  ],
  "rhythm_stats": {
    "sentence_count": 12,
    "mean_words_per_sentence": 14.5,
    "stdev_words_per_sentence": 7.2,
    "verdict": "varied_enough | borderline | too_uniform"
  },
  "em_dash_count": 3,
  "em_dash_threshold": 3,
  "em_dash_verdict": "ok | overuse",
  "v7_signature_lines_detected": ["the specific allowlisted phrases that appeared, if any"],
  "summary": "one-paragraph plain-English summary of what's strong and what's slop in the draft"
}
```

---

*Last updated: 2026-05-12 — locked alongside the tc-ai-slop-reviewer agent build.*
