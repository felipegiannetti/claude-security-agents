# Session Management

**CWE-384** (session fixation), **CWE-613** (insufficient expiration) · OWASP: Identification and Authentication Failures (A07:2021)

## What to Look For

- **Session ID regeneration on privilege change.** Confirm a new session ID is issued on login (and on privilege elevation, e.g. re-auth for a sensitive action) — reusing a pre-login session ID after authentication is session fixation.
- **Cookie attributes.** `HttpOnly` (prevents JS access, mitigates session-token theft via XSS), `Secure` (prevents transmission over plaintext HTTP), `SameSite` (mitigates CSRF-style session riding) — confirm all three are set on the session cookie.
- **Session expiration.** Both idle timeout and absolute maximum lifetime — confirm sessions don't persist indefinitely.
- **Logout invalidates server-side state.** Confirm logout actually invalidates the session server-side (not just clearing the client-side cookie), so a captured session token is invalidated too.
- **Concurrent session handling**, where relevant to the application's threat model (e.g. does changing a password invalidate other active sessions?).

## False-Positive Conditions

- Session cookie attributes are set by a framework's session middleware with secure defaults confirmed enabled (not just "the framework supports this").
- The application uses stateless tokens (e.g. short-lived JWTs) with a deliberate design that doesn't map directly to "session fixation" in the traditional sense — evaluate token-specific concerns via [jwt.md](jwt.md) instead.

## Severity Notes

Missing `HttpOnly`: `medium` (widens XSS impact to session theft). Missing `Secure` on an HTTPS-only app: `medium`. Session fixation (no regeneration on login): `high`. No server-side invalidation on logout: `medium` to `high` depending on how sensitive the session grants access to.
