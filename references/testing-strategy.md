> Last updated: 2026-07-03 · Module version: 0.1

# Testing Strategy

Pairs with `data/testing/test-strategy.csv` (25 rows) — query via `scripts/common/search.py`.

## The Shape to Default To

**Testing pyramid** (`QA001`): many fast unit tests at the base, fewer integration tests in the middle, few end-to-end tests at the top covering only genuinely critical journeys (`QA011`) — signup, login, checkout/payment, the core value-delivering action of the product. Don't invert this; a suite dominated by e2e tests is slow and flaky in CI.

## Per-Layer Tooling (matches this skill's backend stack choices)

| Layer | Node.js/TypeScript | Python |
|---|---|---|
| Unit | Vitest (Vite-based projects) or Jest (`QA003`) | pytest (`QA004`) |
| Component | React/Vue Testing Library (`QA005`) — query by role/text, not implementation detail | — |
| Integration/API | Supertest for in-process HTTP assertions (`QA007`); a real test database, not a mock (`QA006`) | FastAPI `TestClient` (`QA022`); pytest-django with per-test transaction rollback (`QA023`) |
| E2E | Playwright (`QA009`, default recommendation — multi-browser, auto-waiting, built-in trace capture) or Cypress (`QA010`) if already invested there | Playwright (language-agnostic) |

Framework-specific notes: Next.js apps should test Route Handlers/server logic directly without a browser and reserve Playwright for flows that genuinely cross both server and client (`QA021`). Supabase-backed apps should test RLS-dependent logic against a real local Supabase instance or a dedicated test project/branch (`QA024`) — a mocked database can't verify a Postgres policy actually behaves as intended.

## Practices That Matter More Than Tool Choice

- **Mock the boundary, not your own code** (`QA012`) — mock third-party services (Stripe, email providers), not your own business logic; a test that only verifies a mock was called isn't testing the real code path.
- **Test data via factories, not hand-copied fixtures** (`QA013`) — one factory function per entity, overridable per test, so a schema change means updating one place instead of every test file.
- **Test isolation is non-negotiable** (`QA020`) — no test should depend on execution order or shared mutable state; this is also the precondition for parallelizing CI test execution (`QA019`).
- **Fix or delete flaky tests immediately** (`QA017`) — a flaky test left to linger trains the team to ignore future real failures too; there's no acceptable steady state where "that one's just flaky."
- **Coverage is a signal for finding gaps, not a target to hit** (`QA018`) — a rigid numeric threshold enforced without judgment produces low-value tests written purely to satisfy the number.
- **Contract tests when frontend/backend deploy independently** (`QA015`) — skip this for a tightly-coupled monorepo (e.g. Next.js) where both sides always deploy together and can't drift.

## When to Reach for Load Testing

Only around a known event — a launch, a campaign, a seasonal spike (`QA016`) — not as a routine CI habit. The goal is confidence before a specific high-stakes moment, not continuous overhead on every PR.

## TDD — Selectively, Not Dogmatically

Write the failing test first specifically when **fixing a reported bug** (`QA025`) — this guarantees the bug can never silently regress. Full TDD discipline for all new feature development is optional; exploratory work where the solution shape is still unclear often doesn't benefit from writing tests against code that will be reworked.

## Scaffolding

`scripts/testing/generate.py` (this module) scaffolds a test file skeleton for a named resource in the project's testing framework — see the Scripts section of `SKILL.md`.
