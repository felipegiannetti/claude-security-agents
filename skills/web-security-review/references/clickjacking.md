# Clickjacking

**CWE-1021** · OWASP: Security Misconfiguration (A05:2021)

## What to Look For

Absence of framing protection (`X-Frame-Options` and/or a `Content-Security-Policy: frame-ancestors` directive) on pages that perform sensitive state-changing actions — an attacker can embed the page in an invisible iframe on their own site and trick a victim into clicking through to trigger an action they didn't intend.

## What Actually Matters

Not every page needs framing protection — this is a case where a uniform "every page needs `X-Frame-Options`" scan produces low-signal noise. Focus on pages that perform a state-changing action reachable via a simple click (a settings toggle, a one-click purchase/confirm button, an account-linking confirmation) with the user already authenticated. A read-only content page has essentially no clickjacking exposure.

## False-Positive Conditions

- The page/action requires more than a single click plus already-authenticated session (e.g. requires re-entering a password) — clickjacking primarily threatens single-click, ambient-session-authenticated actions.
- Framing protection is applied globally via a framework default or reverse-proxy/CDN configuration (confirm it's actually active, not just configured in application code that might be overridden downstream).

## Severity Notes

Missing framing protection on a genuinely single-click, sensitive, state-changing page: `medium`. On a read-only or non-sensitive page: `low`/`informational`.
