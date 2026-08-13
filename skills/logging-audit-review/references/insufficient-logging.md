# Insufficient Security Logging

**CWE-778** (Insufficient Logging) · OWASP A09:2021 - Security Logging and Monitoring Failures

## What to Look For

Absence of logging for security-relevant events, specifically:

- **Authentication events**: successful login, failed login (with reason where safe to record -- see [sensitive-data-in-logs.md](sensitive-data-in-logs.md) for what NOT to include), logout, password change, MFA enrollment/challenge outcome.
- **Session events**: session creation, session termination, session ID regeneration.
- **Authorization events**: access denied (a 403/401 returned), privilege/role changes, permission grants -- especially time-bound grants and their expiration (see `skills/auth-authz-review/references/dormant-account-lifecycle.md`).
- **Privileged/administrative actions**: any action available only to elevated roles, and especially impersonation/"login as" features -- see [audit-trail-integrity.md](audit-trail-integrity.md).
- **Data export/bulk read operations**: especially of sensitive data categories.

For each, the minimum useful record includes: who (user/service identity), what (the action), when (timestamp), and from where (source IP / originating system).

## Evidence to Look For

- Authentication/session/authorization code paths with no corresponding log call on either the success or failure branch (or both).
- A logging framework/library present in dependencies (a positive signal) but not actually invoked at the security-relevant call sites that matter -- presence of a logging library is not the same as adequate coverage.

## False-Positive Conditions

- The event is logged, just through a mechanism not visible in the reviewed code (e.g. an API gateway or reverse proxy logs all requests including auth attempts) -- note this as "not confirmable from this codebase" per the same discipline as `skills/api-security-review/references/rate-limiting.md`, rather than asserting a confirmed gap.
- The application is genuinely low-sensitivity (per `02_software_context_discovery`) and the specific event has no realistic incident-response value.

## Severity Notes

Missing logging for authentication/authorization failures or privileged actions on a system handling sensitive data: `medium`. Missing logging is rarely `critical` or `high` on its own -- its real cost shows up during incident response, not as a directly exploitable vulnerability -- but it should still be raised as a `CONFIRMED` finding, not just an `ARCH-*` hardening note, when the gap is concrete and the system's context makes it matter (see `02_software_context_discovery`).