# MIME / Type Validation

Supports [file-upload.md](file-upload.md) — the specific question of whether an uploaded file's *claimed* type matches its *actual* content.

## What to Look For

- Validation relying solely on the client-supplied `Content-Type` header or file extension, both of which an attacker fully controls.
- Absence of content-based verification (e.g. checking file signature/magic bytes) for upload flows where type matters for downstream safety (e.g. only images should reach an image-processing pipeline).

## False-Positive Conditions

- Content-based validation (magic byte / library-based type sniffing) is confirmed applied, not just extension/header checks.

## Severity Notes

Usually a contributing factor to a file-upload finding rather than standalone — see [file-upload.md](file-upload.md) for severity in context.
