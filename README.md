# claude-security-agents

AI-powered application security review agents and skills for Claude Code.

See [CLAUDE.md](CLAUDE.md) for the full architecture and design principles. Quick map:

| Path | Purpose |
|---|---|
| [`agents/`](agents) | Claude Code agents: architecture-mapper, security-reviewer, security-verifier |
| [`skills/`](skills) | Reusable security review skills (injection, auth/authz, web, API, files, secrets, dependencies, business logic, crypto, IaC) |
| [`workflow/`](workflow) | The 11-stage deterministic review pipeline |
| [`knowledge/`](knowledge) | Shared reference material: OWASP, CWE, severity/priority standards, framework guides |
| [`prompts/`](prompts) | Reusable prompt fragments and report templates |
| [`scripts/`](scripts) | Deterministic tooling: scanners, git helpers, discovery, reporting |
| [`schemas/`](schemas) | JSON Schemas for data passed between pipeline stages |
| [`config/`](config) | Scanner, severity, priority, remediation, and exclusion configuration |
| [`tests/`](tests) | Regression fixtures and evals (vulnerable/safe examples per category) |
| [`docs/`](docs) | Project documentation |

## Status

Scaffolding stage — structure is in place, most files are stubs pending implementation.
