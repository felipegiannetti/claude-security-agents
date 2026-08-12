# Security Headers

**CWE-693** (protection mechanism failure, general) · OWASP: Security Misconfiguration (A05:2021)

## What to Look For

Presence and correctness of response headers that provide browser-enforced defense-in-depth. None of these are usually a critical finding on their own — treat this reference as a checklist for the *hardening* end of the report, not a source of inflated critical findings.

- **`Content-Security-Policy`**: reduces XSS impact; check for `unsafe-inline`/`unsafe-eval` in `script-src`, which substantially weakens it.
- **`Strict-Transport-Security`**: enforces HTTPS on subsequent visits; relevant only if the app is HTTPS-only (which it should be).
- **`X-Content-Type-Options: nosniff`**: prevents MIME-sniffing-based attacks.
- **`X-Frame-Options` / `frame-ancestors`**: see [clickjacking.md](clickjacking.md).
- **`Referrer-Policy`**: controls whether sensitive URL data leaks via the `Referer` header on outbound navigation/requests.
- **`Set-Cookie` attributes**: see [session-management.md](../../auth-authz-review/references/session-management.md) — related but tracked separately since it's finding-specific, not a general response header.

## False-Positive Conditions

- Headers are set by a CDN/reverse-proxy layer not visible in the application repository — note this as "not confirmable from this codebase" rather than a confirmed missing-header finding; recommend infrastructure-level verification instead of a false claim.
- The specific header genuinely doesn't apply to the response type (e.g. `X-Frame-Options` on a pure JSON API response is not meaningful).

## Severity Notes

Default `low` per `config/severity.config.yaml` for any single missing header. Aggregate/report as hardening recommendations (P4-adjacent) rather than individually escalated findings, unless a specific header's absence is a direct enabler of another confirmed finding (e.g. missing CSP contributing materially to a confirmed XSS's impact) — see `13_security_architecture_recommendations` for infrastructure-level hardening items that don't fit cleanly as per-finding items.
