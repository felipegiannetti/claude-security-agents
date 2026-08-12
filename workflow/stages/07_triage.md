# Stage 07: Triage

## Purpose

Deterministically clean up the candidate finding set before it goes to independent verification: deduplicate, normalize, and assign a preliminary severity — so `security-verifier` spends its effort on distinct, well-formed candidates instead of scanner noise or duplicate reports of the same root cause.

## Scripts

- [normalize_findings.py](../../scripts/reporting/normalize_findings.py)
- [deduplicate_findings.py](../../scripts/reporting/deduplicate_findings.py)

## Inputs

- Candidate findings from `05_llm_review` / `06_data_flow_analysis`.
- [config/severity.config.yaml](../../config/severity.config.yaml).

## Process

1. Normalize all candidates to a single consistent shape ([finding.schema.json](../../schemas/finding.schema.json)).
2. Deduplicate findings that share a root cause (e.g. the same missing validation helper flagged at five call sites) into one finding with multiple locations, rather than five separate findings.
3. Assign preliminary severity per `config/severity.config.yaml`, based on CWE/category and technical impact — independent of the priority calculation, which happens later in `09_prioritization`.
4. Advance status from `CANDIDATE` to `TRIAGED`.

## Outputs

- A deduplicated, normalized, severity-tagged list of `TRIAGED` findings.

## Success Criteria

- No two findings in the triaged list describe the same underlying issue.
- Every finding has a severity assigned via the configured criteria, not an ad hoc judgment call.
