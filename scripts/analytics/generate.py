#!/usr/bin/env python3
"""Scaffold a typed track-plan module ("track plan as code", AN014).

Stdlib only -- no third-party dependencies (references/conventions.md). The
generated module wraps your analytics provider behind one function per event,
so event names and properties are typo-proof, reviewable in PRs, and
documented in one place (AN032).

Event names must follow the object_action convention (AN013): lowercase
snake_case, past-tense verb -- e.g. signup_completed, checkout_started.

Examples:
    python3 generate.py signup_completed checkout_started --provider posthog --dry-run
    python3 generate.py order_completed --provider ga4 --output src/lib/
"""

import argparse
import re
import sys
from pathlib import Path

EVENT_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")

HEADER = '''// analytics.ts -- track plan as code (AN014). One function per event:
// adding an event means adding a function here, in a reviewed PR.
// Rules baked in: object_action naming (AN013), no PII in properties (AN023),
// identify only at the auth boundary (AN015).
{import_line}

// Shared properties attached to every event (AN017). Extend deliberately;
// never put emails, names, or free-text user input here (AN023).
type BaseProps = {{
  plan?: string;
  source?: string;
}};

function track(event: string, props: Record<string, unknown> = {{}}) {{
  // Consent gate (AN024): the provider must already be consent-gated at load;
  // this guard is defense in depth, not the primary control.
  if (typeof window !== "undefined" && !window.__analyticsConsent) return;
{track_call}
}}

// --- Auth boundary (AN015) ---
export function identifyUser(userId: string) {{
  // Opaque internal ID only -- never email (AN023).
{identify_call}
}}

export function resetIdentity() {{
{reset_call}
}}

// --- Events ---
'''

EVENT_FN = '''export function track{pascal}(props: BaseProps = {{}}) {{
  track("{name}", props);
}}
'''

PROVIDERS = {
    "posthog": {
        "import": 'import posthog from "posthog-js";',
        "track": '  posthog.capture(event, props);',
        "identify": '  posthog.identify(userId);',
        "reset": '  posthog.reset();',
    },
    "ga4": {
        "import": "// GA4 via gtag.js -- ensure the tag itself loads only after consent (AN024).",
        "track": '  (window as any).gtag?.("event", event, props);',
        "identify": '  (window as any).gtag?.("set", { user_id: userId });',
        "reset": '  (window as any).gtag?.("set", { user_id: null });',
    },
    "plausible": {
        "import": "// Plausible custom events -- aggregate-only tool; identify/reset are no-ops.",
        "track": '  (window as any).plausible?.(event, { props });',
        "identify": "  // Plausible is cookieless/aggregate by design: no user-level identify (AN002).",
        "reset": "  // no-op",
    },
}


def pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("events", nargs="+", help="Event names in object_action form (e.g. signup_completed)")
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    parser.add_argument("--output", default="generated", help="Output directory (default: generated/)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be written instead of writing it")
    args = parser.parse_args()

    bad = [e for e in args.events if not EVENT_RE.match(e)]
    if bad:
        print(f"error: event names must be object_action snake_case (AN013): {', '.join(bad)}", file=sys.stderr)
        sys.exit(2)

    p = PROVIDERS[args.provider]
    content = HEADER.format(import_line=p["import"], track_call=p["track"],
                            identify_call=p["identify"], reset_call=p["reset"])
    content += "\n".join(EVENT_FN.format(pascal=pascal(e), name=e) for e in args.events)

    out_path = Path(args.output) / "lib/analytics.ts"
    if args.dry_run:
        print(f"--- would write {out_path} ---")
        print(content)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"wrote {out_path}")
    print("Next: gate the provider snippet behind consent (AN024) and add new events only via PR (AN014).")


if __name__ == "__main__":
    main()
