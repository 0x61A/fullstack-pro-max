# Building fullstack-pro-max: a 13-module Claude Code skill, one focused release at a time

`fullstack-pro-max` is a single, self-contained [Claude Code](https://claude.com/claude-code) skill covering the full lifecycle of shipping a web product — backend architecture, database/auth, DevOps, testing, security, e-commerce, distinctive UI/UX, SEO, ads, AI feature integration, analytics, email, and i18n. As of `v0.9.0`: 13 modules, 839 structured data rows, 34 reference docs, 14 stdlib-only Python scripts. Repo: [github.com/0x61A/fullstack-pro-max](https://github.com/0x61A/fullstack-pro-max).

## The architectural bet: one package, action-routed

Most large Claude Code skills either stay small or fragment into dozens of sibling skill folders orchestrated by a thin parent. `fullstack-pro-max` took a third path: **one package**, with `SKILL.md` as a lightweight action router (~200 lines) pointing into `data/` (CSVs), `references/` (Markdown, loaded on demand), and `scripts/` (generators). Every module — Backend, Security, SEO, AI Integration, whatever — follows the exact same two CSV schemas (a decision-matrix variant and a checklist variant) and the exact same ID-prefix convention (`BE`, `SEC`, `SEO`, `AI`...). Once you understand one module's shape, you understand all thirteen.

This paid off directly when the skill grew: adding a 13th module (i18n/localization) didn't require touching the query tooling, the scoring engine, or the validator — they're generic over the schema, not the module.

## The constraint that shaped everything: stdlib-only scripts

Every one of the 14 generator/utility scripts is pure Python standard library. No `requirements.txt`, no vendored venv. This wasn't a style preference — a sibling skill in the same environment had accumulated a 511MB `.venv` from third-party dependencies, and that became the cautionary example driving the decision early on. The generated *code* can use whatever the target project needs (`@anthropic-ai/sdk`, `next-intl`, `resend`), but the tooling that produces it never adds a dependency the user didn't already choose.

## CI that eats its own dog food

The validation workflow doesn't just check syntax. It runs the skill's own static-analysis security scanner (`scripts/security/audit.py`) against the skill's own repository, smoke-tests every generator with `--dry-run`, and cross-checks that every file path mentioned in every reference doc actually exists. When a CSV validator script was first added, it immediately caught a real formatting bug (unescaped commas inside a quoted field) that had shipped in an earlier commit — the tool paid for itself on its first real run.

## Growing in public, one version-tagged slice at a time

Rather than batching a huge "v1.0 mega-release," the skill grew through small, tagged, changelogged increments — four new modules (AI, Analytics, Email, i18n) each shipped as its own minor version, followed by a deliberately scoped "deepening" pass adding a focused 10-20-row addition to four existing modules (local SEO, supply-chain security, ad creative/budget discipline, sector-specific art direction) rather than a single sprawling expansion. Every release: schema-validated data, a self-audit with zero findings, and a CHANGELOG entry explaining *why*, not just *what*.

## What's next

The module list stays append-only by design — IDs never get renumbered once published, only extended. Future work follows the same pattern: pick the highest-value gap, ship it as one clean, validated, tagged release, and let the changelog tell the story.
