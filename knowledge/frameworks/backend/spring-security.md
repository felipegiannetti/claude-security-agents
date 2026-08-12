# Spring / Spring Boot Security

Shared knowledge consumed by [auth-authz-review](../../../skills/auth-authz-review/SKILL.md), [injection-review](../../../skills/injection-review/SKILL.md), and [api-security-review](../../../skills/api-security-review/SKILL.md) when Spring is detected.

## Default Protections (when Spring Security is present)

- Spring Security provides centralized authentication/authorization via `SecurityFilterChain` configuration — a strong signal against the "authorization scattered across controllers" smell (see [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md)), *if* the configuration actually covers every sensitive route. Read the `authorizeHttpRequests`/`antMatchers`/`requestMatchers` rules directly rather than assuming coverage.
- CSRF protection is enabled by default in Spring Security for browser-facing apps.
- Spring Data JPA's query-derivation and `@Query` with named/positional parameters are parameterized by default.

## Common Footguns

- **`@Query` with string concatenation** (`nativeQuery = true` combined with concatenated values, or SpEL injection via `@Query("... :#{#value} ...")` misuse) reintroduces [SQL injection](../../../skills/injection-review/references/sql-injection.md) despite using an ORM.
- **`permitAll()` misconfigurations** — a broad matcher pattern (e.g. `/api/**`) marked `permitAll()` ahead of a more specific authenticated rule can unintentionally expose routes; Spring Security matchers are evaluated in order, first match wins.
- **`@PreAuthorize`/`@Secured` only on some methods** — if authorization is enforced via method-level annotations rather than centralized filter-chain rules, confirm coverage is consistent (see the same architecture smell above) rather than assuming every sensitive method is annotated.
- **CSRF disabled for "API convenience"** (`csrf().disable()`) without confirming the API is actually not cookie-authenticated — see [csrf.md](../../../skills/web-security-review/references/csrf.md).
- **Actuator endpoints** (`/actuator/env`, `/actuator/heapdump`, etc.) exposed without authentication can leak configuration, secrets, and memory contents — confirm `management.endpoints.web.exposure` is scoped appropriately.

## Architecture Notes

Spring's convention-heavy structure (Controller/Service/Repository) maps naturally onto the technical-layering pattern in [layering-patterns.md](../../../skills/architecture-review/references/layering-patterns.md) — evaluate whether a `security/` concern (custom `UserDetailsService`, filters, `@PreAuthorize` expressions) is centralized or duplicated across controllers.
