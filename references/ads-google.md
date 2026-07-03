> Last updated: 2026-07-03 · Module version: 0.1

# Google Ads

Pairs with `data/ads/google-ads-checks.csv` (20 checks) — query via `scripts/common/search.py`.

## Conversion Tracking Is the Foundation

Everything else in this module assumes conversion tracking is accurate — Smart Bidding and Performance Max both optimize toward whatever's marked as a conversion, so a weak proxy metric (page views instead of real leads/purchases) actively steers spend toward the wrong outcome (`ADS001`). **Enhanced Conversions or server-side tagging** (`ADS002`) is the single highest-leverage fix available on most accounts today — browser-only tracking undercounts due to ad blockers and cookie restrictions. Conversion **values** should reflect real revenue/LTV, not a flat placeholder (`ADS003`) — value-based bidding (Target ROAS) is only as good as the value data feeding it.

## Account Structure and Bidding

Structure campaigns around real business logic — product line, funnel stage, geography (`ADS004`) — not ad hoc growth over time. The current Smart-Bidding era favors **fewer, larger campaigns** with sufficient conversion volume over the older exact-match-heavy fragmented structure (`ADS005`) — Smart Bidding needs enough data per campaign to exit the learning phase effectively. Bidding targets (ROAS/CPA) must reflect actual unit economics (`ADS012`), and a newly launched or changed bidding strategy needs adequate time and volume — commonly cited as 2-4 weeks / 30+ conversions — before being judged (`ADS013`). Repeatedly changing strategy before it exits learning resets progress each time and produces consistently mediocre results.

## Keywords in the Broad Match + Smart Bidding Era

Google's current recommended default pairs **broad match with Smart Bidding and active negative keyword hygiene** (`ADS006`) — different from the older exact-match-heavy convention. Review the search terms report on a recurring cadence, not only when performance drops (`ADS007`), and maintain shared negative lists for exclusions that apply account-wide (competitor brand terms, clearly irrelevant intent) rather than duplicating per campaign (`ADS018`).

## Performance Max — Oversight, Not Autopilot

PMax's automation reduces manual control but doesn't eliminate the need for oversight: monitor search-term insights and per-asset-group performance regularly (`ADS009`), configure **brand exclusions** if a separate branded campaign exists to avoid PMax cannibalizing cheap branded traffic (`ADS010`), and use AI Brief/text customization tools to steer messaging rather than leaving fully generic assets to be auto-combined (`ADS011`).

## Quality Score — Diagnose the Right Component

When CPCs are high or impression share is low, check all three Quality Score components (landing page experience, ad relevance, expected CTR) individually rather than assuming the fix is always "bid higher" (`ADS008`) — a low score driven by poor landing page experience won't respond to a bid increase. This connects directly to `ADS017`: verify ad-to-landing-page message match for top-spending campaigns specifically.

## Ad Assets and Audience Signals

Responsive ad assets need genuine variation, not near-duplicates, to earn a Good/Excellent ad strength rating (`ADS014`) — and all relevant ad extensions (sitelinks, callouts, structured snippets) should be configured since they're a factor in ad rank and otherwise free performance left unclaimed (`ADS015`). Upload first-party audience data (customer match, site visitors) as a signal for Smart Bidding/PMax rather than relying solely on Google's cold automated targeting (`ADS016`) — particularly valuable given ongoing third-party signal loss.

## Scoring

Reuses `scripts/common/score.py` — see `ads-scoring-system.md` for the shared formula applied across this whole module.
