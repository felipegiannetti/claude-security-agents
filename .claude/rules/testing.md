# Testing Rules

## Purpose

Measures whether this project actually does what CLAUDE.md claims: find real vulnerabilities and reject false positives, at a rate good enough to trust. Detection quality and false-positive rate are both first-class quality metrics — a system that finds everything but drowns real findings in noise is not a success, and neither is one that stays quiet by rejecting everything.

## Structure

Every important finding category should eventually have a fixture pair under `tests/fixtures/<category>/`:

- `vulnerable/` — a minimal, realistic example that should produce a `CONFIRMED` finding.
- `safe/` — a close variant of the same code that should NOT — differing only in the specific control that makes it safe (parameterization, auto-escaping, an ownership check, etc.), not in unrelated ways. A safe fixture that looks nothing like its vulnerable pair doesn't test discrimination, just detection.

`tests/eval_cases.yaml` enumerates each pair; `tests/expected_findings.yaml` and `tests/expected_false_positives.yaml` record the expected outcome for each side.

## Two Tiers of Evaluation

Not every finding category is mechanically checkable. `tests/test_runner.py` runs two kinds of eval:

1. **Scanner-checkable** (`eval_cases.yaml` entries with a non-null `scanner`): the runner actually executes the relevant `scripts/scanners/*.py` against both fixtures and checks it fires on `vulnerable/` and not on `safe/`. This is real, automated, and covers pattern-detectable categories (SQL injection, secrets).
2. **LLM-review-only** (`scanner: null`): categories like BOLA/IDOR fundamentally require `06_llm_security_review`'s contextual reasoning (is there an ownership check *anywhere* in the call chain) — no deterministic scanner can evaluate that. `test_runner.py` cannot execute an agentic review itself; it reports the expected outcome so a manual or agent-driven pipeline run against the fixture can be checked consistently.

Do not treat tier 2's manual nature as optional — a category with no way to check its false-positive rate is a category whose quality claims are unverified.

## Metrics

From a full eval run (both tiers), track: true positives, false positives, false negatives, precision, recall, and — per CLAUDE.md's emphasis — false-positive rate specifically, since minimizing false positives while keeping real detection is this project's central quality bar (see CLAUDE.md "Core Design Principle" and "the smallest possible set of highly confident findings").

## Regression Discipline

When the pipeline produces a false positive during real use (a Skill flags something `secure-code-review`'s or the specific Skill's own documented false-positive conditions should have caught):

1. Add the specific scenario as a new fixture pair and `eval_cases.yaml` entry — not a vague description, the actual code that triggered it (minimized, with any real secrets/identifiers removed).
2. Update the relevant Skill's false-positive criteria (its `references/*.md`) to explicitly cover the missed condition.
3. Re-run `test_runner.py` to confirm the fix holds and didn't regress anything else.

The same applies in reverse for a missed true positive (false negative) — add it as a fixture, and check whether a Skill's evidence checklist needs to cover the missed pattern.

## What Not to Do

- Never weaken a Skill's verification criteria just to make a fixture pass — CLAUDE.md Development Rule 8 ("never weaken verification requirements") applies to test-chasing as much as to real reviews.
- Never add a fixture pair without both a vulnerable and a safe variant — a category with only "vulnerable" examples can't measure false-positive rate, which is half of what this file exists to protect.
