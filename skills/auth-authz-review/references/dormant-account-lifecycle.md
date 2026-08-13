# Dormant Account Lifecycle

**CWE-262** (Not Using Password Aging, adjacent) / **CWE-613** (Insufficient Session Expiration, conceptually related) -- no single CWE covers this precisely; it sits at the intersection of access control and account management.

## What to Look For

- **No automatic lockout for inactive accounts.** An account (especially a privileged one) that hasn't been used in a long time is a standing attack surface -- a former employee's still-active credentials, a service account nobody remembers, an admin account whose owner left. Check whether the application tracks last-login/last-activity and has any mechanism to flag or lock accounts that exceed a configurable inactivity threshold.
- **No expiration on time-bound permission grants.** A common real-world pattern: "grant this user temporary admin access for a migration" or "temporary coverage while a colleague is out" -- if the grant has no enforced expiration (or the expiration is advisory/documented only, not enforced in code), it silently becomes permanent. Look for permission/role assignment code and check whether an expiration field, if present in the data model, is actually checked at authorization time (not just displayed in an admin UI).
- **Reactivation with no identity re-verification.** If a locked/dormant account can be reactivated without re-confirming the requester is actually the legitimate account owner (e.g. a simple "unlock" button with no additional verification step), the lockout control is largely theater.

## Evidence to Look For

- A `lastLoginAt`/`lastActiveAt`-style field present in the user data model but never read by any scheduled job or authorization check.
- A `grantExpiresAt`/`validUntil`-style field on a role/permission assignment that's rendered in an admin UI (e.g. "expires: 2025-01-01") but not actually checked in the authorization code path -- the check only reads whether the assignment exists, not whether it's still valid.

## False-Positive Conditions

- Dormant-account detection and time-bound grant expiration are confirmed enforced by an external identity provider (e.g. corporate SSO/IdP account lifecycle policies) rather than the application itself -- note as "enforced upstream, not in this codebase" rather than a confirmed gap, and recommend confirming the upstream policy actually covers it.
- The application has no privileged/differentiated access model at all (every account has identical low-risk access), making dormant-account risk minimal.

## Severity Notes

Privileged accounts with no dormancy detection at all: `medium` -- real-world impact depends heavily on how many privileged accounts exist and how attractive they'd be as a target, which is a judgment call informed by `02_software_context_discovery`. A time-bound grant that's silently permanent: `medium`, escalating toward `high` if the elevated privilege in question is broad (e.g. admin) rather than narrow.