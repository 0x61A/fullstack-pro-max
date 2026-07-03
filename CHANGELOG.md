# Changelog

All notable changes to this skill are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/): new checks, data rows, or modules bump **minor**, corrections bump **patch**. The latest version here stays in sync with `metadata.version` in `SKILL.md`.

## [0.3.0] — 2026-07-03

### Added
- **Analytics & Measurement module** (11th module, `AN` prefix, action `measure`): 34 new data rows — `data/analytics/platform-selection.csv` (12: GA4/Plausible/Umami/PostHog/Mixpanel, warehouse-first, server-side tagging, replay, experiments, consent), `event-tracking-patterns.csv` (10: object_action taxonomy, track plan as code, identity boundary, server-side revenue events), `measurement-checklist.csv` (12 checks: PII-free events, consent gating, revenue reconciliation, dedup, UTM hygiene, pipeline alerts).
- `references/analytics-measurement.md` — platform decision tree, event design rules, funnels/retention/north-star discipline, compliance layer; cross-referenced with the Ads module's tracking checks (`ADS051–ADS064`).
- `scripts/analytics/generate.py`: scaffolds a typed track-plan module (PostHog/GA4/Plausible) with event-name validation and a consent guard.
- Workflow 1 (Complete SaaS Launch) gains a `measure` step before `launch-ads`.

## [0.2.0] — 2026-07-03

### Added
- **AI Integration module** (10th module, `AI` prefix, action `integrate-ai`): 43 new data rows — `data/ai/model-selection.csv` (14: Claude model tiers, tiered routing, extended thinking, vision, embeddings, caching, Batch API, Agent SDK), `data/ai/integration-patterns.csv` (13: streaming SSE, tool use, RAG/pgvector, conversation state, evals, retries, semantic caching), `data/ai/llm-security-checks.csv` (16 checks mapped to the OWASP LLM Top 10).
- `references/ai-integration.md` (model decision tree, cost model, RAG shape, quality gates) and `references/ai-security.md` (LLM threat model, OWASP LLM mapping, tool-use escalation, fail-closed rule).
- `scripts/ai/generate.py`: scaffolds a streaming Claude chat endpoint for Next.js App Router, Express, or FastAPI — with auth check, rate-limit hook, input cap, and bounded `max_tokens` baked in.

## [0.1.0] — 2026-07-03

First public release.

### Added
- Nine modules — Backend & API, Database & Auth, DevOps & Deployment, Testing/QA, Security/Cybersecurity, E-commerce & Payments, UI/UX & Distinctive Frontend, SEO, Ads — with ~644 structured data rows, 29 reference docs, and stdlib-only Python scripts.
- `scripts/common/validate.py`: validates every data CSV against the shared schemas (ID prefixes, uniqueness, severities, dates).
- CI workflow (`.github/workflows/validate.yml`): CSV validation, `--help` + dry-run smoke tests for every script, internal file-reference check, and a self-scan of the repo with the skill's own `scripts/security/audit.py`.
- `scripts/security/audit.py`: repeatable `--exclude PATH` flag; the scanner now always skips its own file (its pattern definitions would otherwise match themselves).
- MIT license, English README, Turkish README (`README.tr.md`), this changelog.

[0.3.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.3.0
[0.2.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.2.0
[0.1.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.1.0
