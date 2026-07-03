> Last updated: 2026-07-03 · Module version: 0.1

# UI/UX Quick Reference

Pairs with `data/ui-ux/colors.csv` (20 palettes), `data/ui-ux/typography.csv` (13 pairings), and `data/ui-ux/ux-guidelines.csv` (17 checks) — query via `scripts/common/search.py`. This module's flagship reference is `frontend-distinctiveness.md`; this file covers the more conventional color/type/layout foundations underneath it.

## Choosing a Palette

Start from the product's category and desired feel, then check `UX018`: **does the accent color just follow the category norm, or was it a deliberate choice?** This single question is the highest-leverage, lowest-cost distinctiveness lever available — before reaching for unusual layouts or custom illustration, confirm the palette itself isn't just doing what every competitor already does.

Quick mapping:
- Editorial/premium/portfolio → warm off-white + ink (`UX001`) or deep ink + warm accent (`UX004`)
- Technical/developer tools → cool slate neutrals (`UX002`)
- Wanting bold, confident, stand-out → brutalist black/white + acid accent (`UX003`)
- Wellness/sustainability/lifestyle → muted sage & clay (`UX005`) — distinctive specifically because most competitors default to blue
- Data-dense dashboards → single-hue ramp (`UX009`) — forces real information-hierarchy discipline
- Luxury/hospitality → deep jewel tones (`UX007`)

Always: dedicate colors for status/semantic meaning, never the brand accent (`UX011`); never let color be the only signal (`UX012`, this is a WCAG requirement, see `QA034`). For dark mode: near-black, not pure black (`UX013`), and desaturate/adjust accents for dark backgrounds rather than reusing light-mode values verbatim (`UX014`).

## Choosing Type

Skip the default system/framework font on any brand-forward surface (`UX024`) — Inter/system-ui with zero customization is the single most common tell of an unstyled or templated page, not because those fonts are bad, but because using them unmodified signals no type decision was made. Pair a distinctive display face with a neutral, highly legible body face (`UX021`) rather than using one "safe" font everywhere, or commit to one variable font and let weight/width carry the differentiation (`UX023`).

Small, cheap, easy-to-miss wins: tabular figures for anything that aligns in columns (`UX030`), tighter line-height specifically at display sizes while keeping body text spacious (`UX027`), and a deliberately non-default modular scale ratio (`UX026`).

## UX Fundamentals Beyond Visual Style

- **Loading/empty/error states get the same design attention as the happy path** (`UX045`) — these are disproportionately visible to exactly the users (new, frustrated) whose first impression matters most.
- **Hover/focus/active are visually distinct from each other**, not one generic brightness shift applied to all three (`UX046`) — this also satisfies `QA029`'s accessibility requirement for a genuinely visible focus state.
- **Skeleton loaders match the shape of the content they're replacing**, not a generic spinner for everything (`UX047`).
- **Copy is specific to the actual product**, not interchangeable template copy — genericness in copy is as strong a "templated" tell as genericness in visual design (`UX044`).

## Relationship to the Testing/QA Module

`data/testing/a11y-perf-checklist.csv` (Phase 4) covers the *verifiable* accessibility and performance side (contrast ratios, Core Web Vitals). This module covers the *qualitative* design side. Use both together: the QA checklist for "does it work for everyone and load fast," this module and `frontend-distinctiveness.md` for "does it look intentional and not generic."
