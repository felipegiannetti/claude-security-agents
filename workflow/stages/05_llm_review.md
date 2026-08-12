# Stage 05: LLM Review

## Purpose

Perform the primary vulnerability analysis: correlate scanner evidence with code and architectural context, apply relevant Skills, and produce candidate findings.

## Agent

[security-reviewer](../../agents/security-reviewer.md)

## Inputs

- Architecture model (`02_architecture_discovery`).
- Attack surface map (`03_attack_surface_mapping`).
- Normalized scan results (`04_static_scan`).
- [workflow/routing_rules.yaml](../routing_rules.yaml) to select applicable Skills.

## Process

See [security-reviewer.md](../../agents/security-reviewer.md): Skill selection, scanner correlation, source-to-sink analysis, and candidate finding output.

## Outputs

- A list of candidate findings conforming to [finding.schema.json](../../schemas/finding.schema.json), each with `status: CANDIDATE`.

## Success Criteria

- Every candidate finding cites evidence (actual code, not paraphrase) and a preliminary confidence level.
- No finding is marked `CONFIRMED` at this stage — that requires `08_verification`.
