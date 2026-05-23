# TODO project name — Routes

<!-- For CLIs, replace "URL Tree" with "Commands" and list invocations + flags.
     For ops automation, replace with "Triggers & Actions" — what fires the workflow, what it does.
     For API services, this is your endpoint contract. -->

## URL Tree

```
/                            → TODO
├── TODO                     → TODO
└── TODO
    └── TODO
```

---

## Route Details

### `/TODO` — TODO purpose
- **Auth**: *Public / Required / Admin*
- **Component / handler**: `TODO file path`
- **Data fetched**: *List the service-layer calls.*
- **Sections / behaviour**: *What does the user see / what happens.*
- **Side effects**: *Redirects, revalidation, writes.*

---

### `/TODO/[param]` — TODO purpose
*Repeat the pattern. Keep each entry short — bullet lists beat paragraphs.*

---

## Middleware
*What's protected, what's public, where redirects happen.*

```typescript
// TODO summarise the matcher + auth check
```

---

## Server Actions / Endpoints

### `TODO action name`
```
Input:   TODO shape (zod schema)
Output:  TODO result type
Auth:    TODO (requireAuth() first line?)
Effects:
  1. TODO write 1
  2. TODO write 2
  3. revalidate TODO paths
```

*Repeat per action. Every mutation should be listed here, not buried in code.*

---

## Navigation Structure
*How the user moves through the app. The nav bar, the back arrows, the empty-state CTAs.*
