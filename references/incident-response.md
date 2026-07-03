> Last updated: 2026-07-03 · Module version: 0.1

# Incident Response

Pairs with `data/security/incident-response-checklist.csv` (17 checks) — query via `scripts/common/search.py`. This is preparation-and-process guidance; it assumes the preventive controls in the rest of the security module are already in place and covers what happens when one fails anyway.

## Preparedness — Before Anything Happens

Do these regardless of team size, before an incident, not during one:
1. **Write the plan down** (`SEC108`) — even one page: who to contact, first steps, where to coordinate. Deciding a process for the first time under pressure wastes critical time and increases mistake risk.
2. **Assign roles in advance** (`SEC109`) — at minimum, an incident commander and a communications role, even on a small team. Ambiguity about who's leading tends to produce either no leadership or competing uncoordinated actions.
3. **Actually verify credential rotation works** (`SEC110`) — rehearsed, not assumed. Discovering a rotation process is broken during a real incident turns a containable situation into a prolonged one.
4. **Give people a way to report a suspected issue** (`SEC112`) — a `security@` address or a `security.txt` file. Without one, a well-intentioned researcher who finds a real vulnerability may go public first for lack of a better option.

## The Response Sequence

1. **Detect** — this depends entirely on the alerting built in `infra-cloud-security.md`/`api-security.md` (`SEC111`) actually being wired to notify a human, not just written to an unwatched log.
2. **Triage** — assess severity quickly using the same Critical/High/Medium/Low framing already used throughout this module (`SEC113`), within a defined window for anything potentially critical.
3. **Contain** — stop ongoing harm. **Rotate suspected-compromised credentials immediately** (`SEC115`) — don't wait for investigation to "complete" first; rotate in parallel with investigating. Document containment actions as they happen in the incident channel (`SEC114`), not reconstructed from memory afterward. Isolate without destroying forensic evidence (`SEC116`) — don't redeploy over a compromised instance before capturing its state if you'll need to understand what happened.
4. **Communicate** — inform internal stakeholders proportional to severity, without unnecessary delay (`SEC117`); if user data was affected, follow applicable legal notification requirements with clear, honest communication (`SEC118`). Maintain one authoritative status source during the response (`SEC119`) — fragmented status across DMs produces duplicated or contradictory action.
5. **Eradicate** — fix the actual root cause, not just the symptom (`SEC120`). Rotating a leaked key without finding and fixing *how* it leaked means the same class of incident is likely to recur.
6. **Recover** — explicitly verify the system is clean before fully restoring normal operation (`SEC121`), not assumed clean because containment measures are being lifted.

## Post-Mortem — Where the Real Value Is

Every incident above a defined severity threshold gets a **blameless** post-mortem (`SEC122`) — timeline, what worked, what didn't, concrete action items with owners, explicitly framed around systemic fixes rather than individual fault. A blame-focused culture discourages the honest reporting of near-misses that's precisely what improves future response.

Two things determine whether a post-mortem actually produces improvement rather than just documentation:
- **Action items tracked to actual completion** (`SEC123`) in the team's normal work-tracking system, revisited to confirm they were done — not just written down and forgotten.
- **The IR plan itself gets updated** based on what the post-mortem revealed (`SEC124`) — if the plan had a gap (an unclear role, a rotation step that didn't work as expected), fix the plan, not just the immediate technical issue.

## Severity Framework (reused across this entire security module)

```
Critical = 5.0   High = 3.0   Medium = 1.5   Low = 0.5
```
Same weights as `references/conventions.md` and the `ads` skill's proven scoring model — see `security-scoring.md` for how this is applied to compute an overall security posture score from any of this module's checklists.
