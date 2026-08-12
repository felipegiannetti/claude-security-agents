# Key Management

Complements [private-keys.md](../../secrets-detection/references/private-keys.md) (which covers detecting a *leaked* key) — this reference covers how keys should be handled through their lifecycle even when not leaked.

## What to Look For

- **Keys hardcoded rather than sourced from a secret manager/KMS** — see [secrets-detection](../../secrets-detection/SKILL.md) for detection; this reference is about the architectural expectation.
- **No key rotation mechanism** — a static key used indefinitely increases the impact window of any future compromise; note as a hardening observation (often better suited to `13_security_architecture_recommendations` than a standalone `SEC-*` finding unless a specific weakness is tied to it).
- **Same key used across environments** (development, staging, production sharing one encryption/signing key) — a compromise in a lower-security environment (e.g. a shared staging key with broader developer access) then compromises production data too.
- **Key used for multiple unrelated purposes** (e.g. the same key signs both session tokens and encrypts stored data) — violates key separation, widening the blast radius of any single key's compromise.

## False-Positive Conditions

- Keys are sourced from a dedicated secret manager/KMS with environment-specific isolation.
- Key rotation is confirmed implemented, even if this specific review can't verify rotation *frequency*.

## Severity Notes

Shared key across environments or across unrelated purposes: `medium` to `high` depending on what's exposed. Missing rotation alone: usually `low`/informational or an `ARCH-*` recommendation rather than a standalone finding.
