# Dushi Week Output Guide — Text (Markdown)

The Dushi Week itinerary is delivered as **one clean Markdown text document**. No HTML, no PDF, no DOCX, no photos, no Cloudinary. This file is about making that text read beautifully.

> **Why text-only.** The old pipeline produced HTML + PDF + DOCX with Cloudinary hero photos, a photo picker, crop iteration, and font embedding. It consumed the most time, focus, and tokens for the least guest value, and every photo swap meant regenerating files. Retired. The guest value is the *plan and the words* — put all the energy there. (Brand colors, font embedding, WeasyPrint, the `docx` generator — all gone.)

---

## The one rule that replaces the old "three-file sync"

There is only one file. Edit it, save it, deliver it. No copy-to-workspace, no regenerate-PDF, no fix-the-DOCX-script step. When the user requests a change, change the Markdown and you're done.

---

## Document structure

Same section order as before (see SKILL.md "The Structure of a Dushi Week Itinerary"), now as Markdown headings instead of styled pages:

```
# DUSHI WEEK™ — [Crew Name]          ← cover block (names, dates, villa, "Vacation is holy. ◆")
## The Tommy Coconut Philosophy
## A Letter for [First Names]          ← the personal letter
## Your Week at a Glance               ← table
## Day 1 — [Weekday, Date] — [TITLE]
...
## Day 8 — [Weekday, Date] — [TITLE]
## Good to Know
## Your Crew
## Closing
```

Keep it scannable. Someone should be able to skim the headings and know the shape of their week.

---

## Day-block format

Each day is one `##` section. Inside it:

```
## Day 3 — Saturday, June 19 — THE BLUE DAY

▸ **Cruise Intel:** 2 ships, ~4,800 pax. Popular west-coast beaches will fill by mid-morning,
so today is Sea Aquarium + Mambo Boulevard — the boulevard thrives on the buzz.

**9:00 AM — Slow start.** Coffee on the deck. Nobody is keeping score.
**10:30 AM — Sea Aquarium.** Touch tanks are toddler heaven... [GF options at lunch — let the server know.]
**1:00 PM — Nap window.** (Young families: sacred. ~90 min.)
...

**Culinary Pass Dinner 2 of 5 — Mei Mei** ($35/person → $105 for the three of you). *meimeicuracao.com*

› **Pro tip:** Put the kids' swimwear on top of the suitcase the night before.
› **Not feeling it?** Pool day. Caracasbaai is 500m away and nobody knows about it.

**What's happening at Jan Thiel today:** ...
**What's happening in Curaçao today:** ...
**What's happening at Tommy Coconut today:** ...
```

Conventions:
- **Time entries**: `**7:00 AM — Title.** Description.` Bold the time + title so the day scans vertically.
- **Cruise intel**: lead the day with a `▸` line. Always ship count + pax + what it means.
- **Pro tips / alt options**: short `›` labelled lines, not big callout boxes.
- **The three info boxes** (Jan Thiel / Curaçao / Tommy Coconut today): bold-label lines near the bottom of the day. Mandatory — see lessons-learned.md Section 7.
- **Dietary flags**: write `[GF]` or a short inline note, and ALWAYS put the action on the guest ("let the server know") — never claim TC "handled" it (lessons-learned.md Section 2).
- **Culinary Pass markers**: "Dinner X of 5" with the per-group price. (Two-coconut all-inclusive builds use "Dinner X of 7" and NO $35/credit language — lessons-learned.md Section 3.)
- **Website URLs**: italic, where available.

---

## Week at a Glance — table

```
| Day | Highlight | Dinner | Vibe |
|---|---|---|---|
| 1 — Thu | Land & breathe | Villa Vis (in) | Arrival |
| 2 — Fri | Boat day w/ Captain Mike | Date Night at the House | Ocean |
| ... | ... | ... | ... |
```

---

## Voice carries everything

With no photos and no styling, the writing is the entire experience. Load the `tommy-coconut-voice` skill and write Stage 3 (Relationship register). Sign the letter `**T**`. Use ◆ on cover, philosophy, letter, and closing. One Papiamentu word per section. (Voice rules: lessons-learned.md Section 9.)

---

## File naming

```
Dushi-Week-[CrewName].md
```

Example: `Dushi-Week-Wyand-Cartel.md`. One file. That's it.

---

## Delivery checklist

Before handing the file over:
1. Read every section top to bottom — does it flow like a letter, not a printout?
2. Guest names spelled correctly throughout.
3. All dates and weekdays correct (verify weekdays against a real calendar — lessons-learned.md Section 12).
4. Flight numbers/times match what the user gave (never invent one).
5. Dietary allergies flagged at every restaurant mention — action on the guest, never "handled."
6. Culinary Pass numbering correct (1 of 5 … 5 of 5) and per-group price shown.
7. **Every new / third-party activity ran through the Operator Research Protocol** (SKILL.md) — operator verified with sources, user-approved; nothing invented.
8. Save with the proper filename. No photos, no other formats to generate.
