# Claude Project Starter

A reusable scaffold for shipping fast with Claude Code. Born from the Dushi Lingo build (zero code → deployed app in one session) — the insight is that **decisions made before you open Claude are 10× more valuable than decisions made during.**

This folder gives you:

- 8 doc-skeleton files that capture every decision worth making up front
- Two equivalent entry points: a Claude Cowork **skill** (`scope-project`) or a paste-based **init prompt**
- A hard rule that no code gets written until you've read and approved the docs

## The workflow

### Option A — Skill invocation (recommended)

```bash
mkdir -p ~/Desktop/<new-project>
cd ~/Desktop/<new-project>
claude
```

In Claude, type `/scope-project` (or say "scope a new project", "I want to start a new build", etc.). The skill at `~/.claude/skills/scope-project/SKILL.md` will:

1. Copy the 8 doc skeletons into the current dir
2. Ask 10 scoping questions, one at a time
3. Restate the project in 5 bullets and confirm with you
4. Fill in all 8 docs
5. Post the approval gate and STOP

When you're happy with the docs, reply with `approved` and the phase to start with. **Then** Claude writes code.

### Option B — Paste-based fallback

If the skill isn't available (fresh machine, different Claude install, etc.):

```bash
mkdir -p ~/Desktop/<new-project>
cp -r ~/Templates/claude-project-starter/docs/* ~/Desktop/<new-project>/
cd ~/Desktop/<new-project>
claude
```

Then paste the entire contents of `~/Templates/claude-project-starter/init-prompt.md` as your first message. Same workflow from there.

## What's in this folder

| File | Purpose |
|---|---|
| `README.md` | This file — workflow explainer |
| `init-prompt.md` | The script you paste into Claude to start scoping |
| `docs/CLAUDE.md` | Project rules, tech stack, gotchas, what NOT to do |
| `docs/ARCHITECTURE.md` | Layered design, data flow, architectural rules |
| `docs/SCHEMA.md` | Data model (DB tables / state shapes / API contracts) |
| `docs/ROUTES.md` | URL tree / CLI commands / API endpoints |
| `docs/DESIGN.md` | Brand tokens, components, motion, voice |
| `docs/CONTENT.md` | Seed content (delete if not content-heavy) |
| `docs/PROJECT_STATUS.md` | Phased checklists, decisions log |
| `docs/README.md` | Per-project setup README |

## Project-type guidance

The skeletons are stack-agnostic. They work for web apps, CLIs, ops automation, internal tools — anything.

Some skeletons have header comments noting when to delete or repurpose them:

- **`CONTENT.md`** — delete unless your app has seed content (lessons, catalog, courses, marketing copy)
- **`SCHEMA.md`** — repurpose as "state shapes" if you have no database
- **`ROUTES.md`** — repurpose as "Commands" for CLIs, or "Triggers & Actions" for ops automation
- **`DESIGN.md`** — covers brand voice + output formatting even for headless tools

## Why this works

You're not paying Claude to think for you. You're paying Claude to be a fast, careful, indefatigable executor. The bottleneck is decisions — what stack, what schema, what flow, what NOT to build. Make those decisions yourself, write them down, hand them over.

Eight markdown files cost you 30 minutes up front and save you 10 hours of back-and-forth.

## Future improvements

- ✅ ~~Promote `init-prompt.md` to a Claude Cowork skill~~ — done. Lives at `~/.claude/skills/scope-project/SKILL.md`.
- Add a `~/Templates/.shared-secrets.env` file (gitignored everywhere) for global API keys you reuse across projects
- Add a `stack-presets/` folder with pre-filled CLAUDE.md/ARCHITECTURE.md skeletons for your most common stacks (Next.js+Supabase, FastAPI+Postgres, Hono+D1, etc.)
- Once you've used the skill on 3+ projects, refine the questions based on what kept needing follow-ups
