> Last updated: 2026-07-03 · Module version: 0.1

# Backend Architecture

Core guidance for the `plan` and `build` actions when the module is Backend & API. Pairs with `data/backend/stacks.csv` (query it via `scripts/common/search.py`) for the full decision matrix — this file explains the *reasoning*, folder conventions, and request lifecycle behind the choices in that CSV.

## Stack Decision Tree

Ask these questions in order; stop at the first one that resolves the choice. Full detail and edge cases live in `data/backend/stacks.csv`.

1. **Does a BaaS (Supabase/Firebase) cover the data + auth + storage needs with little custom logic?**
   → Yes, and the data is relational / needs SQL joins/reporting: **Supabase**.
   → Yes, and the data is document-shaped / needs offline-first mobile sync: **Firebase**.
   → No, custom business logic dominates: continue.

2. **Is the team Python-first, or does the product have an AI/ML/data-pipeline component that benefits from native Python libraries?**
   → Yes, API-first and async-heavy: **FastAPI**.
   → Yes, content/admin-heavy with non-technical staff needing an admin UI: **Django** (+ DRF if the frontend is a separate SPA).
   → No: continue.

3. **Is this a single-team, single-repo full-stack app where frontend and backend can deploy together?**
   → Yes, greenfield, Vercel-hosted: **Next.js API Routes / Route Handlers** (default — see row `BE040`).
   → Yes, and mutations are simple form-style actions with no external API consumers: consider **Next.js Server Actions** instead of a separate route.
   → No, backend must scale/deploy/version independently: continue.

4. **Does the team need enforced structure for a larger, multi-domain backend (billing, users, notifications as separate modules)?**
   → Yes: **Nest.js**.
   → No, minimal and flexible is preferred, team is disciplined: **Express.js** (or **Fastify** if a specific performance requirement is already measured, not assumed).

5. **Does the API need to run at the edge for global low-latency, with simple request/response logic (no long-running work)?**
   → Yes: **Cloudflare Workers** (pair with D1/KV/R2, or Hyperdrive to reach an external Postgres).

**Default when nothing above strongly applies**: Next.js (API Routes) + Supabase. This combination covers the majority of MVP, SaaS, and agency-site builds with the least new infrastructure to learn, and both have first-class MCP tooling available when connected in your environment.

## Request Lifecycle (applies across stacks)

Every incoming request should pass through the same conceptual stages, regardless of framework:

1. **Transport** — HTTP/WebSocket connection accepted (framework-handled).
2. **Middleware chain** — CORS, request-id generation (`BE077`), auth token extraction, rate limiting (`BE063`/`BE064`).
3. **Validation** — parse and validate the request against a schema at the boundary (`BE080`) before any handler code runs.
4. **Authorization** — confirm the authenticated principal may perform this specific action on this specific resource (not just "is logged in" — is this the *right* user/tenant, see `BE032` for RLS-backed tenant isolation).
5. **Handler / business logic** — the actual work, ideally with no framework-specific code leaking into this layer (keeps it testable and portable across frameworks if the stack ever changes).
6. **Data access** — repository/query layer; outbound calls here get timeouts (`BE073`) and, where appropriate, retries (`BE071`).
7. **Response shaping** — success responses and errors both pass through the same envelope logic (`BE059`/`BE082`) before serialization.
8. **Observability** — structured log line per request including status, duration, and request id (`BE076`/`BE077`), regardless of success/failure.

## Folder Structure Conventions

### Next.js (App Router)

```
app/
  api/<resource>/route.ts        # or Route Handlers colocated with pages
  (routes)/...                   # page routes
lib/
  db/                            # Supabase/Prisma client, query helpers
  validation/                    # Zod schemas, shared between client & server
  auth/                          # session/token helpers
  errors.ts                      # error envelope + error classes (BE082)
```
Keep `lib/` framework-agnostic where possible — it's the part most likely to be reused if you ever split the backend out.

### Express / Fastify

```
src/
  routes/<resource>.routes.ts     # route definitions only, no logic
  controllers/<resource>.controller.ts   # request/response handling, calls services
  services/<resource>.service.ts  # business logic, framework-agnostic
  repositories/<resource>.repository.ts  # data access
  middleware/                     # auth, error handler (BE084), rate limiting
  validation/                     # Zod/Joi schemas
  errors.ts
```
The controller → service → repository split matters most here specifically *because* Express doesn't impose one for you — without it, logic tends to accumulate directly in route handlers.

### Nest.js

Follow Nest's own module convention (it enforces this structurally, which is the point of choosing it):
```
src/<domain>/
  <domain>.module.ts
  <domain>.controller.ts
  <domain>.service.ts
  dto/                            # class-validator DTOs (validation boundary)
  <domain>.repository.ts (or inject an ORM repository directly)
```

### FastAPI

```
app/
  routers/<resource>.py           # APIRouter per resource
  schemas/<resource>.py           # Pydantic request/response models (BE080, BE085)
  services/<resource>.py          # business logic
  db/                             # session/engine setup, models
  core/
    config.py                     # env/config loading, fail-fast validation (BE081)
    errors.py                     # exception handlers (BE085)
  main.py                         # app factory, middleware registration
```

### Django / DRF

```
<project>/
  <app>/
    models.py
    serializers.py                 # DRF — validation boundary
    views.py  (or viewsets.py)
    urls.py
    admin.py                       # Django Admin registration
  <project>/
    settings/
      base.py, dev.py, prod.py     # environment-specific settings, not scattered env checks
    urls.py
```

### Supabase (BaaS-first, minimal custom backend)

```
supabase/
  migrations/                      # SQL migrations (see database-schema-design.md, Phase 2)
  functions/<name>/index.ts        # Edge Functions for custom logic (BE011)
  seed.sql
```
Most CRUD needs no custom backend code at all here — the auto-generated REST/GraphQL layer plus RLS policies (`BE032`) *is* the backend. Reach for Edge Functions only when logic can't be expressed as a Postgres function/RLS policy.

## Environment Configuration

- Load and validate all required env vars **once, at startup**, and crash immediately if any are missing or malformed (`BE081`) — never let a missing `DATABASE_URL` surface as a confusing runtime error three requests later.
- Separate config by environment (`dev`, `staging`, `prod`) but keep the *shape* of config identical across them — the same schema validates all three, only values differ.
- Never commit real secrets; commit a `.env.example` documenting every required variable's name and purpose (this ships as a template from `scripts/devops/generate.py` in Phase 3).
- Prefer a typed config object (validated via the same Zod/Pydantic pattern as request validation) over scattered `process.env.X` / `os.getenv("X")` calls throughout the codebase — one source of truth, one place that fails fast.

## Choosing Between "One Backend" and "Backend Per Concern"

Most projects this skill will be used for (agency sites, early-stage SaaS) should start as **one backend** (monolith-style, whichever stack was chosen above) — splitting into services before there's a real scaling or team-ownership reason to do so adds coordination overhead without a corresponding benefit. Revisit this only when a concrete pressure appears: a specific component needs independent scaling, a specific component needs a different language (e.g. a Python ML service alongside a Node API), or a separate team needs to own a deploy cycle independently.
