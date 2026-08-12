# Report Template

Top-level document shape for [generate_markdown.py](../scripts/reporting/generate_markdown.py), assembling [executive_summary_template.md](executive_summary_template.md) and [finding_template.md](finding_template.md) per finding. The JSON/SARIF renderers ([generate_json.py](../scripts/reporting/generate_json.py), [generate_sarif.py](../scripts/reporting/generate_sarif.py)) serialize the same underlying [report.schema.json](../schemas/report.schema.json) data; this template only governs the Markdown rendering.

---

```markdown
# Security Review Report

*Generated {{metadata.generated_at}} · {{metadata.repository}} · scope: {{metadata.review_scope}}*

{{executive_summary_template.md rendered here}}

---

## Security Posture

{{Score /100 and a one-paragraph narrative of what it reflects — not just the number.}}

---

## Confirmed Findings

{{finding_template.md rendered for each entry in confirmed_findings, ordered by priority (P0 first), then severity.}}

---

## Remediation Roadmap

### Immediate (P0)
{{remediation_roadmap.immediate as a checklist of finding IDs + one-line titles}}

### Short-Term (P1)
{{remediation_roadmap.short_term}}

### Medium-Term (P2–P3)
{{remediation_roadmap.medium_term}}

### Hardening (P4 and general recommendations)
{{remediation_roadmap.hardening}}

---

## Final Conclusion

{{final_conclusion — a closing paragraph tying the findings back to overall risk and the recommended path forward.}}

---

*Rejected candidate findings and full verification evidence are available in the JSON output for audit purposes and are not repeated here.*
```
