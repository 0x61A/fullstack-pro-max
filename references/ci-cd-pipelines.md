> Last updated: 2026-07-03 · Module version: 0.1

# CI/CD Pipelines

Pairs with `data/devops/ci-cd-patterns.csv` (25 rows) — query via `scripts/common/search.py`.

## Default Pipeline Shape

For most projects on this skill's default stack, recommend this pipeline shape unless something specific points elsewhere:

1. **On every PR**: lint → typecheck → unit/integration tests → build (`DO003`) — all required checks, none skippable, cached dependencies (`DO004`) to keep this fast.
2. **On every PR (if on Vercel/Netlify/Cloudflare Pages)**: automatic preview deployment (`DO009`) — reviewers click through the real thing, not just a diff.
3. **On merge to `main`**: the same checks re-run, then continuous deployment to production (`DO007`) — no manual approval gate unless a specific compliance requirement demands one (`DO008`).
4. **As part of the deploy step**: database migrations run automatically (`DO013`), ordered *before* traffic shifts to the new application version, using the zero-downtime discipline from `database-schema-design.md`.
5. **Immediately after deploy**: automated smoke test against a handful of critical endpoints/pages (`DO014`), with auto-rollback on failure where the platform supports it (`DO015`).

## Branch Strategy

Default to **trunk-based development** (`DO001`) for the projects this skill targets — small-to-mid teams, continuous deployment. Merge to `main` directly (via short-lived feature branches + PR review), hide incomplete work behind feature flags (`DO012`) rather than long-lived branches. Reach for Git Flow (`DO002`) only when there's a real scheduled-release cadence with a formal release-candidate testing phase — that's rare for the agency/SaaS projects this skill is built around.

## What Every Pipeline Needs, Regardless of Stack

- **Four required PR gates**: lint, typecheck, test, build (`DO003`). This is the floor, not a suggestion.
- **Dependency caching** (`DO004`) keyed on the lockfile hash — usually the single biggest CI-speed win available.
- **Secrets in the platform's secret store, never in the repo** (`DO018`) — see `env-secrets-management.md` for the full discipline.
- **Automated dependency updates** (`DO017`) — security patches shouldn't wait for someone to remember to check.
- **Deploy/CI-failure notifications** to wherever the team actually looks (`DO022`) — a broken `main` sitting unnoticed for hours is worse than the notification noise of announcing it.

## Monorepo-Specific Guidance

If the project is a monorepo (multiple apps/packages in one repo):
- Only build/test **affected** packages per PR (`DO006`), not the entire repo — this is the difference between a monorepo staying fast and a monorepo where every PR takes 20 minutes regardless of what changed. Use Turborepo or Nx's dependency-graph-aware task running rather than hand-rolling change detection.
- Deploy each app **independently** based on what actually changed (`DO019`), not as one unit, unless they genuinely always ship together.

## Rollback

Prefer **redeploying the last known-good build** (`DO024`) on platforms with immutable deploy artifacts (Vercel, Netlify, Cloudflare Pages) — this is the fastest possible rollback since no rebuild is needed. Fall back to **git revert + redeploy** (`DO025`) on infrastructure without that concept, or when the rollback also needs to revert a database migration (immutable-artifact rollback alone won't undo a schema change).

## Versioning and Dependency Hygiene

- Semantic versioning + automated changelog generation (`DO016`) matters for libraries/APIs with external consumers — skip the ceremony for internal-only continuously-deployed apps with no external version consumers.
- Automated dependency-update PRs (`DO017`) should run on every project; tune the *policy* (auto-merge patch/security updates, batch and review minor/major) rather than skipping the practice.

## Full detail

The full 25-row decision matrix (deployment strategies, canary/blue-green, IaC, build-performance caching) is in `data/devops/ci-cd-patterns.csv`. Platform-specific choices (Vercel vs Netlify vs Cloudflare vs containers) are in `deployment-platforms.md` and `data/devops/platforms.csv`.
