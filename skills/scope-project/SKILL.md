---
name: scope-project
description: Scope a new project from scratch by walking the user through 10 structured questions, then filling in the 8 doc skeletons in ~/Templates/claude-project-starter/ before any code is written. Use whenever the user says "scope a new project", "start a new project", "I want to build something new", "kick off a new build", "new project setup", "scope this", "let's start a new app", or any variation indicating they want to begin a new project from zero. The skill enforces a hard "no code until approved" gate so the docs become the spec before scaffolding begins.
---

# Scope New Project

End-to-end project scoping. You do NOT write code in this skill — your only job is to copy the 8 doc skeletons into the current working directory, walk the user through 10 scoping questions, fill in the docs based on their answers, and STOP. Code only happens after the user types `approved` in the next turn.

---

## Hard rules for this skill

1. **No code, no scaffolding, no `npm install`, no `git init`, no `mkdir` beyond what Step 1 below allows.** Not until the user types `approved` after reviewing the docs.
2. **No file edits outside the 8 docs you copied into the working directory.**
3. **If the user pushes back on a decision, update the doc — don't argue.**
4. **If a question doesn't fit their project type, skip it and say so — don't force-fit.**
5. **Keep each doc under ~300 lines.** If you need more, split into linked sub-docs.
6. **When in doubt, write less.** Empty sections force decisions; verbose sections hide them.

---

## Step 1 — Confirm working directory and copy skeletons

Before anything else, verify the current working directory is the intended new project root. Ask:

> Confirm the working directory: is this the right place to scope the new project? Current dir: `<pwd output>`. Reply with yes, or tell me where to scope.

If wrong dir, ask the user to `cd` and re-invoke. If correct, run this exact sequence using the Bash tool:

```bash
# Copy the 8 doc skeletons into the current working directory
cp -n ~/Templates/claude-project-starter/docs/*.md .
ls -la *.md
```

The `-n` flag means "don't overwrite if file already exists" — if the user already has a `README.md`, leave it alone and warn them.

Confirm to the user that the skeletons are in place. List which files were created. If any conflicts (existing files not overwritten), tell them which.

---

## Step 2 — Read the skeletons

Read each of the 8 files using the Read tool so you know the structure of the output you'll be producing:
- `CLAUDE.md`
- `ARCHITECTURE.md`
- `SCHEMA.md`
- `ROUTES.md`
- `DESIGN.md`
- `CONTENT.md`
- `PROJECT_STATUS.md`
- `README.md`

Notice the inline italic comments and `TODO` markers — those mark every place that needs filling in.

---

## Step 3 — Ask these 10 questions one at a time

**Wait for the user to answer each question before asking the next.** Do not batch them. Each answer shapes what you write later.

1. **Project name and one-sentence pitch.** What is this, who is it for, what's the wedge?
2. **Project type.** Web app / mobile / CLI / ops automation / internal dashboard / API service / other?
3. **Stack.** Language, framework, hosting target. If they're unsure, suggest 2 sensible options based on type and ask which.
4. **Data layer.** Database (which one)? Airtable? Files? In-memory only? Where does state live, and what's the durability requirement?
5. **Auth model.** Single user / multi-user / public read / SSO / API keys? If multi-user, which provider?
6. **Core user journey.** Walk through what one user does, end to end, in 5–8 steps. This becomes the spine of `ARCHITECTURE.md`.
7. **Data entities.** What "things" exist in this system? (e.g., users, lessons, orders, alerts.) Just names + a one-line purpose for each.
8. **Brand and design.** Inherit tokens from an existing brand? Build new? Pick 3 mood words.
9. **MVP scope.** What MUST ship in v1? What's explicitly Phase 2? Force a cut — the answer is never "everything."
10. **Deploy target and dev URL.** Where does this run in prod? What port for `npm run dev`?

If a question genuinely doesn't apply (e.g., asking about styling tokens for a CLI), say so and skip it. Don't waste their time.

---

## Step 4 — Restate and confirm

After all 10 answers, restate the project in exactly 5 bullets:

```
**Project:** TODO name — TODO pitch
**Type / stack:** TODO
**Data + auth:** TODO
**Core flow:** TODO
**MVP cut:** TODO (Phase 2 parks: TODO)
```

Ask: **"Anything wrong before I write the docs?"**

If they push back, iterate. Re-confirm. Do NOT write to disk until they're happy with the restatement.

---

## Step 5 — Write the 8 doc files

Replace every `TODO`, every italic comment, every empty section across all 8 files. Use the Edit tool for each file — don't rewrite from scratch, fill in the placeholders.

Special handling:
- **`CONTENT.md`** — if the project is not content-heavy (no seed lessons / catalog / marketing copy), delete the file with the Bash tool and add a line to `PROJECT_STATUS.md`'s Technical Decisions Log noting the deletion.
- **`SCHEMA.md`** — if no database, repurpose to document in-memory state shapes, API contracts, or file formats.
- **`ROUTES.md`** — for CLIs, retitle "URL Tree" to "Commands"; for ops automation, retitle to "Triggers & Actions".
- **`DESIGN.md`** — even for headless tools, this covers brand voice and output formatting. Keep it.

Match the style of the skeletons — short tables, bullet lists, explicit rules. No paragraph-of-prose where a bullet would do.

---

## Step 6 — Post the approval gate and stop

When all 8 files are filled in, post exactly this message and then STOP:

> Docs ready. Please review every file before I write code:
>
> - `CLAUDE.md`
> - `ARCHITECTURE.md`
> - `SCHEMA.md`
> - `ROUTES.md`
> - `DESIGN.md`
> - `CONTENT.md` *(or note: deleted, not applicable)*
> - `PROJECT_STATUS.md`
> - `README.md`
>
> When you're done editing and want to start building, reply with the word `approved` and the phase you want to start with (typically Phase 1 scaffolding).

**Do not write code. Do not run `npm install`, `mkdir`, `git init`, or any scaffolding command. Not until that next turn arrives with `approved`.**

---

## Failure modes to avoid

- **Don't paraphrase the questions.** They're tuned. Ask them verbatim.
- **Don't start the questions before Step 1's copy succeeds.** If the cp fails, fix that first.
- **Don't fill in CLAUDE.md halfway and skip to ARCHITECTURE.md.** Finish each file before moving to the next. The skeletons cross-reference each other — partial fills get inconsistent.
- **Don't write code "just to be helpful" while waiting for the user's answer to question 3.** The whole point of this skill is the gate.
- **Don't skip Step 4 (restate and confirm).** Catching a misunderstanding at restatement is 30 seconds; catching it after writing 8 docs is 30 minutes.
- **If the user says "skip the questions, just write the docs based on what I said"** — politely refuse. The questions are the value. Suggest they can answer the questions briefly if they're short on time.

---

## Why this skill exists

Decisions made before you open Claude are 10× more valuable than decisions made during. The 8 docs are not paperwork — they're the spec, the memory, and the shared reference point that survives every context window reset. Filling them in is the most leveraged 30 minutes in the whole project.

The hard "approved" gate is what turns a freestyle build into an executed-against-a-spec build. Keep it.
