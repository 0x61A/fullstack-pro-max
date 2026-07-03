#!/usr/bin/env python3
"""Query helper for this skill's data/**/*.csv files.

Stdlib only (csv, json, argparse, pathlib) -- no third-party dependencies,
per this skill's conventions (see references/conventions.md).

Every CSV in data/ shares at least: id, category, tags, last_verified
(see references/conventions.md for the two schema variants). This script
works against any of them without needing to know which schema a given
file uses.

Examples:
    python3 search.py ../../data/backend/stacks.csv --tag supabase
    python3 search.py ../../data/backend --query "rate limit"
    python3 search.py ../../data/backend/stacks.csv --id BE009
    python3 search.py ../../data/security --category "Threat Modeling" --format json
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def load_rows(path: Path):
    """Yield (source_file, row_dict) for one CSV file or every *.csv under a directory."""
    if path.is_dir():
        files = sorted(path.rglob("*.csv"))
    elif path.is_file():
        files = [path]
    else:
        print(f"error: path not found: {path}", file=sys.stderr)
        sys.exit(1)

    for f in files:
        with f.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                yield f, row


def matches(row: dict, args) -> bool:
    if args.id and row.get("id", "").strip().lower() != args.id.strip().lower():
        return False

    if args.category:
        cat = row.get("category", "")
        if args.category.strip().lower() not in cat.strip().lower():
            return False

    if args.tag:
        tags = [t.strip().lower() for t in row.get("tags", "").split("|")]
        if args.tag.strip().lower() not in tags:
            return False

    if args.severity:
        sev = row.get("severity", "")
        if sev.strip().lower() != args.severity.strip().lower():
            return False

    if args.query:
        needle = args.query.strip().lower()
        haystack = " ".join(str(v) for v in row.values()).lower()
        if needle not in haystack:
            return False

    return True


def print_table(rows_with_source, show_source: bool):
    if not rows_with_source:
        print("No matches.")
        return

    # Prefer a compact, readable subset of columns over dumping every field.
    preferred = ["id", "category", "option", "check", "name", "severity", "priority"]
    _, first_row = rows_with_source[0]
    cols = [c for c in preferred if c in first_row] or list(first_row.keys())[:4]

    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for _, r in rows_with_source)) for c in cols}
    widths = {c: min(w, 40) for c, w in widths.items()}

    def fmt_row(values):
        return "  ".join(str(v)[: widths[c]].ljust(widths[c]) for c, v in zip(cols, values))

    header = [c for c in cols]
    print(fmt_row(header) + ("  source" if show_source else ""))
    print(fmt_row(["-" * widths[c] for c in cols]) + ("  ------" if show_source else ""))
    for src, row in rows_with_source:
        line = fmt_row([row.get(c, "") for c in cols])
        if show_source:
            line += f"  {src.name}"
        print(line)
    print(f"\n{len(rows_with_source)} match(es). Use --format json for full field detail.")


def main():
    parser = argparse.ArgumentParser(
        description="Filter this skill's data/**/*.csv files by id, category, tag, severity, or free-text query."
    )
    parser.add_argument("path", type=Path, help="A CSV file, or a directory to search recursively")
    parser.add_argument("--id", help="Exact match on the id column")
    parser.add_argument("--category", help="Substring match (case-insensitive) on the category column")
    parser.add_argument("--tag", help="Exact match against one of the |-separated values in the tags column")
    parser.add_argument("--severity", help="Exact match on the severity column (checklist-schema CSVs only)")
    parser.add_argument("--query", help="Case-insensitive substring match across all columns")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    parser.add_argument("--limit", type=int, default=50, help="Max rows to show (default 50)")
    args = parser.parse_args()

    results = [(src, row) for src, row in load_rows(args.path) if matches(row, args)]
    results = results[: args.limit]
    show_source = args.path.is_dir()

    if args.format == "json":
        payload = [dict(row, _source=src.name) if show_source else row for src, row in results]
        print(json.dumps(payload, indent=2))
    else:
        print_table(results, show_source)


if __name__ == "__main__":
    main()
