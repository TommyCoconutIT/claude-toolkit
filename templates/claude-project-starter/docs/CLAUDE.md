# Claude Code Instructions — TODO project name

## Project Identity
**TODO project name** — *one-sentence pitch. Who is this for? What's the wedge?*

## Critical Context

### Developer Profile
- **Developer**: TODO name
- **Experience level**: *senior / mid / new to this stack — affects how much hand-holding Claude should do*
- **Communication preference**: *concise (skip basic explanations) / verbose / show-me-options*
- **Autonomous mode behavior**: *when running unattended, skip commentary — scaffold, implement, validate with `<build command>`, done*

### Tech Stack
*Fill in the table — match exact versions. Be specific.*

| Layer | Choice |
|---|---|
| Language | TODO |
| Framework | TODO |
| Data layer | TODO |
| Auth | TODO |
| Styling / UI | TODO |
| Deployment | TODO |

### Project Placement
*Where does this code live? Standalone repo? Monorepo? What does the surrounding directory look like?*

---

## Architecture Patterns
See [ARCHITECTURE.md](./ARCHITECTURE.md) for the system design. Key rules summarised here:

1. **TODO architectural rule 1** — *e.g., "Service layer only — no DB calls in components"*
2. **TODO architectural rule 2**
3. **TODO architectural rule 3**
4. *...add 3–5 more, project-specific*

---

## What NOT to do

*Every project has 3–5 things Claude must never do. Write them down. Examples from past projects:*
- *Never call the DB directly from a component — always go through `src/lib/db/`*
- *Never hardcode hex values — use design tokens*
- *Never use `any` types*
- *Never write to a shared mutable global*

TODO list yours here.

---

## Key Files Quick Reference
*Populate this after scaffolding. Update it as the project grows.*

| File | Purpose |
|---|---|
| TODO | TODO |

---

**Last Updated**: TODO date — initial planning
