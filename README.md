# Claude Toolkit

Personal Claude Code workflow — templates and skills that make new projects move from idea to deployed-app in hours instead of weeks.

This repo is version-controlled because:

- **Backup** — laptop dies, your workflow doesn't
- **Multi-machine sync** — work laptop, home Mac, future cloud workstation, all use the same toolkit
- **Iteration** — every refinement to a skill or template is tracked. You can see what worked, roll back what didn't
- **Sharing** — invite collaborators when a workflow is worth sharing

## Structure

```
claude-toolkit/
├── install.sh                          ← one-shot machine setup
├── templates/
│   └── claude-project-starter/         ← symlinked → ~/Templates/claude-project-starter
│       ├── README.md
│       ├── init-prompt.md
│       └── docs/                       ← 8 doc skeletons for new projects
└── skills/
    └── scope-project/                  ← symlinked → ~/.claude/skills/scope-project
        └── SKILL.md
```

## Install (any machine)

```bash
git clone git@github.com:hairy-coconut/claude-toolkit.git ~/Code/claude-toolkit
cd ~/Code/claude-toolkit
./install.sh
```

The install script creates symlinks so Claude Code finds the skill at `~/.claude/skills/scope-project/` and the templates at `~/Templates/claude-project-starter/`. Once installed, every `git pull` updates everything live.

## Usage

In any Claude Code session in a fresh directory:

```bash
mkdir ~/Desktop/<new-project>
cd ~/Desktop/<new-project>
claude
```

Then say "scope a new project" or type `/scope-project`. The skill walks you through 10 scoping questions, fills in 8 spec docs, and stops — no code until you reply `approved`.

## Iterating

When you find yourself wishing the skill asked a different question, or one of the templates had a section it doesn't have:

```bash
cd ~/Code/claude-toolkit
# edit whatever needs changing — the symlinks mean the edit is live immediately
git add -A && git commit -m "what you changed" && git push
```

On every other machine: `git pull`. Done.

## Adding a new skill

```bash
mkdir skills/<new-skill-name>
# write skills/<new-skill-name>/SKILL.md with frontmatter (name, description) + body
./install.sh         # creates the symlink at ~/.claude/skills/<new-skill-name>/
git add -A && git commit -m "Add <new-skill-name> skill" && git push
```

## What's NOT in this repo

- API keys / secrets → keep in `~/Templates/.shared-secrets.env` (gitignored)
- Project-specific code → goes in its own repo (e.g., `dushi-lingo`)
- Machine-specific config (Claude settings, shell rc) → out of scope, use a dotfiles repo if you want one
