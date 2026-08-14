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

## Installation

This repo is a self-hosted Claude Code plugin marketplace (see `.claude-plugin/marketplace.json`) -- no central approval needed. Inside a Claude Code session (not a regular shell), run once:

```
/plugin marketplace add felipegiannetti/claude-security-agents
/plugin install security-review-agent@security-review-agent
```

This is a one-time, per-user setup -- it registers at `~/.claude/plugins/known_marketplaces.json` and the plugin (its agents, Skills, `/security-review` command, and safety hooks) becomes available in every project you open afterward, not just one. Update later with `/plugin marketplace update`.

Once installed, run `/security-review` inside any repository you want reviewed, or just describe the scope in conversation -- see [docs/usage.md](docs/usage.md).

## Author

Felipe Giannetti Fontenelle -- [LinkedIn](https://www.linkedin.com/in/felipe-giannetti-fontenelle-095501312/) . [GitHub](https://github.com/felipegiannetti) . felipegiannettifontenelle@gmail.com

## Legal / Disclaimer

- This is an AI-assisted tool, not a substitute for a formal, human-led security audit. Findings reflect the confidence and evidence discipline described in [CLAUDE.md](CLAUDE.md), but no automated system -- LLM-based or not -- eliminates false positives or false negatives entirely. Review confirmed findings, especially P0/P1, before acting on them or presenting them to a client.
- Distributed under the [MIT License](LICENSE), "as is," with no warranty of any kind -- see the license text for the full disclaimer of liability.
- `pentest-validator` (dynamic/live-target validation, see [config/pentest.config.yaml](config/pentest.config.yaml)) is disabled by default and must stay that way unless you have explicit, documented authorization to test the specific target you configure. Enabling it, or adding a target, against a system you are not authorized to test is your responsibility, not this project's.
- You are responsible for complying with your own organization's and your client's policies on running third-party tooling (including AI agents) against source code, especially code containing secrets, personal data, or regulated data categories.

## Status

Core system complete: all 5 agents, all 13 Skills, the full 15-stage pipeline, schemas, config, real scanner/reporting scripts, and hooks are implemented and wired together. The test suite has been run for real (not just written) against installed Semgrep/Gitleaks/Trivy/OSV-Scanner.

Known gaps:
- `scripts/pentest/validate_finding.py` only issues non-mutating `GET`/`HEAD`/`OPTIONS` requests by design -- state-changing findings get a generated manual-validation report instead (`scripts/pentest/generate_manual_validation_report.py`), never an automated mutating request.
- **Read-only enforcement is pattern-matching, not a sandbox.** `hooks/deny_mutating_bash.py`'s `PreToolUse` matcher covers both the `Bash` and `PowerShell` tools, and its pattern list recognizes native file-writing, deleting, relocating, and duplicating operations in both shells (and their common short aliases), plus git subcommands, shell redirection into a file, and package-manager installs. This closes the specific PowerShell-vs-Bash gap found during development. It cannot, and does not claim to, catch every possible way a general-purpose interpreter can write a file -- e.g. invoking Python's own file-writing functions via a `python -c`/heredoc call bypasses command-string pattern matching entirely, since the mutation happens inside the interpreter rather than as a recognizable shell command. Closing that class of gap needs OS-level sandboxing/containerization, not a smarter regex. Treat this hook as raising the bar substantially, not as a hard guarantee against a sufficiently deliberate bypass -- see the hook's own docstring for the same caveat stated in-line.
- This project's own test suite (`tests/test_runner.py`) has been run against installed real scanners and against one real third-party vulnerable application (OWASP NodeGoat); it has not been validated against a large-scale production-style codebase.
