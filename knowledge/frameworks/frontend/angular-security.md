# Angular Security

Shared knowledge consumed by [web-security-review](../../../skills/web-security-review/SKILL.md) when Angular is detected.

## Default Protections

- Angular's template binding (`{{ value }}`, `[property]="value"`) contextually auto-escapes based on where the value lands (HTML, attribute, URL, style) via its built-in sanitizer — stronger by default than a simple HTML-escape-everywhere approach.

## Common Footguns

- **`bypassSecurityTrust*` methods** (`bypassSecurityTrustHtml`, `bypassSecurityTrustUrl`, `bypassSecurityTrustResourceUrl`, etc.) are the explicit opt-out of Angular's sanitizer — any attacker-influenced value reaching one is an [XSS](../../../skills/web-security-review/references/xss.md) candidate. Treat every occurrence as a mandatory review point, same as React's `dangerouslySetInnerHTML`.
- **`[innerHTML]` binding** still runs through the sanitizer, but confirm the sanitizer hasn't been globally disabled or replaced with a custom no-op implementation.
- **HttpClient's built-in CSRF handling** (`XSRF-TOKEN` cookie / `X-XSRF-TOKEN` header) only works automatically for same-origin requests through Angular's `HttpClient` — confirm it's actually enabled and that no interceptor strips the header.
- **Route guards are client-side only** — same caveat as React Router: an Angular `CanActivate` guard is a UX control, not a substitute for server-side authorization.
- **`environment.ts` files** compiled into the client bundle are public, identical to React's env var footgun — never place secrets there.

## Architecture Notes

Angular's dependency-injection-heavy structure often centralizes HTTP calls through injectable services — a good pattern for centralizing security-relevant handling (auth token attachment, error handling) if actually done consistently; check whether every HTTP call genuinely goes through the shared service or whether some components bypass it with direct `fetch`/`XMLHttpRequest` calls that skip the centralized behavior.
