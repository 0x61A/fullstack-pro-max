> Last updated: 2026-07-03 · Module version: 0.1

# Auth Patterns

Pairs with `data/database/auth-patterns.csv` (25 rows covering session strategy, passwordless, MFA, authorization models, and managed providers) — query via `scripts/common/search.py`. This file is the decision framework connecting those rows.

## Choosing a Session Strategy

1. **Server-rendered app or same-origin SPA?** → HTTP-only session cookie (`DB031`). Simplest, browser-managed, needs CSRF protection.
2. **Stateless API, mobile app, or serverless/edge function?** → JWT access token (`DB032`), paired with refresh token rotation (`DB033`) so the short-lived access token limits blast radius while the user stays logged in.
3. **Never** ship a long-lived JWT with no refresh/rotation strategy as "the whole auth system" — either add rotation or move to session cookies if you don't actually need statelessness.

## Choosing a Primary Login Method

Default recommendation for a new consumer product: **magic link (`DB034`) or passkeys (`DB036`) as the primary method**, not password-first. Passwords bring password-reset support burden, reuse/breach risk, and hashing implementation risk that passwordless methods sidestep entirely. Reach for traditional password auth (`DB037`, Argon2id specifically) only when there's a real constraint pushing that direction — enterprise buyer expectation, offline-capable login requirement, or a user base that specifically expects it.

If passwords are used:
- Hash with **Argon2id** (`DB037`) — never MD5/SHA1/plain bcrypt-if-avoidable for new systems, never roll your own.
- Password reset via a **time-limited, single-use token** (`DB038`), 15–60 minutes, invalidated after first use.
- **Invalidate all existing sessions on password change** (`DB039`) — this is the step most commonly forgotten, and it's the one that actually closes the loop on a compromised-session scenario.
- **Rate limit login attempts** (`DB040`) by IP and by account — credential stuffing targets exactly this endpoint.

## MFA — When and How

Offer MFA, don't force it, for most consumer products — require it for admin/high-privilege accounts and anything touching money or sensitive data. TOTP via an authenticator app (`DB041`) is the recommended default second factor: free, offline-capable, broadly supported. SMS (`DB042`) is acceptable as an *additional* option for adoption, never as the only MFA method for a high-value account, due to SIM-swap risk. **Always ship recovery codes** (`DB043`) alongside any MFA method — an MFA system with no recovery path turns a lost phone into a support ticket that becomes a full account lockout.

## Authorization: Don't Confuse "Logged In" With "Allowed"

Authentication answers "who is this." Authorization answers "may this specific principal do this specific thing to this specific resource" — a distinct question that must be checked on every request, not inferred from the presence of a valid session.

Three authorization models, in order of typical adoption:
1. **Role-Based Access Control** (`DB047`) — the right starting point for most apps. A handful of roles (admin/editor/viewer) map cleanly to permission sets.
2. **Row-Level Security as the enforcement layer** (`DB046`) — on Supabase/Postgres, push the actual enforcement into the database via RLS policies rather than only checking roles in application code. This means a bug in one API endpoint can't accidentally leak data the way an app-layer-only check can; see `database-schema-design.md` for the schema-side half of this pattern.
3. **Attribute/Policy-Based Access Control** (`DB048`) — only once RBAC's fixed roles genuinely can't express a real requirement (permissions depending on multiple dynamic attributes at once). Don't start here; it's harder to audit at a glance than a role list.

**Never trust a client-supplied identifier for authorization** — derive the acting user from the verified session/token server-side, never from a `userId` field in the request body (this is also called out in `api-design.md`'s security baseline).

## Service-to-Service and Machine Identity

Distinct from end-user auth: when one of your own services, or a third-party integrator, needs to call your API without an interactive user present.
- **API keys** (`DB050`) — simplest, works everywhere, but is a long-lived bearer credential: scope it minimally, support rotation, never expose client-side.
- **OAuth client-credentials grant** (`DB051`) — short-lived tokens instead of a static key, worth the extra setup when both sides already support OAuth and the credential's blast radius matters.

## Build vs. Buy

| Situation | Recommendation |
|---|---|
| Already on Supabase | **Supabase Auth** (`DB052`) — session state integrates directly with RLS (`auth.uid()` available in policies), removing a whole category of "app auth and DB authorization drift apart" bugs. |
| Mobile-first, already on Firebase | **Firebase Auth** (`DB053`). |
| Next.js app, want full control, no per-MAU cost | **NextAuth.js / Auth.js** (`DB054`) — self-hosted, DB-agnostic, many OAuth providers built in. |
| Pre-PMF, want zero auth implementation work, MFA/SSO/breach-detection built in | **Auth0 / Clerk / WorkOS** (`DB055`) — fastest to production, but priced per monthly active user; revisit at scale. |
| B2B selling to enterprise, customer IT requires centralized identity | **SSO via SAML/OIDC** (`DB045`) — often a hard requirement to close enterprise deals; don't build this speculatively before a real deal needs it. |

Default when nothing above strongly applies and the project is already on the skill's default stack (Next.js + Supabase): **Supabase Auth**, for the RLS-integration reason above.

## Common Mistakes This Section Exists to Prevent

- Shipping JWTs with no expiry or no revocation story at all.
- Checking `if (user)` and calling that "authorization" instead of checking whether *this* user may act on *this* resource.
- Building password reset without single-use, time-limited tokens.
- MFA with no recovery-code path.
- Trusting a `role` or `userId` field the client sent in a request body instead of deriving it from the verified token/session server-side.
