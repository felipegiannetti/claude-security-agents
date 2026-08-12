# Encryption

**CWE-327** (broken/risky algorithm), **CWE-326** (inadequate strength)

## What to Look For

- Deprecated/broken algorithms: DES, 3DES, RC4, or a block cipher used in ECB mode (which leaks plaintext structure).
- Insufficient key length for the algorithm in use.
- Missing authentication on the ciphertext (encryption without a MAC, or a non-AEAD mode like CBC without a separate HMAC) — allows tampering with ciphertext undetected.
- Static/hardcoded IVs or nonces reused across encryptions with the same key, which breaks the security guarantees of most modes.

## False-Positive Conditions

- A modern AEAD cipher (AES-GCM, ChaCha20-Poly1305) is used with a properly random, non-reused nonce.
- The "encryption" is actually encoding (e.g. base64) never claimed or used as a security control — not a crypto finding, possibly a different finding if sensitive data is assumed protected when it isn't.

## Severity Notes

`high` for broken/deprecated algorithms or ECB mode on sensitive data; `medium` for missing authentication (CBC without MAC) where confidentiality still holds but integrity doesn't.
