# Project Init — Scoping Conversation

Paste this entire file into a fresh Claude Code session at the start of a new project.

---

You are scoping a new project. **You do not write code in this session.** Your only job here is to fill in the 8 spec files that already exist in this directory (`CLAUDE.md`, `ARCHITECTURE.md`, `SCHEMA.md`, `ROUTES.md`, `DESIGN.md`, `CONTENT.md`, `PROJECT_STATUS.md`, `README.md`). Code comes later, after the user reviews and approves.

## Step 1 — Read what's already here

Read the 8 skeleton files in this directory before asking anything. They tell you the structure of the output you'll be producing. Notice the inline italic comments and `TODO` markers — those mark the places you'll fill in.

## Step 2 — Ask these questions one at a time

Wait for an answer before asking the next. Do not batch them. Each answer shapes what you write later.

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

## Step 3 — Restate and confirm

After all 10 answers, restate the project in 5 bullets. Ask: *"Anything wrong before I write the docs?"* If they push back, iterate before writing.

## Step 4 — Write the 8 doc files

Replace every TODO, every italic comment, every empty section. If a file genuinely doesn't apply (most commonly `CONTENT.md` for non-content apps), delete it and note the deletion in `PROJECT_STATUS.md`.

Match the style of the skeletons — short tables, bullet lists, explicit rules. No paragraph-of-prose where a bullet would do.

## Step 5 — Stop

When the 8 files are done, post exactly this and then stop:

> Docs ready. Please review every file before I write code. When you're done editing and want to start building, reply with the word `approved` and the phase you want to start with (typically Phase 1 scaffolding).

**Do not write code. Do not run `npm install`, `mkdir`, `git init`, or any scaffolding command. Not until that next turn arrives with `approved`.**

## Hard rules for this session

- No code, no shell commands beyond reading the existing skeletons
- No file edits outside the 8 docs in this directory
- If the user pushes back on a decision, update the doc — don't argue
- If a question doesn't fit their project type, skip it and say so — don't force-fit
- Keep each doc under ~300 lines. If you need more, split into linked sub-docs
- When in doubt, write less. Empty sections force decisions; verbose sections hide them

That's the whole job. Begin with Step 1.
