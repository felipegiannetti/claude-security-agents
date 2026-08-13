# Remediation

Stage 14 (`workflow/stages/14_remediation_analysis.md`) turns each confirmed, prioritized finding into actionable guidance -- conforming to `schemas/remediation.schema.json`. This is always text/recommendation only; see `.claude/rules/security.md` "Absolute Read-Only Policy" -- nothing in this project ever applies a fix.

## What Every Remediation Record Contains

- **Summary** -- one or two sentences, what to do.
- **Explanation** -- what's vulnerable and why, framed for someone about to fix it.
- **Fix guidance** -- specific and framework-aware. `config/remediation.config.yaml` → `framework_hints` gives category-specific starting points (e.g. "use parameterized queries" for SQL injection); extend this as `knowledge/frameworks/` grows.
- **Example code** (optional) -- illustrative before/after snippets, explicitly informational.
- **Effort** (`trivial`/`small`/`medium`/`large`) -- see `config/remediation.config.yaml` → `category_default_effort` and `knowledge/standards/remediation-effort-matrix.yaml` for the criteria.
- **Verification steps** -- concrete: a test to add, a manual repro to re-attempt, or a scanner re-run expected to come back clean.

## Effort Estimation

Effort is a separate axis from severity/priority on purpose -- see `docs/prioritization.md`. A trivial-effort critical finding should never sit behind a large-effort medium finding in the roadmap just because "medium < critical" isn't the whole story once effort is considered.

## When a Finding's Root Cause Is Architectural

If `related_architecture_recommendations` is populated, the remediation should note the connection but still stand on its own -- fixing the underlying architecture (see `docs/architecture.md` and `13_security_architecture_recommendations`) is a longer-term structural improvement, not a substitute for the specific fix this finding needs now.

## Proportionality

Per `agents/security-reviewer.md` and the remediation prompt (`prompts/remediation_prompt.md`): a `P0` needs unambiguous, immediately actionable steps. A `P4`/informational item can be brief. Don't write a five-paragraph remediation for a missing security header.
