# Testing

See `.claude/rules/testing.md` for the governing rules; this document is the practical how-to.

## Running the Suite

```bash
pip install -r scripts/requirements.txt
python tests/test_runner.py
```

This requires Python 3.10+ and, for full coverage of the automated tier, Semgrep, Gitleaks, Trivy, and OSV-Scanner installed and on `PATH`. Missing tools degrade to `[SKIP]` for the cases that need them, not a false pass or fail.

## Two Tiers

1. **Scanner-checkable** (`eval_cases.yaml` entries with a non-null `scanner`) -- `test_runner.py` actually runs the scanner against both the `vulnerable/` and `safe/` fixture and checks it fires on one and not the other. Currently: `sql-injection-001`, `secrets-001`, `command-injection-001` (Semgrep/Gitleaks), `dependencies-001` (OSV-Scanner).
2. **LLM-review-only** (`scanner: null`) -- most categories, since contextual reasoning (is there an ownership check *anywhere* in the call chain, is this check-and-act atomic) isn't something a pattern-matching scanner can evaluate. `test_runner.py` prints the expected outcome for a manual or agent-driven pipeline run to check against.

## Adding a Fixture Pair

Every category needs both a `vulnerable/` and a `safe/` example, differing *only* in the specific control that makes the safe one safe -- not in unrelated ways. See any existing pair (e.g. `tests/fixtures/sql-injection/`) as the template. Wire it into all three of `eval_cases.yaml`, `expected_findings.yaml`, `expected_false_positives.yaml`.

## When You Find a Real False Positive or False Negative

1. Minimize the triggering code into a new fixture pair (remove any real secrets/identifiers first).
2. Add it to `eval_cases.yaml`.
3. Update the relevant Skill's false-positive criteria (`skills/*/references/*.md`) to explicitly cover what was missed.
4. Re-run `test_runner.py` to confirm the fix holds.

Never weaken a Skill's verification criteria just to make a fixture pass -- see CLAUDE.md Development Rule 8.

## Lessons From Actually Running This

The first real run of this suite surfaced genuine bugs no amount of code review caught: `osv-scanner`'s CLI changed between major versions, Windows/PowerShell pipes silently prepend a UTF-8 BOM that broke every JSON-reading script, and a fixture pair that shared one sink (`render_template_string`) tripped an unrelated scanner rule regardless of the actual escaping difference being tested. Run the suite for real, on a real environment, before trusting it -- see `docs/usage.md`.
