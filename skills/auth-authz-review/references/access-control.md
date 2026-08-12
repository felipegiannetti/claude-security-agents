# Access Control

**CWE-862** (missing authorization), **CWE-863** (incorrect authorization) · OWASP: Broken Access Control (A01:2021)

This is the reference most directly shared with `api-security-review`'s [bola-idor.md](../../api-security-review/references/bola-idor.md) and [broken-function-authorization.md](../../api-security-review/references/broken-function-authorization.md) — this file covers the general access-control model; those cover the API-specific manifestations in more depth.

## What to Look For

- **Object-level authorization**: does the code verify the authenticated user is actually permitted to act on *this specific* resource (not just that they're authenticated and the resource exists)? The classic gap: `findById(request.params.id)` with no ownership/tenant check before returning or mutating the result.
- **Function-level authorization**: does the code verify the user's role/permission before executing a privileged action, independent of object-level checks? E.g. an "admin-only" endpoint that only checks the object belongs to *some* user, not that the caller has admin rights.
- **Where the check actually lives**: per `.claude/rules/security.md`'s Authorization Validation guidance, search beyond the immediately-flagged handler — middleware, guards/decorators, service-layer checks, and ORM/repository-level scoping (e.g. a repository method that always scopes queries to the current tenant) can all constitute a real, effective check even if the controller itself has none.
- **Default-deny vs. default-allow.** Confirm new routes/actions require an explicit authorization grant rather than being accessible unless explicitly restricted — a default-allow posture means every *new* endpoint is a potential gap.

## False-Positive Conditions

- A centralized authorization mechanism (middleware, policy engine, ORM-level tenant scoping) enforces the check outside the flagged code, and this was *confirmed* by reading that mechanism's actual code — not assumed from its existence elsewhere in the codebase.
- The resource is intentionally public/shared (e.g. a public content listing) and the "missing" check is actually correct behavior for that resource type.

## Severity Notes

Missing object-level check on a sensitive resource (financial, PII): `critical`. Missing object-level check on lower-sensitivity data: `high`. Missing function-level check gating a privileged action: `critical` to `high` depending on the action's impact.
