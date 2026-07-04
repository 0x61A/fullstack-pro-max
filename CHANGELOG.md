# Changelog

All notable changes to this skill are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/): new checks, data rows, or modules bump **minor**, corrections bump **patch**. The latest version here stays in sync with `metadata.version` in `SKILL.md`.

## [0.17.0] — 2026-07-04

### Added
- **Three more real builds** in the "Real builds" section, chosen to be structurally and visually distinct from each other and from the existing two (salon, cafe) — same skill, deliberately different results, not the same template recolored:
  - **Erdem & Kaya Hukuk Bürosu** (legal, `UX070` + `UX127` Swiss/International) — light mode, strict hairline grid, single grotesk, zero shadows/radius.
  - **Fluxlane** (SaaS/dev-tool, fictional, `UX071` + `UX138` bento grid) — deliberately avoids `UX141` dark-technical (already used in the dashboard field test) to prove the same sector can look genuinely different.
  - **Kinetik Performans Stüdyosu** (fitness/wellness, `UX074` + `UX102` condensed display) — dark mode, multi-color gradient mesh, diagonal energy.
  - All screenshotted with headless Chrome the same way as the first two.

## [0.16.1] — 2026-07-04

### Added
- **"Real builds" section** in README.md/BENİ-OKU.md with screenshots of two sites built following this skill's guidance to a finished result (not the bare `examples/` scaffolds, which stay intentionally unfinished): a salon/beauty site (same decision path as the `salon-site` field test — `BE088`, `UX269`, playful-rounded) and a cafe/restaurant site (`UX068` sector direction). Screenshots taken with headless Chrome against the running builds, added as `assets/screenshot-salon-build.png` and `assets/screenshot-cafe-build.png`.

## [0.16.0] — 2026-07-04

### Added
- **`examples/` directory**: real, committed output from actually running the skill's own scripts end to end (not dry-runs) against two field-test prompts. `examples/salon-site/` (a from-scratch small-business site: `plan` → `design`, `PLAN.md` walks through the backend-decision and sector-direction steps) and `examples/dark-technical-dashboard/` (a ready-made-component ask: `design`'s known-sites-library → component-libraries chain → `build`, `COMPONENT-SOURCING.md` walks through it including two live `WebFetch` spot-checks against the component-library sources). `examples/README.md` indexes both. README.md/README.tr.md gained a "Field tests" section summarizing both.

### Fixed
- **`scripts/backend/generate.py` — double-pluralization bug**, caught by the dashboard field test: `naive_plural()` unconditionally appended `s`/`es` to the resource name's last word, so an already-plural input like `projects` or `posts` became `projectses`/`postses`. A word already ending in `s` is now left as-is.
- **`data/ui-ux/colors.csv` `UX088`** (the dark-mode palette used in `generate.py`'s own `--help` example): the row's prose only gave 2 of 4 color roles as literal hex codes, so the script's hex-extraction heuristic silently dropped the accent color to a duplicate of the text color. Added a concrete accent hex (`#5E6AD2`) to the row.
- **`data/ui-ux/component-libraries.csv` `UX262`** (Tremor): live-fetch spot-check found Tremor now also sells a separate premium block library (300+ templates) on top of its free core component set — row updated to reflect both tiers.

## [0.15.0] — 2026-07-04

### Added
- **First field-test pass**: ran the `plan` action against a real "build a from-scratch business website" prompt and the new `design` component-library chain against a "dark-technical dashboard, ready-made component" prompt, using the actual scripts rather than reasoning about them abstractly. The component-library chain (style vocabulary → known-sites-library → component-libraries → Selection Guide) worked end to end with no changes needed. Two real gaps surfaced and were fixed below; caught and fixed one bad cross-reference id in the same pass (`UX133` mistakenly cited as luxury-minimal in a new row — actual id is `UX143`).
- **`data/backend/stacks.csv` — `BE088`**: a static/no-backend option ("static site generator + one serverless form endpoint") for marketing/brochure-site briefs with no accounts, no stored user data, and no dynamic app logic beyond a contact form. Previously all 40 rows assumed some backend was needed, so the single most common "build my business a website" ask had no direct row match. `references/backend-architecture.md`'s Stack Decision Tree gained a new question 0 ("does the brief actually need a backend at all?") ahead of the existing framework-selection questions. Backend module total: 87 → 88 rows.
- **`data/ui-ux/sector-art-direction.csv` — 7 new sector rows (`UX269-UX275`)**: salon/beauty, trades/home services, events/weddings/photography, consulting/professional services, pet care/veterinary, hospitality/boutique lodging, auto services — general local-service/craft business categories that fell outside the original 10 sectors (cafe, healthcare, legal, SaaS, e-commerce, real estate, fitness, finance, education, nonprofit). UI/UX module total: 268 → 275 rows.

## [0.14.1] — 2026-07-04

### Changed
- **README.md / README.tr.md restructure**: added a quick-start section up top, split the module table into "Ship the product" / "Grow the product" groups for scannability, grouped the scripts block by purpose, and added a social-preview image + a "Known Limitations" section (untested-in-the-field status, the two knowledge-authored UI/UX CSVs' no-live-fetch caveat, guidance-not-guarantee). No data or behavior changes.

## [0.14.0] — 2026-07-04

### Added
- **Component-library index** (`data/ui-ux/component-libraries.csv`, `UX245-UX268`, 24 rows): catalogs 18 real component/theme marketplaces (21st.dev, shadcn/ui, shadcn/ui Blocks, Shadcnblocks.com, Aceternity UI, Magic UI, Motion Primitives, Hyperui, Origin UI, Preline UI, Meraki UI, Mamba UI, daisyUI, Flowbite, HeroUI/NextUI, Cult UI, Tremor, v0.dev) plus 6 needs-based "Selection Guide" rows (fastest-to-ship, animation-heavy marketing, zero-budget, data-dense dashboard, non-React framework, AI-prompt-to-code). Unlike the known-sites library, this file is a **live-fetch index, not a static answer** — entries point at where to go look, not what to paste from memory; always `WebFetch` the actual component page for current code/API/pricing before writing anything into a project. UI/UX module total: 244 → 268 rows.
- **`references/component-library-integration.md`**: workflow for when the user wants a ready-made component/theme instead of a from-scratch build. Covers querying the catalog by tag/category, surfacing 2-3 candidates with cost/tradeoff before picking one, live-fetching current code, and integration steps by ecosystem (shadcn/ui-family CLI/copy-paste, markup-only Tailwind kits, installed npm packages, AI generators) — plus a reconciliation checklist (design-token remap, accessibility check, security audit for new third-party JS, license verification, re-skin before shipping brand-forward work). Explicitly scoped apart from `reference-site-analysis.md`/`known-sites-library.csv`, which are for visual inspiration only and never produce copied code.

## [0.13.0] — 2026-07-04

### Added
- **Known-sites library** (`data/ui-ux/known-sites-library.csv`, `UX155-UX244`, 90 rows): maps all 30 `style-vocabulary.csv` styles to 2 real named sites + 1 evergreen gallery-search source (Awwwards/Dribbble/Land-book tag) each, written from existing design knowledge — no live fetch used to build it. Lets the skill suggest concrete inspiration ("Linear and Vercel for dark-technical, or Dribbble's dark-ui tag for fresher picks") when the user names a style or sector but supplies no reference link, instead of guessing from words alone. UI/UX module total: 154 → 244 rows.
- **`reference-site-analysis.md` — "No URL From the User?" section**: documents how to query the library by style tag via `scripts/common/search.py --tag style:UXnnn`, surface named examples + gallery fallback as a confirm-first suggestion, and route the user's pick through the existing WebFetch/live-browser/`scan.py` verification flow before writing a Design Brief. Explicit caveat: the file's `last_verified` means "when this entry was written," not "confirmed live" — sites redesign, always verify before quoting specifics, and the same extract-principles-not-pixels rule applies to named examples same as user-supplied links.

## [0.12.0] — 2026-07-04

### Added
- **Style vocabulary** (`data/ui-ux/style-vocabulary.csv`, `UX125-UX154`, 30 rows): named aesthetic movements as a decision matrix — brutalism, neo-brutalism, swiss/international, bauhaus, art-deco, editorial, kinetic typography, collage/zine, glassmorphism, claymorphism, neumorphism, material-depth, skeuomorphic accents, bento grid, data-dense dashboard, industrial/utility, dark-technical, terminal/mono, luxury-minimal, e-ink/paper, flat 2.0, corporate-clean, playful-rounded, memphis, y2k, vaporwave, retro-futurism, organic/hand-crafted, maximalism, gradient-mesh/aurora. Each row: definition + typical palette/type/layout combination, best-for/avoid-when/tradeoffs, and machine-readable token tendencies in tags (`radius-*`, `shadow-*`, `border-*`, `density-*`).
- **`references/art-direction-derivation.md`**: deriving a visual identity from a verbal brief when there's no reference site — five brand-personality axes (serious↔playful, warm↔technical, luxury↔accessible, calm↔energetic, classic↔experimental), each end mapped to concrete palette/type/layout/motion/style-candidate pulls; a 7-step process anchored to sector recipes and the style vocabulary; a Design DNA output template with a built-in UX050 genericness check and user confirmation gate. UI/UX module total: 124 → 154 rows.
- **`generate.py --style UXnnn`**: applies a style row's token tendencies to the generated output — `--radius-*`, `--shadow-raised/lifted`, `--border-width`, `--space-unit` CSS variables plus matching Tailwind `borderRadius`/`boxShadow` extensions. Tag parsing warns on unknown or conflicting token tags instead of guessing. One command now yields a full token set: `--palette` + `--type` + `--style`.

## [0.11.0] — 2026-07-04

### Added
- **UI/UX module gets its first generator**: `scripts/ui-ux/generate.py` scaffolds design tokens (`design-tokens.css` with color/font/motion CSS variables + `tailwind.config.ts`) from a `colors.csv`/`typography.csv` row id or explicit `--colors`/`--fonts` values, plus optional TODO-marked component skeletons (`--components hero,nav,feature,footer,cta,sidebar,table,form,empty-state`) for `--stack react-tailwind` or plain `html`. Palette role extraction is label-aware (`#hex base`, `accent #hex`) with saturation-threshold fallbacks, and warns instead of guessing when a palette row names no accent hex. Skeletons are deliberately unfinished — TODO structure plus checklist pointers (UX034/044/045/050 etc.), not finished pages.
- **37 new UI/UX data rows** (`UX088-UX124`, module total 87 → 124): `colors.csv` +10 palettes (near-black SaaS dark, neon-on-charcoal, e-ink zero-accent, terracotta, pastel professional, forest+brass, monochrome+red, ocean gradient, Mediterranean, high-vis utility); `typography.csv` +7 pairings (variable grotesk single-family, didone display, monospace display, rounded sans, condensed, slab serif, serif-body/sans-UI split); new `motion-recipes.csv` (10 purpose-driven animation patterns with concrete duration/easing values — stagger reveal, press depth, skeleton shimmer, streaming cursor, optimistic settle, motion tokens); new `responsive-patterns.csv` (10 layout-collapse strategies — rail→drawer, bottom tabs, table→cards, fluid type via clamp(), container queries, art-directed crops).
- **`scan.py` v2**: multiple reference URLs with shared-thread analysis (common colors/font classes/layout keywords — UX083), rough WCAG contrast-ratio estimates on frequent color pairs (UX086 hint), and `--brief` emitting a pre-filled Reference Design Brief markdown draft with TODO markers.

## [0.10.1] — 2026-07-03

### Fixed
- `scripts/security/generate.py` (Next.js template): the generated strict CSP broke local development — Next.js dev mode bundles/HMR execute via `eval()`, which `script-src 'self'` silently blocks (page renders blank, zero console errors), and `frame-ancestors 'none'`/`X-Frame-Options: DENY` break iframe-based local preview tooling. The template now skips the headers when `NODE_ENV !== "production"`; the strict SEC018 baseline still applies unchanged to production builds. Found in real use scaffolding a test project with this skill.

## [0.10.0] — 2026-07-03

### Added
- **Reference-driven design**: when a user describes a desired theme by pointing at example site(s) instead of describing it in words, the UI/UX module now turns those URLs into a written Reference Design Brief before any frontend code is generated. `references/reference-site-analysis.md` documents the process — read with `WebFetch` for structure/copy tone, real computed styles via a live browser tool (Claude Preview / claude-in-chrome) when available, or a cheap offline first pass via the new `scripts/ui-ux/scan.py` (stdlib-only: fetches HTML + same-origin CSS, extracts color frequency, `font-family` declarations, layout keyword hits — no JS rendering). Explicit rule: extract principles, never copy literal assets/copy from the reference.
- `data/ui-ux/reference-analysis-checklist.csv` (`UX078-UX087`, 10 checks): covers the failure modes specific to this workflow — copying instead of extracting, eyeballing colors instead of measuring them, stitching mismatched references into a collage, skipping mobile, and inheriting a reference site's accessibility problems. UI/UX module total: 77 → 87 rows.

## [0.9.1] — 2026-07-03

### Added
- `docs/how-it-was-built.md` — an English write-up of the skill's architectural decisions (single-package action-routing, stdlib-only scripts, CI dogfooding, incremental versioned growth), linked from the README.

## [0.9.0] — 2026-07-03

### Added
- **Sector art-direction recipes** (`data/ui-ux/sector-art-direction.csv`, `UX068-UX077`, 10 rows): starting palette/type/layout directions for 10 business categories — cafe/restaurant, healthcare/clinic, legal, SaaS, e-commerce, real estate, fitness/wellness, fintech, education, nonprofit — each with an explicit "avoid when" so it isn't applied mechanically. UI/UX module total: 67 → 77 rows. New section in `references/frontend-distinctiveness.md`. This closes Phase C's deepening pass (SEO, Security, Ads, UI/UX all expanded this cycle).

## [0.8.0] — 2026-07-03

### Added
- **Creative & budget checks** (`data/ads/creative-budget-checks.csv`, `ADS065-ADS074`, 10 checks): creative concept diversity for entity-level retrieval, fatigue monitoring (frequency + CTR decay), refresh cadence per spend tier, vertical/native-format coverage, UGC-style creative mix, the 70/20/10 budget split, the 3x Kill Rule, ~20% scaling increments, and regulated-category compliance review. Ads module total: 64 → 74 checks. New section in `references/ads-scoring-system.md`.

## [0.7.0] — 2026-07-03

### Added
- **Supply-chain security checks** (`data/security/supply-chain-checks.csv`, `SEC125-SEC134`, 10 checks): automated dependency scanning, enforced lockfiles, pre-merge dependency review, exact-version pinning for security-sensitive packages, CI/CD secret scoping, pinned GitHub Actions (commit SHA not tag), verified build provenance, SBOM generation, and a patch-SLA requirement. Security module total: 124 → 134 checks. New section in `references/infra-cloud-security.md`.

## [0.6.0] — 2026-07-03

### Added
- **Local SEO checks** (`data/seo/local-seo-checks.csv`, `SEO093-SEO112`, 20 checks): GBP claim/categorization/engagement, NAP consistency (site/GBP/directories, crawlable HTML), citations, `LocalBusiness` schema matching the visible page, review generation/response, unique per-location content (Critical — thin-content risk), service-area GBP setup (Critical — fake-storefront suspension risk), and multi-location NAP/GBP management. SEO module total: 92 → 112 checks. New section in `references/seo-technical.md`.

## [0.5.0] — 2026-07-03

### Added
- **i18n / Localization module** (13th module, `IN` prefix, action `localize`): 34 new data rows — `data/i18n/library-selection.csv` (10: next-intl/react-i18next/Paraglide/FormatJS, static vs. database content model, TMS/MT/in-repo translation workflow, Intl API formatting), `routing-content-patterns.csv` (12: subpath/subdomain/ccTLD URL strategy, fallback locale chain, hreflang generation, RTL via logical CSS, ICU pluralization, no string concatenation, locale-aware currency), `l10n-checklist.csv` (12 checks: hardcoded strings, hreflang/sitemap validation, no forced redirects, text expansion, plural grammar, fallback behavior, translation coverage, translated metadata, pseudo-localization in CI, legal text review).
- `references/i18n-localization.md` — library decision tree, content model split, the grammar rules naive i18n gets wrong; cross-referenced with the SEO module's hreflang (`SEO019`) and no-forced-redirect (`SEO020`) rules.
- `scripts/i18n/generate.py`: scaffolds locale routing config, per-locale message stubs (default locale gets real strings, others get TODO-marked stubs with identical key structure), and an hreflang generator for next-intl or react-i18next.
- This closes **Phase B** (4 new modules added this cycle: AI Integration, Analytics, Email, i18n).

## [0.4.0] — 2026-07-03

### Added
- **Email module** (12th module, `EM` prefix, action `integrate-email`): 34 new data rows — `data/email/provider-selection.csv` (10: Resend/Postmark/SES/SendGrid, marketing platforms, mandatory stream separation, React Email/MJML, inbound parsing, sandboxing), `sending-patterns.csv` (10: queue-backed sends, idempotency, suppression webhooks, RFC 8058 one-click unsubscribe, double opt-in, warmup, i18n), `deliverability-checklist.csv` (14 checks: SPF/DKIM/DMARC progression, aligned return-path, Gmail/Yahoo bulk-sender rules, complaint-rate monitoring, list-bombing protection, MTA-STS).
- `references/email-integration.md` — provider decision tree, the four sending non-negotiables, authentication-first deliverability guidance.
- `scripts/email/generate.py`: scaffolds a queue-friendly transactional send module (Resend/Postmark/SES × Node/Python) with suppression, idempotency, and sandbox guards baked in.

## [0.3.0] — 2026-07-03

### Added
- **Analytics & Measurement module** (11th module, `AN` prefix, action `measure`): 34 new data rows — `data/analytics/platform-selection.csv` (12: GA4/Plausible/Umami/PostHog/Mixpanel, warehouse-first, server-side tagging, replay, experiments, consent), `event-tracking-patterns.csv` (10: object_action taxonomy, track plan as code, identity boundary, server-side revenue events), `measurement-checklist.csv` (12 checks: PII-free events, consent gating, revenue reconciliation, dedup, UTM hygiene, pipeline alerts).
- `references/analytics-measurement.md` — platform decision tree, event design rules, funnels/retention/north-star discipline, compliance layer; cross-referenced with the Ads module's tracking checks (`ADS051–ADS064`).
- `scripts/analytics/generate.py`: scaffolds a typed track-plan module (PostHog/GA4/Plausible) with event-name validation and a consent guard.
- Workflow 1 (Complete SaaS Launch) gains a `measure` step before `launch-ads`.

## [0.2.0] — 2026-07-03

### Added
- **AI Integration module** (10th module, `AI` prefix, action `integrate-ai`): 43 new data rows — `data/ai/model-selection.csv` (14: Claude model tiers, tiered routing, extended thinking, vision, embeddings, caching, Batch API, Agent SDK), `data/ai/integration-patterns.csv` (13: streaming SSE, tool use, RAG/pgvector, conversation state, evals, retries, semantic caching), `data/ai/llm-security-checks.csv` (16 checks mapped to the OWASP LLM Top 10).
- `references/ai-integration.md` (model decision tree, cost model, RAG shape, quality gates) and `references/ai-security.md` (LLM threat model, OWASP LLM mapping, tool-use escalation, fail-closed rule).
- `scripts/ai/generate.py`: scaffolds a streaming Claude chat endpoint for Next.js App Router, Express, or FastAPI — with auth check, rate-limit hook, input cap, and bounded `max_tokens` baked in.

## [0.1.0] — 2026-07-03

First public release.

### Added
- Nine modules — Backend & API, Database & Auth, DevOps & Deployment, Testing/QA, Security/Cybersecurity, E-commerce & Payments, UI/UX & Distinctive Frontend, SEO, Ads — with ~644 structured data rows, 29 reference docs, and stdlib-only Python scripts.
- `scripts/common/validate.py`: validates every data CSV against the shared schemas (ID prefixes, uniqueness, severities, dates).
- CI workflow (`.github/workflows/validate.yml`): CSV validation, `--help` + dry-run smoke tests for every script, internal file-reference check, and a self-scan of the repo with the skill's own `scripts/security/audit.py`.
- `scripts/security/audit.py`: repeatable `--exclude PATH` flag; the scanner now always skips its own file (its pattern definitions would otherwise match themselves).
- MIT license, English README, Turkish README (`README.tr.md`), this changelog.

[0.17.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.17.0
[0.16.1]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.16.1
[0.16.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.16.0
[0.15.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.15.0
[0.14.1]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.14.1
[0.14.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.14.0
[0.13.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.13.0
[0.12.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.12.0
[0.11.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.11.0
[0.10.1]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.10.1
[0.10.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.10.0
[0.9.1]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.9.1
[0.9.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.9.0
[0.8.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.8.0
[0.7.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.7.0
[0.6.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.6.0
[0.5.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.5.0
[0.4.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.4.0
[0.3.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.3.0
[0.2.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.2.0
[0.1.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.1.0
