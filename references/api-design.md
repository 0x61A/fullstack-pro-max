> Last updated: 2026-07-03 · Module version: 0.1

# API Design

Guidance for shaping the API surface itself — endpoint/resource design, contracts, and the cross-cutting concerns every endpoint should handle consistently. Pairs with `data/backend/api-patterns.csv` for the full communication-pattern decision matrix (REST vs GraphQL vs tRPC vs gRPC, pagination style, versioning, etc. — query it via `scripts/common/search.py` rather than re-deriving from scratch here).

## Choosing a Communication Pattern

Default to **REST** unless a specific row in `api-patterns.csv` points elsewhere:
- Full-stack TypeScript monorepo where only your own frontend consumes the API → consider **tRPC** (`BE043`) for end-to-end type safety with zero codegen.
- Multiple client types (web + mobile) needing different data shapes from the same resources → consider **GraphQL** (`BE042`).
- Service-to-service inside a microservices architecture → consider **gRPC** (`BE044`).
- Otherwise, REST's ubiquity and HTTP-native caching/tooling make it the safest default, especially for anything a third party or a future unknown client might consume.

## Resource Naming (REST)

- Plural nouns for collections: `/users`, not `/user`.
- Nesting reflects genuine ownership, not just relatedness: `/users/:id/orders` is fine; don't nest more than one level deep — prefer `/orders?userId=:id` over `/users/:id/orders/:orderId/items/:itemId` chains.
- Actions that don't map to CRUD get a verb sub-resource, not a verb in the URL: `POST /orders/:id/cancel`, not `POST /cancelOrder`.
- Query params for filtering/sorting/pagination (`?status=active&sort=-createdAt&cursor=...`), never for identifying the primary resource.

## Contract-First Habits

- Define the request/response schema (Zod, Pydantic, DRF serializer, or an OpenAPI spec) *before* writing the handler body — this is the same validation boundary discipline as `BE080`, applied at design time instead of just runtime.
- Generate API docs from the schema (FastAPI does this automatically; Nest.js via `@nestjs/swagger`; for Express/Fastify, generate an OpenAPI doc from your Zod schemas rather than hand-writing docs that drift from the code).
- Treat a published contract (anything with an external consumer) as something you version deliberately (`BE053`), not something you silently reshape.

## Cross-Cutting Concerns Every Endpoint Should Handle

These apply regardless of which communication pattern or stack was chosen — treat this as the "did I forget something" checklist when adding a new endpoint:

1. **Validation** at the boundary (`BE080`) — reject malformed input before business logic runs.
2. **Authorization**, not just authentication — confirm the caller may act on *this specific* resource (see `database-schema-design.md` / `auth-patterns.md`, Phase 2, for row-level patterns).
3. **Idempotency** for anything with a side effect that a client might retry (`BE058`) — mandatory for payment/order-creation endpoints specifically.
4. **Timeouts** on any outbound call the handler makes (`BE073`).
5. **Consistent error envelope** on failure (`BE082`), consistent success envelope if the project uses one (`BE059`).
6. **Rate limiting** if the endpoint is public or expensive to compute (`BE063`/`BE064`).
7. **Structured logging** with a request/correlation id (`BE076`/`BE077`).
8. **Pagination** on any endpoint that can return an unbounded list (`BE055`/`BE056`) — never ship a collection endpoint with no pagination "for now."

## Webhooks (Designing Your Own)

When your API needs to notify external systems (outbound webhooks, `BE045`):
- Sign every payload (HMAC with a per-consumer secret) so receivers can verify authenticity.
- Include an event id and make delivery idempotent on the receiving end's behalf (send the same event id on retry).
- Retry with exponential backoff (`BE071`) on delivery failure, and give consumers a way to see delivery history/replay a failed event.
- Version your webhook payload shape the same way you'd version a public REST endpoint (`BE053`) — consumers build brittle parsers against whatever you send first.

When *receiving* webhooks from a third party (Stripe, Shopify, Supabase Auth hooks — `BE046`):
- Verify the signature before touching the payload — this is a security boundary, not just validation.
- Handle idempotently — providers retry on timeout, so the same event id may arrive more than once.
- Respond fast (2xx) and do slow work asynchronously (queue it) — most providers will retry (and eventually give up) if your endpoint is slow, turning a slow handler into a duplicate-delivery problem.

## Real-Time and Streaming Endpoints

Choosing between WebSockets, SSE, and polling is in `api-patterns.csv` (`BE047`–`BE050`); once chosen:
- WebSockets: design an explicit message-type protocol (don't just push raw DB rows) so the client and server can evolve independently; plan for reconnection and missed-message replay from the start, not as an afterthought.
- SSE: still needs a heartbeat/keep-alive to detect dead connections through proxies that buffer or time out idle connections.
- Streaming LLM tokens (`BE048`): stream the *tokens*, but still validate/moderate the assembled response server-side before treating it as trusted — token-by-token client rendering doesn't mean the server should skip post-hoc checks.

## Long-Running Work

Never make a client hold an HTTP connection open for genuinely long work (report generation, bulk import, video processing). Use the job-queue-plus-callback or status-polling pattern (`BE051`/`BE052`): return `202 Accepted` with a job id immediately, do the work asynchronously, and let the client either poll `GET /jobs/:id` or receive a webhook/websocket event on completion.

## Bulk and Batch Endpoints

When a client needs to act on many resources at once (`BE057`), return **per-item** success/failure in the response — an all-or-nothing result forces the client to guess which of 50 items actually failed. Shape: `{ results: [{ id, status: "ok" | "error", error?: {...} }] }`.

## API Security Baseline

This is the *design-time* baseline; the full cybersecurity module (threat modeling, API-specific attack classes, infra hardening) lands in Phase 5 — until then, at minimum:
- Auth on every endpoint by default; explicitly opt endpoints *out* of auth (public health check, public webhook receiver) rather than opting endpoints *in*, so a forgotten auth check fails closed, not open.
- CORS configured to an explicit allowlist, never `*` on any endpoint that reads/writes authenticated data.
- Rate limit anything public-facing (`BE063`/`BE064`) before it ships, not after the first abuse incident.
- Never trust client-supplied identifiers for authorization (e.g. don't authorize based on a `userId` in the request body — derive it from the verified auth token).
