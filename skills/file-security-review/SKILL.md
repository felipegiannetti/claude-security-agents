---
name: file-security-review
description: Reviews file handling vulnerabilities - unsafe file upload, insecure download, path traversal, MIME/type validation, and storage security. Use when code accepts, serves, or stores user-supplied files.
---

# File Security Review

Builds on [secure-code-review](../secure-code-review/SKILL.md).

- [File Upload](references/file-upload.md)
- [File Download](references/file-download.md)
- [Path Traversal](references/path-traversal.md)
- [MIME Validation](references/mime-validation.md)
- [Storage Security](references/storage-security.md)

## When to Use

Any entry point handling file upload, download, or storage-by-user-supplied-name — routed here per [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml).

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json).
