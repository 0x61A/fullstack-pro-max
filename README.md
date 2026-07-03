# fullstack-pro-max

[![CI](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml/badge.svg)](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/0x61A/fullstack-pro-max)](https://github.com/0x61A/fullstack-pro-max/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*Türkçe sürüm: [README.tr.md](README.tr.md)*

A single, self-contained [Claude Code](https://claude.com/claude-code) skill for shipping a real web product end to end — distinctive UI/UX, backend architecture, database & auth, deployment, testing, cybersecurity, SEO, ads, and e-commerce payments — with adaptive stack selection rather than one fixed frontend+backend combo.

Built for two use cases: agency/client delivery and personal SaaS builds.

## What's inside

Nine modules, each backed by structured data (CSV), on-demand reference docs, and stdlib-only Python scripts:

| Module | Coverage |
|---|---|
| **Backend & API** | Adaptive stack selection (Next.js/Express/Nest.js/Fastify · FastAPI/Django · Supabase/Firebase · Cloudflare Workers), API design, error handling |
| **Database & Auth** | Schema design, RLS/multi-tenancy, auth strategy matrix, migration safety |
| **DevOps & Deployment** | CI/CD, Vercel/Netlify/Cloudflare/Railway decision matrix, env & secrets |
| **Testing/QA** | Test strategy by stack, accessibility + Core Web Vitals checklist |
| **Security/Cybersecurity** | 124 checks: OWASP Top 10, STRIDE threat modeling, secure coding per stack, API/infra security, incident response — plus a stdlib static secret/pattern scanner |
| **E-commerce & Payments** | Stripe + Shopify integration patterns, signature-verified webhook scaffolds |
| **UI/UX & Distinctive Frontend** | Anti-generic-AI-design playbook — layout/type/motion techniques for non-templated design |
| **SEO** | 92 checks: technical, on-page, content/E-E-A-T, schema selection, GEO/AI-citability |
| **Ads** | 64 checks: Google/Meta/LinkedIn/TikTok/Microsoft + cross-platform tracking/attribution |

~644 data rows, 29 reference docs, 10 scripts. **Zero vendored dependencies** — no bundled venv, no `requirements.txt`.

## What it looks like in use

Query any module's data the same way (shared CSV schema across all nine modules):

```
$ python3 scripts/common/search.py data/ui-ux/distinctiveness-patterns.csv --query "layout"
id     category                option
-----  ----------------------  ----------------------------------------
UX052  Layout Distinctiveness  Break the vertical-stack-of-centered-sec
UX054  Grid Systems            Use an asymmetric or broken grid deliber
UX059  Typography as Layout    Let display type be a primary layout/com
...
6 match(es).
```

Generators scaffold real, opinionated code — e.g. security headers for Next.js:

```
$ python3 scripts/security/generate.py --stack nextjs --dry-run
const securityHeaders = [
  { key: "Content-Security-Policy",
    // TODO: loosen deliberately per resource you actually need -- start strict.
    value: "default-src 'self'; script-src 'self'; ... frame-ancestors 'none'" },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  ...
];
```

## Install

Copy this directory into your Claude Code skills folder:

```bash
git clone https://github.com/0x61A/fullstack-pro-max.git ~/.claude/skills/fullstack-pro-max
```

Then start a new Claude Code session — the skill is picked up automatically from its `SKILL.md` frontmatter. Invoke it with `/fullstack-pro-max <request>` or let it trigger on relevant tasks (planning a stack, building an API, a pre-launch security/SEO audit, etc.).

## Requirements

- **Claude Code** (CLI, desktop, web, or IDE extension).
- **Python 3** for the helper scripts (`search.py`, `score.py`, generators, `audit.py`) — standard library only, no packages to install.
- **Optional MCP servers**: several modules can use connected MCP tooling (Supabase, Vercel, Netlify, Cloudflare, Shopify) for live operations. These are optional — the skill's guidance works without them, and it says so explicitly when an action would benefit from a connector you haven't configured.

## Scripts

Every script supports `--help`:

```bash
python3 scripts/common/search.py data/backend/stacks.csv --query "edge"   # query any CSV
python3 scripts/common/score.py data/security --results results.json       # severity-weighted posture score
python3 scripts/security/audit.py ./my-project                             # static scan for secrets/dangerous patterns
python3 scripts/backend/generate.py posts --stack nextjs-api               # scaffold a CRUD endpoint
python3 scripts/common/validate.py                                          # validate all data CSVs (same check CI runs)
```

## Notes

- **Original content, self-contained.** No runtime dependency on any other skill.
- **CI eats its own dog food.** Every push validates all 644 data rows against the shared schema, smoke-tests every script, checks that internal file references resolve, and scans the repo with the skill's own `scripts/security/audit.py`.
- **Guidance, not a guarantee.** The security, payments, SEO, and ads material is a strong starting point — validate it against your own project's context, compliance requirements, and current platform docs before relying on it in production.

## License

[MIT](LICENSE) © 2026 Ahmet Şerif Kart
