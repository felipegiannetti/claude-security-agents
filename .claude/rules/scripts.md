# Script Development Rules

## Purpose

`scripts/` holds deterministic tooling — operations that don't require LLM reasoning and should never depend on it. Per CLAUDE.md: "Prefer deterministic scripts for operations that do not require LLM reasoning." If a script's output requires judgment (is this reachable, is this actually exploitable), that judgment belongs in an agent/Skill consuming the script's output, not in the script itself.

## Structure

- `scripts/scanners/` — wraps external tools (Semgrep, Gitleaks, Trivy, OSV Scanner) plus `check_kev.py`. Each takes `--path`/`--input`, normalizes to [scan-result.schema.json](../../schemas/scan-result.schema.json) or enriches [finding.schema.json](../../schemas/finding.schema.json)'s `kev` field, and never mutates the target.
- `scripts/git/` — read-only repository inspection (diff, changed files, metadata, history). No command in this directory may be one that mutates the working tree, index, or remote — see `.claude/rules/security.md` "Defensive Execution Policy."
- `scripts/discovery/` — heuristic architecture-mapper support (languages, frameworks, dependencies, entry points, existing controls). These are explicitly heuristics, documented as a starting hypothesis for `agents/architecture-mapper.md` to confirm, never as ground truth.
- `scripts/reporting/` — normalization, deduplication, priority calculation, posture scoring, and report rendering (Markdown/JSON/SARIF).
- `scripts/pentest/` — interface/contract for `agents/pentest-validator.md`'s dynamic validation. Subject to every rule in `config/pentest.config.yaml` and `.claude/rules/security.md` "The One Exception: pentest-validator" — a script here must never execute anything the config gates don't explicitly clear.
- `scripts/lib/` — shared helpers (`common.py`: YAML config loading, subprocess execution, JSON I/O). Import via `sys.path` manipulation from the script's own file location, not relative imports, so scripts remain runnable as standalone CLI entry points regardless of invocation directory.

## Conventions

1. **CLI, not library-only.** Every script is invokable standalone: `argparse`, reads from `--input`/stdin, writes to `--output`/stdout, so agents can call them via `Bash` per `.claude/rules/agents.md` "Tool Usage."
2. **Degrade, don't crash the pipeline.** A missing external tool (scanner not installed), a network failure (KEV feed unreachable), or unparseable output should produce a clear `skipped`/`warning` result on stderr and exit 0 — not an unhandled exception. See `scripts/scanners/check_kev.py` and `scripts/lib/common.py`'s `run_tool` for the pattern. The one exception: a script given genuinely malformed *input it's responsible for* (e.g. invalid JSON on stdin) should fail loudly (non-zero exit), since that's a caller bug, not an environment gap.
3. **Never invoke a scanner in autofix mode.** No `--fix`, `--autofix`, `-y`, or equivalent flag, ever — see `.claude/rules/security.md` "Defensive Execution Policy."
4. **Config-driven, not hardcoded.** Behavior that's plausibly project-specific (which scanners run, severity/priority weights, exclusion paths) reads from `config/*.yaml` via `common.load_yaml_config`, not literals in the script.
5. **Prefer stdlib; declare real dependencies explicitly.** `scripts/requirements.txt` lists what's actually needed (currently just PyYAML for config parsing) — don't add a dependency for something the standard library already does adequately (see `check_kev.py`'s use of `urllib` over adding an HTTP client library).
6. **Mask secrets in output.** Any script that might surface a credential (`run_gitleaks.py`) must mask it before printing/writing — see `.claude/rules/security.md` "Secrets Handling."
7. **Document heuristics as heuristics.** A discovery script's docstring should say plainly that its output is a starting hypothesis, not a confirmed fact, wherever that's true (which is most of `scripts/discovery/`).

## What Belongs in an Agent/Skill Instead

- Anything requiring code comprehension beyond pattern-matching (is this authorization check actually effective) — that's `security-reviewer`/`security-verifier`'s job, not a script's.
- Anything requiring judgment about severity/confidence beyond a documented, auditable formula — `scripts/reporting/calculate_priorities.py` implements `config/priority.config.yaml`'s explicit weights precisely because that formula is meant to be auditable and reproducible, not because priority calculation in general belongs in a script rather than a human/agent judgment call.
