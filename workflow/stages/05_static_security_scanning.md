# Stage 05: Static Security Scanning

## Purpose

Run deterministic tooling to produce evidence — suspicious patterns, exposed secrets, vulnerable dependencies, and misconfigurations — that feeds the LLM-driven review. Scanner output is evidence, never a conclusion (see [security.md](../../.claude/rules/security.md) Scanner Trust Policy).

## Scripts

- [run_semgrep.py](../../scripts/scanners/run_semgrep.py) — static pattern analysis.
- [run_gitleaks.py](../../scripts/scanners/run_gitleaks.py) — secret detection.
- [run_trivy.py](../../scripts/scanners/run_trivy.py) — dependency/misconfig/container scanning.
- [run_osv_scanner.py](../../scripts/scanners/run_osv_scanner.py) — dependency CVEs.
- [check_kev.py](../../scripts/scanners/check_kev.py) — CISA KEV correlation for CVEs found above.

All scanners run per `config/scanners.config.yaml`. None run in autofix mode — see [security.md](../../.claude/rules/security.md) Defensive Execution Policy.

## Inputs

- The review scope from `01_intake`.
- The architecture model from `03_architecture_mapping` (to select which scanners are relevant — e.g. skip a Python-specific scanner on a pure Node.js repo).

## Process

1. Run each enabled scanner against the in-scope files.
2. Normalize each scanner's native output into [scan-result.schema.json](../../schemas/scan-result.schema.json) via `scripts/reporting/normalize_findings.py`.
3. Run `check_kev.py` against any CVEs surfaced by `run_osv_scanner.py`/`run_trivy.py`.

## Outputs

- A normalized list of scan results, each still labeled as raw scanner evidence — not a candidate finding yet. Promotion to `CANDIDATE` happens in `06_llm_security_review`, where results are correlated with code and architectural context.

## Success Criteria

- Every scanner result is normalized to the shared schema regardless of source tool, so downstream stages don't need scanner-specific handling.
- A scanner failure (tool not installed, network unavailable for KEV) degrades that scanner's contribution without failing the whole stage — see each script's own error handling.
