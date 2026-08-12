# Password Reset

**CWE-640** (weak password recovery mechanism) · OWASP: Identification and Authentication Failures (A07:2021)

## What to Look For

- **Reset token strength and single-use.** Confirm the reset token is generated with a cryptographically secure random source (see [random-generation.md](../../cryptography-review/references/random-generation.md)), sufficiently long/high-entropy, and invalidated after first use.
- **Token expiration.** Confirm reset tokens expire in a short window.
- **No user enumeration via response differences.** Confirm the "forgot password" endpoint responds identically (timing and content) whether or not the submitted email/username exists — a differing response is a common, low-effort information leak.
- **Token delivery channel.** Confirm the token is sent only to the account's verified contact method, not returned in the API response or accepted as a client-supplied parameter alongside a new password.
- **Old sessions invalidated on reset.** Confirm a successful password reset invalidates existing sessions/tokens for that account (so a session hijacked before the reset doesn't survive it).
- **Rate limiting on both the request and confirm steps** — see [rate-limiting.md](../../api-security-review/references/rate-limiting.md).

## False-Positive Conditions

- The enumeration-differing response is intentional and accepted risk for a non-sensitive internal tool with no compliance requirement around it (still worth noting as a low-severity observation, but context matters — see `02_software_context_discovery`).
- Token generation uses a framework-provided secure token utility confirmed to use a CSPRNG.

## Severity Notes

Weak/predictable reset token: `critical` (direct account takeover). Missing single-use/expiration: `high`. User enumeration: `low` to `medium` depending on what else it enables (e.g. combined with credential stuffing). Sessions not invalidated on reset: `medium`.
