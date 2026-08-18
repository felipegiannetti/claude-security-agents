# Remediation Prompt

Used by [14_remediation_analysis](../workflow/stages/14_remediation_analysis.md).

---

Include [system_prompt.md](system_prompt.md).

Task: given a `CONFIRMED`, prioritized finding and the detected language/framework from the architecture model, produce remediation guidance conforming to [remediation.schema.json](../schemas/remediation.schema.json). Recommendations are text-only — they are never applied to the repository (see [security.md](../.claude/rules/security.md)).

Cover:

- **Summary** — one or two sentences on what to do.
- **Explanation** — what's vulnerable and why, framed for someone about to fix it (not a restatement of the exploitation scenario).
- **Fix guidance** — specific and framework-aware. Use [remediation.config.yaml](../config/remediation.config.yaml) `framework_hints` where a category match exists; do not give generic "validate your input" advice when a specific mechanism (e.g. "use this ORM's parameterized query builder") is knowable from the architecture model.
- **User-facing error message changes** — when the fix involves what an error response reveals to a caller, apply the Error Detected / Probable Cause / Suggested Action pattern from [secure-coding-standard.md](../knowledge/standards/secure-coding-standard.md) Errors Don't Leak Internals, rather than proposing a bare generic string.
- **Example code** (optional) — illustrative before/after snippets, clearly labeled as informational only.
- **Effort** — one of `trivial` / `small` / `medium` / `large`, starting from `config/remediation.config.yaml` → `category_default_effort` and adjusted for the finding's actual scope (e.g. deduplicated across many call sites raises effort).
- **Verification steps** — concrete: a specific test to add, a manual repro to re-attempt, or a scanner re-run that should come back clean.

Proportion the guidance to risk: a P0 needs unambiguous, immediately actionable steps; a P4/informational item can be brief.

## Reject Vague Guidance

A remediation step is not done just because it names the right general action -- it must be specific enough that someone unfamiliar with the finding could execute it without further research. A one-word or one-phrase instruction with no concrete detail is a failure of this stage, not an acceptably terse answer. Examples of what NOT to write, and what must replace it:

- NOT "Rotate the credential." -- INSTEAD: which specific credential (name/location), rotate it where (which secret manager, which service's dashboard), and what else must happen alongside the rotation (revoke the old value, update every consumer, confirm no other copy exists elsewhere in the codebase per the finding's own evidence).
- NOT "Validate the input." -- INSTEAD: validate WHAT shape/type, using WHICH mechanism this codebase already has available (a specific validation library already in the dependency tree, the framework's built-in validators, a specific existing utility function) -- never generic advice detached from the actual stack.
- NOT "Use a stronger algorithm." -- INSTEAD: name the specific current algorithm/parameters found in the evidence, and the specific replacement (e.g. "bcrypt with cost factor 12" or "AES-256-GCM"), matching `knowledge/frameworks/*` guidance for the detected language/framework where one exists.
- NOT "Add authorization checks." -- INSTEAD: which specific check (ownership comparison against which field, a specific existing middleware/decorator this codebase already uses elsewhere), and where exactly it needs to be added (the specific function/route).

If the architecture model or finding evidence does not contain enough detail to be this specific, that is a signal to say so explicitly ("the exact secret manager in use could not be determined from available evidence -- confirm and rotate via your organization's standard credential rotation process") rather than papering over the gap with a generic instruction that sounds actionable but isn't.
