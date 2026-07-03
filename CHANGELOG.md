# Changelog

All notable changes to this skill are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/): new checks, data rows, or modules bump **minor**, corrections bump **patch**. The latest version here stays in sync with `metadata.version` in `SKILL.md`.

## [0.1.0] — 2026-07-03

First public release.

### Added
- Nine modules — Backend & API, Database & Auth, DevOps & Deployment, Testing/QA, Security/Cybersecurity, E-commerce & Payments, UI/UX & Distinctive Frontend, SEO, Ads — with ~644 structured data rows, 29 reference docs, and stdlib-only Python scripts.
- `scripts/common/validate.py`: validates every data CSV against the shared schemas (ID prefixes, uniqueness, severities, dates).
- CI workflow (`.github/workflows/validate.yml`): CSV validation, `--help` + dry-run smoke tests for every script, internal file-reference check, and a self-scan of the repo with the skill's own `scripts/security/audit.py`.
- `scripts/security/audit.py`: repeatable `--exclude PATH` flag; the scanner now always skips its own file (its pattern definitions would otherwise match themselves).
- MIT license, English README, Turkish README (`README.tr.md`), this changelog.

[0.1.0]: https://github.com/0x61A/fullstack-pro-max/releases/tag/v0.1.0
