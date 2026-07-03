> Last updated: 2026-07-03 · Module version: 0.1

# i18n / Localization

How to make a product genuinely multi-language, not just translated — library choice, URL strategy, content model, and the grammar/layout details that separate real localization from string substitution. Row-level detail: `data/i18n/library-selection.csv`, `routing-content-patterns.csv`, and `l10n-checklist.csv` (score with `scripts/common/score.py`). This module shares two rules directly with SEO: hreflang correctness (`SEO019`) and the no-forced-redirect rule (`SEO020`) — both are restated here as IN017/IN024 and IN025 because they're where i18n and SEO implementations actually meet.

## Library Decision Tree

1. **Next.js App Router?** → **next-intl** (IN001) — server-component support and built-in per-locale routing.
2. **Framework-agnostic React, or React Native?** → **react-i18next** (IN003) — widest plugin ecosystem, most battle-tested.
3. **Want compile-time-checked, zero-runtime-overhead translations across frameworks?** → **Paraglide JS** (IN002).
4. **Standardizing on ICU MessageFormat directly?** → **FormatJS/react-intl** (IN004).

`scripts/i18n/generate.py` scaffolds the routing config, per-locale message stubs, and an hreflang generator for `next-intl` or `react-i18next`:

```bash
python3 scripts/i18n/generate.py en tr --library next-intl --dry-run
```

## Content Model: Static vs. Database

**Static UI strings** (IN005) — buttons, labels, nav, errors — live in per-locale message files, versioned and PR-reviewed. **Database-stored content** (IN006) — blog posts, product descriptions, anything non-developers edit — gets locale as a column/table with its own fallback-query pattern. Don't force one model to do both jobs: message files for interface chrome, DB rows for editorial content.

## Translation Workflow

Below 3 locales with team members who speak the languages: **in-repo human translation** (IN009). At 3+ locales with non-developer translators: a **TMS** (Crowdin/Lokalise/Phrase, IN007) — translation memory and context screenshots pay for themselves fast. **Machine translation** (IN008) is fine for draft speed on a new locale, never for legal/medical/brand-critical copy without a human review pass — that review is IN034, a launch gate, not a nice-to-have.

## URL Strategy

Default: **subpath prefix** `/en/...`, `/tr/...` (IN011) — cheapest, cleanest SEO signal, works for the overwhelming majority of products. Escalate to **subdomain per locale** (IN012) only for real per-region infra needs, and **ccTLD** (IN013) only for genuinely separate regional business entities — ccTLDs fragment SEO authority, so this is a business decision, not just a technical one.

## The Grammar Rules (where naive i18n breaks)

- **No string concatenation, ever** (IN020): `t('you have') + count + t('items')` breaks word order in most non-English languages. One message with placeholders, always.
- **ICU plural categories, not if/else** (IN019, IN027): some languages have six plural categories, not two. A naive English-shaped conditional is grammatically wrong the moment a real locale ships.
- **Intl API for dates/numbers/currency** (IN010, IN028): `Intl.DateTimeFormat`/`Intl.NumberFormat`, never hand-rolled `${month}/${day}/${year}` — that's wrong by default outside the developer's own locale.
- **Fallback locale chain** (IN014, IN030): missing keys degrade to a real language, never a raw key rendered in production — that's a released bug, not a translation gap.

## Layout and RTL

Text expansion is real: German/Finnish/Russian commonly run 30-100% longer than English (IN026) — test with real translated content, not English-length lorem ipsum. If shipping Arabic/Hebrew/Farsi, adopt **logical CSS properties** (`margin-inline`, not `margin-left`, IN018) from the start — retrofitting RTL onto a hardcoded left-right codebase is expensive. Full visual QA in RTL mode is required (IN029); custom components and third-party widgets are the usual holdouts.

## Cross-module hooks

- hreflang implementation and validation → `seo-technical.md` (`SEO019`), this module restates it as IN017/IN024
- No forced IP/browser redirect → `seo-technical.md` (`SEO020`), restated as IN025 (Critical here — it silently hides entire locale versions from crawlers)
- Consent banners and legal text per locale → IN021/IN034, cross-reference `ai-security.md`'s data-lifecycle rules where a locale also implies a different compliance regime (KVKK vs. GDPR vs. CCPA)
- Currency display vs. charged currency → `stripe-integration.md` / `shopify-integration.md` (IN022)
- Localized email subject lines/bodies → `email-integration.md` (EM020)
