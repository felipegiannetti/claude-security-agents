# Audit Trail Integrity

**CWE-778** / **CWE-117** (Improper Output Neutralization for Logs) · OWASP A09:2021

## What to Look For

- **Impersonation / "login as" / support-access features with no distinct audit trail.** A feature that lets an administrator or support agent act as another user is a legitimate and common need, but every action taken while impersonating must be attributable to *both* the impersonator and the impersonated account -- a log showing only the impersonated user's ID makes the real actor unaccountable. This is one of the highest-value logging gaps to find, since impersonation features are inherently high-privilege and commonly under-audited.
- **Mutable/deletable audit logs.** If the application code (not just a database admin) can update or delete existing audit log entries through normal application logic, the audit trail can't be trusted during an investigation -- audit records should be append-only from the application's perspective.
- **Missing before/after values on data changes.** For changes to security-relevant records (permissions, roles, account status, financial data), logging only "record updated" without the old and new values makes it impossible to reconstruct what actually changed.
- **Log injection.** User-controlled input written into a log message without neutralizing newlines/control characters can let an attacker forge fake log entries (e.g. injecting a fake "login successful" line) -- check whether logged user input can contain raw newlines that survive into the log output.

## Evidence to Look For

- An impersonation/support-access code path where the log call (if any) only references `req.session.userId` (the impersonated identity) rather than also recording the original administrator's identity.
- Audit log write paths with a corresponding `UPDATE`/`DELETE` capability reachable from application code (not just from direct database access, which is a separate, infrastructure-level concern).
- Change-tracking code that logs a generic "updated" event without capturing the diff.

## False-Positive Conditions

- Impersonation logging is confirmed to record both identities (e.g. `actingAs: impersonatedUserId, actualUser: adminUserId`).
- Audit records are written to an append-only store (or a separate service/database the application has no update/delete access to) even if the primary data store does support updates.
- Logged user input is confirmed to pass through a structured logging library that safely encodes values (e.g. JSON-structured logging rather than raw string interpolation) -- structured logging inherently resists the log-injection pattern above.

## Severity Notes

Impersonation with no distinct audit trail: `high` -- this directly undermines accountability for a high-privilege feature. Mutable audit logs: `medium`. Missing before/after values: `low` to `medium` depending on the sensitivity of what's being changed. Log injection: `low` unless it can be chained into a more severe issue (e.g. forging entries to cover an actual intrusion).