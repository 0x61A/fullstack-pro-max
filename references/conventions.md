> Last updated: 2026-07-03 · Module version: 0.1

# Conventions

Shared rules every module in this skill follows. Read this once; it is not re-explained in each module's files.

## CSV Schemas

Every `data/**/*.csv` file uses one of two schemas, chosen by what the file represents.

### 1. Decision-Matrix schema

For files that help *choose between options* (e.g. `data/backend/stacks.csv`, `data/devops/platforms.csv`).

| Column | Meaning |
|---|---|
| `id` | Stable ID, see prefix table below (e.g. `BE014`) |
| `category` | Sub-grouping within the module (e.g. `Node.js`, `Python`, `BaaS`) |
| `option` | The thing being recommended (e.g. `Next.js API Routes`) |
| `best_for` | Concrete project types / situations this fits |
| `avoid_when` | Situations where this is a poor fit |
| `tradeoffs` | Short cost/benefit note |
| `tags` | `\|`-separated keywords for `scripts/common/search.py` |
| `last_verified` | `YYYY-MM-DD` |

### 2. Checklist schema

For files that enumerate *checks to run or apply* (e.g. `data/security/owasp-checklist.csv`, `data/seo/technical-seo-checks.csv`).

| Column | Meaning |
|---|---|
| `id` | Stable ID, see prefix table below (e.g. `SEC003`) |
| `category` | Sub-grouping within the module |
| `check` | Short imperative name of the check |
| `description` | What to verify or implement, concretely enough to act on |
| `why_it_matters` | One line on the failure mode this prevents |
| `severity` | `Critical` \| `High` \| `Medium` \| `Low` |
| `tags` | `\|`-separated keywords |
| `last_verified` | `YYYY-MM-DD` |

Both schemas share `id`, `category`, `tags`, `last_verified` so `scripts/common/search.py` can query any CSV in the skill the same way regardless of which schema it uses.

## Check-ID Prefixes

| Module | Prefix | Example |
|---|---|---|
| Backend & API | `BE` | `BE014` |
| Database & Auth | `DB` | `DB007` |
| DevOps & Deployment | `DO` | `DO012` |
| Testing/QA | `QA` | `QA005` |
| Security/Cybersecurity | `SEC` | `SEC031` |
| E-commerce & Payments | `EC` | `EC009` |
| UI/UX & Distinctive Frontend | `UX` | `UX022` |
| SEO | `SEO` | `SEO048` |
| Ads | `ADS` | `ADS017` |
| AI Integration | `AI` | `AI028` |

IDs are stable once published — never renumber an existing row when adding new ones (append, don't reorder), since a future scoring script or cross-reference may point at a specific ID.

## Severity Weights (Checklist CSVs)

Reused from the existing `ads` skill's proven formula — do not reinvent per module:

```
Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
score = 100 - (sum of weights of failed checks / sum of weights of all checks) * 100
```

`scripts/common/score.py` (introduced in Phase 5) implements this generically for any checklist CSV that follows the schema above.

## Reference File Versioning Header

Every `references/*.md` file starts with a one-line metadata header:

```
> Last updated: YYYY-MM-DD · Module version: X.Y
```

Bump the module version (not just the date) when a reference file's guidance changes in a way that would change a prior recommendation, not for typo fixes.

## Module Build Status

Tracked centrally in [`routing.md`](routing.md) — do not duplicate status elsewhere. When a module ships, flip its status there and in `SKILL.md`'s action-routing table in the same edit so they never drift apart.

## Script Conventions

- All scripts are **Python 3 stdlib-only** — no `requirements.txt`, no vendored venv. If a script needs something stdlib can't do, that's a signal to scope it down, not to add a dependency.
- Every script supports `--help` (via `argparse`) and, where it writes files, a `--dry-run` flag that prints what would be written instead of writing it.
- Generator scripts live under `scripts/<module>/generate.py`. Shared utilities live under `scripts/common/`.
