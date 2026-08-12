# Insecure File Download

**CWE-862**-adjacent (missing authorization on file serving)

## What to Look For

- **Missing authorization on file-serving endpoints**: confirm the same object-level authorization discipline as [bola-idor.md](../../api-security-review/references/bola-idor.md) applies to file downloads keyed by ID/filename — a common gap since file-serving code is often written as a generic utility without the same scrutiny as "real" endpoints.
- **Content-Disposition / Content-Type handling**: a file served with an attacker-influenced filename or without a safe `Content-Type`/`X-Content-Type-Options` can enable stored XSS-like effects if the browser renders it inline.

## False-Positive Conditions

- Download endpoint enforces the same ownership/authorization check as the equivalent read endpoint for that resource.

## Severity Notes

Unauthorized access to another user's/tenant's files: `high` to `critical` depending on data sensitivity.
