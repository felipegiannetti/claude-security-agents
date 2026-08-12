# Stage 06: LLM Security Review

## Purpose

Perform the primary vulnerability analysis: correlate scanner evidence with code and architectural context, apply relevant Skills, and produce candidate findings.

## Agent

[security-reviewer](../../agents/security-reviewer.md)

## Inputs

- Architecture model (`03_architecture_mapping`) and software context (`02_software_context_discovery`).
- Attack surface map (`04_attack_surface_mapping`).
- Normalized scan results (`05_static_security_scanning`).
- [workflow/routing_rules.yaml](../routing_rules.yaml) to select applicable Skills.

## Process

See [security-reviewer.md](../../agents/security-reviewer.md): Skill selection, scanner correlation, source-to-sink analysis, and candidate finding output.

## Outputs

- A list of candidate findings conforming to [finding.schema.json](../../schemas/finding.schema.json), each with `status: CANDIDATE`.

## Success Criteria

- Every candidate finding cites evidence (actual code, not paraphrase) and a preliminary confidence level.
- No finding is marked `CONFIRMED` at this stage — that requires `09_independent_verification`.
