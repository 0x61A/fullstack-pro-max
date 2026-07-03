#!/usr/bin/env python3
"""Scaffold locale routing config, per-locale message stubs, and an hreflang
generator for a chosen i18n library.

Stdlib only -- no third-party dependencies (references/conventions.md). The
*generated* code uses the project's own installed i18n library (next-intl or
react-i18next).

Non-negotiables baked into the scaffold: hreflang generated from one routing
source of truth, never hand-maintained per page (IN017); the first locale
given is the default and gets real placeholder strings, the rest get
TODO-marked stubs with identical key structure so translation coverage is
visible (IN031); a demo ICU plural key so plural-category handling (IN019,
IN027) is the pattern from day one, not a retrofit; no string concatenation
in the demo content (IN020).

Examples:
    python3 generate.py en tr --library next-intl --dry-run
    python3 generate.py en tr de --library react-i18next --output src/
"""

import argparse
import re
import sys
from pathlib import Path

LOCALE_RE = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")

NEXT_INTL_ROUTING = '''// i18n/routing.ts -- locale routing config (next-intl). Source of truth for
// hreflang generation (IN017) and the fallback chain (IN014).
import {{ defineRouting }} from "next-intl/routing";

export const locales = [{locales_list}] as const;
export const defaultLocale = "{default_locale}" as const;

export const routing = defineRouting({{
  locales,
  defaultLocale,
  localePrefix: "always", // IN011: subpath strategy (/en/..., /tr/...)
}});
'''

REACT_I18NEXT_CONFIG = '''// src/i18n/config.ts -- i18next config (react-i18next).
// Requires: npm install i18next react-i18next
import i18next from "i18next";
import {{ initReactI18next }} from "react-i18next";

export const locales = [{locales_list}] as const;
export const defaultLocale = "{default_locale}" as const;

i18next.use(initReactI18next).init({{
  resources: {{
    {resources_block}
  }},
  lng: defaultLocale,
  fallbackLng: defaultLocale, // IN014/IN030: missing keys degrade to a real language, never a raw key
  interpolation: {{ escapeValue: false }},
}});

export default i18next;
'''

HREFLANG_HELPER = '''// lib/hreflang.ts -- generates hreflang alternates from the single routing
// source of truth (IN017). Never hand-maintain these tags per page, and
// never force-redirect based on IP/browser locale alone (IN025 -- Critical).
import {{ locales, defaultLocale }} from "{routing_import}";

export function hreflangAlternates(pathname: string): Record<string, string> {{
  const alternates: Record<string, string> = {{}};
  for (const locale of locales) {{
    alternates[locale] = `/${{locale}}${{pathname}}`;
  }}
  alternates["x-default"] = `/${{defaultLocale}}${{pathname}}`;
  return alternates;
}}
'''

DEFAULT_MESSAGES = '''{{
  "common": {{
    "welcome": "Welcome, {{name}}!",
    "itemCount": "{{count, plural, one {{# item}} other {{# items}}}}"
  }}
}}
'''

STUB_MESSAGES = '''{{
  "common": {{
    "welcome": "TODO({locale}): translate -- Welcome, {{name}}!",
    "itemCount": "TODO({locale}): translate -- {{count, plural, one {{# item}} other {{# items}}}}"
  }}
}}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("locales", nargs="+", help="Locale codes, first one is the default (e.g. en tr de)")
    parser.add_argument("--library", required=True, choices=["next-intl", "react-i18next"])
    parser.add_argument("--output", default="generated", help="Output directory (default: generated/)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written instead of writing it")
    args = parser.parse_args()

    bad = [l for l in args.locales if not LOCALE_RE.match(l)]
    if bad:
        print(f"error: locale codes must look like 'en' or 'en-US': {', '.join(bad)}", file=sys.stderr)
        sys.exit(2)

    default_locale, *rest = args.locales
    locales_list = ", ".join(f'"{l}"' for l in args.locales)

    files = {}

    if args.library == "next-intl":
        files["i18n/routing.ts"] = NEXT_INTL_ROUTING.format(locales_list=locales_list, default_locale=default_locale)
        files["lib/hreflang.ts"] = HREFLANG_HELPER.format(routing_import="../i18n/routing")
    else:
        resources_block = "\n    ".join(
            f'{l}: {{ translation: require("../../messages/{l}.json") }},' for l in args.locales
        )
        files["src/i18n/config.ts"] = REACT_I18NEXT_CONFIG.format(
            locales_list=locales_list, default_locale=default_locale, resources_block=resources_block)
        files["lib/hreflang.ts"] = HREFLANG_HELPER.format(routing_import="../src/i18n/config")

    files[f"messages/{default_locale}.json"] = DEFAULT_MESSAGES.format()
    for l in rest:
        files[f"messages/{l}.json"] = STUB_MESSAGES.format(locale=l)

    if args.dry_run:
        for rel_path, content in files.items():
            print(f"--- would write {Path(args.output) / rel_path} ---")
            print(content)
        return

    for rel_path, content in files.items():
        out_path = Path(args.output) / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"wrote {out_path}")
    print(f"Next: translate the TODO-marked stub locales ({', '.join(rest) or 'none'}), then run the l10n checklist (data/i18n/l10n-checklist.csv).")


if __name__ == "__main__":
    main()
