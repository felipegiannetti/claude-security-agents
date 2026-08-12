# AWS

**CWE-16**

## What to Look For

- **S3 buckets**: public read/write access (bucket policy or ACL), missing default encryption, missing block-public-access settings.
- **IAM**: policies with wildcard `Action: "*"` and/or `Resource: "*"`, especially attached to a role a compromised application component could assume.
- **Security Groups**: ingress rules allowing `0.0.0.0/0` on non-public-facing ports (database ports, SSH/RDP, internal service ports).
- **RDS/database instances**: `publicly_accessible = true` without a clear requirement, missing encryption at rest.
- **Secrets Manager / Parameter Store usage**: absence of it (credentials hardcoded elsewhere instead) is itself a signal — cross-reference [key-management.md](../../cryptography-review/references/key-management.md).

## False-Positive Conditions

- Public access is confirmed intentional and scoped to genuinely public resources.
- A broad IAM policy is attached only to a break-glass/emergency-access role with strong compensating controls (MFA enforcement, logging/alerting) — still worth noting at reduced severity.

## Severity Notes

Public S3 bucket with sensitive content, public database, or wildcard IAM policy on an application-facing role: `critical`.
