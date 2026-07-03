> Last updated: 2026-07-03 · Module version: 0.1

# Secure Coding Standards

Pairs with `data/security/owasp-checklist.csv` (35 checks, OWASP Top 10 mapped) and `data/security/secure-coding-checks.csv` (20 checks, per-stack) — query both via `scripts/common/search.py`.

## OWASP Top 10 — the Non-Negotiable Floor

Every one of these gets checked on every project this skill touches, regardless of how small. The five most consistently critical in practice:

1. **Broken Access Control (A01)** — authorization checked server-side on every request, not inferred from what the UI shows (`SEC001`), no insecure direct object references (`SEC002`), default-deny for new endpoints (`SEC003`).
2. **Injection (A03)** — every query parameterized, never string-concatenated (`SEC009`); user input never reaches eval/exec/shell (`SEC010`); framework auto-escaping stays enabled (`SEC012`).
3. **Cryptographic Failures (A02)** — passwords hashed with Argon2id, never encrypted (`SEC006`); no hardcoded secrets in source, ever (`SEC007`).
4. **Security Misconfiguration (A05)** — no default credentials in production (`SEC015`), verbose errors disabled (`SEC016`), security headers set on every response (`SEC018`).
5. **Server-Side Request Forgery (A10)** — server-side requests to user-supplied URLs validated against an allowlist, cloud metadata endpoint blocked (`SEC029`, `SEC030`).

Full mapping of all ten categories to concrete checks is in `data/security/owasp-checklist.csv` — query by category (`A01 Broken Access Control` through `A10 SSRF`, plus `General`).

## Stack-Specific Guidance

**Node.js/TypeScript**: never `eval()`/`new Function()`/`vm` on untrusted input (`SEC058`); guard against prototype pollution when merging user-supplied JSON into objects (`SEC059`); scrutinize new npm packages with postinstall scripts before adding them (`SEC060`).

**Python**: never `eval()`/`exec()`/`pickle.loads()` on untrusted input — pickle deserialization of untrusted data is a direct RCE vector (`SEC061`); never format user input into raw SQL strings even for "just one query" (`SEC062`); always `yaml.safe_load()`, never the default `yaml.load()` (`SEC063`).

**Next.js**: server-only code (DB clients, service-role credentials) must never be importable — even transitively — from a client component (`SEC064`); Middleware auth decisions must verify a signed/httpOnly token, not a plain client-readable cookie (`SEC065`).

**Express/Nest.js**: security middleware (helmet, rate limiting, CORS) applied globally at app level, not per-route opt-in — a per-route model guarantees a future route eventually forgets it (`SEC066`).

**Django**: `DEBUG=False` and `ALLOWED_HOSTS` explicitly verified in production, not assumed (`SEC067`); CSRF protection stays enabled — `@csrf_exempt` is a scoped, reviewed exception, never a global workaround (`SEC068`).

## Database & Client-Side

- **Least-privilege database credentials** per service/purpose (`SEC069`) — a reporting connection doesn't need write access.
- **RLS as the actual multi-tenant boundary**, not solely application-layer filtering (`SEC070`) — a single forgotten `WHERE tenant_id = ?` in app-layer-only enforcement is a cross-tenant leak waiting to happen; this is the security-module reinforcement of `DB015`/`DB030`.
- **Nothing security-relevant lives client-side only** (`SEC071`) — client validation is a UX convenience; re-enforce everything server-side.
- **Prefer httpOnly cookies over localStorage** for session tokens where the auth pattern allows it (`SEC072`) — localStorage is readable by any JS on the page, including a successful XSS payload; httpOnly cookies aren't.

## Process, Not Just Code

- **Security-sensitive PRs get a review pass specifically asking "what could go wrong here"** (`SEC074`), not just functional correctness — this is a different question that's easy to skip without deliberately asking it.
- **Staging gets the same security controls as production** (`SEC075`) when it touches anything resembling real data — "it's just staging" is a common, specifically-targeted gap.
- **Dependencies scanned in CI** (`SEC019`) and **actually kept current** (`SEC020`, `SEC073`) — a vulnerability scanner is only useful if its findings get acted on.

## Using `scripts/security/audit.py`

This module ships a stdlib-only static scanner (see the Scripts section of `SKILL.md`) that greps a project for the most common, mechanically-detectable violations of this checklist: hardcoded-looking secrets (`SEC007`, `SEC056`), missing security headers (`SEC018`), and a handful of dangerous-pattern usages (`eval`, raw SQL string formatting). It is a floor, not a substitute for the judgment-based checks above — a clean scan does not mean the checklist is satisfied.
