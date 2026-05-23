# TODO project name — Design System

<!-- For headless/CLI projects, this covers brand voice and output formatting:
     - How does CLI output look? Colors? Banners? Quiet mode?
     - What tone does the system use in user-facing strings, errors, emails?
     - Repurpose the "Color System" and "Typography" sections accordingly. -->

## 1. Brand Foundation

*Three mood words. North star sentence.*

**Design North Star**: *e.g., "Every screen should feel like ___ — never plastic or 'app-y'."*

---

## 2. Color System

### Core Palette

| Token | Hex | Use |
|---|---|---|
| `--TODO-primary` | TODO | Primary CTAs, accents |
| `--TODO-text` | TODO | Primary text, dark surfaces |
| `--TODO-bg` | TODO | Page background |

### Functional Colors

| Token | Hex | Use |
|---|---|---|
| `--success` | TODO | Confirmations, correct states |
| `--error` | TODO | Errors, destructive actions |
| `--neutral-100` | TODO | Card background |
| `--neutral-600` | TODO | Secondary text |

---

## 3. Typography

```css
--font-display: TODO;   /* headings, hero */
--font-body:    TODO;   /* UI, body */
```

| Role | Font | Size | Weight | Line Height |
|---|---|---|---|---|
| Display | TODO | TODO | TODO | TODO |
| H1 | TODO | TODO | TODO | TODO |
| Body | TODO | TODO | TODO | TODO |

---

## 4. Spacing & Layout

Base unit: **TODO px**. Scale: TODO.

Container widths: max content width TODO. Page padding TODO.

Border radius scale: `sm` TODO · `md` TODO · `lg` TODO · `xl` TODO · `full` 9999px.

---

## 5. Component Specifications

*Per-component blocks. Include background, border, text, padding, hover/active/disabled states, animation duration. Concrete enough that Claude can implement without ambiguity.*

### Primary Button
```
Background:  TODO
Text:        TODO
Border-radius: TODO
Padding:     TODO
Hover:       TODO
Active:      TODO
Disabled:    TODO
```

### TODO another component
*Repeat.*

---

## 6. Motion

**Principle**: *purposeful micro-animations only. Celebrate real events. Never decorate.*

| Event | Animation |
|---|---|
| TODO | TODO duration + easing |

---

## 7. Voice & Tone

*For user-facing copy: tone words, what to avoid, sample lines. Especially important for emails, empty states, error messages, marketing surfaces.*

- **Tone**: TODO three words
- **Avoid**: TODO patterns (jargon, exclamation marks, hedging, etc.)
- **Example**: *Empty state — "TODO line"*

---

## 8. Do's and Don'ts

### Do
- TODO
- TODO
- TODO

### Don't
- TODO
- TODO
- TODO
