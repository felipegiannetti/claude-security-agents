# Stage 11: Security Prioritization

## Purpose

Convert confirmed findings into a remediation order. Severity and priority are separate concepts (see CLAUDE.md's Severity and Priority): severity is technical/business impact, priority is remediation urgency. A P0 and a "Critical" severity finding are not automatically the same finding.

## Script

[calculate_priorities.py](../../scripts/reporting/calculate_priorities.py), driven by [config/priority.config.yaml](../../config/priority.config.yaml).

## Inputs

- `CONFIRMED` findings from `09_independent_verification`, each with severity, confidence, and (for dependency findings) KEV correlation data.
- Dynamic validation results from `10_dynamic_pentest_validation`, when that stage ran — a finding with a successful dynamic confirmation should not score lower in confidence-derived weighting than one verified statically only.

## Process

1. Compute a priority from the weighted factors in `config/priority.config.yaml`: severity, exploitability, exposure, authentication requirements, privileges required, affected data sensitivity, business impact, blast radius, confidence, and remediation effort.
2. Apply `kev_overrides`: a `kev.listed: true` finding is floored at `listed_priority_floor` (P1), and one with `known_ransomware_campaign_use` set is floored at `known_ransomware_campaign_use_priority_floor` (P0) — see [kev-correlation.md](../../skills/dependency-cve-check/references/kev-correlation.md). This is a floor, never a downgrade: if other factors already produced a higher priority, KEV status doesn't lower it.
3. Assign one of: `P0` — Immediate, `P1` — High, `P2` — Medium, `P3` — Low, `P4` — Informational.

## Outputs

- Every `CONFIRMED` finding annotated with a `priority` field and the factors that drove it, so the reasoning is auditable in the final report rather than a black-box number.

## Success Criteria

- A low-severity, low-effort fix and a high-severity, high-effort fix are not defaulted to the same priority just because they share a severity label — effort and exploitability materially move the outcome.
- Priority reasoning is traceable back to `config/priority.config.yaml`, not an unexplained model judgment call.
