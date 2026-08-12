# Executive Summary Template

Audience: CTOs, engineering managers, and other non-security-specialist decision-makers. No jargon without a one-line gloss; every claim traceable to a `CONFIRMED` finding. Used by [generate_markdown.py](../scripts/reporting/generate_markdown.py).

---

```markdown
## Executive Summary

{{2-4 sentence overview: what was reviewed, and the headline risk conclusion.}}

**Overall Risk: {{overall_risk}}**

{{One paragraph: what drives this rating. Name the 1-3 findings that matter most in plain language, not just IDs.}}

### Findings at a Glance

| Severity | Count |
|---|---|
| Critical | {{finding_counts.by_severity.critical}} |
| High | {{finding_counts.by_severity.high}} |
| Medium | {{finding_counts.by_severity.medium}} |
| Low | {{finding_counts.by_severity.low}} |
| Informational | {{finding_counts.by_severity.informational}} |

| Priority | Count | Meaning |
|---|---|---|
| P0 | {{finding_counts.by_priority.P0}} | Fix immediately |
| P1 | {{finding_counts.by_priority.P1}} | Fix this cycle |
| P2 | {{finding_counts.by_priority.P2}} | Fix soon |
| P3 | {{finding_counts.by_priority.P3}} | Backlog |
| P4 | {{finding_counts.by_priority.P4}} | Informational / hardening |

### What This Means for the Business

{{Translate the top findings into business terms: what data or system could be affected, and in what scenario. Avoid restating CVSS/CWE jargon here — that belongs in the technical section.}}

### What Happens If Nothing Is Fixed

{{Concrete consequences for the top 1-3 findings, phrased as realistic scenarios, not worst-case hypotheticals.}}

### Recommended Immediate Actions

{{Bulleted list of P0 items only, each one sentence, phrased as an action ("Add an ownership check to the order-cancellation endpoint"), linking to the finding ID for detail.}}
```

Never state a finding more severely or confidently here than its recorded `severity`/`confidence` in the underlying data — this section summarizes, it doesn't editorialize.
