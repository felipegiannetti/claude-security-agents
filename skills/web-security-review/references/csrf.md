# Cross-Site Request Forgery (CSRF)

**CWE-352** · OWASP: (folded into Broken Access Control, A01:2021, in OWASP 2021)

## What to Look For

- **State-changing requests without a CSRF token** (or equivalent protection) on endpoints reachable via a browser with ambient credentials (cookies) — the risk is an attacker's page triggering a request the victim's browser authenticates automatically.
- **Token validation actually enforced**, not merely a token being present in the form/page — confirm the server rejects requests with a missing/incorrect token rather than only logging a warning.
- **`SameSite` cookie attribute** as a complementary/alternative mitigation — `SameSite=Lax` or `Strict` meaningfully reduces CSRF risk for cookie-authenticated requests; note its presence/absence alongside token-based protection, not instead of checking both.

## False-Positive Conditions

- **The endpoint doesn't rely on ambient credentials** — e.g. it requires a custom header or bearer token that a cross-origin form/script can't automatically attach (this is why many JSON APIs are inherently less CSRF-exposed than cookie-authenticated form endpoints, *if* they genuinely never accept the token via cookie as a fallback).
- **The action is read-only (GET, no state change)** — CSRF concerns apply to state-changing operations; a read-only endpoint that leaks data via CSRF is more accurately an authorization/information-disclosure issue, not classic CSRF.
- **Framework's built-in CSRF middleware is active and confirmed applied to this route** (not bypassed by an exemption/annotation).

## Severity Notes

Missing CSRF protection on a sensitive state-changing action (funds transfer, password/email change, privilege grant): `high`. On a low-impact action: `low` to `medium`.
