---
name: cryptography-review
description: Reviews cryptography usage - encryption, hashing, password storage, random number generation, and key management. Use when code encrypts, hashes, signs, or generates secrets/keys.
---

# Cryptography Review

Builds on [secure-code-review](../secure-code-review/SKILL.md). Cryptography findings are usually about *which primitive/mode/parameters* are used, not a source-sink trace — evidence here is mostly "what algorithm/library call is this" rather than "where does attacker data flow."

- [Encryption](references/encryption.md)
- [Hashing](references/hashing.md)
- [Password Storage](references/password-storage.md)
- [Random Generation](references/random-generation.md)
- [Key Management](references/key-management.md)

## Core Discipline

Don't flag "custom crypto" purely on sight — flag it when it's *doing* something a standard library already solves correctly (encryption, password hashing, token generation). Custom encoding/obfuscation that was never meant to be a security control is a different (and usually much lower-severity, if any) issue.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json).
