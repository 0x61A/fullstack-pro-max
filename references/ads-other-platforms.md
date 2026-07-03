> Last updated: 2026-07-03 · Module version: 0.1

# LinkedIn, TikTok, and Microsoft Ads

Pairs with `data/ads/platform-checks.csv` (16 checks: 6 LinkedIn, 6 TikTok, 4 Microsoft) — query via `scripts/common/search.py`.

## LinkedIn — B2B-Specific Capabilities

Conversion tracking follows the same principle as every other platform in this module (`ADS035`, mirrors `ADS001`) — map to genuine B2B outcomes, not page visits. Account structure uses LinkedIn's current three-tier hierarchy (Campaign Groups → Campaigns → Ad Sets, post-October-2025 terminology) organized around real business objectives (`ADS036`). For Lead Gen Forms, balance form length against lead quality deliberately (`ADS037`) — shorter forms convert better but produce less-qualified leads, a tradeoff tied to actual sales capacity, not a default.

LinkedIn's genuinely distinctive B2B capabilities are frequently underused: **ABM Matched Audiences** for targeting a defined account list directly (`ADS038`), **Thought Leader Ads** for promoting real employee/executive content with genuine engagement rather than as a generic ad unit (`ADS039`), and **Predictive Audiences** for expanding reach from a proven seed list when a narrow ABM list is hitting a ceiling (`ADS040`).

## TikTok — Platform-Native or It Underperforms

Server-side tracking (Events API + Pixel, with deduplication) follows the identical pattern to Meta's CAPI (`ADS041`, mirrors `ADS021`). The single most emphasized, best-evidenced platform-specific principle: **creative must be built platform-native from the start** (`ADS042`) — a repurposed Meta Reels or YouTube Shorts asset consistently and measurably underperforms genuine TikTok-native content (fast cuts, native sound/trends, vertical-first). Creative diversity matters for retrieval here too, following the same logic as Meta's Andromeda system (`ADS043`). Respect **safe zones** so text/UI elements aren't hidden behind native captions/buttons (`ADS044`) — a simple, mechanical spec check still commonly missed. Smart+ automated campaigns need the same oversight discipline as Meta's Advantage+ (`ADS045`), and TikTok Shop's product catalog needs to stay synced with real inventory — the identical principle to `EC025`'s Shopify guidance (`ADS046`).

## Microsoft Ads — Not Just "Smaller Google"

Reviewing an imported Google Ads campaign, not launching it unmodified, matters because Microsoft's audience (older, higher-income skew on average) and auction dynamics genuinely differ (`ADS047`). The platform's standout, underused capability: **LinkedIn-profile-data targeting** for B2B campaigns (`ADS048`) — a targeting dimension Google Ads simply doesn't have, owed to Microsoft's ownership of LinkedIn. Evaluate newer Copilot-integrated AI ad surfaces for relevance rather than dismissing them for being smaller/newer (`ADS049`), and treat Microsoft's typically lower-competition inventory as a genuine incremental-efficiency opportunity, not something to dismiss purely on total-volume grounds (`ADS050`).

## Cross-Platform Pattern Recognition

Notice how many principles repeat across platforms with the same underlying logic: server-side tracking + deduplication (Google Enhanced Conversions / Meta CAPI / TikTok Events API), creative-as-a-retrieval-signal (Meta Andromeda / TikTok's algorithm), learning-phase respect (Google Smart Bidding / Meta Advantage+ / TikTok Smart+), and automation-needs-good-inputs (PMax / Advantage+ / Smart+). These aren't coincidences — they reflect a broader shift across all major ad platforms toward automated, signal-hungry delivery systems. Once this pattern is recognized, auditing a new platform becomes faster: ask the same four questions (is tracking accurate and deduplicated, is creative diverse and platform-native, is the learning phase being respected, are automated campaign types getting good inputs) regardless of which platform it is.
