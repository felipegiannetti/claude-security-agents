# OAuth / OIDC

**CWE-352-adjacent (CSRF on the flow), CWE-601 (open redirect on callback)** · OWASP: Identification and Authentication Failures (A07:2021)

## What to Look For

- **`state` parameter usage (OAuth).** Confirm a `state` value is generated, stored server-side (or signed), and validated on callback — its absence enables CSRF against the OAuth flow (an attacker can bind their own OAuth session to the victim's account).
- **`redirect_uri` / callback validation.** Confirm the redirect URI is validated against a strict allowlist by the authorization server and, on the client side, that the callback handler doesn't blindly redirect based on a request parameter — see [open-redirect.md](../../web-security-review/references/open-redirect.md).
- **ID token validation (OIDC).** Same signature/claim checks as [jwt.md](jwt.md), plus: `nonce` validated to bind the ID token to the specific auth request (prevents replay).
- **PKCE for public clients.** Confirm public clients (SPAs, mobile) use PKCE (`code_verifier`/`code_challenge`) — its absence allows authorization code interception attacks.
- **Token storage after exchange.** Where the resulting access/refresh token is stored client-side, check for the same concerns as [session-management.md](session-management.md).
- **Scope handling.** Confirm the application doesn't grant broader access than the scopes actually returned/consented to.

## False-Positive Conditions

- `state`/`nonce` generation and validation are handled by a well-maintained OAuth/OIDC client library with the relevant checks confirmed enabled.
- The application is a confidential client (server-side, with a client secret) where PKCE is defense-in-depth rather than a hard requirement — still recommended, but its absence alone is lower severity than for a public client.

## Severity Notes

Missing `state` validation: `high` (CSRF-class impact on account linking/login). Missing `redirect_uri` allowlisting: `high` to `critical` depending on whether it enables authorization code/token leakage to an attacker-controlled endpoint. Missing PKCE on a public client: `high`.
