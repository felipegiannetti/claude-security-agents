# Storage Security

Covers where uploaded/generated files end up, complementing [file-upload.md](file-upload.md) (the intake side).

## What to Look For

- **Public-by-default object storage**: files stored in a cloud bucket/container with public read access when they shouldn't be — check bucket/container-level configuration (often visible in IaC, see [iac-misconfig-review](../../iac-misconfig-review/SKILL.md)) as well as per-object ACLs set at upload time.
- **Predictable storage keys**: sequential or guessable object keys/filenames enabling enumeration of other users' files even without a direct authorization bypass.
- **No server-side encryption** for sensitive stored content, where the software context (see `02_software_context_discovery`) indicates that matters (compliance requirements, sensitive data categories).

## False-Positive Conditions

- Storage is confirmed private-by-default with access mediated only through the application's own authorization-checked download endpoint.
- Storage keys are non-guessable (UUIDs or equivalent) even if the bucket itself isn't fully private, meaningfully raising the bar for enumeration.

## Severity Notes

Public bucket containing sensitive user files: `critical`. Predictable keys without public access: `medium` (still requires bypassing the application's auth to matter, but materially weakens defense-in-depth).
