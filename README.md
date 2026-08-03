# ⚠️ Archived — moved into `tommy-os`

**This repo is archived and read-only.** Tommy Coconut's Claude Code skills now live
in the main **`tommy-os`** monorepo, which is the single source of truth for skills too:

- Skills: **`tommy-os/.claude/skills/`** · Project templates: **`tommy-os/.claude/templates/`**
- Working inside `tommy-os`: skills are auto-discovered — nothing to install.
- Global use (outside the repo): run **`scripts/install-claude-skills.sh`** from your `tommy-os` checkout.

See **`tommy-os/.claude/skills/README.md`**. Migrated in **TOS-727**. The legacy
`dushi-week-start.yml` clone workflow was retired (the itinerary clone now runs
in-process in TypeScript inside the portal).

---

# Tommy Coconut — Claude Toolkit

Shared Claude Code workflow for the TC team. Skills, templates, and SOPs for building Dushi Week itineraries and microsites — consistently, regardless of who's doing the build.

This repo is the single source of truth. Everyone clones the same repo, runs the same install, gets the same skills. One pull keeps everyone in sync.

---

## What's in here

```
claude-toolkit/
├── install.sh                                  ← one-shot machine setup (run once per machine)
├── templates/
│   └── claude-project-starter/                 ← doc skeletons for new projects
└── skills/
    ├── dushi-week-builder/                     ← builds the printable Dushi Week itinerary
    │   └── references/
    │       ├── lessons-learned.md              ← read this first, every time
    │       ├── island-database.md              ← restaurants, beaches, crew bios, cruise logic
    │       └── itinerary-standard-sat-to-sat--couple.html
    ├── dushi-week-microsite-from-itinerary/    ← turns the itinerary into a live microsite
    ├── dushi-week-microsite/                   ← architecture reference for the microsite codebase
    ├── dushi-week-microsite-two-coconut/       ← variant: two-coconut (booked guest) flow
    ├── tommy-coconut-voice/                    ← Tommy's voice bible + writing rules
    ├── tommy-advisor-outreach/                 ← cold email pipeline for travel advisors
    └── scope-project/                          ← new-project scoping skill
```

---

## Install (new machine — do this once)

```bash
# 1. Clone the repo
git clone git@github.com:TommyCoconutIT/claude-toolkit.git ~/Code/claude-toolkit

# 2. Run the installer (creates symlinks into ~/.claude/skills/)
cd ~/Code/claude-toolkit
./install.sh

# 3. Install Claude Code if you haven't already
# → https://claude.ai/code  (desktop app, free to install)
```

After install, every `git pull` updates your skills automatically — no re-running the installer.

---

## Staying in sync

```bash
cd ~/Code/claude-toolkit
git pull
```

That's it. The symlinks mean the updated files are live immediately in your next Claude session.

---

## Building a Dushi Week (the short version)

Full SOP is at `skills/dushi-week-builder/references/handoff-sop.md`. The short version:

1. Get the guest info from the Pipeline record in Airtable
2. Open Claude Code in any directory → type `/dushi-week-builder`
3. **Boy reviews + approves the itinerary before you go further** ← hard gate
4. Type `/dushi-week-microsite-from-itinerary` → Claude builds the microsite code
5. Open a PR to `TommyCoconutIT/tommy-os` → **Boy reviews + merges** ← hard gate
6. Wait for Vercel to go green → update Airtable → hand the WhatsApp message to Boy

---

## Two repos — know the difference

| Repo | What it is | Who touches it |
|---|---|---|
| `TommyCoconutIT/claude-toolkit` | The skills and SOPs. This repo. | Everyone on the TC team |
| `TommyCoconutIT/tommy-os` | The website codebase. The microsite code lives here. | TC tech team |

Skills drive what Claude does. The output (TypeScript files) goes into `tommy-os`.

---

## Updating a skill

When something needs to change (a lesson learned, a voice rule update, a new restaurant in the database):

```bash
# Edit the file directly — changes are live immediately via symlinks
cd ~/Code/claude-toolkit
# edit skills/<skill-name>/SKILL.md or references/*.md
git add -A
git commit -m "describe what changed and why"
git push
```

Everyone on the team gets the update on their next `git pull`. **Do not edit skills only on your local machine** — it breaks consistency for everyone else.

---

## Adding a new skill

```bash
mkdir skills/<new-skill-name>
# write skills/<new-skill-name>/SKILL.md
./install.sh   # creates the symlink
git add -A && git commit -m "Add <new-skill-name> skill" && git push
```

---

## What's NOT in this repo

- API keys / secrets → keep in `~/Templates/.shared-secrets.env` (gitignored everywhere)
- Project-specific code → goes in `tommy-os` or its own repo
- Machine-specific Claude settings → `~/.claude/settings.local.json` (gitignored)
