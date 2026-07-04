> Last updated: 2026-07-04 · Module version: 0.2

# Reference Site Analysis

Use this when the user describes a desired theme by pointing at one or more existing sites ("make it feel like X", "something in the style of Y") instead of (or in addition to) describing it in words. Goal: turn example URLs into a concrete, written **Reference Design Brief** before any frontend code gets written — not a literal clone, and not a vague "vibe" guess.

## Process

1. **Read it like a real page, not just a screenshot.** Use `WebFetch` on each URL to get structure, copy tone, section order, apparent CTA strategy, and imagery mood. This is text-level, not visual — it tells you *what* the page is doing, not exact colors/fonts.
2. **Get real computed styles when a live browser tool is available.** If `Claude Preview` (`preview_start`/`preview_inspect`/`preview_screenshot`) or the `claude-in-chrome` MCP is connected in this session, load the reference URL and use it: `preview_inspect` for actual computed CSS (colors, font-family, spacing, border-radius) on specific elements, a screenshot for overall composition. This is strictly more reliable than reading raw CSS — computed styles reflect what actually renders, not just what's declared.
3. **Cheap offline first pass when no live browser tool is available.** Run `python3 scripts/ui-ux/scan.py <url> [<url2> ...]` — stdlib-only, fetches HTML plus same-origin stylesheets and extracts a color-frequency table, `font-family` declarations, layout keyword hits, and rough WCAG contrast estimates on the most frequent color pairs (a UX086 hint, not a measurement). With multiple URLs it also reports the shared thread (common colors/font classes/layout keywords — UX083 support), and `--brief` emits a pre-filled Reference Design Brief draft with TODO markers. It does **not** render JavaScript or measure real layout — treat its output as hints to verify, not ground truth. Say so explicitly when using it.
4. **Reconcile multiple references into one direction.** When the user gives 2-3 example sites, don't average or stitch them — find the *shared thread* (e.g. "all three use high-contrast product photography and minimal chrome") and build the brief around that thread. Note per-site details that are one-offs, not the throughline, and leave those out.
5. **Extract principles, not pixels.** Never copy a reference site's literal copy, imagery, or exact CSS values into the new build — that's both an IP risk and produces a worse, uncredited clone rather than a genuinely fitting design. Write the brief in terms of *decisions* (palette family, type pairing style, layout pattern, motion restraint level), not literal values lifted from the source.
6. **Confirm the brief before generating code.** A short Reference Design Brief (below) is cheap to review and correct; a full page built on a misread reference is not. Share it and get a thumbs-up first, especially for client work.

## No URL From the User? Suggest One From the Known-Sites Library

When the user names a **style or vibe** ("brutalist", "make it feel dark and technical like a dev tool", "Y2K nostalgia") or a **sector** but supplies no example link, don't skip straight to guessing from words — `data/ui-ux/known-sites-library.csv` (`UX155`-`UX244`) is a pre-built map of real, named sites and site-finding sources against all 30 `style-vocabulary.csv` styles, written from existing design knowledge (no live fetch was used to build it).

1. **Query it by style tag**, same as any other CSV: `python3 scripts/common/search.py data/ui-ux/known-sites-library.csv --tag style:UX141` (swap in the `UXnnn` id of the matching `style-vocabulary.csv` row) or `--query "dark-technical"`.
2. **Surface 2-3 named examples to the user**, plus the row's built-in gallery fallback (an Awwwards/Dribbble/Land-book tag to browse) for anything the two named examples don't cover. Frame these as a starting point to confirm, not a decision already made — "Linear and Vercel are the usual references for this look, or I can pull fresher live examples from Dribbble's dark-ui tag — want me to look at one of these, or do you have your own reference in mind?"
3. **Treat `last_verified` on this file as "when this entry was written," not "confirmed live."** Sites redesign; a company on the list may no longer look the way the entry describes. Once the user picks one, run it through the normal process above (`WebFetch`/live browser tool/`scan.py`) before writing the Design Brief — never quote this CSV's `option` text as current fact without that check.
4. **The same IP caution applies double here** — these are curated suggestions for *what to go look at*, not pre-approved design decisions. Extract principles from whatever the live check shows, not from this file's prose.
5. **Gallery rows exist because named flagships saturate.** If a style is heavily copied right now (dark-technical, gradient-mesh), lean on the gallery row over the named flagship — the point of naming Linear/Stripe/Vercel in this file is to show what to avoid converging on, not what to copy.

## Reference Design Brief (template)

```
Reference(s): <url(s)>
Shared thread: <one sentence — the thing all references have in common that we're actually borrowing>
Palette direction: <family + role, e.g. "warm neutral base, single saturated accent for CTAs">
Typography direction: <headline/body pairing style, weight contrast, e.g. "high-contrast serif display + neutral grotesk body">
Layout pattern: <named pattern, e.g. "asymmetric hero with off-grid image, centered-column body">
Motion/interaction level: <restrained | moderate | expressive, plus anything specifically observed>
Deliberate divergence: <what we're changing on purpose and why — ties to `frontend-distinctiveness.md` UX050's "five competitors" check>
Confirmed with user: <yes/no>
```

Feed the resulting brief into the normal UI/UX module workflow — `references/frontend-distinctiveness.md` and `references/ui-ux-quickref.md` still govern the actual design decisions; this file only governs how you turn example URLs into an input for that process.

## Checklist

`data/ui-ux/reference-analysis-checklist.csv` (`UX078`-`UX087`) covers the failure modes specific to this workflow: copying instead of extracting principles, eyeballing colors instead of measuring them, stitching mismatched references together, skipping mobile, and inheriting a reference site's accessibility problems. Run through it before generating code from a reference-driven brief.
