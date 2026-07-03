> Last updated: 2026-07-03 · Module version: 0.1

# Shopify Integration

Pairs with `data/ecommerce/shopify-patterns.csv` (12 rows) — query via `scripts/common/search.py`. If a Shopify MCP server is connected in your environment (`create-product`, `graphql_mutation`, `search_products`, etc.), use it directly for store operations alongside this guidance.

## Hosted Theme vs. Headless

1. **Fastest path to a working store, standard theming is acceptable?** → Shopify-hosted storefront with Liquid themes (`EC018`) — checkout, hosting, PCI compliance, and the storefront all managed by Shopify.
2. **Need a genuinely distinctive, custom frontend** (pairs directly with this skill's UI/UX & Distinctive Frontend module, Phase 7)? → Headless Shopify via the Storefront API with a custom frontend, e.g. Next.js (`EC019`) — full frontend freedom, Shopify remains the commerce engine (inventory, checkout, admin).

Default recommendation: start with a hosted theme unless there's an explicit design/brand reason to go headless — headless is more implementation work and should be a deliberate choice, not a default.

## Checkout — Don't Rebuild It

Use Shopify's hosted checkout (`EC020`) for nearly every integration. It's PCI-compliant, conversion-tested, and includes Shop Pay/accelerated checkout for free. Custom checkout logic (custom discounts, custom shipping rules) belongs in **Shopify Functions** (`EC026`), which extends checkout behavior without forfeiting the platform's compliance and conversion guarantees — this is the correct escape hatch, not a full custom checkout rebuild, which is really only viable on Shopify Plus with explicit checkout-extensibility licensing.

## API Choice

Use the **GraphQL Admin API** for new integrations (`EC021`) — it's where Shopify ships new features first and lets you fetch exactly the fields needed in one request. The REST Admin API is in maintenance mode for many resource types; only stay on it for an existing integration where migration isn't yet justified.

## The Non-Negotiables

- **Verify every webhook's HMAC signature** (`EC022`) before trusting the payload — identical principle to Stripe's `EC006`/`SEC038`.
- **Handle webhook delivery idempotently** (`EC023`) — Shopify redelivers on timeout, same as Stripe (`EC007`).
- **Never share store admin credentials with a third-party integration** (`EC027`) — use Shopify's OAuth flow for scoped, revocable access tokens instead. This is the only legitimate authentication pattern for a Shopify app.
- **Respect rate limits with backoff, not aggressive retry** (`EC028`) — REST uses a leaky-bucket algorithm, GraphQL uses cost-based throttling; retrying in a tight loop against a rate limit makes it worse and can get an app's access further restricted.

## Inventory Discipline

**Shopify is the single source of truth for inventory** (`EC025`) — read/write through its API rather than maintaining a separately-synced count that can drift. A duplicated, independently-maintained inventory number is a classic overselling bug (selling something that's actually out of stock). This matters even more for multi-channel sellers (`EC029`): route all channel orders and inventory updates through Shopify centrally rather than reconciling separate per-channel systems by hand.

## Product Data and SEO

Structured data (schema.org `Product`) on product pages must stay in sync with real Shopify inventory (`EC024`), not a stale snapshot captured at launch — this connects directly to `seo-technical.md` (Phase 8) once that module ships, and to `SEC079`'s general data-freshness concerns. Showing "in stock" for a sold-out product actively hurts both SEO trust signals and user trust.

## Scaffolding

`scripts/ecommerce/generate.py` (this module) can also scaffold a Shopify webhook handler with HMAC verification structure in place — see the Scripts section of `SKILL.md`.
