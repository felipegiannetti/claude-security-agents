# Verifier Prompt

Condensed task prompt corresponding to [agents/security-verifier.md](../agents/security-verifier.md) — used by `08_verification` for a standalone re-verification of a single finding (e.g. re-checking one finding after new evidence surfaces) outside a full pipeline run.

---

Include [system_prompt.md](system_prompt.md).

Task: independently attempt to disprove the given candidate finding. Do not repeat the reviewer's reasoning — re-derive your own conclusion from the repository.

Check, where applicable: is the claimed source actually attacker-controlled; is the sink actually reachable (route exposure, feature flags, dead code); does authentication/authorization exist elsewhere in the path (middleware, guards, service-layer checks, ownership/tenant checks); does the framework provide protection here (ORM parameterization, auto-escaping, CSRF middleware) and is it actually in effect; are there compensating controls (gateway, network isolation, allowlists); for dependency findings, is the vulnerable functionality actually used and is the installed version genuinely in the affected range.

Resolve to one of `CONFIRMED`, `REJECTED`, or `NEEDS_MORE_EVIDENCE`, with a verified attack path (if confirmed) or a specific rejection reason (if rejected) — see the rejection reason list in [security-verifier.md](../agents/security-verifier.md). A rejected false positive is a successful outcome, not a failure to find something.

Output: the finding updated per [finding.schema.json](../schemas/finding.schema.json), `verification` field populated.
