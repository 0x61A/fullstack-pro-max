#!/usr/bin/env python3
"""Static scan for the most common, mechanically-detectable violations of
this module's checklists.

Stdlib only -- no third-party dependencies (references/conventions.md). This
is a floor, not a substitute for the judgment-based checks in
owasp-checklist.csv / secure-coding-checks.csv / api-security-checks.csv --
a clean scan does not mean the checklist is satisfied (see
secure-coding-standards.md).

Detects: hardcoded-looking secrets (SEC007, SEC056), a handful of dangerous
code patterns (SEC009, SEC010, SEC058, SEC061, SEC062, SEC063), and an
absence of security-header configuration anywhere in the project (SEC018,
informational only -- a missing text match doesn't prove headers are unset,
just that this scan found no evidence they are).

Exits non-zero if any Critical/High-severity finding is present, so it can
gate CI.

Examples:
    python3 audit.py /path/to/project
    python3 audit.py /path/to/project --format json
    python3 audit.py /path/to/project --severity high
"""

import argparse
import json
import re
import sys
from pathlib import Path

EXCLUDED_DIRS = {
    "node_modules", ".git", ".next", "dist", "build", "venv", ".venv",
    "__pycache__", ".turbo", "coverage", ".pytest_cache", "target", ".cache",
}
SCAN_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".py", ".mjs", ".cjs"}

# (rule_id, severity, description, compiled regex, redact_match)
SECRET_PATTERNS = [
    ("SEC007-aws-key", "Critical", "Hardcoded-looking AWS access key ID",
     re.compile(r"AKIA[0-9A-Z]{16}"), True),
    ("SEC007-stripe-live", "Critical", "Hardcoded-looking Stripe live secret key",
     re.compile(r"sk_live_[0-9a-zA-Z]{20,}"), True),
    ("SEC007-slack-token", "Critical", "Hardcoded-looking Slack token",
     re.compile(r"xox[baprs]-[0-9a-zA-Z\-]{10,}"), True),
    ("SEC007-private-key", "Critical", "Embedded private key block",
     re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), False),
    ("SEC007-generic-secret-assignment", "High",
     "Variable named like a secret assigned a long literal string",
     re.compile(
         # No leading \b so this also matches camelCase identifiers like
         # `apiSecret` or `authToken`, not just snake_case/standalone words.
         r"(?i)(api[_-]?key|secret|token|password|passwd)[a-zA-Z0-9_]*\s*[:=]\s*[\"']([A-Za-z0-9_\-\/+=]{16,})[\"']"
     ), True),
]

DANGEROUS_PATTERNS = [
    ("SEC058-eval", "Critical", "eval()/new Function() on what may be untrusted input",
     re.compile(r"\b(eval|new Function)\s*\(")),
    ("SEC010-shell", "Critical", "Shell execution with shell=True or os.system",
     re.compile(r"(shell\s*=\s*True|os\.system\s*\()")),
    ("SEC061-pickle", "Critical", "pickle.loads() -- deserialization of untrusted data can execute code",
     re.compile(r"pickle\.loads?\s*\(")),
    ("SEC063-yaml-load", "High", "yaml.load() without an explicit safe Loader",
     re.compile(r"yaml\.load\s*\((?!.*Loader\s*=\s*yaml\.SafeLoader)")),
    ("SEC012-dangerously-set-html", "High", "dangerouslySetInnerHTML -- bypasses React's auto-escaping (XSS risk)",
     re.compile(r"dangerouslySetInnerHTML")),
    ("SEC009-fstring-sql", "High", "Possible SQL built via string formatting/concatenation instead of parameterized queries",
     re.compile(r"(?i)(f[\"'].*\b(select|insert|update|delete)\b.*\{|[\"']\s*\+\s*\w+\s*\+\s*[\"'].*\b(select|insert|update|delete)\b)")),
]

HEADER_HINTS = ["Content-Security-Policy", "Strict-Transport-Security"]


def redact(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "…" + value[-2:]


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix in SCAN_EXTENSIONS:
            yield path


def scan_file(path: Path, patterns):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        for rule_id, severity, description, pattern, *rest in patterns:
            redact_match = rest[0] if rest else False
            m = pattern.search(line)
            if m:
                snippet = redact(m.group(0)) if redact_match else m.group(0)
                findings.append({
                    "file": str(path), "line": i, "rule": rule_id,
                    "severity": severity, "description": description, "match": snippet,
                })
    return findings


def check_env_gitignored(root: Path):
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return {"file": str(root), "line": 0, "rule": "DO046-no-gitignore",
                "severity": "Medium", "description": "No .gitignore found -- confirm .env is never committed",
                "match": ""}
    content = gitignore.read_text(encoding="utf-8", errors="ignore")
    if ".env" not in content:
        return {"file": str(gitignore), "line": 0, "rule": "DO046-env-not-ignored",
                "severity": "High", "description": ".gitignore exists but doesn't appear to exclude .env files",
                "match": ""}
    return None


def check_security_headers_present(root: Path):
    for path in iter_source_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(hint in text for hint in HEADER_HINTS):
            return None
    return {"file": str(root), "line": 0, "rule": "SEC018-no-security-headers-found",
            "severity": "Medium",
            "description": "No Content-Security-Policy/Strict-Transport-Security configuration found anywhere in scanned files -- verify security headers are set (scripts/security/generate.py can scaffold them)",
            "match": ""}


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="Project root to scan")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low"], default="low",
                         help="Minimum severity to report (default: low, i.e. everything)")
    args = parser.parse_args()

    if not args.path.is_dir():
        print(f"error: not a directory: {args.path}", file=sys.stderr)
        sys.exit(2)

    findings = []
    for f in iter_source_files(args.path):
        findings.extend(scan_file(f, SECRET_PATTERNS))
        findings.extend(scan_file(f, DANGEROUS_PATTERNS))

    env_finding = check_env_gitignored(args.path)
    if env_finding:
        findings.append(env_finding)

    header_finding = check_security_headers_present(args.path)
    if header_finding:
        findings.append(header_finding)

    min_rank = SEVERITY_ORDER[args.severity]
    findings = [f for f in findings if SEVERITY_ORDER[f["severity"].lower()] <= min_rank]
    findings.sort(key=lambda f: SEVERITY_ORDER[f["severity"].lower()])

    if args.format == "json":
        print(json.dumps(findings, indent=2))
    else:
        if not findings:
            print("No findings at or above the requested severity. This is a floor, not a full audit -- see secure-coding-standards.md for what a static scan can't catch.")
        for f in findings:
            loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
            match_part = f" -- match: {f['match']}" if f["match"] else ""
            print(f"[{f['severity'].upper()}] {f['rule']} {loc}\n  {f['description']}{match_part}")
        print(f"\n{len(findings)} finding(s). This static scan complements, not replaces, the checklists in data/security/*.csv.")

    critical_or_high = any(SEVERITY_ORDER[f["severity"].lower()] <= 1 for f in findings)
    sys.exit(1 if critical_or_high else 0)


if __name__ == "__main__":
    main()
