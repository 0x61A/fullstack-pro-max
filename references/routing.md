> Last updated: 2026-07-03 · Module version: 0.2

# Routing

Load this file first when an action doesn't obviously map to a single file. It tells you which module owns an action and which reference/data/script files to load. All 13 modules are built; the Graceful Degradation Rule below is preserved for if this skill ever grows a module that isn't built yet.

## Module Build Status

| Module | Status | Phase | Data | References |
|---|---|---|---|---|
| Backend & API | ✅ Built | 1 | `data/backend/*.csv` | `backend-architecture.md`, `api-design.md` |
| Database & Auth | ✅ Built | 2 | `data/database/*.csv` | `database-schema-design.md`, `auth-patterns.md` |
| DevOps & Deployment | ✅ Built | 3 | `data/devops/*.csv` | `ci-cd-pipelines.md`, `deployment-platforms.md`, `env-secrets-management.md` |
| Testing/QA | ✅ Built | 4 | `data/testing/*.csv` | `testing-strategy.md`, `accessibility-performance-audit.md` |
| Security/Cybersecurity | ✅ Built | 5 | `data/security/*.csv` (134 checks) | `security-threat-modeling.md`, `secure-coding-standards.md`, `api-security.md`, `infra-cloud-security.md`, `incident-response.md`, `security-scoring.md` |
| E-commerce & Payments | ✅ Built | 6 | `data/ecommerce/*.csv` | `stripe-integration.md`, `shopify-integration.md` |
| UI/UX & Distinctive Frontend | ✅ Built | 7 | `data/ui-ux/*.csv` (124 rows) | `ui-ux-quickref.md`, `frontend-distinctiveness.md` (flagship), `reference-site-analysis.md` |
| SEO | ✅ Built | 8 | `data/seo/*.csv` (112 rows) | `seo-technical.md`, `seo-content-eeat.md`, `seo-scoring-system.md` |
| Ads | ✅ Built | 9 | `data/ads/*.csv` (74 rows) | `ads-google.md`, `ads-meta.md`, `ads-other-platforms.md`, `ads-scoring-system.md` |
| AI Integration | ✅ Built | B1 | `data/ai/*.csv` (43 rows) | `ai-integration.md`, `ai-security.md` |
| Analytics | ✅ Built | B2 | `data/analytics/*.csv` (34 rows) | `analytics-measurement.md` |
| Email | ✅ Built | B3 | `data/email/*.csv` (34 rows) | `email-integration.md` |
| i18n / Localization | ✅ Built | B4 | `data/i18n/*.csv` (34 rows) | `i18n-localization.md` |

Update this table (and the mirrored summary in `SKILL.md`) in the same edit whenever a module ships. Never let the two drift.

## Action → Module Map

| Action | Trigger phrases (examples) | Primary module(s) | What's loaded |
|---|---|---|---|
| `plan` | "plan this app", "what stack should I use", "architecture for X" | Backend (stack selection) + Database + DevOps | All three module-backed — `backend-architecture.md` (Stack Decision Tree), `database-schema-design.md`, `deployment-platforms.md` |
| `build` | "build the API", "scaffold backend", "implement endpoint" | Backend | — (built) |
| `design` | "design the UI", "make this look unique", "landing page design", "make it look like <site>" | UI/UX & Distinctive Frontend | Module-backed — always load `references/frontend-distinctiveness.md` for brand-forward work (marketing/landing/portfolio pages); `ui-ux-quickref.md` for color/type/UX fundamentals; `scripts/ui-ux/generate.py` to scaffold tokens/skeletons from a chosen palette+pairing; if the user supplies example site URL(s), also `references/reference-site-analysis.md` + `scripts/ui-ux/scan.py` (`--brief` drafts the Reference Design Brief) |
| `integrate` | "add auth", "connect database", "add Stripe" | Database & Auth / E-commerce | Both module-backed — Database & Auth (`database-schema-design.md`, `auth-patterns.md`, `scripts/database/generate.py`) and E-commerce (`stripe-integration.md`, `shopify-integration.md`, `scripts/ecommerce/generate.py`) |
| `deploy` | "deploy to Vercel", "set up CI/CD" | DevOps & Deployment | Module-backed (`ci-cd-pipelines.md`, `deployment-platforms.md`, `env-secrets-management.md`, `scripts/devops/generate.py`) — combine with the connected Vercel/Netlify/Cloudflare MCP tools directly |
| `test` | "write tests", "test coverage", "e2e strategy" | Testing/QA | Module-backed (`testing-strategy.md`, `accessibility-performance-audit.md`, `scripts/testing/generate.py`) |
| `secure` | "security audit", "OWASP check", "is this safe to ship" | Security/Cybersecurity | Module-backed: 134 checks across OWASP, threat modeling, secure coding, API security, infra/cloud, supply-chain, incident response — plus `scripts/security/audit.py` (static scan) and `scripts/common/score.py` (posture scoring) |
| `integrate-payments` | "add Stripe", "Shopify checkout" | E-commerce & Payments | Module-backed (`stripe-integration.md`, `shopify-integration.md`, `scripts/ecommerce/generate.py`) + Shopify MCP tools |
| `optimize-seo` | "SEO audit", "improve rankings" | SEO | Module-backed: 112 checks across technical, on-page, content/E-E-A-T, schema-type selection, and local SEO (`data/seo/*.csv`), plus `scripts/common/score.py` for posture scoring |
| `launch-ads` | "set up ads", "ad campaign" | Ads | Module-backed: 74 checks across Google, Meta, LinkedIn/TikTok/Microsoft, cross-platform tracking/attribution, and creative/budget discipline (`data/ads/*.csv`), plus `scripts/common/score.py` |
| `integrate-ai` | "add AI to the app", "chatbot feature", "Claude API", "add RAG/LLM feature" | AI Integration | Module-backed (`ai-integration.md`, `ai-security.md`, `data/ai/*.csv`, `scripts/ai/generate.py`) — always pair with the LLM security checklist before shipping user-facing AI |
| `measure` | "add analytics", "set up GA4/PostHog", "track conversions", "funnel/retention analysis" | Analytics | Module-backed (`analytics-measurement.md`, `data/analytics/*.csv`, `scripts/analytics/generate.py`, `scripts/common/score.py`) — paid-media tracking overlaps live in the Ads module (`ADS051–ADS064`) |
| `integrate-email` | "send emails", "password reset email", "newsletter setup", "deliverability/DMARC/SPF" | Email | Module-backed (`email-integration.md`, `data/email/*.csv`, `scripts/email/generate.py`, `scripts/common/score.py`) — always separate transactional and marketing streams (EM007) |
| `localize` | "add another language", "i18n this app", "multi-language site", "hreflang setup" | i18n / Localization | Module-backed (`i18n-localization.md`, `data/i18n/*.csv`, `scripts/i18n/generate.py`, `scripts/common/score.py`) — hreflang/no-forced-redirect rules are shared with the SEO module (`SEO019`/`SEO020`) |
| `review` / `audit` | "review this codebase", "full audit", "pre-launch check" | Cross-module | `references/workflows.md` — Complete SaaS Launch, Client Delivery Package, Pre-Launch Audit, and Security Hardening Pass chains, combining every module's checks/scripts |

## Graceful Degradation Rule

All 13 modules are now built (Phases 0-9 + B1-B4 complete) — every row in the table above is module-backed. If a future module is ever added to this skill and marked 🔜 Planned, the same rule applies: still help using general best practice, never refuse, but say explicitly the answer isn't backed by this skill's own checklist/data yet, so the user knows the difference between "verified against our checklist" and "general knowledge."

## Cross-Module Workflows

Four documented chains live in [`workflows.md`](workflows.md): Complete SaaS Launch, Client Delivery Package, Pre-Launch Audit, and Security Hardening Pass. Load it for any request spanning more than one module.
