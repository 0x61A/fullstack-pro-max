> Last updated: 2026-07-03 · Module version: 0.1

# API Security

Pairs with `data/security/api-security-checks.csv` (15 checks, aligned with industry API-security-specific risk categories) — query via `scripts/common/search.py`. This is the API-specific deepening of `secure-coding-standards.md`'s general OWASP coverage.

## The Two Highest-Impact API-Specific Checks

Industry API security research consistently ranks these as the most common and most damaging API-specific vulnerability classes — check them first, on every API:

1. **Broken Object-Level Authorization (`SEC077`)** — every request referencing a specific resource ID verifies the caller is authorized for *that specific instance*, not just that they're authenticated. This is IDOR (`SEC002`) applied specifically to API design: `GET /orders/123` must check the caller owns order 123, not just that order 123 exists.
2. **Broken Function-Level Authorization (`SEC078`)** — privileged operations (admin actions, data export, config changes) verify role/permission server-side at the function level, independent of whatever the UI does or doesn't expose.

## Data Exposure

APIs commonly leak more than intended through two related mechanisms:
- **Excessive data exposure** (`SEC079`) — serializing a full internal model/ORM object instead of an explicit response DTO means every new internal field automatically leaks through existing endpoints as the model evolves.
- **Mass assignment / over-posting** (`SEC080`) — accepting a full request body and binding it directly to a model lets a client set fields it was never meant to control (a user setting their own `role` field). Always use an explicit allowlist of user-editable fields on update/create endpoints.

## Rate Limiting and Resource Consumption

- Every public or resource-intensive endpoint is rate-limited (`SEC081`), scoped per authenticated identity where possible, not IP alone (`SEC082`) — IP-only limiting is both bypassable via rotation and unfair to users sharing a NAT.
- Pagination enforces a **server-side** maximum page size regardless of what the client requests (`SEC087`) — an unbounded `?limit=` parameter is a straightforward resource-exhaustion vector.
- GraphQL APIs specifically need query depth/complexity limits (`SEC088`) — the flexible query shape that makes GraphQL powerful also makes an unbounded nested query a denial-of-service vector unique to this pattern.

## Input Validation, Restated for APIs

Every request parameter validated for type, format, range, and length (`SEC083`) before business logic runs — this is `BE080`/`SEC031` applied at the API layer specifically, and it's the first line of defense against both injection and resource-exhaustion attacks.

## Business Logic — Beyond Technical Checks

Automated scanners find injection and auth bugs; they don't find business logic flaws (`SEC084`) — can a discount code be applied twice, can a quantity go negative, can a state machine transition skip a required step. This requires domain-aware manual review of what sequences of individually-valid API calls could produce an exploitable outcome. Review this explicitly for anything touching money or inventory.

## Inventory and Lifecycle

You can't secure what you don't know exists. Maintain a current, complete inventory of every exposed endpoint including internal/deprecated ones (`SEC085`), and actually decommission deprecated API versions rather than leaving them running unpatched indefinitely "just in case" (`SEC086`) — shadow and zombie endpoints are a recurring finding in real-world API breaches.

## Practical Checklist for a New Endpoint

Before shipping any new API endpoint, confirm:
- [ ] Auth requirement explicitly declared, defaulting to required (`SEC076`)
- [ ] Object-level authorization checked if it references a resource ID (`SEC077`)
- [ ] Response shape is an explicit DTO, not a raw model dump (`SEC079`)
- [ ] Write operations use an explicit field allowlist (`SEC080`)
- [ ] Rate limiting applied if public-facing or expensive (`SEC081`)
- [ ] Input validated for type/format/range/length (`SEC083`)
- [ ] Added to the endpoint inventory (`SEC085`)
