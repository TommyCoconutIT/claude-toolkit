# TODO project name — Schema

<!-- For non-DB projects, repurpose this file to document in-memory state shapes, API contracts, or file formats. The structure still applies: define entities, their fields, their relationships. -->

**Source of truth**: TODO — *e.g., `src/db/schema.ts` (Drizzle), or `prisma/schema.prisma`, or this file itself*

---

## Tables / Entities

### `TODO entity name`
*One-line purpose.*

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | TODO | PK | TODO |
| TODO | TODO | TODO | TODO |

**Access rules**: *RLS policy, who can read/write, what's public.*

---

### `TODO another entity`
*Repeat the pattern. Keep entities small — fewer than 10 columns each is a healthy bias.*

---

## Relationships

```
TODO ──────── TODO (1:M)
TODO ──────── TODO (M:M via TODO join table)
```

---

## Indexes

*List the non-default indexes and why each exists. Indexes are decisions, not afterthoughts.*

- `TODO` on `(col_a, col_b)` — for the `TODO query` lookup
- *...*

---

## Generated Types

*Where do TypeScript / generated types live? `src/db/schema.ts` exports them? `prisma generate`? Hand-written `types/`? Be explicit.*

---

## Migration Strategy

*How are schema changes made? `drizzle-kit generate`, `prisma migrate dev`, hand-rolled SQL, Supabase SQL Editor? When are migrations applied to staging vs prod?*
