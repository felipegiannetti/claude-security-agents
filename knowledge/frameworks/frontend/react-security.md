# React Security

Shared knowledge consumed by [web-security-review](../../../skills/web-security-review/SKILL.md) and [architecture-mapper](../../../agents/architecture-mapper.md) when React is detected.

## Default Protections

- JSX escapes interpolated values by default (`{value}`) — text is rendered as text, not parsed as markup. This is React's main built-in XSS mitigation.

## Common Footguns

- **`dangerouslySetInnerHTML`** — the explicit opt-out of auto-escaping. Any attacker-influenced value reaching it is a [stored/reflected XSS](../../../skills/web-security-review/references/xss.md) candidate. Treat every occurrence as a mandatory review point.
- **`href`/`src` built from user input** — React does not sanitize URLs; a `javascript:` URI in an attacker-controlled `href` executes on click. Validate the scheme (allowlist `http:`/`https:`) before use.
- **Client-side-only route guards** — a route "protected" only by React Router logic with no corresponding server-side authorization check on the underlying API is not a security control, only a UX one. See [access-control.md](../../../skills/auth-authz-review/references/access-control.md).
- **Secrets in client bundles** — anything in a `REACT_APP_*`/Vite `VITE_*`-prefixed env var is compiled into the shipped JS and is public. Treat as client-exposed, not secret — see [api-keys.md](../../../skills/secrets-detection/references/api-keys.md).
- **`useEffect` fetching based on URL params without validation** — client-side SSRF-adjacent risk is limited (runs in the user's own browser), but can still enable request forgery against internal-network-only APIs reachable from the user's machine in some deployment topologies.

## Architecture Notes

A React frontend has no security boundary of its own — every access-control decision must be re-enforced by the backend API it talks to. When mapping architecture, treat the React app itself as fully untrusted from the backend's perspective, regardless of what client-side checks exist.
