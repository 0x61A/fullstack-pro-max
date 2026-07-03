> Last updated: 2026-07-03 · Module version: 0.1

# Deployment Platforms

Pairs with `data/devops/platforms.csv` (17 rows covering hosting, database hosting, storage, background jobs, CDN, and region strategy) — query via `scripts/common/search.py`.

## Hosting Decision

1. **Next.js app, or any frontend framework wanting zero-config git-integrated deploys with preview URLs?** → **Vercel** (`DO026`) — the default recommendation, matching this skill's default stack. Use the connected Vercel MCP directly for deploys, build logs, and project management (`deploy_to_vercel`, `get_deployment_build_logs`, `list_projects`).
2. **Static/JAMstack site across a non-Next.js framework, or want a mature framework-agnostic platform?** → **Netlify** (`DO027`), via the connected Netlify MCP.
3. **Need global edge latency, or want to consolidate on Cloudflare's ecosystem (Workers, D1, KV, R2)?** → **Cloudflare Pages/Workers** (`DO028`), via the connected Cloudflare MCP — but check package compatibility with the Workers runtime (V8 isolate, not full Node) before committing.
4. **Need a persistent process** (WebSocket server, long-running worker, traditional Express/Nest.js/Django app that doesn't fit the serverless request/response shape)? → **Railway / Render / Fly.io** (`DO029`) for a Docker-based deploy without managing raw infrastructure.
5. **Specific compliance/data-residency requirement, or very high sustained predictable traffic where reserved infra beats pay-per-use?** → **Self-managed VPS/Kubernetes** (`DO030`) — only when a concrete requirement demands it; the ongoing operational burden is real and most projects this skill targets shouldn't take this on prematurely.

Default for a project with no strong constraint: **Vercel**, matching the Next.js default from `backend-architecture.md`'s Stack Decision Tree.

## Database & Storage Hosting

- **Already using Supabase as the BaaS?** → its managed Postgres is the natural default (`DO031`) — database, auth, storage, and realtime in one platform, with MCP tooling available when connected.
- **Want a plain managed relational database with git-like branching for preview environments?** → Neon or PlanetScale (`DO032`).
- **On Cloudflare Workers and need to reach a traditional Postgres/MySQL (not D1)?** → Cloudflare Hyperdrive (`DO033`) for connection pooling from a request-scoped runtime.
- **File uploads/object storage?** → default to the platform-native option (Supabase Storage, Cloudflare R2, Vercel Blob — `DO034`) unless a specific region/compliance/scale requirement points at S3 (`DO035`). R2 specifically has zero egress fees, a meaningful cost difference at scale.

## Background Jobs

- **Simple scheduled task** (nightly report, cleanup job)? → platform-native cron (`DO036`: Vercel Cron, Supabase Edge Function cron, Cloudflare Cron Triggers).
- **Real job workload** needing retries, backoff, concurrency control, or a dead-letter queue (`BE074`)? → a managed queue service (`DO037`) — don't try to force this shape onto a scheduled function.

## Serverless vs. Traditional — the Recurring Question

Default to **serverless/edge functions** (`DO041`) for anything fitting the request/response shape — no infrastructure to manage, true scale-to-zero cost. Reach for a **traditional long-running process** (`DO042`) specifically when the workload needs persistent connections (WebSockets), sustained CPU/memory beyond function limits, or in-memory state across requests. This mirrors the `BE065`/`data/backend/api-patterns.csv` guidance — don't re-litigate it separately per module, the answer is the same reasoning applied to infrastructure choice.

## Multi-Region: Default to No

Start single-region, close to your primary user base (`DO040`). Multi-region adds real complexity (which region is the source of truth for a write? how do you handle replication lag?) that the overwhelming majority of projects this skill targets don't need. Add it only in response to measured latency data showing a real user-facing problem in specific regions — never as a default architectural assumption for a new project.

## Domain & CDN

Keep domain/DNS management on the same platform as hosting where offered (`DO039`) — one fewer dashboard, faster SSL provisioning. CDN comes bundled with Vercel/Netlify/Cloudflare by default (`DO038`) — don't add a separate CDN layer unless a specific need (highly custom cache-key logic, an existing enterprise CDN relationship) isn't met by the bundled one.

## Using the Connected MCP Tools

This environment already has Vercel, Netlify, Cloudflare, and Supabase MCP servers connected — use them directly rather than walking the user through dashboard clicks:
- Vercel: `deploy_to_vercel`, `get_deployment`, `get_deployment_build_logs`, `list_projects`, `get_runtime_logs`, `get_runtime_errors`.
- Cloudflare: Workers/D1/KV/R2 management tools (`workers_get_worker`, `d1_database_query`, `kv_namespace_*`, `r2_bucket_*`).
- Supabase: `apply_migration`, `execute_sql`, `list_tables`, `get_advisors`, project/branch management.
- Netlify: deploy and project services readers/updaters.
