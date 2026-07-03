> Last updated: 2026-07-03 · Module version: 0.1

# Email Integration

Transactional and marketing email for a web product — provider choice, sending architecture, and the deliverability layer that decides whether anything actually reaches an inbox. Row-level detail: `data/email/provider-selection.csv`, `sending-patterns.csv`, and `deliverability-checklist.csv` (score with `scripts/common/score.py`).

## Provider Decision Tree

1. **Transactional only, JS/TS stack?** → **Resend** (EM001) for DX and React Email, or **Postmark** (EM002) when deliverability reputation is the overriding concern (auth-critical products).
2. **High volume, AWS shop, ops capacity?** → **SES** (EM003) — cheapest pipe, but you own warmup, suppression, and monitoring yourself.
3. **Marketing/newsletter?** → a dedicated platform (EM005). **Never through the transactional stream** — stream separation (EM007) plus per-purpose subdomains (EM019) is the one architecture rule this module treats as mandatory.
4. **Self-hosted SMTP?** → effectively never (EM006).

## Sending Architecture (the four non-negotiables)

1. **Queue-backed** (EM011): the request path enqueues; a worker sends with retries. Email never blocks a user response.
2. **Idempotent** (EM012): an idempotency key per logical send — retries must not double-send receipts.
3. **Suppression-aware** (EM013, EM027): bounce/complaint webhooks (signature-verified, same discipline as Stripe webhooks in `stripe-integration.md`) feed one suppression store that *every* send path checks.
4. **Sandboxed outside production** (EM010): Mailpit/Mailtrap locally and in staging. A seeded staging DB plus a live email key is how companies accidentally email their whole customer base.

`scripts/email/generate.py` scaffolds a queue-friendly send module with these hooks in place:

```bash
python3 scripts/email/generate.py --provider resend --stack node --dry-run
```

## Deliverability: authentication first

SPF (EM021) + DKIM (EM022) + DMARC (EM023) are table stakes — Gmail/Yahoo enforce them for bulk senders (EM025), and DMARC should progress `p=none → quarantine → reject` on a schedule, not sit at `none` forever. The commonly-missed fourth piece: a **custom aligned return-path** (EM024). Verify all of it with a real round-trip test quarterly (EM033) — DNS drifts silently.

Operational reputation: warm up new domains before volume (EM018), watch complaint (<0.1%) and bounce (<2%) rates with alerts (EM026), prune dead addresses (EM028), and protect signup forms from list-bombing (EM029).

Compliance: one-click unsubscribe headers on all non-transactional mail (EM014, RFC 8058 — mandatory for bulk Gmail/Yahoo), consent + double opt-in for marketing lists (EM015), sender-identity requirements per region (EM034 — KVKK/CAN-SPAM/ePrivacy).

## Templates

Templates live in the repo, versioned and PR-reviewed (EM016) — React Email or MJML (EM008) rather than hand-maintained table HTML. Always ship a real plain-text part (EM017), keep total size under Gmail's ~102KB clipping limit (EM030), and localize subject + body from the user's locale, not inline translation (EM020).

## Cross-module hooks

- Webhook signature verification and idempotency → E-commerce module (`stripe-integration.md` § Webhooks) — same pattern, different provider
- API keys and rotation → `env-secrets-management.md` (EM032 is its email-specific application)
- Signup rate limiting → `api-security.md` (EM029 overlaps its abuse checks)
- Marketing-consent records → `database-schema-design.md` (consent timestamp/source columns)
- Email capture forms on marketing pages → SEO/Ads modules' landing-page guidance
