> Last updated: 2026-07-03 · Module version: 0.1

# Accessibility & Performance Audit

Pairs with `data/testing/a11y-perf-checklist.csv` (25 checks: 14 accessibility, 11 performance) — query via `scripts/common/search.py`. This is the lighter, QA-focused a11y/performance checklist; the full cybersecurity module (Phase 5) is separate and deeper.

## Accessibility — the Critical-Severity Floor

Before anything else, these five are marked Critical in the checklist and represent complete blockers for some users, not minor polish:
- Semantic HTML elements used for their actual purpose (`QA026`) — a `<div>` styled as a button gets none of the built-in keyboard/focus/screen-reader behavior a real `<button>` gets for free.
- Color contrast meeting WCAG AA (`QA027`) — 4.5:1 normal text, 3:1 large text; check muted/secondary text specifically, it's where this most commonly fails.
- Full keyboard operability (`QA028`) plus a visible focus indicator on every focusable element (`QA029`) — never strip focus outlines without an equally visible replacement.
- Labeled form inputs (`QA031`) — a placeholder is not a label; it disappears exactly when the user starts interacting with the field.
- An escape route from every modal (`QA037`) — Escape key or a visible close button, no permanent focus trap.

## Accessibility — Running the Check

Two layers, both necessary:
1. **Automated scan in CI** (`QA039`) — axe-core (via Playwright/Cypress) or an eslint accessibility plugin, as a required PR check. Catches roughly a third of WCAG issues reliably (contrast, missing labels, ARIA misuse) for near-zero ongoing cost once wired in.
2. **Manual keyboard-only pass** — tab through the actual interface without a mouse before shipping a new flow; automated scans don't catch everything (logical tab order, whether a custom widget's keyboard behavior actually makes sense).

Beyond the floor: icon-only buttons need an accessible name (`QA032`), heading hierarchy must stay sequential (`QA033`), never convey information by color alone (`QA034`), respect `prefers-reduced-motion` (`QA035`), provide a skip-to-content link (`QA036`), and keep touch targets at least 44×44px on mobile (`QA038`).

## Performance — Core Web Vitals

The three that are both user-experience-critical and directly affect search ranking, all marked Critical:
- **LCP < 2.5s** (`QA040`) — largest visible content element rendered.
- **INP < 200ms** (`QA041`) — responsiveness to interaction throughout the session, not just the first click.
- **CLS < 0.1** (`QA042`) — no unexpected layout shift; reserve space for images/embeds/async content before it arrives.

**Measure with real field data (CrUX/RUM), not just lab scores** (`QA050`) — a page can score perfectly on a fast dev machine in Lighthouse and still perform poorly for real users on mid-range mobile over cellular. Lab scores are for local iteration; field data is what actually matters for both users and ranking.

## Performance — the Usual Suspects

In rough order of typical impact:
1. **Unoptimized images** (`QA043`) — consistently the single largest contributor to page weight; serve WebP/AVIF with responsive sizing.
2. **Render-blocking resources** (`QA048`) and **unmanaged third-party scripts** (`QA046`) — anything not needed for above-the-fold content should be deferred/async, and every third-party script should be periodically re-justified (each one is a third party with code execution on your page).
3. **Monolithic JS bundles** (`QA045`) — route-level code splitting so users download only what the current page needs; enforce with a **bundle-size budget in CI** (`QA049`) so regressions are caught per-PR, not discovered after the fact.
4. **Lazy-loading** below-the-fold content (`QA044`) and **non-blocking font loading** (`QA047`, `font-display: swap`) round out the list.

## Relationship to the UI/UX Module (Phase 7)

This checklist covers *verifiable, testable* accessibility and performance checks — the kind you can automate or measure. The UI/UX & Distinctive Frontend module (Phase 7) covers the qualitative design side (color systems, typography, layout, distinctiveness) that this checklist doesn't touch. Use both together when reviewing a UI: this file for "does it work for everyone and load fast," that module for "does it look intentional and not generic."
