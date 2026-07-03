> Last updated: 2026-07-03 · Module version: 0.1

# LLM Application Security

The 16 checks live in `data/ai/llm-security-checks.csv` (AI028–AI043, scoreable with `scripts/common/score.py`). This file explains the threat model behind them. It extends — not replaces — the core Security module: an AI endpoint is still an API endpoint, so `api-security.md` (auth, BOLA, rate limiting) applies first.

## The one-sentence threat model

**Everything the model reads is attacker input, and everything the model writes is untrusted output — in both directions, act accordingly.**

Two consequences fall out of this:

1. **Input side (injection):** users, retrieved documents, emails, and webpages can all carry instructions. You cannot reliably filter injection with prompts alone — mitigate by *structure*: instructions in the system role, data in delimited content blocks (AI028, AI029), and permissions enforced outside the prompt (AI032).
2. **Output side (execution):** rendering, executing, or acting on model output without validation turns a hallucination or a successful injection into XSS, SQL injection, or an unwanted state change (AI030, AI037).

## OWASP LLM Top 10 → this module's checks

| OWASP LLM (2025) | Covered by |
|---|---|
| LLM01 Prompt Injection | AI028, AI029, AI036 |
| LLM02 Insecure Output Handling | AI030, AI037 |
| LLM03 Training Data / Corpus Poisoning | AI041 |
| LLM04 Model Denial of Service | AI035, AI036 |
| LLM05 Supply Chain | AI042 |
| LLM06 Sensitive Info Disclosure | AI032, AI033, AI034 |
| LLM07 Insecure Plugin/Tool Design | AI031, AI037 |
| LLM08 Excessive Agency | AI031 |
| LLM09 Overreliance | AI043 |
| LLM10 Model Theft | out of scope for API consumers (provider-side control) |

## Tool use is the escalation path

A model with no tools can at worst say something wrong. A model with tools can *do* something wrong. Rank your effort accordingly:

- Read-only tools before write tools; row-scoped queries (the requesting user's data only) before broad queries.
- Human confirmation for destructive/irreversible/spending actions — the model proposes, the user disposes (AI031).
- Validate tool arguments like any API input: schema first, then business rules (ownership, state, ranges) (AI037).
- Log every tool call with its triggering conversation ID (AI039) — this is your incident-response trail (see `incident-response.md`).

## Fail closed

Guardrail down ≠ guardrail passed. If moderation, permission checks, or the model itself errors, degrade to refusal or a static safe response — never to "proceed unchecked" (AI038). Wire this into the same error-handling taxonomy as the rest of the backend (`data/backend/error-handling.csv`).

## Data lifecycle

Conversations are user data with the full KVKK/GDPR obligations attached: minimize what enters prompts (AI034), keep secrets out entirely (AI033), define retention up front, and make deletion reach DB, logs, caches, *and* vendor-side settings (AI040).

## Scoring

Run the checklist like any other module:

```bash
python3 scripts/common/score.py data/ai --results results.json
```

Treat any failing Critical (AI028–AI032) as a launch blocker for a user-facing AI feature.
