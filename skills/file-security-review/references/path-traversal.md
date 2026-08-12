# Path Traversal

**CWE-22** · OWASP: Broken Access Control (A01:2021)

## What to Look For

Attacker-influenced data (filename, path parameter) used to construct a filesystem path without normalizing/constraining it — allowing `../` sequences (or absolute paths, or encoded variants) to escape the intended directory and reach arbitrary files.

## Source-to-Sink Checklist

1. Confirm the value reaches a filesystem read/write/delete call.
2. Confirm there's no normalization + prefix-check (resolve the path, then verify it's still within the intended base directory) before use.
3. Check for encoding-based bypasses if a naive string-based `../` filter exists (URL-encoded, double-encoded, or OS-specific separators).

## False-Positive Conditions

- The value is resolved to an absolute path and validated to remain within an allowed base directory *after* resolution (not just string-matched before).
- The value is constrained to a safe, non-path-like format before use (e.g. a UUID looked up in a database rather than used directly as a path).

## Severity Notes

`critical` when write/delete is reachable or when readable files include credentials/config; `high` for read-only traversal to less sensitive files.
