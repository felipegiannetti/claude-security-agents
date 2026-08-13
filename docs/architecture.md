# Architecture

Security Review Agent is organized into layers that mirror the pipeline itself. If you're new to the codebase, read this before touching anything.

## Layers

| Layer | Directory | Role |
|---|---|---|
| Agents | `agents/` | Coordinate reasoning. Thin -- they orchestrate, they don't hold domain knowledge. |
| Skills | `skills/` | Reusable security methodology, one per vulnerability domain. Agents load these, not the other way around. |
| Workflow | `workflow/` | The deterministic 15-stage pipeline definition (`pipeline.yaml`) and per-stage documentation (`stages/*.md`), plus routing rules mapping code signals to Skills. |
| Knowledge | `knowledge/` | Shared reference data multiple Skills draw from: OWASP/CWE mappings, severity/priority/confidence/effort matrices, framework-specific guides. |
| Prompts | `prompts/` | Reusable prompt fragments for stages that have no dedicated agent, plus the report rendering templates. |
| Scripts | `scripts/` | Deterministic tooling -- scanner wrappers, git helpers, discovery heuristics, report generation. No LLM reasoning happens here. |
| Schemas | `schemas/` | JSON Schema contracts for every structure passed between stages. |
| Config | `config/` | Tunable behavior (severity/priority weights, exclusions, pentest authorization) kept separate from reasoning. |
| Hooks | `hooks/` | `PreToolUse` enforcement scripts backing the read-only policy at the tool layer, not just the prompt layer. |
| Tests | `tests/` | Regression fixtures (vulnerable/safe pairs) and the eval runner. |

## The Five Agents

- **architecture-mapper** -- builds the architectural model everything else depends on.
- **security-reviewer** -- primary vulnerability analysis; produces candidate findings.
- **security-verifier** -- independently tries to disprove each candidate.
- **architecture-advisor** -- assesses structure, produces `ARCH-*` recommendations (a separate axis from vulnerabilities).
- **pentest-validator** -- optional, disabled by default, the only agent that isn't purely read-only (it may send non-mutating HTTP requests to an explicitly authorized running target).

Every agent but `pentest-validator` is 100% read-only against everything, including a running target. `pentest-validator` is read-only against the *source repository* always, and against a *running system* only within the strict gate described in `agents/pentest-validator.md` and `config/pentest.config.yaml`.

## Two Report Axes

The final report has two structurally separate sections: **Application Security** (`SEC-*` confirmed vulnerabilities) and **Software Architecture** (`ARCH-*` structural recommendations). See `docs/reporting.md`.

## Where to Start Reading

1. `CLAUDE.md` -- the project's own constitution: purpose, core design principle, finding lifecycle, severity/priority, read-only policy.
2. `workflow/pipeline.yaml` -- the stage list end to end.
3. Whichever agent/skill you're about to touch.
