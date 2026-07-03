#!/usr/bin/env python3
"""Cheap first-pass analysis of a reference site's HTML/CSS for design cues.

Stdlib only -- urllib for fetching, re/html.parser for extraction. No JS
rendering, no real layout measurement: this is a quick palette/font/keyword
hint pass meant to run *before or alongside* a live look via WebFetch or a
browser tool (Claude Preview / claude-in-chrome), not instead of one. See
references/reference-site-analysis.md for the full workflow.

Examples:
    python3 inspect.py https://example.com
    python3 inspect.py https://example.com --max-css 5 --timeout 15
"""
import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; fullstack-pro-max-inspect/1.0)"
COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|rgba?\([^)]+\)")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)", re.IGNORECASE)
LAYOUT_KEYWORDS = [
    "display:grid", "display: grid", "display:flex", "display: flex",
    "grid-template-columns", "position:sticky", "position: sticky",
    "backdrop-filter", "clip-path", "mix-blend-mode", "aspect-ratio",
]


class PageMetaParser(HTMLParser):
    """Collects <link rel=stylesheet href=...>, <title>, and meta description."""

    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.title = None
        self.description = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and (attrs.get("rel") or "").lower() == "stylesheet" and attrs.get("href"):
            self.stylesheets.append(attrs["href"])
        elif tag == "meta" and (attrs.get("name") or "").lower() == "description":
            self.description = attrs.get("content")
        elif tag == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._in_title and self.title is None:
            self.title = data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def top_colors(text, limit=12):
    counts = {}
    for match in COLOR_RE.findall(text):
        key = match.lower().strip()
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])[:limit]


def font_families(text, limit=8):
    seen = {}
    for match in FONT_FAMILY_RE.findall(text):
        value = match.strip().rstrip(";").strip()
        seen[value] = seen.get(value, 0) + 1
    return sorted(seen.items(), key=lambda kv: -kv[1])[:limit]


def layout_hits(text):
    lowered = text.lower()
    return [kw for kw in LAYOUT_KEYWORDS if kw in lowered]


def analyze(url, max_css=3, timeout=10):
    html = fetch(url, timeout=timeout)
    meta = PageMetaParser()
    meta.feed(html)

    css_blobs = [html]
    fetched_css = []
    for href in meta.stylesheets[:max_css]:
        css_url = urljoin(url, href)
        if urlparse(css_url).netloc != urlparse(url).netloc:
            continue  # same-origin only -- keep this a lightweight, low-risk pass
        try:
            css_blobs.append(fetch(css_url, timeout=timeout))
            fetched_css.append(css_url)
        except Exception:
            continue

    combined = "\n".join(css_blobs)
    return {
        "url": url,
        "title": meta.title,
        "meta_description": meta.description,
        "stylesheets_found": len(meta.stylesheets),
        "stylesheets_fetched": fetched_css,
        "top_colors": top_colors(combined),
        "font_families": font_families(combined),
        "layout_keyword_hits": layout_hits(combined),
        "note": (
            "Static HTML/CSS scan only -- no JS rendering, no real layout "
            "measurement. Cross-check with a live browser tool (Claude Preview "
            "/ claude-in-chrome) and read references/reference-site-analysis.md "
            "before finalizing a Reference Design Brief."
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", help="Reference site URL to analyze")
    parser.add_argument("--max-css", type=int, default=3, help="Max same-origin stylesheets to fetch (default: 3)")
    parser.add_argument("--timeout", type=int, default=10, help="Per-request timeout in seconds (default: 10)")
    args = parser.parse_args()

    try:
        result = analyze(args.url, max_css=args.max_css, timeout=args.timeout)
    except Exception as exc:
        print(f"Error fetching {args.url}: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
