# Hashing

**CWE-327**-adjacent (general-purpose hashing) — for password-specific hashing see [password-storage.md](password-storage.md), which has stricter requirements.

## What to Look For

- MD5 or SHA1 used where collision resistance matters (integrity checks, deduplication keys derived from sensitive content) — both are cryptographically broken for collision resistance, though still sometimes acceptable for non-security checksums (verify the actual use case before flagging).
- A general-purpose hash (SHA-256, etc.) used for *passwords* — this is a password-storage finding, not merely a "weak hash," since fast general-purpose hashes are unsuitable for password storage regardless of output size — see [password-storage.md](password-storage.md).

## False-Positive Conditions

- MD5/SHA1 used only for non-security purposes (cache keys, non-sensitive content deduplication, checksums against accidental corruption, not adversarial tampering).

## Severity Notes

`medium` for weak hashing used in a security-relevant integrity check; not a finding at all for genuinely non-security use — see [password-storage.md](password-storage.md) for the password case specifically (higher severity).
