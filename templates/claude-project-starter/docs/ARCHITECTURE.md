# TODO project name — Architecture

## 1. High-Level Goal
*One paragraph. What this is, who it's for, what it replaces, what makes it different.*

---

## 2. Tech Stack

| Layer | Choice |
|---|---|
| TODO | TODO |

*Match the table in `CLAUDE.md`. This is the canonical version — link other docs to here.*

---

## 3. App Structure

*Directory tree. Annotate each folder with one-line purpose. Example:*

```
TODO/
└── src/
    ├── TODO/             ← TODO purpose
    ├── TODO/             ← TODO purpose
    └── TODO/             ← TODO purpose
```

---

## 4. Data Model

See [SCHEMA.md](./SCHEMA.md) for the full schema.

### Logical Layers
*Group entities into layers — what's "content" (seeded, rarely changes) vs "user" (mutated as the app runs) vs "system" (computed/cached).*

- **TODO layer** — TODO entities
- **TODO layer** — TODO entities

### Core Relationships
*ASCII diagram or list. The 1:M and M:M edges between entities.*

```
TODO ──────── TODO (1:M)
```

---

## 5. Core User Flow

*The spine of the product. 5–8 steps end-to-end.*

```
TODO → TODO → TODO → TODO
```

---

## 6. Authentication
*Provider, session strategy, where `userId` comes from, how protected routes work.*

---

## 7. Caching Strategy

| Data | Cache TTL | Revalidation |
|---|---|---|
| TODO | TODO | TODO |

*Read-heavy public data: long TTL. User-specific data: short TTL + revalidate on mutation. Be explicit.*

---

## 8. Architectural Rules

*The non-negotiables. These are what makes the codebase coherent. Every rule should be enforceable in code, not just docs.*

1. **TODO rule** — *what it means, why it matters*
2. **TODO rule**
3. **TODO rule**
4. *...continue. Aim for 6–8 rules.*

---

## 9. Build Phases

See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for the live status. High level:

- **Phase 1 (MVP):** *one-line summary*
- **Phase 2 (post-MVP):** *one-line summary*
- **Phase 3 (production-grade):** *one-line summary — usually empty until Phase 1 lands*
