> Last updated: 2026-07-03 · Module version: 0.1

# Database & Schema Design

Pairs with `data/database/schema-patterns.csv` (30 rows) and `data/database/migrations-checklist.csv` (21 checks) — query both via `scripts/common/search.py`. This file covers the reasoning connecting them: how to approach a schema from scratch and how to evolve it safely afterward.

## Designing a New Schema — Order of Operations

1. **Identify the core entities and their true ownership relationships** before touching SQL — a user owns orders, an order owns line items. Get this right first; column-level decisions (types, indexes) are easy to fix later, ownership/foreign-key structure is not.
2. **Default to full normalization** for core business entities (`DB008`) — only reach for JSONB (`DB007`) when an attribute set genuinely varies per row in a way no fixed schema captures well (product variant attributes, webhook payload archival, user preference blobs).
3. **Choose the primary key strategy per table, not globally** — public-facing resources lean UUID (`DB001`) or UUID+slug (`DB003`), pure-internal high-volume tables can use bigint (`DB002`). Don't dogmatically pick one PK style for an entire schema.
4. **Add `created_at`/`updated_at` to every table** (`DB006`) from the first migration — this is close to a universal default, not a per-table decision.
5. **Decide soft-delete vs hard-delete per table explicitly** (`DB004`/`DB005`) based on whether compliance or "undo" is a real requirement — don't default to soft-delete everywhere; it has a real query-complexity cost.
6. **Model the multi-tenancy strategy before writing the first migration**, if this is a multi-tenant SaaS — retrofitting tenant isolation onto an already-shipped shared-table schema is far more painful than choosing correctly up front. Default recommendation: shared tables + `tenant_id` + Row-Level Security (`DB015`) on Supabase/Postgres, escalating to schema-per-tenant (`DB016`) or database-per-tenant (`DB017`) only when a concrete enterprise/compliance requirement demands it.

## Indexing Discipline

Postgres does **not** automatically index foreign key columns — this is the single most common cause of a slow join in production that "should have been fast." Baseline rule: every foreign key column and every column that appears in a `WHERE`, `JOIN`, or `ORDER BY` clause on a query you actually run should have a B-tree index (`DB019`) unless you have a specific reason not to (write-heavy table where the read pattern doesn't justify it).

Beyond the baseline:
- **Partial indexes** (`DB020`) when a query always filters on a stable condition (`WHERE deleted_at IS NULL`) — smaller and faster than indexing the whole column.
- **Composite index column order matters** (`DB021`) — leading column should be the one most consistently used in equality filters across your actual query patterns, not just "the more important-sounding column."
- **GIN indexes** (`DB022`) for JSONB queries, array containment, and full-text search — B-tree can't serve these efficiently.

Don't index speculatively — every index has a write-cost. Add indexes driven by real or clearly-anticipated query patterns, not "just in case."

## Multi-Tenancy Decision (SaaS-specific)

Default recommendation, absent a specific enterprise/compliance requirement: **shared tables + `tenant_id` + Row-Level Security** (`DB015`). On Supabase this makes tenant isolation a database-enforced guarantee (`auth.uid()` / a `tenant_id` claim checked in the policy) rather than something every single query has to remember to filter by — see `DB030`: colocate the RLS policy with the migration that creates the table it protects, in the same commit, every time.

Escalate only when a concrete pressure appears:
- A specific enterprise customer's contract requires stronger isolation → schema-per-tenant (`DB016`).
- A regulatory/data-residency requirement demands full separation → database-per-tenant (`DB017`).

## Migration Safety (day-to-day discipline)

Full 21-check list is in `data/database/migrations-checklist.csv` — the shape of the discipline:

1. **Every migration is reversible** (`DB056`) and the rollback is actually tested against a non-production environment (`DB072`), not just written and assumed to work.
2. **Nothing destructive happens in one step** (`DB057`) — deprecate, confirm nothing depends on it, then remove, across separate migrations/releases.
3. **Zero-downtime by default** for any table receiving live writes: `CREATE INDEX CONCURRENTLY` (`DB061`), `NOT VALID` + separate `VALIDATE CONSTRAINT` for new foreign keys on large tables (`DB062`), batched backfills (`DB060`), add+backfill+drop for renames (`DB059`).
4. **In-flight application code must tolerate the new schema mid-rollout** (`DB063`) — during a rolling deploy, both old and new code run simultaneously against the same database; a migration that only the new code can handle correctly will break requests served by old-code instances.
5. **Automate application** (`DB064`) through the deploy pipeline (see `ci-cd-pipelines.md`, Phase 3), never by a developer running SQL by hand against production.
6. **Never edit an already-applied migration** (`DB065`) — once it's run against any shared environment, treat the file as immutable and write a new migration for further changes.

## Supabase-Specific Workflow

Since Supabase is this skill's first-class BaaS recommendation, and if its MCP is connected in your environment:
- Author migrations as versioned SQL files under `supabase/migrations/`, applied via the Supabase CLI or the connected MCP's `apply_migration` tool — never as ad-hoc changes through the dashboard for anything meant to be reproducible (`DB074`).
- Keep seed/reference data in `seed.sql`, separate from structural migrations (`DB075`), so a dev/staging environment can be reset without re-running every structural change.
- Use `get_advisors` (via the connected MCP) after schema changes to catch missing RLS policies or other Supabase-specific lint issues before they reach production.
- Use `list_tables` before designing new migrations to confirm you're building against the actual current schema, not a stale mental model of it.
