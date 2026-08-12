# Mass Assignment

**CWE-915** · OWASP API3:2023

## What to Look For

A request body deserialized/bound directly onto an internal model/entity without an explicit allowlist of settable fields — letting an attacker set fields they shouldn't control (e.g. `role: "admin"`, `isVerified: true`, `accountBalance`) simply by including them in the request body, even though the UI never exposes those fields.

## False-Positive Conditions

- A DTO/input-schema layer explicitly allowlists bindable fields (the entity itself is never directly bound to request input).
- The framework's binding mechanism is confirmed configured with an explicit allowlist/denylist for sensitive fields.

## Severity Notes

`critical` when a privilege or financial field is assignable this way; `medium` to `high` for other unintended field exposure.
