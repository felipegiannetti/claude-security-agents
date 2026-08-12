# Finding Template

Canonical Markdown rendering for a single finding, used by [generate_markdown.py](../scripts/reporting/generate_markdown.py). Fields map directly to [finding.schema.json](../schemas/finding.schema.json) — a field with no data is omitted from the rendered output, not printed as empty.

---

```markdown
### {{id}} — {{title}}

| | |
|---|---|
| **Severity** | {{severity}} |
| **Priority** | {{priority}} — {{priority_label}} |
| **Confidence** | {{confidence}} |
| **Category** | {{category}} |
| **CWE** | {{cwe}} |
| **OWASP** | {{owasp_category}} |
| **Location** | `{{location.file}}:{{location.line_start}}` |

**Summary**

{{one-paragraph plain-language description}}

**Evidence**

\`\`\`{{language}}
{{evidence[].snippet}}
\`\`\`

**Data Flow**

{{data_flow[] rendered as SOURCE → ... → SINK, each step annotated (confirmed) or (assumed)}}

**Attack Vector**

{{attack_vector}}

**Exploitation Scenario**

{{exploitation_scenario}}

**Attacker Prerequisites**

- Authentication required: {{attacker_prerequisites.authentication_required}}
- Privileges required: {{attacker_prerequisites.privileges_required}}
- Network position: {{attacker_prerequisites.network_position}}

**Impact**

- Technical: {{technical_impact}}
- Business: {{business_impact}}
- If unresolved: {{consequences_if_unresolved}}

**Remediation**

{{remediation.summary}}

{{remediation.fix_guidance}}

{{remediation.example_code[] if present, each labeled before/after}}

Estimated effort: {{remediation.effort}}

**Verification Steps**

{{remediation.verification_steps[] as a checklist}}

**Priority Rationale**

{{prioritization_prompt.md output — why this landed at this priority}}
```

For `REJECTED` findings that are surfaced in an appendix (optional, for transparency/audit), render only: id, title, category, and `false_positive_analysis.conclusion` — no exploitation scenario or remediation section, since none applies.
