# Cloud Credentials

**CWE-798**

## What to Look For

AWS access keys, Azure service principal secrets, GCP service account JSON keys, or equivalent hardcoded in source, config, container images, or CI/CD pipeline definitions. Also check IaC files (see [iac-misconfig-review](../../iac-misconfig-review/SKILL.md)) for credentials embedded directly rather than referenced from a secret manager.

## Category-Specific Notes

- Cloud credentials are typically the highest-impact secret category — a leaked cloud credential can grant access far beyond the application itself (other services, other data, billing).
- Check the associated IAM policy/role scope if determinable — a credential scoped to one narrow action is lower-impact than one with broad account access, but both are findings.

## Severity Notes

`critical`, essentially without exception — the blast radius of a leaked cloud credential is rarely containable to just "this application."
