> Last updated: 2026-07-03 · Module version: 0.1

# Analytics & Measurement

How to instrument a product so the numbers can actually be trusted — platform choice, event design, funnels/retention, and the compliance layer. Row-level detail lives in `data/analytics/platform-selection.csv`, `event-tracking-patterns.csv`, and `measurement-checklist.csv` (score the checklist with `scripts/common/score.py`). This module covers *product/site* measurement; paid-media tracking (pixels, CAPI, attribution windows) lives in the Ads module (`data/ads/tracking-attribution-checks.csv`) — the two share dedup, consent, and UTM discipline, cross-referenced below.

## Platform Decision Tree

1. **Marketing/brochure site only?** → Plausible (AN002) for privacy-first simplicity, Umami (AN003) if self-hosting is cheap for you, GA4 (AN001) if Google Ads integration is the point.
2. **SaaS/product app?** → PostHog (AN004) is the default: funnels, retention, replay, flags, and A/B tests in one tool with a generous free tier. Mixpanel/Amplitude (AN005) when a mature org wants dedicated behavioral tooling.
3. **Both?** → Two tools, cleanly split (AN008): marketing site on the web-analytics pick, app on the product-analytics pick. Don't force one tool to do both jobs badly.
4. **Data team with a warehouse?** → Warehouse-first raw events (AN006) — but only if someone owns it.
5. **Heavy ad spend?** → Add server-side tagging (AN007), which the Ads module also requires (`ADS051`); share the infrastructure.

## Event Design (where analytics actually fails)

Analytics fails at instrumentation, not at dashboards. The rules that prevent the usual wreckage:

- **One naming convention, enforced**: `object_action`, snake_case, past tense (AN013). One owner reviews every new event name.
- **Track plan as code** (AN014): a typed module with one function per event — `scripts/analytics/generate.py` scaffolds it. Typos become compile errors; the plan is diffable in PRs.
- **State changes, not clicks** (AN016): `subscription_upgraded`, not `upgrade_button_clicked`. Events survive redesigns.
- **Identity at the auth boundary** (AN015): `identify(userId)` at login/signup, `reset()` at logout, opaque IDs — never email.
- **Revenue from the server** (AN021): `order_completed` fires from the webhook/DB layer, reconciled weekly against Stripe/Shopify (AN027). Client-side purchase events are for UX analysis only.
- **QA before release** (AN022): new events fire once, with expected properties, under both consent states.

## Funnels, Retention, North Star

Work backwards from the activation moment (AN018): define what "this user got the value" means, then instrument the 3–6 steps leading there. Retention is weekly cohorts on the core value action, not logins (AN019). Cap the reporting surface at one north-star metric plus 3–5 input metrics with owners (AN020, AN031) — every chart beyond that must justify its existence.

## The Compliance Layer (Critical rows)

- **No PII in events, properties, or replay** (AN023) — analytics tools must never become an ungoverned second copy of personal data.
- **Consent actually gates the scripts** (AN024): verify in devtools under granted/denied/changed states. This is the same Consent Mode discipline as `ADS055`, applied to the whole measurement stack. Cookieless tools (AN002/AN003) can remove the banner need for analytics — document the basis.
- **Retention windows + deletion runbook** include every analytics vendor (AN025); KVKK/GDPR deletion reaches them too.

## Trust Mechanics

The checklist rows that keep numbers believable: one canonical definition per metric (AN026), dedup shared client/server events by event ID (AN029 — same rule as `ADS053`), filter bots and internal traffic (AN028), enforce UTM hygiene (AN030 — same convention the Ads module reconciles against, `ADS063`), alert when event volume collapses (AN033), and run experiments with pre-registered metrics and no peeking (AN034, pairs with AN010).

## Cross-module hooks

- Paid-media tracking, CAPI, attribution windows, MER → Ads module (`ads-scoring-system.md`, `ADS051–ADS064`)
- Consent UX and cookie banner implementation → Security module's privacy checks + `ai-security.md`'s data-lifecycle rules for AI features
- Event QA → fold into the Testing module's release checklist (`testing-strategy.md`)
- Storing first-touch UTMs on the user record → `database-schema-design.md`
