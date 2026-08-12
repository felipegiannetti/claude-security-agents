# Terraform

**CWE-16**

## What to Look For

- Hardcoded credentials/secrets in `.tf` files or `.tfvars` committed to the repository — see [secrets-detection](../../secrets-detection/SKILL.md).
- Resources provisioned with public access by default (public S3-equivalent buckets, security groups/firewall rules allowing `0.0.0.0/0` on sensitive ports, publicly accessible databases).
- State file (`terraform.tfstate`) committed to version control — state files often contain sensitive resource attributes (including plaintext secrets for some providers) and should never be in the repository.
- Overly permissive IAM policies defined in Terraform (wildcard actions/resources) — see the cloud-provider-specific references below.

## False-Positive Conditions

- Public access is confirmed intentional for a genuinely public resource (e.g. static asset hosting) and scoped narrowly (specific paths, not the whole bucket/service).
- The `.tfstate` in the repository is a stale/example file, not the actual state backing a real deployment (still worth flagging as a hygiene issue, but lower severity).

## Severity Notes

Public database/security-group misconfiguration: `critical`. Committed state file with live secrets: `critical`. Overly broad IAM policy: `high`.
