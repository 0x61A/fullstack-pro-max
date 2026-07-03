> Last updated: 2026-07-03 · Module version: 0.1

# Security Scoring

How to turn a pass/fail run through this module's 124 checks (across `owasp-checklist.csv`, `threat-modeling-checks.csv`, `secure-coding-checks.csv`, `api-security-checks.csv`, `infra-cloud-security-checks.csv`, `incident-response-checklist.csv`) into a single comparable posture score, using `scripts/common/score.py`.

## The Formula

Reused verbatim from the existing `ads` skill's proven severity-weighted model (see `references/conventions.md`):

```
Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
score = 100 - (sum of weights of FAILED checks / sum of weights of ALL checks) * 100
```

A score of 100 means every check in the evaluated set passed. A single failed Critical check drags the score down disproportionately more than a failed Low check — this is deliberate: a security posture with one critical hole is not "95% secure," it's exposed at that one point regardless of how many low-severity items are clean.

## Running It

```
python3 scripts/common/score.py data/security/owasp-checklist.csv --results results.json
```

Where `results.json` maps check IDs to pass/fail:
```json
{"SEC001": "pass", "SEC002": "fail", "SEC003": "pass", ...}
```

Checks not present in the results file are treated as **not evaluated** and excluded from the denominator, not counted as failures — a partial audit produces a score for what was actually checked, not a penalized score for what wasn't reached yet. The tool reports both the score and the excluded/not-evaluated count so this distinction is visible, not silent.

## Interpreting the Score

This score is a **summary signal for tracking posture over time and prioritizing remediation**, not a certification or a substitute for reading the actual failed checks. A 90 with one failed Critical item (SSRF, `SEC029`) needs to be treated as more urgent than an 85 with several failed Low items, even though the numeric score suggests otherwise at a glance — always look at *which* checks failed, not just the aggregate number.

## Scoring Per-Category vs. Overall

Run the score separately per CSV (OWASP, threat modeling, secure coding, API, infra, incident response) to see which category is weakest, then an overall score across all six combined for a single headline number. A project might score well on OWASP basics but poorly on infra/access-management — that distinction is lost if you only ever look at one combined number.

## Relationship to Ads/SEO Scoring (Phases 8-9)

The same `scripts/common/score.py` and the same Critical/High/Medium/Low weighting will be reused for the SEO and Ads modules' checklists once built (Phase 8-9) — one shared scoring engine across every audit-shaped module in this skill, not three reimplementations of the same formula.
