> Last updated: 2026-07-03 · Module version: 0.1

# SEO Scoring

Reuses the exact severity-weighted formula from `security-scoring.md` and `scripts/common/score.py`, applied to this module's 76 checklist-schema checks across `data/seo/technical-seo-checks.csv` (34), `data/seo/onpage-checks.csv` (23), and `data/seo/content-eeat-checks.csv` (19). `data/seo/schema-types.csv` is a decision-matrix reference (which schema type to use), not a pass/fail checklist, so it isn't scored the same way — use it as a lookup table when auditing structured data instead.

## The Formula

```
Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
score = 100 - (sum of weights of FAILED checks / sum of weights of EVALUATED checks) * 100
```

Identical weighting to the security module and the `ads` skill this pattern originated from — one consistent scoring language across every audit-shaped module in this skill, so a "72" means the same thing whether it's a security score, an SEO score, or (once Phase 9 ships) an Ads score.

## Running It

```
python3 scripts/common/score.py data/seo/technical-seo-checks.csv --results results.json
python3 scripts/common/score.py data/seo --results results.json   # all three checklist CSVs + schema-types.csv combined
```

`scripts/common/score.py` silently skips rows with no `severity` column value it recognizes, which is exactly what happens with `schema-types.csv` (a decision-matrix file with no `severity` column at all) — so pointing the scorer at the whole `data/seo/` directory is safe and automatically scores only the three checklist files.

## What "Critical" Means in This Module

Calibrate expectations against a few examples already in the checklists:
- `SEO005` (accidental noindex left over from staging) and `SEO029` (migration with no redirect map) are Critical — both are silent, high-blast-radius mistakes that can zero out organic traffic with no other symptom.
- `SEO047` (content mismatched to actual search intent) and `SEO050` (thin content) are Critical — these aren't technical bugs, but they're identified as the most consistent drivers of ranking failure even on technically flawless pages.
- `SEO060` (anonymous bylines on YMYL content) and `SEO066` (fabricated/undisclosed reviews) are Critical — trust and regulatory risk, not just ranking risk.

A high score with a single failed Critical item should be treated as more urgent than a lower score with several failed Low items — always inspect *which* checks failed, not just the aggregate number (same guidance as `security-scoring.md`).

## Auditing in Practice

1. Run the technical checklist first — a site failing crawlability/indexability basics (`SEO001`-`SEO010`) has little use for a content-quality audit until those are fixed; content quality can't compensate for a page search engines can't find or won't index.
2. Run on-page and content-eeat checks together — these two files are where most of the actual writing/optimization work lives, and they inform each other (e.g. `SEO047`'s intent-match check and `SEO067`'s depth check are closely related).
3. Cross-reference `schema-types.csv` when auditing structured data specifically, confirming the *type* chosen matches the content (a Product schema on a page that isn't really a product listing is itself a finding, separate from whether the markup validates).

## Relationship to the seo-geo/seo-technical Sibling Skills

This module is deliberately original and self-contained (see `conventions.md`), not a copy of the existing `seo`/`seo-technical`/`seo-geo` skill family's content — but the underlying subject matter (technical SEO, E-E-A-T, GEO) is the same domain, so findings from either should broadly agree. If this module's guidance and a sibling skill's guidance ever conflict, that's worth flagging rather than silently picking one — SEO best practices do shift, and `SEO070`/`SEO071`'s AI-content guidance in particular is an area worth re-verifying against current platform behavior periodically (see `conventions.md`'s versioning policy).
