# Field test: ready-made component sourcing for a dark-technical dashboard

**Prompt tested:** "I need a dark, technical-looking dashboard like a dev tool -- can you use a ready-made component instead of building from scratch?"

## `design` action walkthrough

1. **Style match (`data/ui-ux/style-vocabulary.csv`):**
   ```
   $ python3 scripts/common/search.py data/ui-ux/style-vocabulary.csv --query "dark-technical"
   ```
   → `UX141` (Dark & Technical).

2. **No link supplied → known-sites-library suggestion first** (`references/reference-site-analysis.md` § "No URL From the User?"):
   ```
   $ python3 scripts/common/search.py data/ui-ux/known-sites-library.csv --tag style:UX141
   ```
   → `UX203` Linear, `UX204` Vercel (named flagships), `UX205` (Awwwards/Dribbble/Land-book gallery fallback).

3. **Ready-made component instead of from-scratch → component-libraries.csv** (`references/component-library-integration.md`):
   ```
   $ python3 scripts/common/search.py data/ui-ux/component-libraries.csv --category "Selection Guide" --query "dashboard"
   ```
   → `UX266`: for a data-dense dashboard, pair **Tremor** (`UX262`, charts/KPI cards) with **shadcn/ui Blocks** or **Preline** (`UX248`/`UX255`, surrounding app chrome).

4. **Live-fetch verification before quoting anything as current fact** (the mandatory step — this file's CSV entries are knowledge-authored, not fetched at write time):
   - `WebFetch https://tremor.so` → confirmed: "35+ fully open-source, accessible components for dashboards and charts. Built with React, Tailwind CSS and Radix UI" — matches the CSV row. **New since the row was written:** Tremor now also sells a separate 300+-template premium block library on top of the free core — the CSV row (`UX262`) was updated with this detail as a direct result of this check.
   - `WebFetch https://ui.shadcn.com/blocks` → confirmed: "Clean, modern building blocks," "Open Source. Free forever," dashboards/sidebars/login/data-tables — matches the CSV row (`UX248`) with no changes needed.

## Generated output (this directory)

```
python3 scripts/ui-ux/generate.py \
  --palette UX088 --type UX098 --style UX141 \
  --components hero,nav,sidebar,table --stack react-tailwind \
  --output examples/dark-technical-dashboard

python3 scripts/backend/generate.py projects --stack nextjs-api \
  --output examples/dark-technical-dashboard
```

Real output committed in this folder: `design-tokens.css`, `tailwind.config.ts`, `components/{Hero,Nav,Sidebar,Table}.tsx`, and a CRUD scaffold at `app/api/projects/`.

## What this test confirmed vs. found

- **Confirmed:** the full style → known-sites-library → component-libraries → Selection Guide chain resolves cleanly and points at real, still-accurate sources (both live-fetch spot checks matched the CSV's claims).
- **Found and fixed upstream (see `CHANGELOG.md` v0.15.0 and the commit after it):**
  - `data/ui-ux/colors.csv` row `UX088` (the palette used above, and the one in the script's own `--help` example) only had 2 of 4 color roles as literal hex codes in its prose — the generator's hex-extraction heuristic silently degraded the accent color to a duplicate of the text color. Fixed by adding a concrete accent hex to the row.
  - `scripts/backend/generate.py`'s naive pluralizer double-pluralized any resource name already given in plural form -- `projects` → `projectses`, `posts` → `postses`. This is a common real input (`projects` is exactly what got typed above), not an edge case. Fixed: a word already ending in `s` is now left as-is instead of getting `+es` appended.
  - `python3 scripts/security/audit.py examples/` correctly flagged the freshly-generated scaffold for missing security headers and a missing `.gitignore` -- expected and correct: generated output is a starting point, and `scripts/security/generate.py` is the separate step that adds headers.
