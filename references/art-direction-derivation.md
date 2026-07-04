> Last updated: 2026-07-04 · Module version: 0.3

# Art-Direction Derivation

Use this when there's **no reference site** to analyze (that case is `reference-site-analysis.md`) and no obvious sector recipe fit — the user describes a business/product in words and you need to derive a visual identity from scratch, deliberately, instead of defaulting to the safest look. Output: a written **Design DNA** block (below), confirmed with the user before code — the brief-less sibling of UX087's rule.

## The five personality axes

Ask the user to place the brand on these (or infer from their description and state your inference explicitly). Each axis end pulls concrete design decisions:

| Axis | ← end pulls | → end pulls |
|---|---|---|
| **Serious ↔ Playful** | restrained palette, editorial/swiss bones (`UX127`/`UX130`), radius-none/soft, motion restrained | saturated palette, rounded/neo-brutalist bones (`UX147`/`UX126`), radius-pill, expressive motion |
| **Warm ↔ Technical** | warm neutrals/terracotta (`UX091`/`UX096`), humanist or serif type (`UX104`), organic touches (`UX152`) | cool darks (`UX088`), grotesk/mono type (`UX098`/`UX100`), dark-technical/terminal (`UX141`/`UX142`) |
| **Luxury ↔ Accessible** | whitespace as wealth (`UX143`), hairline rules, didone display (`UX099`), muted metallics (`UX093`) | friendly density, clear labels, rounded sans (`UX101`), corporate-clean or flat bones (`UX146`/`UX145`) |
| **Calm ↔ Energetic** | e-ink/paper (`UX144`/`UX090`), shadow-none, density-airy, minimal motion | high-vis accents (`UX097`), memphis/kinetic energy (`UX148`/`UX131`), scroll-driven motion (`UX112`) |
| **Classic ↔ Experimental** | editorial/deco/bauhaus heritage (`UX130`/`UX129`/`UX128`), proven pairings | brutalism/collage/maximalism (`UX125`/`UX132`/`UX153`), variable-font play, broken grids (UX054) |

Rules of thumb:
- **Two axes dominate.** Pick the two the user feels strongest about; let the other three default to center. Optimizing all five produces mush.
- **Tension is a feature.** "Technical but warm" (e.g. dark-technical bones + terracotta accent + one organic signature) is more distinctive than either pole alone — deliberate axis tension is where non-templated identities live.
- **The sector recipe is the starting point, not the answer.** If a `sector-art-direction.csv` row (UX068-UX077) matches the business, start there, then push it along the axes the user cares about. The recipe unmodified = the category's average look.

## Process

1. **Sector anchor** — check `data/ui-ux/sector-art-direction.csv` for the closest business category; note its default direction and its `avoid_when`.
2. **Axis placement** — place the brand on the five axes (confirm with the user; 2 dominant axes).
3. **Style candidates** — query `data/ui-ux/style-vocabulary.csv` (30 styles, UX125-UX154) for 2-3 candidates matching the dominant axes; check each candidate's `avoid_when` against the actual product. The style row's tags carry token tendencies (`radius-*`, `shadow-*`, `density-*`, `border-*`) that `scripts/ui-ux/generate.py --style` consumes directly.
4. **Palette + type** — pick from `colors.csv`/`typography.csv` rows consistent with the chosen style (each style row's option text names its typical combination).
5. **Signature element** — pick one ownable element (UX048): a shape language, a motion signature (`motion-recipes.csv`), a textured accent (`UX137`). This is what survives the "five competitors" test.
6. **Genericness check** — run UX050 against the assembled DNA: could this exact combination belong to five competitors? If yes, push one decision further along an axis.
7. **Confirm, then generate** — share the Design DNA block, get a yes, then scaffold: `python3 scripts/ui-ux/generate.py --palette UXnnn --type UXnnn --style UXnnn [--components ...]`.

## Design DNA block (template)

```
Business: <one line — what it is, who buys>
Sector anchor: <UXnnn sector recipe or "none — novel category">
Axes (dominant two bolded): serious/playful X · warm/technical X · luxury/accessible X · calm/energetic X · classic/experimental X
Style direction: <UXnnn style + one sentence why, incl. its avoid_when cleared>
Palette: <UXnnn or explicit family+role>
Typography: <UXnnn pairing>
Signature element: <the one ownable thing (UX048)>
Deliberate tension: <which axis combination makes this NOT the category default>
UX050 check: <why five competitors couldn't ship this with a logo swap>
Confirmed with user: <yes/no>
```

Downstream: `frontend-distinctiveness.md` still governs execution quality; `reference-site-analysis.md` replaces steps 1-3 when the user brings example URLs instead of words. If both exist (references *and* verbal brand description), the reference brief wins on observed specifics, this process fills what the references don't show.
