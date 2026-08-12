# Stage: Prioritization

TODO: Define purpose, inputs, outputs, and success criteria for this stage.

## Inputs

- TODO
- For dependency findings: KEV correlation output from
  `scripts/scanners/check_kev.py` (see
  [kev-correlation.md](../../skills/dependency-cve-check/references/kev-correlation.md)).
  A `kev.listed: true` finding is floored at the priority configured in
  `config/priority.config.yaml` → `kev_overrides` (P1, or P0 if
  `known_ransomware_campaign_use` is set) regardless of its CVSS-derived
  severity. This is a priority floor, never a ceiling or a downgrade.

## Outputs

- TODO
