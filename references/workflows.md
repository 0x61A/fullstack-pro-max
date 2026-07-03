> Last updated: 2026-07-03 · Module version: 0.1

# Cross-Module Workflows

Multi-step chains combining the action-routing table in `SKILL.md`. Every module referenced below is built (Phases 0-9 complete) — none of these chains hit a placeholder. Before starting any of these, apply **"Ask Before You Build"** from `SKILL.md` — confirm stack, scope, and any irreversible steps before executing them, don't run a whole chain silently on assumptions.

## Workflow 1: Complete SaaS Launch (0 → production)

For a new product being built from scratch, personal or client:

1. **`plan`** — confirm the stack via the Stack Decision Tree (`backend-architecture.md`) and `data/backend/stacks.csv`. Ask the 2-4 clarifying questions from "Ask Before You Build" if the user hasn't already stated a preference. Default: Next.js + Supabase absent a reason otherwise.
2. **`build`** — scaffold the backend/API (`scripts/backend/generate.py`), following `api-design.md`'s conventions (pagination, error taxonomy, idempotency).
3. **`integrate`** (database & auth) — design the schema (`database-schema-design.md`), choose the auth pattern (`auth-patterns.md`), scaffold migrations (`scripts/database/generate.py` with `--rls` for any multi-tenant table).
4. **`design`** — before shipping any brand-forward page, load `frontend-distinctiveness.md` and pick 2-3 techniques to apply systemically (not one of everything). Run the `UX067` competitive-comparison self-check before calling the UI done.
5. **`secure`** — run the OWASP + secure-coding checklist relevant to the stack chosen in step 1 (`secure-coding-standards.md`). Scaffold security headers (`scripts/security/generate.py`). Run the static scan (`scripts/security/audit.py`) before considering this step complete.
6. **`test`** — write tests for critical journeys per `testing-strategy.md`'s pyramid (`scripts/testing/generate.py`), and run the accessibility/performance checklist (`accessibility-performance-audit.md`).
7. **`deploy`** — scaffold CI/CD (`scripts/devops/generate.py`), choose the hosting platform per `deployment-platforms.md`, confirm env/secrets discipline (`env-secrets-management.md`) before the first real deploy.
8. **`integrate-payments`** (if applicable) — Stripe or Shopify per `stripe-integration.md`/`shopify-integration.md`, scaffold the webhook handler (`scripts/ecommerce/generate.py`), and confirm test-mode keys are in use until explicitly ready to go live.
9. **`optimize-seo`** — run the technical + on-page checklist (`seo-technical.md`) before launch, not after — `SEO029`'s migration/launch redirect discipline applies to a first launch too if replacing an existing site.
10. **`launch-ads`** — only after `secure` and `optimize-seo` have run; confirm conversion tracking (`ADS001`/`ADS002`-equivalent for the chosen platform) is verified working before spending real budget.

## Workflow 2: Client Delivery Package (agency use case)

For delivering a finished product to a client, with a defined handoff point:

1. Run **Workflow 1** in full through step 9.
2. **`review`/`audit`** — run `scripts/common/score.py` against `data/security`, `data/seo`, and (if ads were set up) `data/ads` to produce three posture scores for the delivery report — see `security-scoring.md`/`seo-scoring-system.md`/`ads-scoring-system.md` for the shared formula.
3. Package the three scores plus a short "what's built vs. what the client should monitor going forward" note (test-mode payment keys still active? DNS/domain access handed off? who owns credential rotation post-handoff — see `SEC093` offboarding guidance, applied in reverse to a *new* access grant).
4. If continuing to `launch-ads` post-handoff, confirm who owns ad account access and billing before campaigns go live.

## Workflow 3: Pre-Launch Audit (existing project, about to ship)

For a project that's already built and is about to go live or relaunch:

1. **`secure`** — run the full security module: `data/security/owasp-checklist.csv` + `secure-coding-checks.csv` + `api-security-checks.csv` at minimum. Run `scripts/security/audit.py` against the actual codebase. Score the result with `scripts/common/score.py`.
2. **`test`** — run the accessibility/performance checklist (`accessibility-performance-audit.md`) — this is fast to check and catches the most user-visible pre-launch issues.
3. **`optimize-seo`** — run `technical-seo-checks.csv` in full; if this is a migration/relaunch (not a first launch), `SEO029`'s redirect-map requirement is Critical severity, not optional.
4. **`review`** — aggregate: any Critical-severity finding across security or SEO should block launch until resolved or explicitly accepted as a known risk by the person with authority to accept it — don't let a Critical finding pass silently because the score was "still pretty high" (see `security-scoring.md`'s note on this exact interpretation trap).

## Workflow 4: Security Hardening Pass (standalone)

For an existing project getting a dedicated security review, independent of a launch:

1. Run **`secure`**'s full checklist set (all 6 CSVs in `data/security/`), not just OWASP — threat modeling (`security-threat-modeling.md`) if the project has grown new data flows since it was last reviewed, secure coding (`secure-coding-standards.md`), API security (`api-security.md`) if it exposes an API, infra/cloud security (`infra-cloud-security.md`).
2. Run `scripts/security/audit.py` against the real codebase and treat any Critical/High finding as a required fix, not a suggestion (the script itself exits non-zero on these, making it CI-gateable — see `SKILL.md`'s Scripts section).
3. Score with `scripts/common/score.py` and record the result for tracking posture over time (`security-scoring.md`).
4. If this is the project's first-ever security pass, also walk `incident-response.md`'s preparedness checklist (`SEC108`-`SEC112`) — a plan should exist *before* it's needed, and a hardening pass is a natural moment to establish one if it doesn't exist yet.

## Notes on Chaining Actions

- Every step above references files that exist today — if a future addition to this skill ever adds a step that isn't built yet, say so explicitly rather than silently skipping it (same rule as "Ask Before You Build" and the graceful-degradation note in `routing.md`).
- These workflows are starting points, not rigid scripts — skip steps that don't apply (no e-commerce component, no ads spend planned) and adjust order when the project's actual constraints demand it (e.g. security review before design finalization for a genuinely high-risk data type).
- `scripts/common/score.py` and `scripts/common/search.py` work identically across Security, SEO, and Ads — once familiar with one module's scoring/search pattern, the same commands apply to the others with just a different `data/` path.
