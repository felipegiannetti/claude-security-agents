# Stage 07: Data Flow Analysis

## Purpose

Deepen the source-to-sink trace for candidate findings where `06_llm_security_review`'s initial pass left a step in the chain unconfirmed. This stage exists so that data-flow depth is a deliberate, checkable step in the pipeline rather than something that quietly varies with how thorough a single review pass happened to be.

## Prompt

[review_prompt.md](../../prompts/review_prompt.md) (data-flow-analysis section) — runs in the orchestrating context, re-invoking `security-reviewer`'s reasoning on specific candidates rather than the whole codebase.

## Inputs

- Candidate findings from `06_llm_security_review` whose `data_flow` field is incomplete or whose confidence is below `MEDIUM` due to an unconfirmed path step.

## Process

For each such candidate, re-trace:

```
SOURCE → PARSING → TRANSFORMATION → VALIDATION → AUTHENTICATION → AUTHORIZATION → BUSINESS LOGIC → SINK
```

explicitly resolving the specific unconfirmed step — e.g. "is this validator actually applied on this route" or "does this value ever leave the trusted internal network before reaching the sink." Use [source-sink-analysis.md](../../skills/secure-code-review/references/source-sink-analysis.md) and [data-flow-analysis.md](../../skills/secure-code-review/references/data-flow-analysis.md) for methodology.

## Outputs

- Updated candidate findings with a complete `data_flow` field and a revised confidence level. Findings that still can't be resolved are marked `NEEDS_MORE_EVIDENCE` rather than passed forward with an artificially high confidence.

## Success Criteria

- No candidate finding reaches `08_security_triage` with a data-flow claim that hasn't been explicitly checked at least once.
