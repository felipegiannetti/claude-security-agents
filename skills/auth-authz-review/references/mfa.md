# Multi-Factor Authentication (MFA)

**CWE-308** (use of single-factor authentication where MFA is expected) and related · OWASP: Identification and Authentication Failures (A07:2021)

## What to Look For

- **MFA enforcement can't be skipped via a parameter or alternate flow.** Confirm there isn't a code path (e.g. a legacy login endpoint, an API-key-based flow, a "remember me" mechanism) that bypasses the MFA check that the primary flow enforces.
- **MFA is checked server-side as a gate**, not just as a UI step the client is expected to complete honestly — confirm the server tracks "MFA satisfied" as part of session state and enforces it before granting access to protected resources.
- **Second factor is actually verified**, not merely "requested" — e.g. a TOTP code is checked against the server-computed value, not compared to a client-asserted "verified: true" flag.
- **Backup/recovery codes** are single-use, sufficiently random, and don't reduce the effective security below the primary factor.
- **Brute-force protection on the MFA code itself** — a 6-digit TOTP code has limited entropy; confirm rate limiting/lockout on repeated failed attempts.

## False-Positive Conditions

- MFA state is enforced through a well-tested, centrally-applied session/middleware check rather than scattered per-endpoint checks (still worth confirming coverage, but a centralized mechanism is inherently lower-risk than per-endpoint duplication — see `skills/architecture-review/references/security-architecture-smells.md`).

## Severity Notes

A discoverable MFA bypass path: `critical` (defeats the purpose of the control entirely). Missing rate limiting on code verification: `high` (makes brute-forcing a 6-digit code practical). Weak backup code generation: `high`.
