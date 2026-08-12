# Remediation Prompt

Used by [14_remediation_analysis](../workflow/stages/14_remediation_analysis.md).

---

Include [system_prompt.md](system_prompt.md).

Task: given a `CONFIRMED`, prioritized finding and the detected language/framework from the architecture model, produce remediation guidance conforming to [remediation.schema.json](../schemas/remediation.schema.json). Recommendations are text-only — they are never applied to the repository (see [security.md](../.claude/rules/security.md)).

Cover:

- **Summary** — one or two sentences on what to do.
- **Explanation** — what's vulnerable and why, framed for someone about to fix it (not a restatement of the exploitation scenario).
- **Fix guidance** — specific and framework-aware. Use [remediation.config.yaml](../config/remediation.config.yaml) `framework_hints` where a category match exists; do not give generic "validate your input" advice when a specific mechanism (e.g. "use this ORM's parameterized query builder") is knowable from the architecture model.
- **Example code** (optional) — illustrative before/after snippets, clearly labeled as informational only.
- **Effort** — one of `trivial` / `small` / `medium` / `large`, starting from `config/remediation.config.yaml` → `category_default_effort` and adjusted for the finding's actual scope (e.g. deduplicated across many call sites raises effort).
- **Verification steps** — concrete: a specific test to add, a manual repro to re-attempt, or a scanner re-run that should come back clean.

Proportion the guidance to risk: a P0 needs unambiguous, immediately actionable steps; a P4/informational item can be brief.
