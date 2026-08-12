# Privilege Escalation

**CWE-269**

## What to Look For

- **Horizontal**: acting as another user of equal privilege — largely covered by [bola-idor.md](../../api-security-review/references/bola-idor.md); noted here for the business-logic angle when it happens through a workflow rather than a direct object reference (e.g. an "invite a teammate" flow that lets the inviter also set the invitee's *own* future permissions beyond what the inviter has).
- **Vertical**: acting with higher privilege than granted — a user-editable profile/settings endpoint that also accepts a `role` field (see [mass-assignment.md](../../api-security-review/references/mass-assignment.md)), or a self-service account-upgrade flow that doesn't validate the upgrade path server-side (e.g. skipping a payment or approval step to reach "premium"/"admin" status).
- **Privilege retained after revocation**: a session/token that still carries elevated privilege after the underlying role was revoked, because privilege is cached at login time and never re-checked.

## False-Positive Conditions

- Role/permission fields are never client-settable, and role changes only happen through a separate, properly-authorized administrative path.
- Privilege is re-checked per-request (or the session is invalidated on role change) rather than cached indefinitely.

## Severity Notes

`critical` for a path to admin/privileged role without proper authorization; `high` for horizontal escalation depending on data sensitivity.
