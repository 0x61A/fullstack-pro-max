# Field test: from-scratch small-business site

**Prompt tested:** "build a from-scratch website for my business" (a local hair/beauty salon, no existing codebase, no stated preferences).

## `plan` action walkthrough

1. **Question 0 (Stack Decision Tree, `references/backend-architecture.md`):** does this need a backend at all? The brief is pages + a booking/contact form, no accounts, no stored user data → **no**. Stops here instead of running the full Node/Python/BaaS/Edge decision tree.
   ```
   $ python3 scripts/common/search.py data/backend/stacks.csv --id BE088
   ```
   → `BE088`: static site generator (Next.js static export / Astro) + one serverless form endpoint for the contact/booking form.

2. **Sector direction (`data/ui-ux/sector-art-direction.csv`):**
   ```
   $ python3 scripts/common/search.py data/ui-ux/sector-art-direction.csv --tag salon
   ```
   → `UX269`: soft warm-neutral palette, generous whitespace, before/after or portfolio imagery as hero.

3. **Style + tokens.** `UX269`'s direction maps onto the **playful-rounded** style (`UX147` in `style-vocabulary.csv` — approachable, soft, rounded) and a warm palette (`UX091` — Terracotta + Cream) with a friendly type pairing (`UX101` — Rounded Sans Display + Neutral Sans Body).

## Generated output (this directory)

```
python3 scripts/ui-ux/generate.py \
  --palette UX091 --type UX101 --style UX147 \
  --components hero,nav,feature,footer --stack html \
  --output examples/salon-site
```

Produced `design-tokens.css`, `hero.html`, `nav.html`, `feature.html`, `footer.html` — real output committed in this folder, not a transcript. Every file still has TODO markers for real copy/imagery and needs the UX050 "five competitors" genericness check (`data/ui-ux/ux-guidelines.csv`) before shipping — this is a starting point, per the script's own stated intent, not a finished page.

## What this test confirmed vs. found

- **Confirmed:** the `plan` → `design` handoff (backend decision → sector direction → style/palette/type → token+skeleton generation) runs cleanly end to end with real script output, no manual patching needed.
- **Found and fixed upstream (see repo `CHANGELOG.md` v0.15.0):** before this test, `data/backend/stacks.csv` had no row for "no backend needed" — the single most common answer for a brief like this one. `BE088` and the Stack Decision Tree's question 0 were added directly because of this test.
