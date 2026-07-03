#!/usr/bin/env python3
"""Scaffold secure-by-default security headers middleware for a stack.

Stdlib only -- no third-party dependencies (references/conventions.md).
Implements the security-headers baseline from data/security/owasp-checklist.csv
row SEC018: Content-Security-Policy, Strict-Transport-Security,
X-Content-Type-Options, frame-ancestors/X-Frame-Options, Referrer-Policy,
and Permissions-Policy, applied globally rather than per-route (SEC066).

The generated CSP is intentionally strict (self-only by default) with TODO
markers -- loosen it deliberately per external resource your app actually
needs (fonts, analytics, payment widgets), don't start permissive.

Examples:
    python3 generate.py --stack nextjs --output ./my-app
    python3 generate.py --stack express --output ./my-app --dry-run
    python3 generate.py --stack fastapi --output ./my-app
"""

import argparse
from pathlib import Path

STACKS = ["nextjs", "express", "fastapi"]

CSP_DEFAULT = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


def render_nextjs() -> str:
    return f"""// Security headers middleware (SEC018) -- applied to every response globally,
// not per-route (SEC066's reasoning applied to Next.js).
// Add this headers() function to next.config.js, or adapt into middleware.ts
// if you need per-route variation.

/** @type {{import('next').NextConfig}} */
const isDev = process.env.NODE_ENV !== "production";

const securityHeaders = [
  {{
    key: "Content-Security-Policy",
    // TODO: loosen deliberately per resource you actually need (fonts, analytics,
    // payment widgets) -- start strict, don't start permissive.
    value: "{CSP_DEFAULT}",
  }},
  {{ key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" }},
  {{ key: "X-Content-Type-Options", value: "nosniff" }},
  {{ key: "X-Frame-Options", value: "DENY" }},
  {{ key: "Referrer-Policy", value: "strict-origin-when-cross-origin" }},
  {{ key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" }},
];

module.exports = {{
  async headers() {{
    // Dev-only skip: Next.js dev mode bundles/HMR rely on runtime script
    // evaluation, which a strict script-src 'self' silently blocks -- every
    // client script fails and the page renders blank with zero console errors.
    // frame-ancestors 'none' / X-Frame-Options DENY also break local
    // iframe-based preview tooling.
    // Neither concern exists in a real deployment; the strict baseline above
    // applies as-is to the production build.
    if (isDev) return [];
    return [
      {{
        source: "/:path*",
        headers: securityHeaders,
      }},
    ];
  }},
}};
"""


def render_express() -> str:
    return f"""// Security headers middleware (SEC018) -- registered globally at app level
// (SEC066), before route handlers, so every response gets it automatically.
//
// The `helmet` npm package covers this more thoroughly and is the recommended
// production choice (`npm install helmet` then `app.use(helmet())` with a
// custom CSP directive). This hand-rolled version is provided so the file is
// usable with zero new dependencies if you want to review the headers
// explicitly before adding helmet.

function securityHeaders(req, res, next) {{
  // TODO: loosen the CSP deliberately per resource you actually need.
  res.setHeader("Content-Security-Policy", "{CSP_DEFAULT}");
  res.setHeader("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  next();
}}

module.exports = {{ securityHeaders }};

// In your app setup:
//   const {{ securityHeaders }} = require("./middleware/security-headers");
//   app.use(securityHeaders); // register before route handlers (SEC066)
"""


def render_fastapi() -> str:
    return f"""\"\"\"Security headers middleware (SEC018) -- registered once at the app
level (SEC066 applied to FastAPI), so every response gets it automatically.
\"\"\"

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# TODO: loosen deliberately per resource you actually need.
CSP = "{CSP_DEFAULT}"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = CSP
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


# In your app factory:
#   from .middleware.security_headers import SecurityHeadersMiddleware
#   app.add_middleware(SecurityHeadersMiddleware)
"""


RENDERERS = {"nextjs": render_nextjs, "express": render_express, "fastapi": render_fastapi}
FILE_PATHS = {
    "nextjs": "next.config.js.security-headers-snippet.js",
    "express": "src/middleware/security-headers.js",
    "fastapi": "app/middleware/security_headers.py",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stack", required=True, choices=STACKS)
    parser.add_argument("--output", type=Path, default=Path("./generated"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    content = RENDERERS[args.stack]()
    target = args.output / FILE_PATHS[args.stack]

    if args.dry_run:
        print(f"--- would write {target} ---")
        print(content)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"wrote {target}")
    if args.stack == "nextjs":
        print("Merge the headers()/securityHeaders content into your real next.config.js -- this file is a snippet, not a drop-in replacement.")
    print("Review and loosen the CSP deliberately per external resource your app actually needs (SEC018).")


if __name__ == "__main__":
    main()
