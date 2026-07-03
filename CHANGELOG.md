# Changelog

All notable changes to this skill are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/): new checks, data rows, or modules bump **minor**, corrections bump **patch**. The latest version here stays in sync with `metadata.version` in `SKILL.md`.

## [0.7.0] — 2026-07-03

### Added
- **Supply-chain security checks** (`data/security/supply-chain-checks.csv`, `SEC125-SEC134`, 10 checks): automated dependency scanning, enforced lockfiles, pre-merge dependency review, exact-version pinning for security-sensitive packages, CI/CD secret scoping, pinned GitHub Actions (commit SHA not tag), verified build provenance, SBOM generation, and a patch-SLA requirement. Security module total: 124 → 134 checks. New section in `references/infra-cloud-security.md`.

## [0.6.0] — 2026-07-03

### Added
- **Local SEO checks** (`data/seo/local-seo-checks.csv`, `SEO093-SEO112`, 20 checks): GBP claim/categorization/engagement, NAP consistency (site/GBP/directories, crawlable HTML), citations, `LocalBusiness` schema matching the visible page, review generation/response, unique per-location content (Critical — thin-content risk), service-area GBP setup (Critical — fake-storefront suspension risk), and multi-location NAP/GBP management. SEO module total: 92 → 112 checks. New section in `references/seo-technical.md`.

## [0.5.0] — 2026-07-03

### Added
- **i18n / Localization module** (13th module, `IN` prefix, action `localize`): 34 new data rows — `data/i18n/library-selection.csv` (10: next-intl/react-i18next/Paraglide/FormatJS, static vs. database content model, TMS/MT/in-repo translation workflow, Intl API formatting), `routing-content-patterns.csv` (12: subpath/subdomain/ccTLD URL strategy, fallback locale chain, hreflang generation, RTL via logical CSS, ICU pluralization, no string concatenation, locale-aware currency), `l10n-checklist.csv` (12 checks: hardcoded strings, hreflang/sitemap validation, no forced redirects, text expansion, plural grammar, fallback behavior, translation coverage, translated metadata, pseudo-localization in CI, legal text review).
- `references/i18n-localization.md` — library decision tree, content model split, the grammar rules naive i18n gets wrong; cross-referenced with the SEO module's hreflang (`SEO019`) and no-forced-redirect (`SEO020`) rules.
- `scripts/i18n/generate.py`: scaffolds locale routing config, per-locale message stubs (default locale gets real strings, others get TODO-marked stubs with identical key structure), and an hreflang generator for next-intl or react-i18next.
- This closes **Phase B** (4 new modules added this cycle: AI Integration, Analytics, Email, i18n).

## [0.4.0] — 2026-07-03

### Added
- **Email module** (12th module, `EM` prefix, action `integrate-email`): 34 new data rows — `data/email/provider-selection.csv` (10: Resend/Postmark/SES/SendGrid, marketing platforms, mandatory stream separation, React Email/MJML, inbound parsing, sandboxing), `sending-patterns.csv` (10: queue-backed sends, idempotency, suppression webhooks, RFC 8058 one-click unsubscribe, double opt-in, warmup, i18n), `deliverability-checklist.csv` (14 checks: SPF/DKIM/DMARC progression, aligned return-path, Gmail/Yahoo bulk-sender rules, complaint-rate monitoring, list-bombing protection, MTA-STS).
- `references/email-integration.md` — provider decision tree, the four sending non-negotiables, authentication-first deliverability guidance.
- `scripts/email/generate.py`: scaffolds a queue-friendly transactional send module (Resend/Postmark/SES × Node/Python) with suppression, idempotency, and sandbox guards baked in.

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

[0.7.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.7.0
[0.6.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.6.0
[0.5.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.5.0
[0.4.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.4.0
[0.3.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.3.0
[0.2.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.2.0
[0.1.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.1.0
