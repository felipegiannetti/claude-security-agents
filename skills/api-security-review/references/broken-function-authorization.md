# Broken Function-Level Authorization

**CWE-862** · OWASP API5:2023

## What to Look For

An endpoint performing a privileged action (admin, internal, elevated-role) that doesn't verify the caller's role/permission independent of any object-level check. Common gap: an endpoint reuses a "user owns this object" check but never confirms the *action* itself requires elevated privilege (e.g. a "delete any user" admin endpoint that only checks the target user exists).

## False-Positive Conditions

- Role/permission check confirmed enforced centrally (middleware, guard, policy engine) and actually applied to this route.
- The action genuinely requires no elevated privilege.

## Severity Notes

`critical` to `high` depending on the privileged action's impact (data deletion, privilege grants, financial actions rank higher).
