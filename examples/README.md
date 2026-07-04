# Field-test examples

Real output from actually running this skill's own scripts end to end against two representative prompts — not dry-runs, not transcripts. The generated files are committed as-is (TODOs and all), because the point of a field test is what the skill really produces, not a cleaned-up version of it.

| Scenario | Prompt tested | Actions exercised | Notes |
|---|---|---|---|
| [`salon-site/`](salon-site) | "Build a from-scratch website for my [small business]." | `plan` → `design` | Backend decision tree's "does this need a backend at all" branch, sector art direction, token+skeleton generation. |
| [`dark-technical-dashboard/`](dark-technical-dashboard) | "I need a dark, technical dashboard — use a ready-made component instead of building from scratch." | `design` (known-sites-library → component-libraries chain) → `build` | Live-fetch verification of two component-library sources, token+skeleton generation, a real backend CRUD scaffold. |

Both runs found and fixed real bugs/gaps in the skill itself — see each folder's own `.md` write-up and `CHANGELOG.md` (`v0.15.0` and the following commit) for the specifics. Re-running either command in a scenario's `.md` file should reproduce the same output against the current version of this skill.
