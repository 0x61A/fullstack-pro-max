> Last updated: 2026-07-03 · Module version: 0.1

# Environment & Secrets Management

Pairs with `data/devops/env-management.csv` (13 rows) — query via `scripts/common/search.py`.

## The Non-Negotiable Baseline

Every project, no exceptions:
1. **`.env.example` committed, `.env` gitignored** (`DO045`) — every required variable documented by name and purpose in the template, real values never in git.
2. **Never commit a real secret, even temporarily** (`DO046`) — a secret removed in a later commit is still in git history and must be treated as compromised. Use pre-commit scanning (`scripts/security/audit.py`, Phase 5) to catch this before it happens.
3. **Validate all required env vars at startup, fail fast** (`DO047`, also `BE081`) — a missing variable should crash the process immediately with a clear message, never surface as a confusing runtime error three requests later.

## Build-Time vs. Runtime — the Most Common Real Leak

This is the single most common real-world way a secret ends up exposed in a shipped product, so it gets its own emphasis: frontend frameworks bake certain env vars directly into the **client-visible JavaScript bundle** at build time (Next.js `NEXT_PUBLIC_*`, Vite `VITE_*`). Anything with that prefix is visible to anyone who opens browser devtools — no exception, no obfuscation.

- Only genuinely public values belong behind a public prefix: a publishable/anon key designed for client use (Stripe publishable key, Supabase anon key), a public API base URL.
- Everything else — database credentials, service role keys, private API keys — stays server-only, read via a plain (non-prefixed) env var, never passed as a prop into client-rendered code.
- Before adding a new env var, explicitly ask: *is this meant to be public, or did it just get the public prefix by copy-paste habit?* That one-second check is what prevents this class of leak.

## Where Secrets Live

Default: the hosting platform's own environment variable store, scoped per environment (production/preview/development) — Vercel/Netlify/Cloudflare dashboards or their MCP/CLI equivalents (`DO043`). This is sufficient for the overwhelming majority of projects this skill targets. Escalate to a dedicated secrets manager (`DO044`) only for larger orgs needing centralized rotation/audit across multiple services beyond a single hosting platform.

## Scoping

- **Least privilege per credential** (`DO052`): a CI deploy token, a database user, a third-party API key should have only the specific permissions the thing using it actually needs.
- **Separate credentials per environment** (`DO052`, `DO053`): a staging database credential should never also work against production; every third-party integration (Stripe, Shopify, email providers) should have distinct dev/staging/production keys wherever the provider supports it — this is what prevents a test run from accidentally charging a real card or sending a real email.
- **CI pipeline secrets are a distinct set from runtime application secrets** (`DO054`) — a compromised CI pipeline shouldn't automatically have the same blast radius as a compromised running application.

## Rotation

Rotate on a schedule as baseline hygiene, and **immediately, unconditionally, after any suspected exposure** (`DO051`) — "we're not sure it was actually leaked" is not a reason to delay rotation. Build/verify the rotation capability before you need it urgently during an actual incident, not while scrambling during one.

## Documentation

Note where each secret comes from and who can regenerate it (`DO055`) — even for a solo project, write this down before there's a second contributor. This is what turns a rotation-under-pressure scenario (post-incident, or an offboarding teammate) into a five-minute lookup instead of an investigation.

## `.env.example` Generation

`scripts/devops/generate.py` (this module) scaffolds a `.env.example` file alongside a CI workflow — see the Scripts section of `SKILL.md`.
