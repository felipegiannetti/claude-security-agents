# Excessive Data Exposure

**CWE-213** · OWASP API3:2023

## What to Look For

An endpoint that serializes an entire internal object (including fields like password hashes, internal flags, other users' data, or fields not meant for this caller) and relies on the client to filter what it displays — rather than the server returning only the fields the caller should see. Common in APIs that serialize ORM entities directly.

## False-Positive Conditions

- A response DTO/serializer explicitly allowlists returned fields.
- The "extra" fields are genuinely non-sensitive (e.g. internal timestamps with no confidentiality value).

## Severity Notes

`high` when sensitive fields (credentials, tokens, other users' PII) are exposed; `low` to `medium` for non-sensitive internal metadata.
