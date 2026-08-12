# Unsafe File Upload

**CWE-434** · OWASP: Security Misconfiguration / Injection-adjacent

## What to Look For

- **Extension/type validation bypassable**: check based on client-supplied `Content-Type` or filename extension alone (both attacker-controlled) rather than actual file content — see [mime-validation.md](mime-validation.md).
- **Executable upload into a servable directory**: an uploaded file landing somewhere the web server will execute it (e.g. a `.php`/`.jsp`/`.aspx` file uploaded into a public web root).
- **No size limit**: enables resource-exhaustion via large uploads.
- **Filename used unsanitized**: see [path-traversal.md](path-traversal.md) — an attacker-controlled filename used to construct a storage path.

## False-Positive Conditions

- Uploaded files are stored outside any web-servable path and/or in object storage with no execute capability, regardless of extension.
- Content-based type validation (not just extension/`Content-Type` header) is confirmed applied.

## Severity Notes

Upload leading to remote code execution (executable landing in a servable path): `critical`. Upload bypassing type restrictions without RCE path: `medium` to `high` depending on what the restriction was protecting against.
