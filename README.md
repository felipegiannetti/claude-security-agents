# claude-security-agents

AI-powered application security review agents and skills for Claude Code.

See [CLAUDE.md](CLAUDE.md) for the full architecture and design principles. Quick map:

| Path | Purpose |
|---|---|
| [`agents/`](agents) | 5 agents: architecture-mapper, security-reviewer, security-verifier, architecture-advisor, pentest-validator (disabled by default) |
| [`skills/`](skills) | 13 reusable review skills (secure-code-review, injection, auth/authz, web, API, files, secrets, dependencies, business logic, crypto, IaC, architecture-review, logging-audit-review) |
| [`workflow/`](workflow) | The 15-stage deterministic review pipeline, plus `routing_rules.yaml` mapping languages/frameworks/entry points to Skills |
| [`knowledge/`](knowledge) | Shared reference material: OWASP, CWE, severity/priority/confidence/effort standards, framework-specific security guides |
| [`prompts/`](prompts) | Reusable prompt fragments and report templates |
| [`scripts/`](scripts) | Deterministic tooling: real scanner wrappers (Semgrep/Gitleaks/Trivy/OSV-Scanner + CISA KEV correlation + CVE age/severity policy), git helpers, discovery heuristics, reporting (priority scoring, Markdown/JSON/SARIF) |
| [`schemas/`](schemas) | JSON Schemas for data passed between pipeline stages, including the dual Application-Security / Software-Architecture report axes |
| [`config/`](config) | Scanner, severity, priority, remediation, exclusion, and pentest-authorization configuration |
| [`hooks/`](hooks) | `PreToolUse` enforcement scripts backing the read-only policy, wired into both `.claude-plugin/plugin.json` and `.claude/settings.json` |
| [`tests/`](tests) | Regression fixtures and evals — 12 categories have real vulnerable/safe example pairs, run by `tests/test_runner.py` against the real scanner scripts |
| [`docs/`](docs) | Project documentation (10 files, complete) |

## Status

Core system complete: all 5 agents, all 13 Skills, the full 15-stage pipeline, schemas, config, real scanner/reporting scripts, and hooks are implemented and wired together. The test suite has been run for real (not just written) against installed Semgrep/Gitleaks/Trivy/OSV-Scanner.

Known gaps:
- `scripts/pentest/validate_finding.py` only issues non-mutating `GET`/`HEAD`/`OPTIONS` requests by design -- state-changing findings get a generated manual-validation report instead (`scripts/pentest/generate_manual_validation_report.py`), never an automated mutating request.
- **Read-only enforcement is incomplete on Windows.** `hooks/deny_mutating_bash.py`'s `PreToolUse` matcher now covers both the `Bash` and `PowerShell` tools (fixed -- it previously only matched `Bash`, which meant PowerShell was a complete, unmonitored bypass of the entire read-only policy on any Windows session). Its pattern list itself still only recognizes Bash-syntax commands plus the shell-agnostic ones (git subcommands, package-manager installs) -- it does NOT yet recognize PowerShell-native file cmdlets (`Remove-Item`/`ri`/`del`, `Set-Content`, `New-Item`, `Copy-Item`, `Move-Item`, `Out-File`, redirection). Until that pattern list is extended, a Windows session with the PowerShell tool available can still write/delete/move files directly in the analyzed repository, bypassing the intended read-only guarantee. Do not treat this project as safe for unattended/high-trust use on Windows until this is closed.
- This project's own test suite (`tests/test_runner.py`) has been run against installed real scanners and against one real third-party vulnerable application (OWASP NodeGoat); it has not been validated against a large-scale production-style codebase.
