> Last updated: 2026-07-03 · Module version: 0.1

# Technical SEO

Pairs with `data/seo/technical-seo-checks.csv` (34 checks) and `data/seo/onpage-checks.csv` (23 checks) — query via `scripts/common/search.py`.

## The Foundational Layer — Crawlability and Indexability

Before anything else, confirm search engines can actually reach and index the content: `robots.txt` doesn't accidentally block important sections (`SEO001` — a single overly broad Disallow rule can deindex an entire site with no other symptom), the sitemap is current and submitted (`SEO002`), and there's no accidental `noindex` tag left over from staging (`SEO005` — one of the most common, highest-severity real-world incidents, and entirely silent until traffic drops). Check canonical tags point to the correct URL, self-referencing or deliberately consolidating near-duplicates (`SEO006`).

## Mobile-First and JavaScript Rendering

Google indexes primarily using the **mobile** version of a page (`SEO013`) — confirm mobile rendering has full content parity with desktop, not a stripped subset. For anything client-rendered, critical content and internal links should be present in the initial server response via SSR/SSG (`SEO015`), not solely dependent on JavaScript execution — this matters not just for search engines (which do render JS, but as a separate, delayed, resource-constrained pass) but for AI crawlers and social preview bots that render less reliably.

## Redirects and Migrations

301 for permanent moves, never 302 (`SEO008`) — a 302 doesn't reliably pass ranking signal the way a 301 does. No redirect chains longer than one hop (`SEO009`) — each hop adds latency and measurable link-equity loss. Any site migration (domain change, URL restructure, platform switch) needs a **complete URL redirect map before launch** (`SEO029`) — un-redirected migrations are one of the most common causes of sudden, severe traffic drops, and it's entirely preventable with proper planning.

## Performance — Connects Directly to the Testing/QA Module

Core Web Vitals are covered in depth in `accessibility-performance-audit.md` (`QA040`-`QA050`) — don't duplicate that content here, but note the SEO-specific framing: TTFB matters foundationally since no downstream metric can beat it (`SEO021`), and Core Web Vitals should be monitored via **field data (CrUX)**, not lab scores alone (`SEO033`, restating `QA050`) — Google's ranking systems use real-user field data, not Lighthouse.

## Structured Data — Accuracy Over Coverage

Structured data must validate without errors (`SEO023`) **and** accurately reflect visible page content (`SEO024`) — mismatched structured data (a price in JSON-LD that doesn't match the visible price) violates Google's guidelines and risks losing rich-result eligibility or worse. See `data/seo/schema-types.csv` and `seo-scoring-system.md`'s sibling reference for which schema type fits which content.

## International SEO

hreflang implementation errors (missing reciprocal links, wrong language-region codes, missing self-reference) are among the most common international SEO mistakes (`SEO019`) and can cause the wrong regional page to rank in the wrong market. Never force-redirect based on IP/browser locale alone (`SEO020`) — this can prevent crawlers from ever discovering non-default regional versions.

## On-Page Fundamentals

- **Unique title tags under ~60 characters, primary topic near the front** (`SEO035`, `SEO036`) — duplicate/missing titles across pages is a common, high-impact issue.
- **Single H1 matching actual page topic** (`SEO038`) — this is `QA033`'s heading hierarchy requirement with SEO framing added.
- **Descriptive internal link anchor text, not "click here"** (`SEO044`) — a genuinely useful relevance signal wasted by generic anchor text.
- **Important pages get proportionally more internal links** (`SEO045`) — internal linking is one of the strongest signals a site controls directly for communicating page importance.

## AI Crawler Access — a 2026-Era Addition

Explicitly decide (don't inherit a CMS default) whether AI crawlers (GPTBot, PerplexityBot, ClaudeBot, etc.) are allowed or blocked (`SEO031`). For sites prioritizing AI-search citability as a traffic source, `llms.txt` (`SEO032`) is a low-cost, emerging convention worth adopting.

## Log Files Over Dashboard-Only Monitoring

For larger/established sites, periodically analyze raw server logs (`SEO025`) rather than relying solely on Search Console's sampled, delayed reporting — log files show ground-truth crawler behavior and can reveal crawl-budget waste or unexpected blocking that dashboard tools miss entirely.
