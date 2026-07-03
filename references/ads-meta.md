> Last updated: 2026-07-03 · Module version: 0.1

# Meta Ads (Facebook, Instagram, Threads)

Pairs with `data/ads/meta-ads-checks.csv` (14 checks) — query via `scripts/common/search.py`.

## Pixel/CAPI Health

Both browser-side Pixel and server-side Conversions API should fire for the same events, deduplicated via a shared `event_id` (`ADS021`) — this is the Meta-specific application of the general server-side tracking principle in `tracking-attribution-checks.csv`. CAPI without correct deduplication doesn't just fail to help — it actively inflates reported conversions, corrupting optimization decisions. Check **Event Match Quality** in Events Manager periodically (`ADS022`) and add match-quality fields (hashed email, phone, external_id) where missing. Standard events (Purchase, Lead, CompleteRegistration) must map to genuinely corresponding business actions (`ADS023`) — misused events degrade optimization the same way inaccurate conversion actions do in Google Ads.

## Creative Diversity — the Andromeda-Era Requirement

In the current Andromeda/Entity-ID delivery system, creative diversity is itself a signal the algorithm uses for retrieval, not just a testing best-practice (`ADS024`). Near-duplicate variations (same creative, different headline) don't provide usable diversity. Monitor for **creative fatigue** proactively via leading indicators — rising frequency, declining CTR/CPA trend within a stable audience (`ADS025`) — rather than reacting after CPA has already spiked. Produce creative **platform-native to its placement** (vertical 9:16 for Reels/Stories, not a repurposed horizontal video) since visibly repurposed content consistently underperforms (`ADS026`).

## Advantage+ — Automation Needs Good Inputs

Advantage+ Shopping/App campaigns are "creative-as-targeting" by design (`ADS027`) — the automation's targeting quality is bottlenecked by creative input quality far more than in manually-targeted campaigns, so give it genuine creative diversity and accurate catalog/conversion data, not a minimal setup. Confirm the campaign **objective** genuinely matches the business goal (`ADS028`) — this is selected once at creation and determines what the delivery system fundamentally optimizes toward; a mismatched objective (Traffic instead of Sales) can't be compensated for by anything else in the setup.

## Structure and Targeting

Mirror the Google Ads consolidation principle: fewer, larger ad sets concentrate conversion volume better than heavy fragmentation (`ADS029`), and the **learning phase should be respected** — avoid repeated significant edits that reset it (`ADS030`, same reasoning as `ADS013`). Default to **broad or Advantage+ audience targeting** rather than heavily narrowed manual targeting (`ADS031`) — Meta's delivery system has consistently shown broad targeting outperforming narrow targeting when creative and signal quality are strong. Exclude retargeting audiences from prospecting campaigns to avoid budget overlap and muddied attribution (`ADS032`).

## Compliance — Regulated Categories

Health, financial, housing, and employment/credit ads follow Meta's category-specific policy restrictions, including **Special Ad Category** settings (`ADS033`) — housing/employment/credit ads specifically can't use age/gender/zip targeting regardless of how compliant the copy itself is. This is a configuration requirement, not just a copywriting one.

## Budget Sizing

Daily budget needs to be high enough relative to the CPA/ROAS target to realistically generate the conversion volume needed to exit the learning phase — commonly cited around 50 conversions/week (`ADS034`). An underfunded ad set can spend indefinitely without ever optimizing properly; check this before concluding an audience or creative "isn't working."
