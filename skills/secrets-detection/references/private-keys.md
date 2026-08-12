# Private Keys

**CWE-321** (hardcoded cryptographic key)

## What to Look For

PEM-format private keys (SSH, TLS/SSL, code-signing, JWT-signing) committed to the repository — often recognizable by the `-----BEGIN ... PRIVATE KEY-----` header even when the surrounding file isn't named suggestively.

## Category-Specific Notes

- Distinguish a key that's actually in use from one that's clearly a test/example fixture (e.g. a well-known publicly-documented test key used by a library's own test suite) — see [key-management.md](../../cryptography-review/references/key-management.md) for the broader key-lifecycle context.
- A leaked JWT-signing private key is especially severe: it typically enables forging arbitrary authenticated tokens, not just impersonating one service.

## Severity Notes

`critical`, essentially without exception, for any private key confirmed to be in active use.
