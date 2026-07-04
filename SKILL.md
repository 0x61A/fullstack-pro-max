---
name: fullstack-pro-max
description: "Full-stack product delivery skill for agency/client and personal SaaS builds. Covers distinctive, non-templated UI/UX and frontend design (turning user-supplied reference site URLs into a Reference Design Brief before coding, suggesting real named sites per style/sector from a built-in 90-entry known-sites library when the user has no link, or sourcing ready-made components/themes from real component marketplaces like 21st.dev/shadcn/ui/Aceternity UI via live fetch + a copy-paste integration guide when the user wants a pre-built starting point instead of a from-scratch build); backend architecture (Node.js/Next.js/Express/Nest.js, Python FastAPI/Django, or Supabase/Firebase BaaS — auto-selected per project); database & auth design; CI/CD & deployment (Vercel, Netlify, Cloudflare); QA testing; deep cybersecurity (threat modeling, secure coding, API/infra security, incident response — OWASP and beyond); SEO; paid ads; e-commerce payments (Stripe, Shopify); AI feature integration (Claude API — model selection, streaming chat, tool use, RAG, LLM security); analytics & measurement (GA4/PostHog/Plausible selection, event taxonomy, funnels/retention, consent-compliant tracking); email (Resend/Postmark/SES selection, transactional sending patterns, SPF/DKIM/DMARC deliverability); and i18n/localization (next-intl/react-i18next selection, URL strategy, hreflang, RTL, ICU pluralization). Actions: plan, build, design, integrate, integrate-ai, integrate-email, measure, localize, deploy, test, secure, integrate-payments, optimize-seo, launch-ads, audit, review. Adaptive stack selection, not locked to one frontend+backend combo."
metadata:
  version: "0.20.0"
  last_updated: "2026-07-04"
---

# Fullstack Pro Max — Full-Stack Product Delivery

One skill for shipping a real product end to end: distinctive UI/UX, backend architecture, database & auth, deployment, testing, cybersecurity, SEO, ads, e-commerce payments, AI feature integration, analytics & measurement, email, and i18n/localization. Built for two use cases — agency/client delivery and personal SaaS builds — with adaptive stack selection rather than one fixed frontend+backend combo.

All 13 modules (Backend, Database & Auth, DevOps, Testing/QA, Security, E-commerce, UI/UX, SEO, Ads, AI Integration, Analytics, Email, i18n) are built — see `references/routing.md` for the full action-to-file map. If a future module is ever added and not yet built, this skill degrades gracefully: reason from general best practice and say so explicitly, rather than refusing.

## When to Apply

### Must Use
- Scaffolding a new project's backend/API from scratch
- Choosing a stack (frontend, backend, database, hosting) for a new build
- Designing or reviewing API endpoints, error handling, or request/response contracts
- Pre-launch security, SEO, or ads audits (see `references/workflows.md` § Pre-Launch Audit)
- Setting up CI/CD, deployment, database schema, or auth

### Recommended
- Mid-project architecture questions ("is this the right stack for what we're building")
- Code review that touches backend structure, API design, or error handling
- Deciding between competing patterns (REST vs GraphQL, cursor vs offset pagination, etc.)

### Skip
- Pure content writing or copy editing unrelated to building/shipping the product
- Non-technical business questions (pricing strategy, market research) with no engineering component
- Purely visual/CSS polish on an already-built page with no architectural question involved

**Decision criteria**: if the task is about *deciding how to build, ship, secure, or grow* a web product, this skill applies.

## Ask Before You Build

This skill defaults to asking clarifying questions before starting non-trivial work, not to guessing silently and hoping the guess matches what the user actually needed. (This mirrors how this skill itself was built — two rounds of structured questions on architecture, scope, and dependency policy before a single file was written.)

**Ask 2-4 concrete questions before:**
- Choosing a stack for a new project (frontend/backend/database/hosting) — unless the user already stated a preference or the existing codebase already implies one.
- Any `secure` work — what's the deployment target, what data is actually at risk, is there a compliance context (GDPR, PCI, none)? A generic OWASP pass without this context risks solving the wrong problem.
- Any `integrate-payments` work — Stripe vs. Shopify, subscription vs. one-time, and an explicit confirmation of test-mode vs. live keys before any code that could trigger a real charge.
- Any irreversible or hard-to-undo action — a production deploy, a migration against a live table, rotating/deleting a credential, a DNS/domain change. Match the caution level in the top-level system instructions on risky actions; this skill doesn't override that.
- A request broad enough to have multiple reasonable interpretations ("build the backend" could mean a scaffold, a full CRUD API, or a production-ready API with auth+tests+deploy — ask which, don't guess the most expensive interpretation by default).

**Don't ask when:**
- The answer is already visible in the codebase, the conversation, or this skill's own stated defaults (don't ask "which test framework" if `package.json` already has one installed).
- The task is small, reversible, and low-stakes (a copy tweak, a single CSS value, a typo fix).
- The user already stated a clear preference earlier in the conversation — don't re-ask something they already told you.

**How to ask:** batch questions together (2-4 at once, via a structured question tool if available, otherwise a short numbered list) rather than trickling out one question per turn. Offer a recommended default in each question where a sensible one exists (see Stack Selection Logic below for the default stack), and treat "I don't know, you decide" as a valid answer that unblocks proceeding with the stated default — don't force a decision the user doesn't have an opinion on.

**When asking isn't possible** (fully autonomous/non-interactive execution): state the assumption explicitly before proceeding — "Assuming Next.js + Supabase since no stack was specified" — rather than silently picking one with no note that a decision was made on the user's behalf.

## Action-Routing Table

| Action | Status | Module | Load |
|---|---|---|---|
| `plan` | ✅ Built | Backend (stack selection) + Database + DevOps | `references/backend-architecture.md` (Stack Decision Tree), `references/database-schema-design.md`, `data/backend/stacks.csv` |
| `build` | ✅ Backend built | Backend & API | `references/backend-architecture.md`, `references/api-design.md`, `scripts/backend/generate.py` |
| `design` | ✅ Built | UI/UX & Distinctive Frontend | `references/frontend-distinctiveness.md` (flagship — always load for brand-forward work), `references/ui-ux-quickref.md`, `scripts/ui-ux/generate.py` (tokens + skeletons, `--style` for aesthetic direction); example sites given → `references/reference-site-analysis.md` + `scripts/ui-ux/scan.py`; no example link but a style/sector named → `data/ui-ux/known-sites-library.csv` (90 rows, real named sites + gallery sources per style) via `scripts/common/search.py`, then same reference-site-analysis flow; wants a ready-made component/theme instead of from-scratch → `data/ui-ux/component-libraries.csv` (24 rows: 21st.dev, shadcn/ui, Aceternity UI, Magic UI, and 14 more, live-fetched not memorized) + `references/component-library-integration.md`; no references, identity from scratch → `references/art-direction-derivation.md` + `data/ui-ux/style-vocabulary.csv` |
| `integrate` | ✅ Built | Database & Auth / E-commerce | `references/database-schema-design.md`, `references/auth-patterns.md`, `scripts/database/generate.py` (for db/auth); `references/stripe-integration.md`, `shopify-integration.md`, `scripts/ecommerce/generate.py` (for payments) |
| `deploy` | ✅ Built | DevOps & Deployment | `references/ci-cd-pipelines.md`, `references/deployment-platforms.md`, `references/env-secrets-management.md`, `scripts/devops/generate.py`, plus the connected Vercel/Netlify/Cloudflare MCP tools |
| `test` | ✅ Built | Testing/QA | `references/testing-strategy.md`, `references/accessibility-performance-audit.md`, `scripts/testing/generate.py` |
| `secure` | ✅ Built | Security/Cybersecurity | `references/security-threat-modeling.md`, `secure-coding-standards.md`, `api-security.md`, `infra-cloud-security.md`, `incident-response.md`, `security-scoring.md`, `scripts/security/{generate,audit}.py`, `scripts/common/score.py` |
| `integrate-payments` | ✅ Built | E-commerce & Payments | `references/stripe-integration.md`, `shopify-integration.md`, `scripts/ecommerce/generate.py`, plus the connected Shopify MCP tools |
| `optimize-seo` | ✅ Built | SEO | `references/seo-technical.md`, `seo-content-eeat.md`, `seo-scoring-system.md`, `data/seo/*.csv`, `scripts/common/score.py` |
| `launch-ads` | ✅ Built | Ads | `references/ads-google.md`, `ads-meta.md`, `ads-other-platforms.md`, `ads-scoring-system.md`, `data/ads/*.csv`, `scripts/common/score.py` |
| `integrate-ai` | ✅ Built | AI Integration | `references/ai-integration.md`, `references/ai-security.md`, `data/ai/*.csv`, `scripts/ai/generate.py`, `scripts/common/score.py` |
| `measure` | ✅ Built | Analytics | `references/analytics-measurement.md`, `data/analytics/*.csv`, `scripts/analytics/generate.py`, `scripts/common/score.py` |
| `integrate-email` | ✅ Built | Email | `references/email-integration.md`, `data/email/*.csv`, `scripts/email/generate.py`, `scripts/common/score.py` |
| `localize` | ✅ Built | i18n / Localization | `references/i18n-localization.md`, `data/i18n/*.csv`, `scripts/i18n/generate.py`, `scripts/common/score.py` |
| `review` / `audit` | ✅ Built | All (cross-module) | `references/workflows.md` — chains the module-specific checks/scripts above into Complete SaaS Launch, Client Delivery Package, Pre-Launch Audit, and Security Hardening Pass sequences |

Full detail, trigger phrases, and the graceful-degradation rule live in [`references/routing.md`](references/routing.md) — load it whenever an action doesn't obviously map to a single file above.

## Module Reference

### Backend & API — ✅ Built (Phase 1)
Adaptive stack selection (Node.js: Next.js API Routes/Express/Nest.js/Fastify; Python: FastAPI/Django; BaaS: Supabase/Firebase; Edge: Cloudflare Workers) plus API design conventions (REST/GraphQL/tRPC/gRPC choice, pagination, versioning, idempotency, rate limiting) and error-handling patterns (taxonomy, retries, observability, per-stack conventions).
- Data: `data/backend/stacks.csv` (41 rows — includes `BE088`, a static/no-backend option for marketing-site briefs with no accounts or stored data), `data/backend/api-patterns.csv` (25 rows), `data/backend/error-handling.csv` (22 rows)
- References: `references/backend-architecture.md`, `references/api-design.md`
- Script: `scripts/backend/generate.py` — scaffolds a CRUD endpoint (route/controller/service or router/schema files as appropriate) for a named resource in any of the 6 supported stacks. Run `python3 scripts/backend/generate.py --help`.

### Database & Auth — ✅ Built (Phase 2)
Schema design patterns (normalization, PK strategy, soft/hard delete, multi-tenancy via RLS, indexing), auth strategy matrix (session/JWT/OAuth/magic-link/passkey/MFA/authorization models), migrations safety discipline. First-class Supabase coverage — if the Supabase MCP is connected in your environment, use it for `execute_sql`, `apply_migration`, `list_tables`, `get_advisors`.
- Data: `data/database/schema-patterns.csv` (30 rows), `data/database/auth-patterns.csv` (25 rows), `data/database/migrations-checklist.csv` (21 checks)
- References: `references/database-schema-design.md`, `references/auth-patterns.md`
- Script: `scripts/database/generate.py` — scaffolds a Supabase SQL migration (with optional starter RLS policies) or a Prisma model fragment for a named table. `python3 scripts/database/generate.py --help`.

### DevOps & Deployment — ✅ Built (Phase 3)
CI/CD pipeline shape (branch strategy, required gates, deploy strategy, rollback), Vercel/Netlify/Cloudflare/Railway platform decision matrix, env/secrets management discipline. If the Vercel, Netlify, or Cloudflare MCP tools are connected in your environment, use them directly for deploys/logs/project management alongside this module's guidance.
- Data: `data/devops/ci-cd-patterns.csv` (25 rows), `data/devops/platforms.csv` (17 rows), `data/devops/env-management.csv` (13 rows)
- References: `references/ci-cd-pipelines.md`, `references/deployment-platforms.md`, `references/env-secrets-management.md`
- Script: `scripts/devops/generate.py` — scaffolds a GitHub Actions CI workflow (lint/typecheck/test/build, platform-appropriate deploy step) plus a `.env.example`. `python3 scripts/devops/generate.py --help`.

### Testing/QA — ✅ Built (Phase 4)
Test strategy by stack (unit/integration/e2e, tooling per stack, mocking/factory/isolation discipline), plus a 25-check accessibility + Core Web Vitals performance checklist.
- Data: `data/testing/test-strategy.csv` (25 rows), `data/testing/a11y-perf-checklist.csv` (25 checks)
- References: `references/testing-strategy.md`, `references/accessibility-performance-audit.md`
- Script: `scripts/testing/generate.py` — scaffolds a test file skeleton (Vitest/Jest/pytest/Playwright) for a named subject. `python3 scripts/testing/generate.py --help`.

### Security/Cybersecurity — ✅ Built (Phase 5, full-depth "big three" module)
Genuine cybersecurity-expert depth, not a checklist skim: OWASP Top 10 mapped to concrete checks, STRIDE-based threat modeling, secure coding standards per stack (Node.js/Python/Next.js/Express/Django), API-specific security (BOLA, mass assignment, rate limiting, GraphQL complexity), infra/cloud security (IAM, network exposure, backups, DNS), supply-chain/dependency security (SCA, CI/CD pipeline hardening, SBOM), and a full incident-response lifecycle (preparedness → detection → containment → eradication → blameless post-mortem). 134 checks total.
- Data: `data/security/owasp-checklist.csv` (35), `threat-modeling-checks.csv` (20), `secure-coding-checks.csv` (20), `api-security-checks.csv` (15), `infra-cloud-security-checks.csv` (17), `incident-response-checklist.csv` (17), `supply-chain-checks.csv` (10)
- References: `references/security-threat-modeling.md`, `secure-coding-standards.md`, `api-security.md`, `infra-cloud-security.md`, `incident-response.md`, `security-scoring.md`
- Scripts: `scripts/security/generate.py` (scaffolds security-headers middleware for Next.js/Express/FastAPI), `scripts/security/audit.py` (stdlib regex-based static scan for hardcoded secrets, dangerous patterns, missing headers — exits non-zero on Critical/High findings, CI-gateable), `scripts/common/score.py` (shared severity-weighted posture scoring, also reused by the SEO and Ads modules)

### E-commerce & Payments — ✅ Built (Phase 6)
Stripe (checkout approach selection, subscriptions/metered billing, webhook non-negotiables, refunds/disputes, Connect, Tax) and Shopify (hosted vs. headless, checkout extensibility via Functions, GraphQL Admin API, inventory-as-source-of-truth) integration patterns. If the Shopify MCP is connected in your environment, use it directly for product/discount/order operations alongside this module's guidance.
- Data: `data/ecommerce/stripe-patterns.csv` (17 rows), `data/ecommerce/shopify-patterns.csv` (12 rows)
- References: `references/stripe-integration.md`, `references/shopify-integration.md`
- Script: `scripts/ecommerce/generate.py` — scaffolds a signature-verified, idempotent webhook handler for Stripe or Shopify across Next.js/Express/FastAPI. `python3 scripts/ecommerce/generate.py --help`.

### UI/UX & Distinctive Frontend Design — ✅ Built (Phase 7)
Flagship focus: producing frontend design that doesn't read as templated or generic-AI-looking — art-direction frameworks, unique layout/type/motion techniques, plus a curated original color/typography/UX-guideline set. This is the module that directly answers "make this look unique, not templated." When the user describes the desired theme by pointing at existing sites instead of (or alongside) words, `references/reference-site-analysis.md` turns those URLs into a written Reference Design Brief before any code gets written — extracting principles (palette, type pairing, layout pattern), never copying literal assets/copy.
- Data: `data/ui-ux/colors.csv` (30 palettes), `typography.csv` (20 pairings), `style-vocabulary.csv` (30 named aesthetic movements — brutalism to gradient-mesh — each with best-for/avoid-when/tradeoffs and machine-readable token tendencies in tags), `ux-guidelines.csv` (17 checks), `distinctiveness-patterns.csv` (17 flagship techniques), `sector-art-direction.csv` (17 sector recipes — cafe/restaurant, healthcare, legal, SaaS/tech, e-commerce, real estate, fitness, finance, education, nonprofit, plus 7 general local-service sectors: salon/beauty, trades/home services, events/weddings/photography, consulting/professional services, pet care/veterinary, hospitality/boutique lodging, auto services), `reference-analysis-checklist.csv` (10 checks), `motion-recipes.csv` (10 purpose-driven animation patterns with duration/easing values), `responsive-patterns.csv` (10 layout-collapse strategies), `known-sites-library.csv` (90 rows — 2 real named sites + 1 evergreen gallery-search source per style, all 30 styles), `component-libraries.csv` (24 rows — 18 real component/theme marketplaces like 21st.dev/shadcn/ui/Aceternity UI plus 6 needs-based selection-guide rows, indexed for live-fetch not memorized) — 275 rows total
- References: `references/ui-ux-quickref.md`, `references/frontend-distinctiveness.md` (flagship — load this for any brand-forward marketing/landing/portfolio work), `references/reference-site-analysis.md` (load when the user supplies example site URLs, or names a style/sector with none — now covers suggesting from `known-sites-library.csv`), `references/component-library-integration.md` (load when the user wants a ready-made component/theme rather than a from-scratch build — sources real code from `component-libraries.csv` via live fetch, then a copy-paste/CLI integration guide by ecosystem), `references/art-direction-derivation.md` (load when there's no reference site — derives a Design DNA from five brand-personality axes, anchored to sector recipes and the style vocabulary)
- Scripts: `scripts/ui-ux/generate.py` — scaffolds design tokens (`design-tokens.css` + `tailwind.config.ts`) from a palette/typography row id or explicit values, applies a style row's radius/shadow/border/density tendencies via `--style UXnnn`, plus optional TODO-marked component skeletons (hero/nav/feature/footer/cta/sidebar/table/form/empty-state) for react-tailwind or plain HTML; `scripts/ui-ux/scan.py` — stdlib scan of reference URL(s): color frequency, font declarations, layout keywords, WCAG contrast estimates, multi-URL shared-thread analysis, and `--brief` for a pre-filled Reference Design Brief draft. Both support `--help`.

### SEO — ✅ Built (Phase 8, 112 checks)
Technical SEO, on-page, content/E-E-A-T, schema-type selection, and local SEO — original content, self-contained (not shared with the existing `seo`/`seo-audit` skills). Includes GEO (AI Overviews/ChatGPT/Perplexity citability) checks folded into the content module.
- Data: `data/seo/technical-seo-checks.csv` (34), `onpage-checks.csv` (23), `content-eeat-checks.csv` (19), `schema-types.csv` (16 schema.org type decision matrix), `local-seo-checks.csv` (20: GBP, NAP consistency, LocalBusiness schema, reviews, location pages, multi-location) — 112 rows total
- References: `references/seo-technical.md`, `references/seo-content-eeat.md`, `references/seo-scoring-system.md`
- Scoring: reuses `scripts/common/score.py` — same severity-weighted formula as the Security module

### Ads — ✅ Built (Phase 9, 74 checks)
Google/Meta/LinkedIn/TikTok/Microsoft ad audits, plus cross-platform tracking & attribution (server-side tracking, deduplication, consent mode, MER as an attribution-bias sanity check) — original content, self-contained (not shared with the existing `ads`/`ads-audit` skills).
- Data: `data/ads/google-ads-checks.csv` (20), `meta-ads-checks.csv` (14), `platform-checks.csv` (16, LinkedIn+TikTok+Microsoft), `tracking-attribution-checks.csv` (14), `creative-budget-checks.csv` (10) — 74 rows total
- References: `references/ads-google.md`, `references/ads-meta.md`, `references/ads-other-platforms.md`, `references/ads-scoring-system.md` (also covers cross-platform tracking/attribution)
- Scoring: reuses `scripts/common/score.py`

### AI Integration — ✅ Built (Phase B1)
Adding AI features to a product with the Claude API: model tier selection (Fable 5 / Opus 4.8 / Sonnet 5 / Haiku 4.5 with tiered routing), streaming SSE endpoints, tool use, RAG over pgvector, prompt caching and cost control, eval discipline (golden sets, LLM-as-judge), and a 16-check LLM security checklist mapped to the OWASP LLM Top 10 (prompt injection, insecure output handling, excessive agency, denial-of-wallet).
- Data: `data/ai/model-selection.csv` (14 rows), `data/ai/integration-patterns.csv` (13 rows), `data/ai/llm-security-checks.csv` (16 checks)
- References: `references/ai-integration.md`, `references/ai-security.md`
- Script: `scripts/ai/generate.py` — scaffolds a streaming Claude chat endpoint (Next.js App Router/Express/FastAPI) with auth, rate-limit, and input-cap hooks baked in. `python3 scripts/ai/generate.py --help`.

### Analytics & Measurement — ✅ Built (Phase B2)
Platform selection (GA4/Plausible/Umami for web, PostHog/Mixpanel/Amplitude for product, warehouse-first, server-side tagging), event design that survives redesigns (object_action taxonomy, track plan as code, identity at the auth boundary, server-side revenue events), funnels/retention/north-star discipline, and a 12-check measurement checklist (PII-free events, consent gating, revenue reconciliation, UTM hygiene, pipeline alerts). Paid-media tracking stays in the Ads module — the two share dedup/consent/UTM rules.
- Data: `data/analytics/platform-selection.csv` (12 rows), `event-tracking-patterns.csv` (10 rows), `measurement-checklist.csv` (12 checks)
- Reference: `references/analytics-measurement.md`
- Script: `scripts/analytics/generate.py` — scaffolds a typed track-plan module (PostHog/GA4/Plausible) with consent guard and naming validation. `python3 scripts/analytics/generate.py --help`.

### Email — ✅ Built (Phase B3)
Transactional + marketing email: provider selection (Resend/Postmark/SES/SendGrid, dedicated marketing platforms, mandatory stream separation), sending architecture (queue-backed, idempotent, suppression-aware, sandboxed outside production), and a 14-check deliverability checklist (SPF/DKIM/DMARC progression, aligned return-path, Gmail/Yahoo bulk-sender rules, one-click unsubscribe, warmup, complaint-rate monitoring, KVKK/CAN-SPAM).
- Data: `data/email/provider-selection.csv` (10 rows), `sending-patterns.csv` (10 rows), `deliverability-checklist.csv` (14 checks)
- Reference: `references/email-integration.md`
- Script: `scripts/email/generate.py` — scaffolds a queue-friendly send module (Resend/Postmark/SES × Node/Python) with suppression, idempotency, and sandbox guards baked in. `python3 scripts/email/generate.py --help`.

### i18n / Localization — ✅ Built (Phase B4)
Multi-language product delivery: library selection (next-intl/react-i18next/Paraglide/FormatJS), content model (static message files vs. database-stored content), translation workflow (in-repo/TMS/MT+review), URL strategy (subpath default, subdomain, ccTLD), and a 12-check l10n checklist covering the grammar/layout details naive i18n gets wrong (ICU pluralization, no string concatenation, RTL, text expansion, hreflang correctness). Shares hreflang and no-forced-redirect rules with the SEO module.
- Data: `data/i18n/library-selection.csv` (10 rows), `routing-content-patterns.csv` (12 rows), `l10n-checklist.csv` (12 checks)
- Reference: `references/i18n-localization.md`
- Script: `scripts/i18n/generate.py` — scaffolds locale routing config, per-locale message stubs, and an hreflang generator (next-intl/react-i18next). `python3 scripts/i18n/generate.py --help`.

## Stack Selection Logic

Default recommendation for a greenfield project with no strong constraint pointing elsewhere: **Next.js (API Routes) + Supabase**. It covers the majority of MVP, SaaS, and agency-site builds with the least new infrastructure to learn, and both have first-class MCP tooling available when connected in your environment.

Deviate from the default when:
- The team is Python-first or the product has a real AI/ML/data-pipeline component → **FastAPI** (API-first) or **Django** (admin/content-heavy).
- The backend needs enforced structure across multiple domains for a larger team → **Nest.js**.
- The product is mobile-first and needs offline-first sync → **Firebase**.
- The API needs to run at the edge for global low-latency, simple request/response only → **Cloudflare Workers**.

Full decision tree with the reasoning behind each branch: `references/backend-architecture.md` § Stack Decision Tree — starts with a "does this even need a backend" check before the framework-selection questions. Full row-by-row matrix with 41 stack/project-type combinations: `data/backend/stacks.csv` (query via `scripts/common/search.py`).

## Cross-Module Workflows

Four documented multi-step chains — Complete SaaS Launch, Client Delivery Package, Pre-Launch Audit, and Security Hardening Pass — live in [`references/workflows.md`](references/workflows.md). Load it whenever a request spans more than one module (e.g. "get this ready to launch," "audit this before we hand it to the client").

## Conventions

CSV schema (decision-matrix vs. checklist variants), check-ID prefixes per module, severity-weighting formula for scoring, reference-file versioning header format: all defined once in [`references/conventions.md`](references/conventions.md). Every module follows these — read it before authoring or querying any module's data.

## Scripts

All scripts are Python 3, **stdlib-only** (no `requirements.txt`, no vendored venv — this skill operates on the user's real project code, so it relies on the project's own installed dependencies rather than shipping its own environment).

- `scripts/common/search.py` — query any `data/**/*.csv` file by id, category, tag, severity, or free-text. `python3 scripts/common/search.py --help`.
- `scripts/backend/generate.py` — scaffold a CRUD endpoint for a named resource in any supported backend stack. `python3 scripts/backend/generate.py --help`.
- `scripts/database/generate.py` — scaffold a Supabase SQL migration or Prisma model fragment for a named table. `python3 scripts/database/generate.py --help`.
- `scripts/devops/generate.py` — scaffold a CI workflow and `.env.example` for a chosen stack/platform. `python3 scripts/devops/generate.py --help`.
- `scripts/testing/generate.py` — scaffold a test file skeleton (Vitest/Jest/pytest/Playwright). `python3 scripts/testing/generate.py --help`.
- `scripts/security/generate.py` — scaffold security-headers middleware (Next.js/Express/FastAPI). `python3 scripts/security/generate.py --help`.
- `scripts/security/audit.py` — static-scan a project for hardcoded secrets, dangerous code patterns, and missing security headers. `python3 scripts/security/audit.py --help`.
- `scripts/common/score.py` — compute a severity-weighted score from any checklist-schema CSV against a results file. `python3 scripts/common/score.py --help`.
- `scripts/ecommerce/generate.py` — scaffold a Stripe or Shopify webhook handler (Next.js/Express/FastAPI). `python3 scripts/ecommerce/generate.py --help`.
- `scripts/common/validate.py` — validate every `data/**/*.csv` against the shared schemas in `references/conventions.md` (ID prefixes, uniqueness, severities, dates). Run after authoring or editing any data row. `python3 scripts/common/validate.py --help`.
- `scripts/ai/generate.py` — scaffold a streaming Claude chat endpoint (Next.js/Express/FastAPI) with auth, rate-limit, and input-cap hooks. `python3 scripts/ai/generate.py --help`.
- `scripts/analytics/generate.py` — scaffold a typed track-plan module (PostHog/GA4/Plausible) from a list of event names. `python3 scripts/analytics/generate.py --help`.
- `scripts/email/generate.py` — scaffold a queue-friendly transactional email module (Resend/Postmark/SES × Node/Python). `python3 scripts/email/generate.py --help`.
- `scripts/i18n/generate.py` — scaffold locale routing config, message stubs, and an hreflang generator (next-intl/react-i18next). `python3 scripts/i18n/generate.py --help`.
- `scripts/ui-ux/scan.py` — scan reference site(s) HTML/CSS for color/font/layout hints, contrast estimates, and a `--brief` design-brief draft (no JS rendering). `python3 scripts/ui-ux/scan.py --help`.
- `scripts/ui-ux/generate.py` — scaffold design tokens + optional component skeletons from palette/typography/style data rows (`--style` applies an aesthetic movement's token tendencies). `python3 scripts/ui-ux/generate.py --help`.
