> Last updated: 2026-07-03 · Module version: 0.2

# Infrastructure & Cloud Security

Pairs with `data/security/infra-cloud-security-checks.csv` (17 checks) — query via `scripts/common/search.py`. Covers the platform/infrastructure layer beneath the application code covered by `secure-coding-standards.md` and `api-security.md`.

## Supply Chain — a 10-check addition (`data/security/supply-chain-checks.csv`, SEC125-SEC134)

Known-vulnerable dependencies are the most common real-world breach vector, and it's nearly free to automate a defense: **automated scanning on every PR** (`SEC125`), **enforced lockfiles** (`npm ci`, not `npm install`, `SEC126`), and a lightweight review pass before adding any new package — most supply-chain compromises land through a small unreviewed dependency, not a headline framework (`SEC127`). Pin security-sensitive packages (auth, crypto, payments) to exact versions, not caret ranges (`SEC128` — several real npm attacks propagated through auto-accepted patch updates). In CI/CD: scope secrets per job (`SEC130`, Critical), pin third-party GitHub Actions to a commit SHA not a floating tag (`SEC131`), and verify deployed artifacts trace back to a reviewed commit (`SEC132`). Generate an SBOM per release so a disclosed CVE can be answered in minutes, not hours (`SEC133`), and set an actual SLA for patching disclosed vulnerabilities — scanning without a response SLA just produces an ignored backlog (`SEC134`). Cross-references `AI042`'s SDK-pinning guidance in the AI Integration module.

## Access Management — the Highest-Leverage Category

Platform/dashboard access (Vercel, Supabase, Cloudflare, GitHub) is often a higher-value compromise target than an application-level vulnerability, since it can touch deploy pipelines, secrets, and infrastructure directly:
- **Least-privilege IAM per service** (`SEC091`) — no shared/broad admin credential used for convenience.
- **MFA required on every platform account with production access** (`SEC092`), not just the primary owner.
- **Offboarding revokes access same-day, across every platform** (`SEC093`) — stale access from a departed team member is entirely preventable and commonly found only during an audit, if ever.
- **Production database access uses a distinct, more restricted credential than staging/dev** (`SEC094`).

## Network Exposure

- **Database never directly internet-reachable without restriction** (`SEC095`) — restrict to the application's network/VPC, a connection pooler, or an explicit allowlist. This should never depend solely on credential strength.
- **Internal/admin tooling not on the public internet by default** (`SEC096`) — "nobody will find it" is not a security control; internal tools held to a lower bar than the customer-facing app are a common, specifically-targeted gap.

## Backups — Verify, Don't Assume

**Automated backups exist and are periodically restored, not just scheduled** (`SEC101`) — a backup job reporting success and a backup actually being restorable are different claims; the gap between them is discovered during a real incident if it's never tested. Backups are also exactly as sensitive as the production data they contain and need equivalent access control (`SEC102`), not looser protection as a lower-scrutiny artifact.

## Container/Serverless-Specific

If containerized: minimal, current base images (`SEC098`) and non-root execution (`SEC099`) — running as root inside a container means a container-escape vulnerability grants root on the host. If serverless: scope each function's execution role to only what that specific function needs (`SEC100`) — a shared execution role across all functions means one function's vulnerability has every function's combined permissions.

## DNS and Domain — Underrated Severity

Domain hijacking is a severe, high-impact attack: losing control of the domain can redirect all traffic, intercept email, and undermine every other control on the application. Registrar account MFA and registrar/transfer lock (`SEC104`) are cheap, high-leverage protections. Also audit DNS records periodically for stale entries pointing at decommissioned services (`SEC105`) — classic subdomain-takeover setup.

## Environment Separation

Production and non-production infrastructure should be **meaningfully** separated (`SEC107`) — separate database instances, ideally separate cloud project/account — not just a different table prefix or env var within otherwise-shared infrastructure. Logical-only separation means a bug or compromise in the lower-scrutiny non-production environment has a direct path to production resources.

## Connecting to This Environment's MCP Tools

Several checks here map directly to MCP tools that may be connected in your environment:
- `SEC092`/`SEC093` (platform access/offboarding) — periodically review team access via each platform's dashboard/API.
- `SEC095` (database network exposure) — use Supabase's `get_advisors` to catch exposed-database and related lint findings.
- `SEC101` (backup verification) — Supabase's `restore_project`/branching tools can be used to periodically rehearse a restore.
- `SEC106` (CI/CD credential scoping) — verify Vercel/Netlify/Cloudflare deploy tokens used in CI are scoped service credentials, not a developer's personal login.
