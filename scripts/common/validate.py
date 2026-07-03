#!/usr/bin/env python3
"""Validate every data/**/*.csv against the conventions in references/conventions.md.

Checks, per file:
  - header matches exactly one of the two schemas (decision-matrix or checklist)
  - every id uses the module's registered prefix and is unique across the whole skill
  - checklist severity is one of Critical/High/Medium/Low
  - last_verified parses as YYYY-MM-DD
  - no empty required cells

Exits non-zero if any check fails, so it can gate CI. Stdlib only.
"""
import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

DECISION_HEADER = ["id", "category", "option", "best_for", "avoid_when", "tradeoffs", "tags", "last_verified"]
CHECKLIST_HEADER = ["id", "category", "check", "description", "why_it_matters", "severity", "tags", "last_verified"]
SEVERITIES = {"Critical", "High", "Medium", "Low"}

# module directory -> allowed ID prefix (see conventions.md "Check-ID Prefixes")
PREFIXES = {
    "ai": "AI",
    "analytics": "AN",
    "backend": "BE",
    "database": "DB",
    "devops": "DO",
    "email": "EM",
    "testing": "QA",
    "security": "SEC",
    "ecommerce": "EC",
    "ui-ux": "UX",
    "seo": "SEO",
    "ads": "ADS",
}

ID_RE = re.compile(r"^([A-Z]+)(\d{3,})$")


def validate_file(path: Path, module: str, seen_ids: dict) -> list:
    errors = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            return [f"{path}: file is empty"]

        if header == DECISION_HEADER:
            schema = "decision"
        elif header == CHECKLIST_HEADER:
            schema = "checklist"
        else:
            return [f"{path}: header matches neither schema: {header}"]

        expected_prefix = PREFIXES.get(module)
        if expected_prefix is None:
            errors.append(f"{path}: module dir '{module}' has no registered ID prefix (update PREFIXES + conventions.md)")

        for lineno, row in enumerate(reader, start=2):
            if len(row) != len(header):
                errors.append(f"{path}:{lineno}: expected {len(header)} columns, got {len(row)}")
                continue
            rec = dict(zip(header, row))

            for col, val in rec.items():
                if not val.strip():
                    errors.append(f"{path}:{lineno}: empty '{col}'")

            m = ID_RE.match(rec["id"])
            if not m:
                errors.append(f"{path}:{lineno}: malformed id '{rec['id']}'")
            else:
                if expected_prefix and m.group(1) != expected_prefix:
                    errors.append(f"{path}:{lineno}: id '{rec['id']}' should use prefix '{expected_prefix}'")
                if rec["id"] in seen_ids:
                    errors.append(f"{path}:{lineno}: duplicate id '{rec['id']}' (also in {seen_ids[rec['id']]})")
                else:
                    seen_ids[rec["id"]] = f"{path.name}:{lineno}"

            if schema == "checklist" and rec["severity"] not in SEVERITIES:
                errors.append(f"{path}:{lineno}: invalid severity '{rec['severity']}'")

            try:
                datetime.strptime(rec["last_verified"], "%Y-%m-%d")
            except ValueError:
                errors.append(f"{path}:{lineno}: last_verified '{rec['last_verified']}' is not YYYY-MM-DD")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", nargs="?", default=None,
                        help="skill root directory (default: two levels up from this script)")
    args = parser.parse_args()

    root = Path(args.root) if args.root else Path(__file__).resolve().parents[2]
    data_dir = root / "data"
    if not data_dir.is_dir():
        print(f"error: {data_dir} not found", file=sys.stderr)
        return 2

    files = sorted(data_dir.glob("*/*.csv"))
    if not files:
        print(f"error: no CSV files under {data_dir}", file=sys.stderr)
        return 2

    seen_ids: dict = {}
    errors = []
    rows_total = 0
    for path in files:
        errors.extend(validate_file(path, path.parent.name, seen_ids))
        rows_total += max(0, sum(1 for _ in path.open(encoding="utf-8")) - 1)

    if errors:
        for e in errors:
            print(f"FAIL {e}")
        print(f"\n{len(errors)} error(s) across {len(files)} files.")
        return 1

    print(f"OK: {len(files)} CSV files, {rows_total} rows, {len(seen_ids)} unique IDs — all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
