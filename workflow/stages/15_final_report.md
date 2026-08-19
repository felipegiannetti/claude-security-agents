# Stage 15: Final Report

## Purpose

Produce the deliverable: a report that helps the reader decide what to fix first, why it matters, and what happens if it isn't fixed — not just a list of findings (see CLAUDE.md's Final Security Report). The report has two axes: **Application Security** (vulnerabilities) and **Software Architecture** (structural recommendations) — they are related but never conflated. An imperfect architecture is not automatically presented as a vulnerability, and a vulnerability is never buried inside an architecture recommendation.

## Scripts

- [generate_markdown.py](../../scripts/reporting/generate_markdown.py)
- [generate_json.py](../../scripts/reporting/generate_json.py)
- [generate_sarif.py](../../scripts/reporting/generate_sarif.py) — Application Security axis only; SARIF has no meaningful representation for architecture recommendations.
- [calculate_security_posture.py](../../scripts/reporting/calculate_security_posture.py) — overall risk rollup.

## Prompts / Templates

- [executive_summary_template.md](../../prompts/executive_summary_template.md)
- [finding_template.md](../../prompts/finding_template.md)
- [report_template.md](../../prompts/report_template.md)

## Inputs

- All findings with remediation guidance from `14_remediation_analysis` (Application Security axis).
- Architecture assessment from `12_architecture_assessment` and recommendations from `13_security_architecture_recommendations` (Software Architecture axis).
- The requested output format(s) from `01_intake`.

## Process

1. Compute overall security posture and finding counts by severity/priority via `calculate_security_posture.py`.
2. Assign final `SEC-NNN` identifiers to vulnerability findings and `ARCH-NNN` identifiers to architecture recommendations — distinct numbering spaces, never mixed.
3. Render the executive summary (audience: CTOs, managers, business stakeholders) and the technical body (audience: developers, security engineers) per [report.schema.json](../../schemas/report.schema.json).
4. Build the security remediation roadmap: immediate (P0), short-term (P1), medium-term (P2–P3), hardening (P4 and general recommendations).
5. Build the architecture roadmap separately, per `ARCH-P0`–`ARCH-P3`, phrased as gradual evolution steps, not a single "rewrite everything" recommendation (see [architecture-advisor.md](../../agents/architecture-advisor.md)).
6. Present the rendered report directly in the conversation. Never create a file inside the analyzed repository to hold it -- see CLAUDE.md's `outputs/` section and `.claude/rules/security.md` "Absolute Read-Only Policy," which forbids creating files inside the analyzed repository with no exception for the report itself. Only if the user explicitly asks for a saved file, write it OUTSIDE the analyzed project (a path they specify, or a scratch/temp location) and tell them exactly where. A missing `outputs/`, `config/`, or any other directory in the analyzed project is never a reason to stop or fail this stage -- the target project is never expected to mirror this plugin's own structure.

## Outputs

A report with two clearly separated sections:

- **Application Security**: Executive Summary, Overall Risk, Finding Counts, Priority Overview, Confirmed Findings (with evidence, attack vectors, data flows, exploitation scenarios, and — when available — Dynamic Validation results alongside Static Analysis and Independent Verification), Business Impact, Consequences if Unresolved, Recommended Remediation, Remediation Effort, Verification Steps, Remediation Roadmap.
- **Software Architecture**: current-state summary, strengths, structural problems, security-relevant technical debt, recommended organization, architecture recommendations (`ARCH-NNN`) with benefits/costs/risks/complexity, and a phased architecture roadmap.
- A **Final Conclusion** tying both axes together.

In Markdown, JSON, and/or SARIF (Application Security axis) per request. Markdown is normally rendered directly in the conversation; if JSON/SARIF is requested as a saved file, the same rule applies -- outside the analyzed project, never inside it.

## Success Criteria

- A non-technical reader can find the top 3 things to fix and why from the executive summary alone, for both axes.
- A developer can act on a finding or a recommendation using only its own section, without needing to re-derive context from the codebase.
- Report content matches the underlying data exactly — no finding is described more severely or confidently in prose than its recorded severity/confidence, and no architecture recommendation is phrased as a confirmed vulnerability.
