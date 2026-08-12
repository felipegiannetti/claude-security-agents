# NoSQL Injection

**CWE-943** · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data reaching a NoSQL query (MongoDB, etc.) in a form that lets it inject query *operators* rather than being treated purely as a data value — most commonly when a query filter is built directly from a parsed JSON request body without type/shape constraints, letting an attacker submit an object (e.g. `{"$ne": null}` or `{"$gt": ""}`) where a scalar was expected.

## Source-to-Sink Checklist

1. Confirm the query filter/document is built from request data — check whether the framework parses the body as JSON (making operator injection possible) vs. only form-encoded scalars.
2. Confirm there's no schema/type validation forcing the field to a scalar type before it reaches the query.
3. Check whether the query is a simple lookup (e.g. login/authentication check) where operator injection would let an attacker bypass a condition entirely — this is the highest-impact variant (authentication bypass).
4. For JavaScript-evaluating NoSQL features (e.g. `$where`, server-side JS execution), treat the same as [code-injection.md](code-injection.md) — the impact is code execution, not just query manipulation.

## False-Positive Conditions

- **Schema validation before query construction**: the framework or an explicit schema (e.g. a validation library) rejects non-scalar input for fields used in the query.
- **ODM/ORM-level type coercion**: the object-document mapper enforces field types before building the underlying query.
- **Query built from a fixed, code-defined structure** with only leaf scalar values substituted from user input (not user-controlled keys).

## Severity Notes

Default `high` per `config/severity.config.yaml`. Escalate toward `critical` when the affected query gates authentication or authorization (operator injection producing an auth bypass).
