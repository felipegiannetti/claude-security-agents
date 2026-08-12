# Vue Security

Shared knowledge consumed by [web-security-review](../../../skills/web-security-review/SKILL.md) when Vue is detected.

## Default Protections

- Vue's template interpolation (`{{ value }}`) HTML-escapes by default, and `:attr="value"` bindings are escaped appropriately for their attribute context.

## Common Footguns

- **`v-html` directive** is Vue's explicit opt-out of auto-escaping (equivalent to React's `dangerouslySetInnerHTML`) — any attacker-influenced value bound via `v-html` is an [XSS](../../../skills/web-security-review/references/xss.md) candidate. Treat every occurrence as a mandatory review point.
- **Dynamic component rendering** (`<component :is="...">`) driven by user-influenced input can render unintended components if the value isn't constrained to a known-safe allowlist.
- **`v-bind:href`/`v-bind:src` from user input** — same `javascript:` URI risk as React; validate the scheme before binding.
- **`VUE_APP_*` (Vue CLI) / `VITE_*` (Vite) env vars** are compiled into the client bundle and are public — never place secrets there.
- **Server-Side Rendering (Nuxt/Vue SSR)** introduces the same server/client trust-boundary blurring as Next.js — API routes and server middleware in a Nuxt app are full backend code and need the same review depth as any other server endpoint.

## Architecture Notes

As with React/Angular, Vue provides no security boundary of its own — every access-control decision must be re-enforced server-side regardless of what client-side route guards or conditional rendering exist.
