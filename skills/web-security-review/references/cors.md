# CORS Misconfiguration

**CWE-942** · OWASP: Security Misconfiguration (A05:2021)

## What to Look For

- **Reflected `Access-Control-Allow-Origin`**: the server echoes back whatever `Origin` header the request sent, effectively allowing any origin — especially dangerous when combined with `Access-Control-Allow-Credentials: true`, which permits credentialed cross-origin requests from any site.
- **Wildcard origin with credentials**: `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` is invalid per spec in browsers, but check for the reflected-origin variant above, which achieves the same effect and *does* work.
- **Overly broad allowlist**: an allowlist that includes wildcarded subdomains or patterns broader than actually needed (e.g. matching via a loose regex that unintentionally matches attacker-registerable domains).
- **Preflight bypass assumptions**: confirm sensitive actions aren't reachable via "simple requests" (which skip preflight) in a way that defeats an otherwise-correct CORS policy.

## False-Positive Conditions

- The allowlist is a fixed, explicit list of trusted origins with no reflection and no wildcard/credentials combination risk.
- The endpoint returns no sensitive data and performs no state change, making CORS exposure low-impact even if the policy is loose (still worth noting, but proportionate severity).

## Severity Notes

Reflected origin + credentials allowed on an endpoint returning sensitive data: `critical` (effectively bypasses same-origin policy for authenticated data). Reflected origin without credentials: `medium` to `high` depending on data sensitivity. Overly broad but non-reflected allowlist: `low` to `medium`.
