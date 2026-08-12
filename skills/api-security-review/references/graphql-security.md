# GraphQL Security

Multiple OWASP API categories apply to GraphQL through a different shape than REST.

## What to Look For

- **Field-level authorization**: GraphQL's flexible querying means authorization must be checked per-field/per-resolver, not just per-endpoint — a single GraphQL endpoint can expose many different access-control surfaces. See [access-control.md](../../auth-authz-review/references/access-control.md).
- **Query depth/complexity limits**: absence enables resource-exhaustion via deeply nested or highly-repeated queries — a GraphQL-specific form of [rate-limiting.md](rate-limiting.md)'s concern.
- **Introspection enabled in production**: not a vulnerability by itself, but expands attacker reconnaissance of the full schema, including unused/internal fields.
- **Batching abuse**: query batching used to bypass per-request rate limits.

## False-Positive Conditions

- Field-level authorization confirmed enforced via a directive/middleware applied consistently across resolvers.
- Query complexity analysis/depth limiting is confirmed configured.

## Severity Notes

Missing field-level authorization on a sensitive resolver: same severity as the equivalent REST finding (`bola-idor.md`/`broken-function-authorization.md`). Missing depth/complexity limits: `medium`.
