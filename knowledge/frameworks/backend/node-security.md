# Node.js / Express Security

Shared knowledge consumed by [web-security-review](../../../skills/web-security-review/SKILL.md) and [api-security-review](../../../skills/api-security-review/SKILL.md) when Express (or a similar minimal Node framework) is detected. See [nestjs-security.md](nestjs-security.md) for the more opinionated NestJS framework specifically.

## No Defaults By Default

Unlike Django/Spring, a bare Express app has essentially no security middleware unless explicitly added — this is the single most important framework-specific fact to check first: is `helmet` (security headers), CSRF protection, and rate limiting actually present, or is this a from-scratch implementation?

## Common Footguns

- **No built-in ORM parameterization** — if using a raw driver (`pg`, `mysql2`) directly rather than an ORM/query builder, string-concatenated queries are a direct [SQL injection](../../../skills/injection-review/references/sql-injection.md) risk with no framework safety net.
- **`child_process.exec()` vs. `execFile()`/`spawn()`** — `exec()` invokes a shell (command-injection risk if any argument is attacker-influenced, see [command-injection.md](../../../skills/injection-review/references/command-injection.md)); `execFile()`/`spawn()` with an argument array do not.
- **Prototype pollution** — merging attacker-controlled JSON into an object (`Object.assign`, lodash `merge`, a hand-rolled deep-merge) without guarding against `__proto__`/`constructor.prototype` keys can pollute the global `Object.prototype`, with effects ranging from denial-of-service to, in some code patterns, further exploitation.
- **`eval`/`new Function()`/`vm` module misuse** with attacker-influenced input — see [code-injection.md](../../../skills/injection-review/references/code-injection.md).
- **Missing `helmet()`** — no default security headers ([security-headers.md](../../../skills/web-security-review/references/security-headers.md)) unless explicitly added.
- **JWT verification without `algorithms` pinned** — a common `jsonwebtoken` library footgun, same as any JWT usage — see [jwt.md](../../../skills/auth-authz-review/references/jwt.md).

## Architecture Notes

Express's minimalism means architectural conventions (layering, centralized authorization) are entirely up to the team — check whether the codebase has actually adopted a consistent structure or whether each route handler reinvents its own patterns (a signal for [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md) "duplicated security logic").
