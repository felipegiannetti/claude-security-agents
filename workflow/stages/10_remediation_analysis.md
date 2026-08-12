# Stage 10: Remediation Analysis

## Purpose

Turn each confirmed, prioritized finding into actionable guidance — what's wrong, why, how to fix it, and how to verify the fix — without ever applying it (see CLAUDE.md's Remediation Requirements and [security.md](../../.claude/rules/security.md)).

## Prompt

[remediation_prompt.md](../../prompts/remediation_prompt.md)

## Inputs

- `CONFIRMED` findings with an assigned `priority` from `09_prioritization`.
- The detected language/framework from the architecture model, so guidance is idiomatic (e.g. parameterized queries via the specific ORM in use, not generic advice).

## Process

For each finding, produce:

1. What is vulnerable and why.
2. Where the issue exists (already known from the finding's location).
3. How an attacker could exploit it (already known from the verified attack path).
4. Realistic consequences if left unresolved.
5. How it should be fixed — specific, framework-aware, proportionate to risk. May include example code or pseudocode as informational guidance only.
6. Estimated remediation effort (`trivial` / `small` / `medium` / `large` per [remediation-effort-matrix.yaml](../../knowledge/standards/remediation-effort-matrix.yaml)).
7. Verification steps the team can use to confirm the fix actually closes the gap.

## Outputs

- Each finding annotated with a remediation record conforming to [remediation.schema.json](../../schemas/remediation.schema.json).

## Success Criteria

- Remediation guidance is specific enough to act on without further research, but never phrased as something this system will apply itself.
