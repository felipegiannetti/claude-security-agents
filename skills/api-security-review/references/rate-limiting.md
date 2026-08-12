# Rate Limiting / Resource Consumption

**CWE-770** · OWASP API4:2023

## What to Look For

Endpoints with no limit on request volume, payload size, or result-set size — particularly authentication (brute-force), password reset (see [password-reset.md](../../auth-authz-review/references/password-reset.md)), MFA code verification, and any endpoint performing expensive operations (search, export, report generation) on user-controlled parameters.

## False-Positive Conditions

- Rate limiting confirmed enforced at a gateway/reverse-proxy layer not visible in the application repository — note as "not confirmable from this codebase," recommend infrastructure-level verification rather than asserting a false positive or a confirmed finding either way.
- The endpoint is genuinely low-cost and not a plausible resource-exhaustion or brute-force target.

## Severity Notes

`high` on authentication/MFA/password-reset endpoints (enables brute-force); `medium` on expensive-operation endpoints; `low` elsewhere.
