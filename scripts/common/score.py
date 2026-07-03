#!/usr/bin/env python3
"""Compute a severity-weighted score from any checklist-schema CSV in this skill.

Stdlib only -- no third-party dependencies (references/conventions.md).
Reuses the weighting formula documented in references/conventions.md and
references/security-scoring.md (originally proven in the `ads` skill):

    Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
    score = 100 - (sum of weights of FAILED checks / sum of weights of
                    EVALUATED checks) * 100

Checks not present in --results are excluded from the denominator (treated
as not-evaluated), not counted as failures -- a partial run scores what was
actually checked.

--results is a JSON file mapping check id -> "pass" | "fail" | "n/a".
"n/a" (not applicable) is also excluded from the denominator.

Examples:
    python3 score.py ../../data/security/owasp-checklist.csv --results results.json
    python3 score.py ../../data/security --results results.json  # score every CSV combined
"""

import argparse
import csv
import json
import sys
from pathlib import Path

WEIGHTS = {"critical": 5.0, "high": 3.0, "medium": 1.5, "low": 0.5}


def load_checks(path: Path):
    """Yield (source_file, row_dict) for one CSV or every *.csv under a directory."""
    files = sorted(path.rglob("*.csv")) if path.is_dir() else [path]
    for f in files:
        with f.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if "severity" in row and row.get("id"):
                    yield f, row


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="A checklist-schema CSV, or a directory to score all CSVs in")
    parser.add_argument("--results", type=Path, required=True, help='JSON file: {"CHECK_ID": "pass"|"fail"|"n/a"}')
    args = parser.parse_args()

    if not args.results.exists():
        print(f"error: results file not found: {args.results}", file=sys.stderr)
        sys.exit(1)
    results = json.loads(args.results.read_text(encoding="utf-8"))

    checks = list(load_checks(args.path))
    if not checks:
        print(f"error: no checklist-schema rows found under {args.path}", file=sys.stderr)
        sys.exit(1)

    total_weight = 0.0
    failed_weight = 0.0
    evaluated = 0
    not_evaluated = 0
    unknown_ids = []
    by_severity_failed = {}

    for _src, row in checks:
        check_id = row["id"]
        severity = row.get("severity", "").strip().lower()
        weight = WEIGHTS.get(severity)
        if weight is None:
            continue  # skip rows with an unrecognized/missing severity value

        outcome = results.get(check_id)
        if outcome is None:
            not_evaluated += 1
            continue
        if outcome not in ("pass", "fail", "n/a"):
            unknown_ids.append((check_id, outcome))
            continue
        if outcome == "n/a":
            continue

        evaluated += 1
        total_weight += weight
        if outcome == "fail":
            failed_weight += weight
            by_severity_failed[severity] = by_severity_failed.get(severity, 0) + 1

    if unknown_ids:
        print(f"warning: {len(unknown_ids)} result(s) had an unrecognized outcome value (want pass/fail/n-a): {unknown_ids[:5]}", file=sys.stderr)

    if total_weight == 0:
        print("No evaluated checks with a recognized severity -- nothing to score.")
        sys.exit(0)

    score = 100 - (failed_weight / total_weight) * 100

    print(f"Score: {score:.1f} / 100")
    print(f"Evaluated: {evaluated} checks ({not_evaluated} not evaluated, excluded from denominator)")
    if by_severity_failed:
        print("Failed checks by severity:")
        for sev in ("critical", "high", "medium", "low"):
            if sev in by_severity_failed:
                print(f"  {sev.capitalize()}: {by_severity_failed[sev]}")
    else:
        print("No failed checks among those evaluated.")


if __name__ == "__main__":
    main()
