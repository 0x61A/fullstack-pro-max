> Last updated: 2026-07-03 · Module version: 0.1

# Ads Scoring & Cross-Platform Tracking/Attribution

Reuses the exact severity-weighted formula from `security-scoring.md`/`seo-scoring-system.md` and `scripts/common/score.py`, applied across this module's 64 checks: `data/ads/google-ads-checks.csv` (20), `meta-ads-checks.csv` (14), `platform-checks.csv` (16), and `data/ads/tracking-attribution-checks.csv` (14) — the cross-platform tracking/attribution checklist this file also covers in depth, since it doesn't have its own dedicated `ads-*.md` file.

## The Formula

```
Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
score = 100 - (sum of weights of FAILED checks / sum of weights of EVALUATED checks) * 100
```

```
python3 scripts/common/score.py data/ads/google-ads-checks.csv --results results.json
python3 scripts/common/score.py data/ads --results results.json   # all four ads CSVs combined
```

One consistent scoring language across Security, SEO, and Ads — a "72" means the same thing in every module.

## Cross-Platform Tracking & Attribution (`data/ads/tracking-attribution-checks.csv`)

This checklist applies across every platform above, and is where the most severe, easy-to-miss issues tend to live:

**Server-side tracking is the top priority, ranked by spend.** Implement server-side tagging or platform-native server-side APIs (sGTM, Meta CAPI, TikTok Events API, Google Enhanced Conversions) starting with the platforms receiving the most budget (`ADS051`) — this is the single highest-leverage fix for tracking accuracy in the current privacy-restricted browser environment. Once implemented, monitor the **server-side hit ratio** as an ongoing health metric (`ADS052`) — a correct setup can silently degrade (an expired token, a broken deployment) with no obvious symptom until someone investigates a discrepancy.

**Deduplication needs active verification, not assumption.** Every platform running dual browser+server tracking needs its `event_id`-based deduplication actually verified working (`ADS053`) — an undetected failure inflates reported conversions, which looks like a tracking win while actually corrupting every downstream optimization and reporting decision. This is Critical severity for a reason: it's invisible until specifically checked.

**PII is always hashed before transmission** (`ADS054`) — every platform's server-side API requires this, and it's also a genuine privacy obligation independent of the platform requirement, connecting directly to the Security module's general PII-handling discipline (`SEC-*` checks in `secure-coding-standards.md`).

**Consent Mode reflects real consent, and its output is modeled, not measured.** Implement Consent Mode v2 or the platform equivalent so tracking behavior genuinely adjusts to actual user consent (`ADS055`) — both a compliance requirement (GDPR/ePrivacy) and a data-quality one. When consent-mode conversion modeling is active for non-consenting users, treat those numbers as **statistically estimated**, not directly observed, when interpreting performance (`ADS056`) — over-confident optimization on modeled data is a subtle, easy mistake.

## Attribution — Every Platform Is Biased Toward Crediting Itself

Choose an attribution model that matches the account's actual customer journey length, not whatever the platform defaults to unreviewed (`ADS057`), and use Data-Driven Attribution where conversion volume is sufficient to support it (`ADS058`). Critically: **no single platform's self-reported attribution should be trusted at face value when summed across platforms** (`ADS059`) — Google, Meta, and TikTok will each tend to over-credit themselves, and naively summing their individually-reported ROAS/conversions systematically overstates total marketing-driven results.

The check against this bias is **blended MER** (Marketing Efficiency Ratio: total revenue ÷ total spend), tracked alongside individual platform ROAS as an independent, platform-attribution-bias-free sanity check (`ADS060`). When platform-reported numbers collectively imply more revenue than the business actually generated, MER is what catches it.

## Mobile-Specific

App advertisers need `AdAttributionKit` (`ADS061`) to recover iOS attribution signal lost to App Tracking Transparency restrictions, and a Mobile Measurement Partner (AppsFlyer, Adjust, Branch, Singular — `ADS062`) for unified, network-agnostic attribution when running multiple ad networks — the same self-crediting bias problem as `ADS059`, specific to mobile SDKs.

## Practical Hygiene

Consistent UTM tagging across every platform's campaigns (`ADS063`) is what makes downstream analytics reconciliation possible in the first place — inconsistent tagging breaks the ability to independently verify ad-platform-reported data, undermining `ADS059`/`ADS060`'s cross-checking. Attribution/conversion windows should be set deliberately per the account's actual consideration period (`ADS064`), not left at platform defaults universally — a short window undercounts a long B2B sales cycle, a long window over-credits an impulse-purchase product.
