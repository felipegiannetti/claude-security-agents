# Review Prompt

Condensed task prompt corresponding to [agents/security-reviewer.md](../agents/security-reviewer.md) — used by `05_llm_review` and re-invoked narrowly by `06_data_flow_analysis` when a specific candidate finding needs a deeper source-to-sink trace.

---

Include [system_prompt.md](system_prompt.md).

## Full review task (05_llm_review)

Given the architecture model, attack surface map, and normalized scanner results, select relevant Skills via [routing_rules.yaml](../workflow/routing_rules.yaml), correlate scanner evidence with code, and produce candidate findings.

For every scanner result: locate the code, determine whether it's actually reachable and attacker-influenced, check the relevant Skill's false-positive conditions, and only promote it to a candidate finding if it survives that correlation.

For every candidate involving attacker-influenced data, trace what applies of `SOURCE → PARSING → TRANSFORMATION → VALIDATION → AUTHENTICATION → AUTHORIZATION → BUSINESS LOGIC → SINK`. Do not conclude a vulnerability from pattern-matching alone (string concatenation near a query, `findById`-style calls, etc.) — confirm attacker control and check for controls elsewhere in the path first.

Output candidate findings per [finding.schema.json](../schemas/finding.schema.json) with `status: CANDIDATE`.

## Data-flow deep-dive task (06_data_flow_analysis)

Given one specific candidate finding whose `data_flow` is incomplete or whose confidence is capped by an unconfirmed step, resolve that specific step only (e.g. "is this validator actually applied on this route"). Use [data-flow-analysis.md](../skills/secure-code-review/references/data-flow-analysis.md) and [source-sink-analysis.md](../skills/secure-code-review/references/source-sink-analysis.md). Update the finding's `data_flow` and `confidence`; if the step still can't be resolved, set `status: NEEDS_MORE_EVIDENCE` rather than guessing.
