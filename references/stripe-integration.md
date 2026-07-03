> Last updated: 2026-07-03 · Module version: 0.1

# Stripe Integration

Pairs with `data/ecommerce/stripe-patterns.csv` (17 rows) — query via `scripts/common/search.py`.

## Choosing a Checkout Approach

1. **Fastest path, least frontend work?** → Stripe Checkout, hosted (`EC001`) — redirect to Stripe's page, lowest PCI burden.
2. **Need the checkout to feel fully embedded in your app's UI?** → Stripe Elements (`EC002`) — still never touches raw card data server-side (Stripe's iframes handle that), more implementation surface than hosted Checkout.
3. **Building a genuinely custom flow** (multi-step, marketplace splitting)? → Payment Intents API directly (`EC003`) — most flexible, but you own correctly handling every intent status including SCA/3D Secure `requires_action`.

Default recommendation absent a specific reason otherwise: **Stripe Checkout**. It's the least code, the lowest compliance burden, and Stripe's own conversion-optimized flow.

## Recurring Revenue

Stripe Billing (`EC004`) handles subscription lifecycle, proration, invoicing, and dunning (automatic retry on failed renewal) — these are genuinely hard to build correctly from scratch and this is where most home-grown subscription systems accumulate bugs. For usage-based pricing specifically, report usage to Stripe and let metered billing (`EC005`) handle proration based on actual consumption rather than hand-rolling usage-to-invoice logic.

## The Non-Negotiables — Get These Right Every Time

These aren't situational tradeoffs; skipping any of them is a real vulnerability or a real bug waiting to happen:

- **Verify every webhook signature** (`EC006`) before trusting the payload — the payments-specific case of `SEC038`.
- **Handle webhook delivery idempotently** (`EC007`) — Stripe redelivers on timeout; use the event id as a dedup key.
- **Respond 2xx fast, do slow work async** (`EC008`) — a slow handler looks like a failure to Stripe and triggers a retry, compounding the idempotency requirement.
- **Compute charge amounts server-side from the actual order** (`EC009`), never trust a client-supplied total — the payments case of `SEC040`.
- **Separate test and live API keys completely** (`EC010`) — never a live key outside production, matching `DO053`.
- **Never expose the secret key client-side** (`EC016`) — only the publishable key (`pk_...`) is safe in the browser; the secret key can create charges and access customer data.
- **Use Stripe's `Idempotency-Key` header on charge-creating requests** (`EC017`) — a client retry/double-click shouldn't create a duplicate charge; Stripe deduplicates automatically within a 24-hour window if you pass the key.

## Refunds and Disputes

Treat a refund as a first-class state transition in your own order state machine (`EC011`, see `DB029`), not something that only exists in the Stripe dashboard — a refund that doesn't update your own order state produces a mismatch between what Stripe shows and what your system/customer sees. Dispute (chargeback) webhooks need an **active alert to a human**, not passive logging (`EC012`) — missing Stripe's response deadline means an automatic loss regardless of merit.

## Beyond Cards

For an international or diverse customer base, Stripe's unified Payment Element (`EC013`) surfaces regionally relevant payment methods (wallets, bank debits, BNPL) without separate per-method integration — meaningfully higher conversion for close to zero extra work. For marketplace/platform businesses paying out multiple parties, Stripe Connect (`EC014`) handles the genuinely hard regulatory parts (KYC on payees, payout compliance) that are extremely costly to build independently. For multi-jurisdiction tax, Stripe Tax (`EC015`) handles rate/nexus/category logic that changes too frequently to maintain by hand.

## Scaffolding

`scripts/ecommerce/generate.py` (this module) scaffolds a Stripe webhook handler with signature verification and idempotent-processing structure already in place — see the Scripts section of `SKILL.md`.
