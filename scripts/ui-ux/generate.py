#!/usr/bin/env python3
"""Scaffold design tokens (and optional component skeletons) from this skill's
UI/UX data rows.

Stdlib only -- no third-party dependencies (references/conventions.md).

Token sources, in precedence order:
  --colors/--fonts explicit values  >  --palette/--type CSV row ids

Palette rows (data/ui-ux/colors.csv) embed hex values in prose, so extraction
is heuristic: first hex = base, second = surface (if 3+ present), last =
accent, the darkest remaining = text. Override any role explicitly with
--colors "base,surface,text,accent" when the guess is wrong.

Component skeletons are deliberately unfinished: TODO-marked structure that
still requires real copy, real imagery, and the UX050 "could five competitors
ship this page?" check. They are starting points, not finished pages -- this
skill's whole UI/UX module exists to avoid templated output.

--style applies a style-vocabulary.csv row's token tendencies (radius, shadow,
border width, spacing density) on top of the palette/type choice -- see
references/art-direction-derivation.md for how to pick the style.

Examples:
    python3 generate.py --palette UX088 --type UX098 --dry-run
    python3 generate.py --palette UX088 --type UX100 --style UX141 --dry-run
    python3 generate.py --colors "#0B0B0E,#131318,#E7E7EA,#5E6AD2" --fonts "Inter" --output ./my-app
    python3 generate.py --palette UX091 --type UX099 --style UX130 --components hero,nav,footer --stack html --output ./site
"""

import argparse
import csv
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
DATA = SKILL_ROOT / "data" / "ui-ux"
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")
COMPONENTS = ["hero", "nav", "feature", "footer", "cta", "sidebar", "table", "form", "empty-state"]
STACKS = ["react-tailwind", "html"]


def load_row(csv_name: str, row_id: str) -> dict:
    path = DATA / csv_name
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["id"] == row_id:
                return row
    sys.exit(f"error: id {row_id} not found in {path.name}")


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


ROLE_WORDS = {"base": "base", "wash": "base", "surface": "surface", "surfaces": "surface",
              "text": "text", "ink": "text", "accent": "accent", "accents": "accent"}
HEX_THEN_WORD = re.compile(r"(#[0-9A-Fa-f]{3,6})\s+([A-Za-z-]+)")
WORD_THEN_HEX = re.compile(r"([A-Za-z-]+)\s+(#[0-9A-Fa-f]{3,6})")


def saturation(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return max(r, g, b) - min(r, g, b)


def roles_from_palette(option_text: str) -> dict:
    """Role assignment from hexes in a palette row's prose. Rows label roles
    inline ('#F7F4EE base', 'accent #C6FF4F') -- use those labels first, fall
    back to position, and pick the most saturated leftover for a missing accent."""
    hexes = HEX_RE.findall(option_text)
    if not hexes:
        sys.exit('error: palette row has no extractable hex values -- pass --colors "base,surface,text,accent"')

    roles: dict[str, str] = {}
    labeled = set()
    for hex_c, word in HEX_THEN_WORD.findall(option_text):
        role = ROLE_WORDS.get(word.lower())
        if role and role not in roles:
            roles[role], _ = hex_c, labeled.add(hex_c.lower())
    for word, hex_c in WORD_THEN_HEX.findall(option_text):
        role = ROLE_WORDS.get(word.lower())
        if role and role not in roles:
            roles[role], _ = hex_c, labeled.add(hex_c.lower())

    leftover = [h for h in hexes if h.lower() not in labeled]
    if "base" not in roles and leftover:
        roles["base"] = leftover.pop(0)
    if "base" not in roles:
        sys.exit('error: could not identify a base color -- pass --colors explicitly')
    if "accent" not in roles and leftover:
        candidate = max(leftover, key=saturation)
        if saturation(candidate) > 0.15:  # a near-gray "accent" is a misread, not an accent
            roles["accent"] = candidate
            leftover.remove(candidate)
    if "text" not in roles and leftover:
        dark_base = luminance(roles["base"]) < 0.5
        candidate = (max if dark_base else min)(leftover, key=luminance)
        if saturation(candidate) < 0.25:  # text must be near-neutral; saturated leftovers are accents
            roles["text"] = candidate
            leftover.remove(candidate)

    roles.setdefault("surface", roles["base"])
    roles.setdefault("text", "#E7E7EA" if luminance(roles["base"]) < 0.5 else "#1A1A1A")
    if "accent" not in roles:
        roles["accent"] = roles["text"]
        print("warning: palette row names no accent hex -- accent set to text color; "
              'override with --colors "base,surface,text,accent"', file=sys.stderr)
    return roles


def roles_from_args(colors_arg: str) -> dict:
    parts = [c.strip() for c in colors_arg.split(",") if c.strip()]
    if len(parts) < 2:
        sys.exit('error: --colors needs at least "base,accent"')
    names = ["base", "surface", "text", "accent"]
    roles = dict(zip(names, parts))
    roles.setdefault("surface", roles["base"])
    roles.setdefault("text", "#E7E7EA" if luminance(roles["base"]) < 0.5 else "#1A1A1A")
    roles.setdefault("accent", parts[-1])
    if len(parts) == 2:  # base,accent shorthand
        roles["accent"] = parts[1]
        roles["surface"] = roles["base"]
    return roles


def fonts_from_type_row(option_text: str) -> dict:
    """Type rows describe pairing *logic*, not families -- emit TODO placeholders."""
    return {"display": "/* TODO: pick display family per this pairing */", "body": "/* TODO: pick body family */", "note": option_text}


# Style-vocabulary rows (style-vocabulary.csv, UX125-UX154) embed token
# tendencies in their tags column. Known tags map to concrete token values;
# unknown radius-*/shadow-*/density-*/border-* tags warn instead of guessing.
STYLE_TAG_VALUES = {
    "radius-none": ("radius", {"--radius-sm": "0", "--radius-md": "0", "--radius-lg": "0"}),
    "radius-soft": ("radius", {"--radius-sm": "4px", "--radius-md": "8px", "--radius-lg": "16px"}),
    "radius-pill": ("radius", {"--radius-sm": "8px", "--radius-md": "16px", "--radius-lg": "9999px"}),
    "shadow-none": ("shadow", {"--shadow-raised": "none", "--shadow-lifted": "none"}),
    "shadow-flat": ("shadow", {"--shadow-raised": "0 1px 2px rgb(0 0 0 / 0.06)", "--shadow-lifted": "0 2px 8px rgb(0 0 0 / 0.08)"}),
    "shadow-soft": ("shadow", {"--shadow-raised": "0 2px 8px rgb(0 0 0 / 0.08)", "--shadow-lifted": "0 8px 24px rgb(0 0 0 / 0.12)"}),
    "shadow-hard": ("shadow", {"--shadow-raised": "4px 4px 0 var(--color-text)", "--shadow-lifted": "6px 6px 0 var(--color-text)"}),
    "border-hairline": ("border", {"--border-width": "1px"}),
    "border-heavy": ("border", {"--border-width": "2px"}),
    "density-tight": ("density", {"--space-unit": "4px"}),
    "density-airy": ("density", {"--space-unit": "8px"}),
}
TOKEN_TAG_PREFIXES = ("radius-", "shadow-", "border-", "density-")


def style_tokens_from_row(row: dict) -> dict:
    """Collect token declarations from a style row's tags. First tag wins per
    group; conflicting or unknown token-looking tags produce a warning."""
    tokens: dict[str, str] = {}
    seen_groups: set[str] = set()
    for tag in row["tags"].split("|"):
        tag = tag.strip()
        if tag in STYLE_TAG_VALUES:
            group, values = STYLE_TAG_VALUES[tag]
            if group in seen_groups:
                print(f"warning: style row {row['id']} has conflicting {group}-* tags; keeping the first", file=sys.stderr)
                continue
            seen_groups.add(group)
            tokens.update(values)
        elif tag.startswith(TOKEN_TAG_PREFIXES):
            print(f"warning: unknown style token tag '{tag}' in {row['id']} -- ignored", file=sys.stderr)
    return tokens


def render_style_block(row: dict, tokens: dict) -> str:
    style_name = row["option"].split("—")[0].strip()
    lines = [f"\n  /* style tokens -- {row['id']} ({style_name}) */"]
    lines += [f"  {name}: {value};" for name, value in tokens.items()]
    return "\n".join(lines) + "\n"


def render_style_ext(tokens: dict) -> str:
    parts = []
    if "--radius-md" in tokens:
        parts.append(f'      borderRadius: {{ sm: "{tokens["--radius-sm"]}", DEFAULT: "{tokens["--radius-md"]}", lg: "{tokens["--radius-lg"]}" }},')
    if "--shadow-raised" in tokens:
        parts.append(f'      boxShadow: {{ raised: "{tokens["--shadow-raised"]}", lifted: "{tokens["--shadow-lifted"]}" }},')
    if not parts:
        return ""
    return "\n" + "\n".join(parts)


TOKENS_CSS = """/* design-tokens.css -- generated by fullstack-pro-max (UX114: tokens, not one-offs).
   Import once, before component styles. */
:root {{
  --color-base: {base};
  --color-surface: {surface};
  --color-text: {text};
  --color-accent: {accent};
  --color-muted: color-mix(in srgb, var(--color-text) 55%, var(--color-base));
  --color-border: color-mix(in srgb, var(--color-text) 14%, var(--color-base));

  /* type -- {type_note} */
  --font-display: {display_font};
  --font-body: {body_font};
{style_block}
  /* motion tokens (UX114) */
  --motion-fast: 120ms;
  --motion-base: 200ms;
  --motion-slow: 400ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}}

@media (prefers-reduced-motion: reduce) {{
  :root {{ --motion-fast: 0ms; --motion-base: 0ms; --motion-slow: 0ms; }}
}}
"""

TAILWIND_CONFIG = """import type {{ Config }} from "tailwindcss";

// generated by fullstack-pro-max -- palette {palette_src}, pairing {type_src}
export default {{
  content: ["./app/**/*.{{ts,tsx}}", "./components/**/*.{{ts,tsx}}"],
  theme: {{
    extend: {{
      colors: {{
        base: "{base}",
        surface: "{surface}",
        ink: "{text}",
        accent: "{accent}",
      }},
      fontFamily: {{
        display: ["var(--font-display)"],
        body: ["var(--font-body)"],
      }},{style_ext}
      transitionDuration: {{ fast: "120ms", base: "200ms", slow: "400ms" }},
      transitionTimingFunction: {{ out: "cubic-bezier(0.16, 1, 0.3, 1)" }},
    }},
  }},
  plugins: [],
}} satisfies Config;
"""

# -- component skeletons: structure + checklist pointers, deliberately unfinished --

REACT_COMPONENTS = {
    "hero": """export function Hero() {
  // UX034: this hero is asymmetric on purpose -- don't recentre it back to the default.
  // UX044: replace every TODO with copy specific to THIS product, not template phrases.
  return (
    <section className="border-b border-ink/10 px-8 py-24 md:px-16">
      <div className="max-w-3xl">
        <p className="mb-4 font-display text-sm text-accent">{/* TODO: kicker */}</p>
        <h1 className="font-display text-5xl font-bold leading-tight md:text-6xl">{/* TODO: specific value prop */}</h1>
        <p className="mt-6 max-w-xl text-lg text-ink/70">{/* TODO: mechanism, not adjectives */}</p>
        <div className="mt-10">
          <a href="#" className="rounded-md bg-accent px-5 py-3 font-medium text-base transition-colors duration-base ease-out hover:bg-accent/90">
            {/* TODO: verb-first CTA */}
          </a>
        </div>
      </div>
    </section>
  );
}
""",
    "nav": """export function Nav() {
  // UX115/UX116: pick the mobile collapse pattern deliberately (drawer vs bottom tabs).
  return (
    <header className="sticky top-0 z-40 border-b border-ink/10 bg-base/90 backdrop-blur">
      <nav className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
        <a href="/" className="font-display font-bold">{/* TODO: wordmark */}</a>
        <div className="hidden gap-6 md:flex">{/* TODO: 3-5 links max */}</div>
        <button className="md:hidden" aria-label="Menu">{/* TODO: drawer trigger */}</button>
      </nav>
    </header>
  );
}
""",
    "feature": """export function FeatureSection() {
  // UX035: vary this section's rhythm vs. its neighbors -- don't clone padding.
  // UX117: grid collapses to a stack; keep source order logical.
  return (
    <section className="mx-auto grid max-w-6xl gap-8 px-6 py-20 md:grid-cols-3">
      {/* TODO: map real features; each card = claim + mechanism, not icon + adjective */}
      <div className="rounded-lg bg-surface p-8 transition-transform duration-base ease-out hover:-translate-y-1">
        <h3 className="font-display font-semibold">{/* TODO */}</h3>
        <p className="mt-2 text-sm text-ink/70">{/* TODO */}</p>
      </div>
    </section>
  );
}
""",
    "footer": """export function Footer() {
  return (
    <footer className="border-t border-ink/10 px-6 py-12 text-sm text-ink/60">
      <div className="mx-auto flex max-w-6xl flex-col justify-between gap-6 md:flex-row">
        <span>{/* TODO: legal line */}</span>
        <nav className="flex gap-6">{/* TODO: secondary links */}</nav>
      </div>
    </footer>
  );
}
""",
    "cta": """export function CtaBand() {
  // UX043: generous space around the CTA is the emphasis tool -- resist cramming.
  return (
    <section className="px-6 py-24 text-center">
      <h2 className="font-display text-3xl font-bold">{/* TODO: restate the outcome */}</h2>
      <a href="#" className="mt-8 inline-block rounded-md bg-accent px-6 py-3 font-medium text-base">
        {/* TODO: same CTA verb as hero */}
      </a>
    </section>
  );
}
""",
    "sidebar": """export function Sidebar() {
  // UX115: persistent rail >=1024px, overlay drawer below -- wire the drawer state in the shell.
  return (
    <aside className="hidden w-60 shrink-0 border-r border-ink/10 p-4 lg:block">
      <div className="mb-6 font-display font-bold">{/* TODO: product name */}</div>
      <nav className="space-y-1">{/* TODO: nav items with active state distinct from hover (UX046) */}</nav>
    </aside>
  );
}
""",
    "table": """export function DataTable() {
  // UX118: below tablet width this should render as labeled cards, not a squeezed table.
  return (
    <div className="overflow-x-auto rounded-lg border border-ink/10">
      <table className="w-full text-sm">
        <thead className="bg-surface text-left text-ink/60">
          <tr>{/* TODO: th cells -- tabular-nums on numeric columns */}</tr>
        </thead>
        <tbody>{/* TODO: rows; hover actions need touch equivalents (UX120) */}</tbody>
      </table>
    </div>
  );
}
""",
    "form": """export function Form() {
  // UX123: single column, full-width fields, correct inputmode/autocomplete per field.
  return (
    <form className="mx-auto max-w-md space-y-5">
      <label className="block">
        <span className="mb-1 block text-sm text-ink/70">{/* TODO: label */}</span>
        <input className="w-full rounded-md border border-ink/20 bg-surface px-4 py-2.5 outline-none transition-colors duration-fast focus:border-accent" />
      </label>
      {/* UX113: on validation error -- shake + color + message, never color alone */}
      <button className="w-full rounded-md bg-accent py-3 font-medium text-base">{/* TODO */}</button>
    </form>
  );
}
""",
    "empty-state": """export function EmptyState() {
  // UX045: empty states are disproportionately what NEW users see -- design, don't default.
  return (
    <div className="flex flex-col items-center gap-4 py-24 text-center">
      <div className="h-12 w-12 rounded-full bg-surface">{/* TODO: real illustration/icon, consistent with the icon set (UX041) */}</div>
      <p className="font-display font-semibold">{/* TODO: what belongs here */}</p>
      <p className="max-w-sm text-sm text-ink/60">{/* TODO: the one action that fixes emptiness */}</p>
      <button className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-base">{/* TODO */}</button>
    </div>
  );
}
""",
}

HTML_COMPONENT = """<!-- {name}.html -- generated skeleton. Uses design-tokens.css variables.
     TODO-marked on purpose: real copy + the UX050 five-competitors check before shipping. -->
<section class="{name}">
  <!-- TODO: port the structure from the react-tailwind variant of '{name}' in
       this skill's scripts/ui-ux/generate.py, using var(--color-*) tokens.
       Checklist pointers: {checks} -->
</section>
"""

HTML_CHECKS = {
    "hero": "UX034 asymmetry, UX044 specific copy",
    "nav": "UX115/UX116 collapse pattern",
    "feature": "UX035 rhythm, UX117 stack order",
    "footer": "UX044 copy",
    "cta": "UX043 whitespace emphasis",
    "sidebar": "UX115 rail-to-drawer",
    "table": "UX118 card transform, UX120 touch actions",
    "form": "UX123 single column + inputmode",
    "empty-state": "UX045 designed empty state",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--palette", help="colors.csv row id, e.g. UX088")
    parser.add_argument("--type", dest="type_row", help="typography.csv row id, e.g. UX098")
    parser.add_argument("--colors", help='explicit roles: "base,surface,text,accent" (or "base,accent")')
    parser.add_argument("--fonts", help='explicit families: "Display Family, Body Family"')
    parser.add_argument("--style", dest="style_row", help="style-vocabulary.csv row id, e.g. UX126 -- applies the style's radius/shadow/border/density token tendencies")
    parser.add_argument("--components", help=f"comma list from: {','.join(COMPONENTS)}")
    parser.add_argument("--stack", choices=STACKS, default="react-tailwind")
    parser.add_argument("--output", type=Path, default=Path("./generated"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.colors and not args.palette:
        sys.exit("error: provide --palette UXnnn or explicit --colors")

    if args.colors:
        roles = roles_from_args(args.colors)
        palette_src = "explicit --colors"
    else:
        row = load_row("colors.csv", args.palette)
        roles = roles_from_palette(row["option"])
        palette_src = f"{args.palette} ({row['option'].split('(')[0].strip()})"

    if args.fonts:
        parts = [f.strip() for f in args.fonts.split(",")]
        fonts = {"display": f'"{parts[0]}", sans-serif', "body": f'"{parts[-1]}", sans-serif', "note": "explicit --fonts"}
        type_src = "explicit --fonts"
    elif args.type_row:
        trow = load_row("typography.csv", args.type_row)
        fonts = fonts_from_type_row(trow["option"])
        type_src = args.type_row
    else:
        fonts = {"display": "system-ui, sans-serif", "body": "system-ui, sans-serif", "note": "default system stack -- pass --type or --fonts"}
        type_src = "none"

    style_block, style_ext = "", ""
    if args.style_row:
        srow = load_row("style-vocabulary.csv", args.style_row)
        stokens = style_tokens_from_row(srow)
        if stokens:
            style_block = render_style_block(srow, stokens)
            style_ext = render_style_ext(stokens)

    files: dict[str, str] = {}
    files["design-tokens.css"] = TOKENS_CSS.format(
        **roles, type_note=fonts["note"][:120], display_font=fonts["display"], body_font=fonts["body"],
        style_block=style_block,
    )
    if args.stack == "react-tailwind":
        files["tailwind.config.ts"] = TAILWIND_CONFIG.format(**roles, palette_src=palette_src, type_src=type_src, style_ext=style_ext)

    if args.components:
        wanted = [c.strip() for c in args.components.split(",") if c.strip()]
        bad = [c for c in wanted if c not in COMPONENTS]
        if bad:
            sys.exit(f"error: unknown component(s) {bad}; valid: {COMPONENTS}")
        for name in wanted:
            if args.stack == "react-tailwind":
                fname = "components/" + "".join(w.capitalize() for w in name.split("-")) + ".tsx"
                files[fname] = REACT_COMPONENTS[name]
            else:
                files[f"{name}.html"] = HTML_COMPONENT.format(name=name, checks=HTML_CHECKS[name])

    if args.dry_run:
        for fname, content in files.items():
            print(f"--- would write {args.output / fname} ---")
            print(content)
        return

    for fname, content in files.items():
        target = args.output / fname
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"wrote {target}")
    print("Next: fill every TODO with product-specific copy, then run the UX050 'five competitors' check (ux-guidelines.csv) before shipping.")


if __name__ == "__main__":
    main()
