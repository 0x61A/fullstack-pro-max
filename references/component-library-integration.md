> Last updated: 2026-07-04 · Module version: 0.1

# Component Library Integration

Use this when the user wants a **ready-made component or theme** rather than a from-scratch build — "use something like 21st.dev," "is there a pre-built pricing table I can start from," "grab a shadcn theme for this." This is a different workflow from `reference-site-analysis.md`: that file is about *visual inspiration* (extract principles, never copy code); this file is about *actual reusable code* from a component/theme marketplace, brought in deliberately and reviewed before it ships.

`data/ui-ux/component-libraries.csv` (`UX245`-`UX268`) catalogs 18 real component/theme sources (21st.dev, shadcn/ui, Aceternity UI, Magic UI, Origin UI, Tailwind UI-adjacent marketplaces, Preline, Flowbite, Tremor, and more) plus 6 "Selection Guide" rows for common needs (fastest-to-ship, animation-heavy marketing, zero-budget, dashboards, non-React frameworks, AI-prompt-to-code). Unlike the known-sites-library, **this file is a live-fetch index, not a static answer** — always confirm current component code/API/pricing with `WebFetch` (or a connected live-browser tool) before writing anything from it into a project. Libraries update their component APIs and pricing tiers regularly; the `option` text here is a pointer to go look, not a snippet to paste from memory.

## Process

1. **Identify what's actually needed.** A component type (hero, navbar, pricing table, dashboard shell, login form) and any hard constraints: framework (React/Next.js/Vue/Svelte/plain HTML), Tailwind vs. other CSS approach, budget (free-only vs. paid-OK), and whether shadcn/ui ownership (code lands in-repo) matters to the team.
2. **Query the catalog.** `python3 scripts/common/search.py data/ui-ux/component-libraries.csv --tag hero` (swap the tag for the component type or need), or `--category "Selection Guide"` for a needs-based shortcut, or `--query "dashboard"` for free-text search across all fields.
3. **Surface 2-3 candidates to the user, not one silent pick.** Name the library, its tradeoff, and its cost tier — "For an animated hero, Aceternity UI or Magic UI both fit; Aceternity leans more 3D/parallax, Magic UI more particle/text-effect. Both have a free tier — want me to pull the current component code from one of these, or do you already have a library in mind?"
4. **Fetch the current code before writing anything.** Once a library and component are chosen, `WebFetch` the specific component's page (or use a connected live-browser tool) to get the actual current markup/JSX/install command — never reconstruct it from training-data memory, since these libraries change their APIs and file structure over time.
5. **Integrate by ecosystem, since the install path differs:**
   - **shadcn/ui-family** (shadcn/ui, shadcn/ui Blocks, 21st.dev, Origin UI, Cult UI, Aceternity UI, Magic UI, Shadcnblocks.com) — typically `npx shadcn@latest add <registry-url-or-name>`, or manual copy-paste into `components/ui/`. Code lands in the project's own repo; the team owns and can freely edit it afterward.
   - **Markup-only Tailwind kits** (Hyperui, Meraki UI, Mamba UI, and Tailwind UI/Preline's static blocks) — copy-paste the HTML/JSX directly, then wire up any interactivity (dropdown/modal state) yourself, and remap class names onto the project's own design tokens rather than leaving the kit's default palette in place.
   - **Installed packages** (HeroUI/NextUI, Flowbite React/Vue, Tremor, daisyUI) — `npm install` the package, import components, and theme through the library's own variant/theme API rather than editing its internals.
   - **AI generators** (v0.dev, 21st.dev's AI mode) — treat the output as a first draft only; it still needs the same review as hand-written code before it ships.
6. **Reconcile with the project, every time:**
   - Remap the imported component's colors/spacing/radius onto the project's existing design tokens — don't leave two competing color systems in one codebase.
   - Run it past `data/testing/a11y-perf-checklist.csv` — imported components can carry accessibility gaps (missing labels, poor focus order) that the source library itself may not have fixed.
   - Run `scripts/security/audit.py` if the component pulled in new third-party JS — check for anything that looks like an unexpected network call or inline script.
   - Check the library's current license terms (via the same `WebFetch` you already did) before shipping a paid-marketplace component into client work — verify seat/usage terms rather than assuming "paid once, use anywhere."
   - Still run brand-forward pages past `frontend-distinctiveness.md` — a popular library's default look is, by definition, something many other sites already use; re-skin before calling it done for anything brand-forward.

## When to use this vs. `reference-site-analysis.md` / `known-sites-library.csv`

- User points at a **look/vibe/competitor site** with no working code involved → `reference-site-analysis.md` (has a URL) or `known-sites-library.csv` (has no URL, needs a suggestion) — extract principles, write original code.
- User wants an **actual working component/page they can drop in and adapt** → this file — fetch real code from a real source, review it, then ship it.
- Both can chain: pick a visual direction from the known-sites-library flow first, then use this file to find a component library whose default look is already close to that direction (e.g. "dark-technical" direction → Aceternity UI/shadcn/ui dark-mode blocks as a faster starting point than a from-scratch build).
