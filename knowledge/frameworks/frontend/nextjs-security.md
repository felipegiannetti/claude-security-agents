# Next.js Security

Extends [react-security.md](react-security.md) — Next.js inherits every React consideration plus server-side concerns from its hybrid rendering model.

## Framework-Specific Points

- **API Routes / Route Handlers** (`pages/api/*`, `app/**/route.ts`) are full backend endpoints — review them with the same rigor as any other server route (auth, authorization, injection, all of [api-security-review](../../../skills/api-security-review/SKILL.md)), not as "just frontend code."
- **Server Components / `getServerSideProps` / `getStaticProps`** run server-side and may have access to secrets/internal services unavailable to the client — confirm no client-exposed prop accidentally serializes a secret value into the page's initial HTML/JSON payload.
- **Middleware** (`middleware.ts`) is a common place authentication/authorization is centralized — a good sign per [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md), but verify it actually covers every sensitive route rather than being bypassable via a route not matched by its `matcher` config.
- **`NEXT_PUBLIC_*` env vars** are bundled into client JS, identical to Create React App's `REACT_APP_*` — never place a secret there.
- **Image Optimization API** (`/_next/image`) proxies and fetches remote images by URL — if `images.domains`/`remotePatterns` in `next.config.js` is misconfigured too broadly, this can become an [SSRF](../../../skills/web-security-review/references/ssrf.md) vector.
- **ISR/on-demand revalidation endpoints** often require a secret token — confirm it's actually checked and not just documented as a convention.

## Architecture Notes

Next.js blurs the frontend/backend boundary — when mapping architecture, explicitly identify which parts of a Next.js app are server-only (API routes, Server Components, Server Actions) vs. client-shipped, since the trust boundary runs through the framework itself rather than at a clean network edge.
