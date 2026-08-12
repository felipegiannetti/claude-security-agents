# BOLA / IDOR (Broken Object Level Authorization)

**CWE-862** · OWASP API1:2023

## What to Look For

An endpoint that accepts an object identifier (path param, query param, body field) and returns/mutates that object without verifying the caller is authorized for *that specific object* — not just that the object exists. See [access-control.md](../../auth-authz-review/references/access-control.md) for the general model.

## False-Positive Conditions

- Ownership/tenant check confirmed present in middleware, service layer, or ORM-level scoping — search beyond the handler itself.
- The resource is intentionally public.

## Severity Notes

`critical` on sensitive data (financial, PII); `high` otherwise.
