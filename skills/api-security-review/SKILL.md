---
name: api-security-review
description: Reviews API-specific vulnerabilities - BOLA/IDOR, broken function-level authorization, mass assignment, rate limiting, excessive data exposure, GraphQL security, and webhook security. Use when reviewing REST/GraphQL API endpoints.
---

# API Security Review

Builds on [secure-code-review](../secure-code-review/SKILL.md) and [access-control.md](../auth-authz-review/references/access-control.md) — most API vulnerabilities are access-control failures at the object or function level. See [knowledge/owasp/owasp-api-top10.md](../../knowledge/owasp/owasp-api-top10.md) for category mapping.

- [BOLA / IDOR](references/bola-idor.md)
- [Broken Function-Level Authorization](references/broken-function-authorization.md)
- [Mass Assignment](references/mass-assignment.md)
- [Rate Limiting](references/rate-limiting.md)
- [Excessive Data Exposure](references/excessive-data-exposure.md)
- [GraphQL Security](references/graphql-security.md)
- [Webhook Security](references/webhook-security.md)

## When to Use

Any REST or GraphQL endpoint from the attack surface map — routed here per [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml).

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json).
