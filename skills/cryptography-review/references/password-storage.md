# Password Storage

**CWE-916** (insufficient computational effort)

## What to Look For

- Passwords hashed with a fast general-purpose hash (MD5, SHA-1, SHA-256/512 alone) instead of a purpose-built, computationally-expensive password hash (bcrypt, scrypt, Argon2id, or PBKDF2 with a high iteration count).
- Missing or reused salt — a per-password random salt is required even with a proper algorithm; without it, precomputed rainbow-table attacks become practical again.
- Passwords stored reversibly encrypted rather than hashed (encryption implies a decryption path exists — password verification never needs one).
- Insufficient work factor/cost parameter for the algorithm in use (e.g. bcrypt cost too low for current hardware).

## False-Positive Conditions

- A recognized password-hashing library/algorithm (bcrypt, Argon2id, scrypt, PBKDF2 with adequate iterations) is confirmed in use with per-password salting handled by the library (most modern libraries handle salting automatically — verify it isn't disabled).

## Severity Notes

`critical` for reversible encryption or a fast general-purpose hash with no salt; `high` for a proper algorithm with a clearly insufficient work factor.
