> Last updated: 2026-07-03 · Module version: 0.1

# Content Quality & E-E-A-T

Pairs with `data/seo/content-eeat-checks.csv` (19 checks) — query via `scripts/common/search.py`. Covers the four pillars Google's quality guidelines name explicitly: Experience, Expertise, Authoritativeness, Trustworthiness.

## Experience — the Newest Pillar

For content types where firsthand experience genuinely matters (reviews, tutorials, comparisons), the content should show evidence of actual use, not purely synthesized research (`SEO058`). The strongest, hardest-to-fake signal here is **original photos/video** of the actual product or process (`SEO059`) — stock imagery on a "review" visibly undermines the credibility the review is trying to establish.

## Expertise — Especially for YMYL Content

For Your-Money-or-Your-Life topics (health, finance, legal, safety), anonymous or generic "Admin" bylines are a weak trust signal (`SEO060`) — attribute content to a named person with credentials relevant to the topic, and back that with an actual, linked author bio page (`SEO061`). A byline name with no accessible bio provides no way for a reader — or an AI system evaluating the content — to verify the claimed expertise.

## Authoritativeness — External Validation

Authoritativeness is fundamentally about being recognized by others in the field, not self-declared: citations/links from other reputable sources in the same topic area (`SEO062`) are a core signal that's hard to fabricate and correspondingly valuable when genuinely earned. An About page clearly establishing who's behind the site and why they're credible (`SEO063`) is the foundational, low-cost version of this that every site should have regardless of scale.

## Trustworthiness — the Pillar Most Directly Tied to Regulatory Risk

- **Real, verifiable contact information** (`SEO064`) — its absence is disproportionately noticed on YMYL and e-commerce sites specifically.
- **Claims backed by citations**, especially statistics (`SEO065`) — increasingly scrutinized as AI-generated content (which can hallucinate confident-sounding but unsupported claims) has become common.
- **Genuine, non-fabricated reviews with proper disclosure of any incentivization** (`SEO066`) — this is both an ethical/regulatory risk (FTC enforcement) and a severe trust-damage risk if discovered; never worth the ranking upside.

## Content Depth — Completeness, Not Word Count

Depth means covering what a knowledgeable searcher would actually expect (`SEO067`) — the natural sub-questions and related considerations a topic raises — not artificial padding to hit a word count. Thin content remains one of the most consistent drivers of ranking failure for otherwise technically sound pages (`SEO050` in `onpage-checks.csv`).

## AI-Assisted Content — Editorial Value Is the Requirement, Not the Tool

The guidance here is not "avoid AI tools" — it's that AI-assisted content needs human review adding genuine accuracy checking, perspective, and specificity before publishing (`SEO070`). The detectable, ranking-relevant problem isn't AI involvement; it's **generic output published unedited**: repetitive structure, hedge-everything phrasing, no concrete examples (`SEO071`). Fix this by ensuring specificity and genuine editorial value in what ships, regardless of how the first draft was produced.

## GEO — Generative Engine Optimization

For AI Overviews, ChatGPT search, and Perplexity, the unit of citation is a **passage**, not a page — write key paragraphs to stand alone as a complete answer if extracted in isolation (`SEO072`). State the subject's identity and key facts early and unambiguously (`SEO073`) rather than requiring several paragraphs of context to become clear — an AI system extracting from mid-paragraph benefits from unambiguous entity identification near the point of extraction. Keep brand/entity descriptions consistent across every source an AI system might draw from (`SEO074`) — inconsistency across your own site and third-party mentions makes it harder for an AI system to synthesize a confident, accurate answer.

## Freshness — Real Updates, Not Gamed Dates

Review and update time-sensitive content on a defined cadence (`SEO068`), and expose accurate `datePublished`/`dateModified` via structured data (`SEO034` in `technical-seo-checks.csv`). Search engines have become more resistant to freshness-gaming — bumping a date with no real content change — so accurate dates that reflect genuine updates build trust signal over time, while detected gaming can work against a site's credibility.
