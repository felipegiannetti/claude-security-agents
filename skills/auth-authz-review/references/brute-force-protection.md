# Brute-Force / Automation Protection on Authentication

**CWE-307** (Improper Restriction of Excessive Authentication Attempts) · OWASP A07:2021 -- complements [rate-limiting.md](../../api-security-review/references/rate-limiting.md), which covers rate limiting generally; this reference is specifically about the authentication flow's own defenses.

## What to Look For

- **No progressive response to repeated failed login attempts.** After N failed attempts (a small, finite number), is there any escalation -- a CAPTCHA challenge, an increasing delay, a temporary account lock, or a step-up to MFA? A login endpoint that accepts unlimited attempts at full speed with no escalation is directly brute-forceable, especially against weak or leaked-and-reused passwords.
- **No protection on unauthenticated, automation-prone endpoints generally.** Beyond login specifically: signup, password-reset request (see `skills/auth-authz-review/references/password-reset.md`), and any public form submission endpoint are common automation/abuse targets (credential stuffing, fake account creation, resource exhaustion) and should have some combination of rate limiting and bot-mitigation (CAPTCHA or equivalent) proportionate to the endpoint's sensitivity.
- **Lockout that itself becomes a denial-of-service vector.** The inverse failure mode: if N failed attempts *permanently* locks the account with no self-service recovery, an attacker can lock out legitimate users just by attempting (and failing) logins with their usernames -- check that lockout is time-limited or has a safe self-service unlock path (e.g. via a verified email/MFA channel), not simply indefinite.

## Evidence to Look For

- A login handler with no attempt counter, no CAPTCHA integration, and no delay/backoff logic in the code path.
- A signup or password-reset-request endpoint with the same absence.

## False-Positive Conditions

- Rate limiting and/or CAPTCHA is confirmed enforced at an infrastructure layer (API gateway, WAF, reverse proxy) not visible in the application repository -- note as "not confirmable from this codebase," recommend infrastructure-level verification rather than asserting a confirmed gap, matching the discipline in `skills/api-security-review/references/rate-limiting.md`.
- The endpoint genuinely can't be abused at scale for a meaningful outcome (e.g. an internal-only tool behind a separately authenticated network boundary, per `02_software_context_discovery`).

## Severity Notes

No brute-force protection at all on the primary login endpoint: `high` -- directly enables credential-stuffing and password-guessing attacks at scale. Missing protection on signup/password-reset-request: `medium`. A lockout mechanism that itself enables denial-of-service against legitimate users: `medium`.