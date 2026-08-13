---
name: auth-authz-review
description: Reviews authentication and authorization logic - JWT handling, OAuth/OIDC flows, session management, password reset, MFA, and access control. Use when code touches login, tokens, sessions, or permission checks.
---

# Auth & Authz Review

Builds on [secure-code-review](../secure-code-review/SKILL.md). Authentication (who are you) and authorization (what can you do) are distinct failure modes with distinct evidence requirements — don't conflate a missing authorization check with a missing authentication check.

- [JWT](references/jwt.md)
- [OAuth / OIDC](references/oauth-oidc.md)
- [Session Management](references/session-management.md)
- [Password Reset](references/password-reset.md)
- [MFA](references/mfa.md)
- [Access Control](references/access-control.md)
- [Dormant Account Lifecycle](references/dormant-account-lifecycle.md)
- [OAuth Account Linking](references/oauth-account-linking.md)
- [Brute-Force Protection](references/brute-force-protection.md)

## When to Use

Whenever the architecture model identifies an authentication mechanism, or the attack surface map flags an entry point touching login, session, token issuance/validation, password reset, MFA enrollment/verification, or any authorization-gated resource — routed here per [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml).

## Core Discipline

- **Authorization checks must be searched for beyond the immediate handler.** A missing check in a controller is not evidence of a vulnerability if a middleware, service-layer check, or ORM-level scoping enforces it elsewhere — see [access-control.md](references/access-control.md) and `agents/security-verifier.md`'s Authorization Validation.
- **"Authenticated" is not "authorized."** Confirm which specific check (if any) constrains *which* resources an authenticated user can act on, not just whether they're logged in.
- **Prefer framework/library mechanisms over custom implementations as the default-safe case** — but verify the framework mechanism is actually configured correctly (e.g. JWT signature verification actually enabled, not just present in the dependency tree).

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json). Common categories: `authentication-bypass`, `broken-object-level-authorization`, `broken-function-level-authorization`, `session-fixation`, `insecure-token-handling`, `dormant-account-abuse`, `oauth-account-linking-flaw`, `missing-brute-force-protection`.
