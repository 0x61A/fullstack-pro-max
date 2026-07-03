> Last updated: 2026-07-03 · Module version: 0.1

# Threat Modeling

Pairs with `data/security/threat-modeling-checks.csv` (20 checks, STRIDE-organized) — query via `scripts/common/search.py`. This is the "think before you build" half of the security module; `secure-coding-standards.md` and `api-security.md` are the "verify what you built" half.

## When to Actually Do This

Not every feature needs a formal threat-modeling session. Do it explicitly for: anything touching authentication/authorization, anything handling payments or PII, any new third-party integration with meaningful data access, and any feature introducing a new trust boundary (a new user role, a new way external data enters the system). A CRUD form for a non-sensitive internal preference doesn't need this ceremony.

## The Process, Practically

1. **Draw the data flow** (`SEC036`) — even a whiteboard sketch: what enters, where it's stored, what transforms it, where it exits. You cannot reason about the threats below without this step done first.
2. **Identify trust boundaries** (`SEC050`) — the specific points where data crosses from one trust level to another (client → server, your service → third party, one internal service → another). Every threat category below is anchored to a specific boundary crossing, not the system in the abstract.
3. **Walk STRIDE per boundary** — for each trust boundary identified, ask the six questions below.
4. **Prioritize by realistic likelihood × impact** (`SEC054`) — not every identified threat gets the same urgency; an unprioritized wall of findings tends to result in nothing getting fixed.
5. **Revisit when the data flow changes materially** (`SEC055`) — a threat model is a living artifact for actively-developed features, not a one-time document.

## STRIDE, Applied

- **Spoofing** — can something falsely claim an identity? Check every actor in the data flow has its identity verified appropriately (`SEC037`); webhook senders specifically need signature verification, not IP-allowlist-only trust (`SEC038`).
- **Tampering** — can data be modified in transit or storage without detection? Never trust client-supplied values for anything with financial consequence — compute totals server-side from the source of truth, don't accept a client-supplied price (`SEC040`).
- **Repudiation** — can an actor deny having done something? Actions with real consequence need to be attributable to a specific authenticated principal (`SEC042`), and the audit trail itself needs to be protected from modification by the actors it records (`SEC043`).
- **Information Disclosure** — is more exposed than intended? Map what each API response actually returns, don't assume it's minimal (`SEC044`) — over-fetching from an ORM object is the most common way this happens silently.
- **Denial of Service** — can availability be degraded? Rate-limit or queue anything resource-intensive (`SEC046`), and bound anything recursive/unbounded that's driven by user input (`SEC047`).
- **Elevation of Privilege** — can an actor gain capabilities beyond what they should have? This is where mass assignment (`SEC049`) and stale/client-supplied role claims (`SEC048`) live — both are common, both are critical severity.

## Trust Boundaries Deserve Special Attention

The most common threat-modeling gap isn't missing a STRIDE category — it's missing a trust boundary entirely, usually "internal" service-to-service calls that get implicitly trusted by network location alone (`SEC051`). Treat every service boundary as needing its own authentication, even inside a VPC — "it's on the internal network" is not authorization.

## Third-Party Risk as Its Own Category

A new dependency or third-party integration is effectively granting an external party code execution or data access in your system (`SEC052`, `SEC053`). Review what it can actually reach before adopting it, not after an incident reveals the scope was broader than assumed.

## Feeding Into the Rest of the Module

Threats identified here that turn into concrete, verifiable checks belong in `secure-coding-standards.md`, `api-security.md`, or `infra-cloud-security.md` depending on where the fix lives. Threat modeling identifies *what could go wrong*; the other reference files in this module are *how you verify it doesn't*.
