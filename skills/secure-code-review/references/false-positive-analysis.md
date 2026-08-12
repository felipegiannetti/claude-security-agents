# False Positive Analysis

The discipline of actively trying to disprove a candidate finding *before* reporting it — not just after, when `security-verifier` gets to it. Doing this early saves a verification round-trip and produces a better-calibrated `confidence` value from the start.

## The General Method

For any candidate, before finalizing it, ask: **what would have to be true for this to NOT be exploitable — and is any of it actually true here?** Check, in roughly this order (see also `.claude/rules/security.md` "Vulnerability Validation"):

1. **Is the source really attacker-controlled?** A value read from a database might originally have come from attacker input (stored XSS) or might be entirely server-generated (an internal ID) — these are different risk profiles even though both are "database reads."
2. **Is the sink actually reachable?** Dead code, a feature flag that's off, an admin-only code path, or a route that's never registered all mean the sink isn't reachable in practice.
3. **Is there validation/sanitization that neutralizes this specific sink?** Not validation *somewhere* — validation that matters for *this* sink (e.g. length validation doesn't stop SQL injection; type validation to integer *does*).
4. **Does the framework provide protection here by default?** ORM parameterization, template auto-escaping, and CSRF middleware are common examples — verify the specific call site actually uses the safe path, not just that the framework offers one.
5. **Is there an authorization check elsewhere in the call chain?** Missing authorization in a controller doesn't mean missing authorization overall if a service-layer check, a repository-level tenant filter, or a middleware/guard enforces it — search beyond the immediate file.
6. **Is this test/example/generated code**, not something that ships or runs against real data?

## Category-Specific False-Positive Conditions

Each domain Skill documents its own conditions in detail — this is the general pattern they follow:

- **SQL Injection**: prepared statements, ORM parameterized queries/query builders with safe binding.
- **XSS**: contextual escaping, framework auto-escaping, sanitization libraries, content that's genuinely static/trusted (not user-influenced).
- **Broken Authorization**: resource-ownership checks, service-layer authorization, middleware, policy engines — checked *outside* the immediately-flagged location.
- **Vulnerable Dependency**: installed version outside the affected range, vulnerable code path not actually invoked by the application, KEV-listed status absent *and* no other exploitability evidence (see `skills/dependency-cve-check/references/kev-correlation.md` — absence from KEV is not itself a false-positive signal).

See each domain Skill's own reference material (e.g. `skills/injection-review/references/sql-injection.md`) for the full list relevant to that category.

## What This Is Not

This is not a mandate to talk yourself out of real findings. The goal is calibration, not suppression — CLAUDE.md's Development Rules are explicit that verification quality must never be weakened to reduce or inflate finding counts in either direction. If, after this analysis, the finding still holds, report it with the confidence the evidence actually supports.
