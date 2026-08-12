# Stage 11: Final Report

## Purpose

Produce the deliverable: a report that helps the reader decide what to fix first, why it matters, and what happens if it isn't fixed — not just a list of findings (see CLAUDE.md's Final Security Report).

## Scripts

- [generate_markdown.py](../../scripts/reporting/generate_markdown.py)
- [generate_json.py](../../scripts/reporting/generate_json.py)
- [generate_sarif.py](../../scripts/reporting/generate_sarif.py)
- [calculate_security_posture.py](../../scripts/reporting/calculate_security_posture.py) — overall risk rollup.

## Prompts / Templates

- [executive_summary_template.md](../../prompts/executive_summary_template.md)
- [finding_template.md](../../prompts/finding_template.md)
- [report_template.md](../../prompts/report_template.md)

## Inputs

- All findings with remediation guidance from `10_remediation_analysis`.
- The requested output format(s) from `01_intake`.

## Process

1. Compute overall security posture and finding counts by severity/priority via `calculate_security_posture.py`.
2. Assign final `SEC-NNN` identifiers.
3. Render the executive summary (audience: CTOs, managers, business stakeholders) and the technical body (audience: developers, security engineers) per [report.schema.json](../../schemas/report.schema.json).
4. Build the remediation roadmap: immediate (P0), short-term (P1), medium-term (P2–P3), hardening (P4 and general recommendations).
5. Emit the requested format(s) into `outputs/`.

## Outputs

A report containing at minimum: Executive Summary, Overall Risk, Finding Counts, Priority Overview, Confirmed Findings (with evidence, attack vectors, data flows, exploitation scenarios), Business Impact, Consequences if Unresolved, Recommended Remediation, Remediation Effort, Verification Steps, Remediation Roadmap, Final Conclusion — in Markdown, JSON, and/or SARIF per request.

## Success Criteria

- A non-technical reader can find the top 3 things to fix and why from the executive summary alone.
- A developer can act on a finding using only its technical section, without needing to re-derive context from the codebase.
- Report content matches the underlying findings exactly — no finding is described more severely or confidently in prose than its recorded severity/confidence.
