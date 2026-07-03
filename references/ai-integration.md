> Last updated: 2026-07-03 · Module version: 0.1

# AI Feature Integration

How to add an AI feature to a web product with the Claude API — model choice, endpoint shape, grounding, cost control, and quality gates. Row-level detail lives in `data/ai/model-selection.csv` and `data/ai/integration-patterns.csv`; security is its own file (`ai-security.md`) and is **not optional** — read it before shipping anything user-facing.

## Model Decision Tree

1. **Start at Claude Sonnet 5** (`claude-sonnet-5`) for any product feature. It is the cost/quality workhorse (AI003).
2. **Drop to Haiku 4.5** when the task is classification, routing, moderation pre-filtering, autocomplete, or any high-volume low-nuance call (AI004). Verify quality on a golden set first — don't assume.
3. **Escalate to Opus 4.8 / Fable 5** only when evals show Sonnet failing: hard multi-step reasoning, complex agentic coding, high-stakes analysis (AI001, AI002).
4. **Mixed workload?** Route by tier (AI005): a cheap classifier or a rule decides which model serves each request. Measure the routing decision itself — misrouting hard tasks to Haiku is a silent quality bug.
5. **Extended thinking** (AI006) is a per-request dial, not a model choice: turn it on for the hard 5% of requests, keep it off for chat latency.

Anthropic has **no embeddings API** — RAG retrieval uses an external embedding provider (Voyage is the usual pairing, AI008). Version the embedding model; changing it invalidates the whole index.

## Endpoint Shape

**Default: streaming SSE** for anything a human watches (AI015). Non-streaming is for code-consumed output and background jobs (AI016). `scripts/ai/generate.py` scaffolds a streaming chat endpoint for Next.js (App Router), Express, or FastAPI — signature:

```bash
python3 scripts/ai/generate.py --stack nextjs-api --model claude-sonnet-5 --dry-run
```

The scaffold bakes in the non-negotiables so they don't get forgotten later: auth check before the model call, per-user rate limiting hook, `max_tokens` bound, input length cap, and API key from env — never from code (see `env-secrets-management.md`).

## The Cost Model (know it before you ship)

Input tokens dominate most chat products because history is replayed every turn (AI020). The levers, in order of impact:

1. **Prompt caching** (AI010) — stable system prompt + tools first in the prompt, conversation appended after; cache hits cut input cost up to ~90% and improve TTFT. Design prompts so the stable prefix never changes mid-conversation.
2. **History budgeting + summarization** (AI013) — cap replayed turns; summarize older context.
3. **Tiered routing** (AI005) and **semantic caching** (AI025) for high-traffic features.
4. **Batch API** (AI011) for anything async — 50% discount.

Set a per-user and global daily spend cap from day one (AI035) — this is a security control as much as a budget one.

## Grounding: RAG in this stack

Default shape for Supabase/Postgres projects: **pgvector** in the same database (AI018) — no second datastore, and retrieval can honor RLS so permission filtering happens in the query, not in the prompt (AI032, critical).

- Chunk by semantic unit (headings/sections), not fixed character windows (AI019).
- Store `source`, `updated_at`, and a permission scope with every chunk.
- Measure retrieval hit-rate on a golden question set **before** tuning prompts — bad retrieval with a great prompt still produces confident wrong answers.
- Govern the corpus like code: review before indexing, keep a rebuild path (AI041).

## Quality Gates

A prompt change is a deploy. Treat it like one:

- **Golden set** (AI023): ~20 real inputs with expected properties, run before every prompt/model change. Keep prompts versioned in the repo, changed via PR (AI021).
- **LLM-as-judge** (AI024) scales grading, but calibrate against human labels first.
- **Retry + fallback** (AI022): backoff on 429/529; optionally degrade to a cheaper model to stay up. Never blind-retry a side-effectful agent action.

## Architecture Discipline

Single well-prompted call → tool use → multi-step orchestration, in that order (AI026). Reach for the **Claude Agent SDK** when the feature genuinely is an agent (tool loops, file operations, subagents); stay on the raw Messages API for prompt-in/answer-out features (AI014). Prompting + RAG before fine-tuning, almost always (AI027).

## Cross-module hooks

- Secrets & keys → `env-secrets-management.md` (DevOps)
- Endpoint auth & rate limiting → `api-security.md` (Security)
- LLM-specific threats → `ai-security.md` + `data/ai/llm-security-checks.csv` (score with `scripts/common/score.py`)
- Storing conversations → `database-schema-design.md` (soft-delete + retention apply to chat history too)
