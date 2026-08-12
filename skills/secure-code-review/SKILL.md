---
name: secure-code-review
description: General-purpose secure code review methodology - data-flow and source-sink analysis, and false-positive triage. Use as the default entry point for reviewing a diff or codebase for security issues, and as the shared foundation every other Skill in this project builds on.
---

# Secure Code Review

This is the foundational Skill. Every other Skill in this project (injection-review, auth-authz-review, web-security-review, etc.) assumes this methodology rather than restating it — read this first, then load the domain-specific Skill for the category at hand.

- [Methodology](references/methodology.md) — the review process itself, step by step.
- [Data Flow Analysis](references/data-flow-analysis.md) — how to trace a value through a codebase.
- [Source Sink Analysis](references/source-sink-analysis.md) — how to reason about a specific source/sink pair.
- [False Positive Analysis](references/false-positive-analysis.md) — the discipline of actively trying to disprove a candidate finding before reporting it.

## When to Use

At the start of `06_llm_security_review` for any finding category, and again narrowly in `07_data_flow_analysis` when a specific candidate needs a deeper trace. Domain Skills (injection-review, etc.) tell you *what patterns to look for*; this Skill tells you *how to confirm whether a pattern found is actually exploitable*.

## Core Discipline

1. **Never conclude from pattern alone.** A dangerous function name, a `findById`-style call, or a scanner hit is a reason to *look closer*, not a conclusion.
2. **Trace before you claim.** Follow [source-sink-analysis.md](references/source-sink-analysis.md)'s SOURCE → ... → SINK model for the specific path in question — don't reason about the vulnerability class in the abstract.
3. **Actively look for what would disprove the finding**, per [false-positive-analysis.md](references/false-positive-analysis.md), before writing it up. If security-reviewer skips this step, security-verifier will do it anyway and reject the finding — do it first and save the round trip.
4. **State what you didn't check.** If a step in the path couldn't be confirmed from available evidence, say so — mark confidence accordingly rather than rounding up.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json), with the `data_flow` field populated per [data-flow-analysis.md](references/data-flow-analysis.md) and `confidence` reflecting how much of the path was actually confirmed vs. assumed.
