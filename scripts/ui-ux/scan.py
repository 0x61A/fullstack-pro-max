#!/usr/bin/env python3
"""Cheap first-pass analysis of reference site(s) HTML/CSS for design cues.

Stdlib only -- urllib for fetching, re/html.parser for extraction. No JS
rendering, no real layout measurement: this is a quick palette/font/keyword
hint pass meant to run *before or alongside* a live look via WebFetch or a
browser tool (Claude Preview / claude-in-chrome), not instead of one. See
references/reference-site-analysis.md for the full workflow.

v2: accepts multiple URLs (shared-thread analysis per UX083), estimates WCAG
contrast ratios on the most frequent color pairs (UX086 hint), and --brief
emits a pre-filled Reference Design Brief markdown draft.

Examples:
    python3 scan.py https://example.com
    python3 scan.py https://a.com https://b.com --brief
    python3 scan.py https://example.com --max-css 5 --timeout 15
"""
import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; fullstack-pro-max-scan/2.0)"
COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|rgba?\([^)]+\)")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)", re.IGNORECASE)
LAYOUT_KEYWORDS = [
    "display:grid", "display: grid", "display:flex", "display: flex",
    "grid-template-columns", "position:sticky", "position: sticky",
    "backdrop-filter", "clip-path", "mix-blend-mode", "aspect-ratio",
    "container-type", "@container",
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


def normalize_hex(color):
    """#abc / #aabbcc -> #aabbcc lowercase; rgb()/rgba() left as-is (skipped for contrast)."""
    if not color.startswith("#"):
        return color.lower()
    h = color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.lower()


def top_colors(text, limit=12):
    counts = {}
    for match in COLOR_RE.findall(text):
        key = normalize_hex(match.strip())
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


def relative_luminance(hex_color):
    """WCAG relative luminance for a #rrggbb color."""
    h = hex_color.lstrip("#")
    channels = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    l1, l2 = sorted((relative_luminance(c1), relative_luminance(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def contrast_estimates(colors, limit=5):
    """Rough WCAG hints on the most frequent hex pairs (UX086). Estimates only:
    frequency in CSS text says nothing about which colors actually sit on which."""
    hexes = [c for c, _ in colors if c.startswith("#")][:6]
    pairs = []
    for i in range(len(hexes)):
        for j in range(i + 1, len(hexes)):
            ratio = contrast_ratio(hexes[i], hexes[j])
            pairs.append({
                "pair": f"{hexes[i]} on {hexes[j]}",
                "ratio": round(ratio, 2),
                "wcag": "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA-large-only" if ratio >= 3 else "fail",
            })
    pairs.sort(key=lambda p: -p["ratio"])
    return pairs[:limit]


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
    colors = top_colors(combined)
    return {
        "url": url,
        "title": meta.title,
        "meta_description": meta.description,
        "stylesheets_found": len(meta.stylesheets),
        "stylesheets_fetched": fetched_css,
        "top_colors": colors,
        "font_families": font_families(combined),
        "layout_keyword_hits": layout_hits(combined),
        "contrast_estimates": contrast_estimates(colors),
    }


def shared_thread(results):
    """Intersection hints across multiple references (UX083): the brief should be
    built on what the references share, not a collage of their one-offs."""
    if len(results) < 2:
        return None
    color_sets = [{c for c, _ in r["top_colors"] if c.startswith("#")} for r in results]
    shared_colors = set.intersection(*color_sets)
    dark_leaning = [
        r["url"] for r in results
        if any(relative_luminance(c) < 0.2 for c, n in r["top_colors"][:3] if c.startswith("#"))
    ]
    font_sets = []
    for r in results:
        generics = set()
        for fam, _ in r["font_families"]:
            low = fam.lower()
            for g in ("serif", "sans", "mono"):
                if g in low:
                    generics.add(g)
        font_sets.append(generics)
    shared_font_classes = set.intersection(*font_sets) if font_sets else set()
    all_layout = [set(r["layout_keyword_hits"]) for r in results]
    return {
        "shared_exact_colors": sorted(shared_colors),
        "dark_leaning_references": dark_leaning,
        "shared_font_classes": sorted(shared_font_classes),
        "shared_layout_keywords": sorted(set.intersection(*all_layout)) if all_layout else [],
    }


BRIEF_TEMPLATE = """# Reference Design Brief (draft — generated by scan.py, verify before use)

Reference(s): {urls}
Shared thread: {thread} <!-- TODO: replace with the actual design throughline, one sentence -->
Palette direction: {palette} <!-- TODO: describe as family+role, not literal hexes (UX078) -->
Typography direction: {typography} <!-- TODO: name the pairing logic explicitly (UX080) -->
Layout pattern: {layout} <!-- TODO: name the pattern (UX081); static scan can't see rendered layout -->
Motion/interaction level: unknown — static fetch only, verify with a live browser tool (UX082)
Deliberate divergence: <!-- TODO: what we change on purpose and why (UX084) -->
Confirmed with user: no

## Scan evidence (hints, not ground truth — no JS rendering)
{evidence}

> Checklist before code: data/ui-ux/reference-analysis-checklist.csv (UX078-UX087).
> Mobile viewport (UX085) and real computed styles still need a live browser check.
"""


def build_brief(results, thread):
    urls = ", ".join(r["url"] for r in results)
    first = results[0]
    hex_colors = [c for c, _ in first["top_colors"] if c.startswith("#")][:4]
    dark = hex_colors and relative_luminance(hex_colors[0]) < 0.3
    palette = f"{'dark-leaning' if dark else 'light-leaning'} base observed; frequent colors: {', '.join(hex_colors) or 'none extracted'}"
    fams = [f for f, _ in first["font_families"][:3]]
    typography = f"declared families: {'; '.join(fams) if fams else 'none extracted'}"
    layout = ", ".join(first["layout_keyword_hits"]) or "no layout keywords found in static CSS"
    if thread:
        thread_txt = (
            f"shared exact colors: {', '.join(thread['shared_exact_colors']) or 'none'}; "
            f"shared font classes: {', '.join(thread['shared_font_classes']) or 'none'}; "
            f"shared layout keywords: {', '.join(thread['shared_layout_keywords']) or 'none'}"
        )
    else:
        thread_txt = "single reference"
    evidence_lines = []
    for r in results:
        evidence_lines.append(f"- {r['url']} — title: {r['title']!r}; top colors: "
                              f"{', '.join(c for c, _ in r['top_colors'][:5])}; "
                              f"best contrast pairs: " +
                              ("; ".join(f"{p['pair']} = {p['ratio']} ({p['wcag']})" for p in r['contrast_estimates'][:2]) or "n/a"))
    return BRIEF_TEMPLATE.format(urls=urls, thread=thread_txt, palette=palette,
                                 typography=typography, layout=layout, evidence="\n".join(evidence_lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("urls", nargs="+", help="Reference site URL(s) — 2-3 for shared-thread analysis")
    parser.add_argument("--max-css", type=int, default=3, help="Max same-origin stylesheets to fetch per URL (default: 3)")
    parser.add_argument("--timeout", type=int, default=10, help="Per-request timeout in seconds (default: 10)")
    parser.add_argument("--brief", action="store_true", help="Emit a pre-filled Reference Design Brief markdown draft instead of JSON")
    args = parser.parse_args()

    results = []
    for url in args.urls:
        try:
            results.append(analyze(url, max_css=args.max_css, timeout=args.timeout))
        except Exception as exc:
            print(f"error fetching {url}: {exc}", file=sys.stderr)
    if not results:
        sys.exit(1)

    thread = shared_thread(results)

    if args.brief:
        print(build_brief(results, thread))
        return

    out = {"references": results}
    if thread:
        out["shared_thread"] = thread
    out["note"] = (
        "Static HTML/CSS scan only -- no JS rendering, no real layout measurement. "
        "Contrast ratios are frequency-pair estimates, not measured text/background pairs. "
        "Cross-check with a live browser tool and read references/reference-site-analysis.md."
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
