---
name: web-security-review
description: Reviews common web vulnerabilities - XSS, CSRF, CORS misconfiguration, SSRF, open redirect, clickjacking, and missing security headers. Use when reviewing web-facing request/response handling.
---

# Web Security Review

Builds on [secure-code-review](../secure-code-review/SKILL.md).

- [XSS](references/xss.md)
- [CSRF](references/csrf.md)
- [CORS](references/cors.md)
- [SSRF](references/ssrf.md)
- [Open Redirect](references/open-redirect.md)
- [Clickjacking](references/clickjacking.md)
- [Security Headers](references/security-headers.md)

## When to Use

Whenever the attack surface map includes browser-facing entry points (HTML rendering, redirects, CORS-enabled APIs) or server-side request-making functionality (webhooks, URL fetchers, image/link previews) — routed here per [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml).

## Core Discipline

- These categories vary enormously in impact — a missing `X-Frame-Options` header (clickjacking) and an unrestricted SSRF against internal infrastructure are both "web security" findings but not remotely the same severity. Assess actual reachable impact per category, don't apply a single template severity.
- Several of these (CSRF, clickjacking, most headers) are mitigated by *absence of an attack surface* just as validly as by an explicit control — e.g. an API that only accepts `application/json` and never `application/x-www-form-urlencoded` has a structurally different CSRF risk profile than one that doesn't. Note this context rather than flagging every missing header uniformly.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json). Common categories: `stored-xss`, `reflected-xss`, `dom-xss`, `csrf`, `ssrf`, `open-redirect`, `clickjacking`, `cors-misconfiguration`, `missing-security-headers`.
