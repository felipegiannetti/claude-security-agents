# Report Template

Top-level document shape for [generate_markdown.py](../scripts/reporting/generate_markdown.py), assembling [executive_summary_template.md](executive_summary_template.md) and [finding_template.md](finding_template.md) per finding. The JSON/SARIF renderers ([generate_json.py](../scripts/reporting/generate_json.py), [generate_sarif.py](../scripts/reporting/generate_sarif.py) — SARIF covers the Application Security axis only) serialize the same underlying [report.schema.json](../schemas/report.schema.json) data; this template only governs the Markdown rendering. Two axes, always visually and structurally separate: **Application Security** (`SEC-*`) and **Software Architecture** (`ARCH-*`) — see [15_final_report.md](../workflow/stages/15_final_report.md).

---

```markdown
# Security Review Report

*Generated {{metadata.generated_at}} · {{metadata.repository}} · scope: {{metadata.review_scope}}*
{{if metadata.dynamic_validation_performed: note that dynamic validation ran, and against which authorized target}}

{{executive_summary_template.md rendered here}}

---

# Part 1 — Application Security

## Security Posture

{{Score /100 and a one-paragraph narrative of what it reflects — not just the number.}}

## Confirmed Findings

{{finding_template.md rendered for each entry in application_security.confirmed_findings, ordered by priority (P0 first), then severity.}}

## Remediation Roadmap

### Immediate (P0)
{{application_security.remediation_roadmap.immediate as a checklist of finding IDs + one-line titles}}

### Short-Term (P1)
{{application_security.remediation_roadmap.short_term}}

### Medium-Term (P2–P3)
{{application_security.remediation_roadmap.medium_term}}

### Hardening (P4 and general recommendations)
{{application_security.remediation_roadmap.hardening}}

---

# Part 2 — Software Architecture

{{Only rendered if software_architecture is present — architecture assessment is not always run.}}

## Current State

{{software_architecture.current_state_summary}}

**Strengths**
{{software_architecture.strengths as a list}}

**Structural Problems**
{{software_architecture.structural_problems as a list, each with its supporting evidence}}

**Security-Relevant Technical Debt**
{{software_architecture.security_relevant_technical_debt as a list}}

## Architecture Recommendations

{{For each entry in software_architecture.recommendations, rendered similarly to finding_template.md but using architecture-recommendation.schema.json fields: ARCH-NNN, title, priority (ARCH-P0..P3), assessed_problem, recommendation, rationale, security_implications, benefits, costs, risks, complexity_introduced, phased_path as a numbered list, and related_findings (SEC-NNN cross-references) if present.}}

## Architecture Roadmap

{{software_architecture.architecture_roadmap.phases, each phase's description and the recommendation IDs it covers — phased, never a single "rewrite everything" step.}}

---

## Final Conclusion

{{final_conclusion — a closing paragraph tying both the Application Security and Software Architecture axes back to overall risk and the recommended path forward.}}

---

*Rejected candidate findings and full verification (and, when performed, dynamic validation) evidence are available in the JSON output for audit purposes and are not repeated here.*
```
