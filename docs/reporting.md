# Reporting

Stage 15 produces the final deliverable, per `schemas/report.schema.json`, rendered by `scripts/reporting/generate_markdown.py` (Markdown), `generate_json.py` (JSON assembly), and `generate_sarif.py` (SARIF, Application Security axis only).

## Two Axes, Never Merged

- **`application_security`** -- confirmed vulnerabilities (`SEC-*`): finding counts, confirmed findings with full evidence, remediation roadmap.
- **`software_architecture`** -- structural recommendations (`ARCH-*`), present only if stages 12-13 ran: current-state summary, strengths, structural problems, recommendations, architecture roadmap.

An imperfect architecture is never presented as a vulnerability, and a vulnerability is never softened into an architecture recommendation. See `.claude/rules/security.md` "Security Findings vs. Architecture Recommendations."

## Rendering Is Deterministic, Content Isn't

`generate_markdown.py` and friends are pure formatters -- they take an already-assembled `report.schema.json`-shaped JSON (prose already written by the pipeline's LLM stages) and render it into the shapes defined in `prompts/report_template.md`, `prompts/executive_summary_template.md`, and `prompts/finding_template.md`. They never write prose themselves -- see `.claude/rules/scripts.md`.

## Audience Split Within the Markdown Report

- **Executive Summary** -- CTOs, managers, non-specialists. No unglossed jargon; every claim traceable to a `CONFIRMED` finding; never states something more severely than its recorded `severity`/`confidence`.
- **Technical body** -- developers, security engineers. Full evidence, attack vectors, data flows, exploitation scenarios, and -- when available -- Dynamic Validation results alongside Static Analysis and Independent Verification.

## Output Formats

| Format | Script | Covers |
|---|---|---|
| Markdown | `generate_markdown.py` | Both axes, full detail |
| JSON | `generate_json.py` | Both axes, machine-readable, assembles metadata + posture score + findings |
| SARIF | `generate_sarif.py` | Application Security axis only -- SARIF has no meaningful representation for architecture recommendations |

## Security Posture Score

`scripts/reporting/calculate_security_posture.py` computes a 0-100 score via a deliberately simple, explainable deduction model (front-loaded on `P0`/`P1` findings) -- see the script's own docstring for the exact point values. It's meant to be auditable, not a black box.
