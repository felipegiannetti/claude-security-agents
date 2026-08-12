# GCP

**CWE-16**

## What to Look For

- **Cloud Storage buckets**: `allUsers`/`allAuthenticatedUsers` granted IAM roles (the GCP equivalent of a public S3 bucket) — `allAuthenticatedUsers` in particular is often mistaken for "internal only" but means any Google account holder, not just this organization's.
- **IAM**: primitive roles (`Owner`/`Editor`) granted to a service account when a narrower predefined/custom role would do.
- **Firewall rules**: `0.0.0.0/0` source ranges on non-load-balancer-facing ports.
- **Cloud SQL**: instances with a public IP and no authorized-networks restriction, or missing `require_ssl`.
- **Service account key files**: long-lived JSON key files generated and potentially committed to source — see [cloud-credentials.md](../../secrets-detection/references/cloud-credentials.md); prefer workload identity federation where the platform supports it.

## False-Positive Conditions

- `allUsers`/`allAuthenticatedUsers` access is confirmed intentional for genuinely public content, scoped to specific objects/paths.

## Severity Notes

Public bucket with sensitive content, public Cloud SQL with no network restriction, or `Owner` role on an application service account: `critical`.
