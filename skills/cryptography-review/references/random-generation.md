# Random Generation

**CWE-338** (weak PRNG)

## What to Look For

A non-cryptographic pseudo-random number generator (e.g. a language's default `random`/`Math.random`-style function, or a seeded PRNG with a predictable seed like current time) used to generate a security-relevant value: session tokens, password-reset tokens (see [password-reset.md](../../auth-authz-review/references/password-reset.md)), API keys, CSRF tokens, or any value an attacker must not be able to predict or reproduce.

## False-Positive Conditions

- The random value has no security relevance (e.g. randomizing display order, sampling for analytics) — a weak PRNG is fine there.
- A cryptographically secure random source (CSPRNG) is confirmed in use — e.g. the language/platform's dedicated "secure random" API, not its general-purpose one.

## Severity Notes

`critical` for a predictable session/auth/reset token generator (directly enables account takeover via prediction); `low`/`informational` for weak randomness with no security relevance.
