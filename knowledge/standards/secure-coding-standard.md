# Secure Coding Standard

Cross-cutting principles referenced by multiple Skills, so they're defined once here rather than repeated. This is not a vulnerability checklist — see `skills/` for category-specific methodology. This is the shared baseline those Skills assume.

## Input Handling

- Validate at trust boundaries (see `architecture.schema.json`'s `trust_boundaries`), not deep inside business logic where the origin of a value has already been lost.
- Prefer allowlisting (accept known-good shapes/values) over blocklisting (reject known-bad patterns) wherever the valid input space is enumerable.
- Validation and encoding are not interchangeable: validation constrains *what* a value can be; encoding controls how it's *interpreted* in a specific output context (HTML, SQL, shell, URL). A value can be validated and still need context-specific encoding at its actual sink.

## Separation of Data and Control Plane

The unifying idea behind every injection category (see `skills/injection-review/SKILL.md`): keep attacker-influenced data and the interpreter's control syntax structurally separate — parameterized queries, argument-array process execution, template variables (not template markup) — rather than trying to sanitize a mixed string after the fact.

## Least Privilege

Every component, service account, and database credential should hold only the access its actual function requires. This is both a per-finding concern (e.g. is a service account's database role broader than necessary) and an architectural one (see `skills/architecture-review/references/security-architecture-smells.md` "Services/Components With Overly Broad Privileges").

## Fail Closed

On an error in a security-relevant check (a validation exception, an authorization lookup failure, a signature verification error), the default behavior must be to deny, not to proceed. Code that catches an authorization check's exception and continues as if authorized is a fail-open bug regardless of how rare the exception is expected to be.

## Defense in Depth, Not Defense in Only One Layer

A control at one layer (e.g. frontend validation) is a UX improvement, not a security control, unless the same constraint is also enforced server-side. Don't credit a finding as mitigated because a client-side check exists — see `skills/architecture-review/references/security-architecture-smells.md` "Excessive Trust in Frontend-Supplied Data."

## Secrets Never in Source

Credentials, API keys, and private keys belong in a secret manager or environment configuration outside version control — never hardcoded, even temporarily, even in a comment marked `# TODO remove before commit`. See `skills/secrets-detection/SKILL.md`.

## Errors Don't Leak Internals

Error responses to untrusted callers should not include stack traces, internal file paths, query fragments, or dependency version strings that aid reconnaissance — log the detail server-side, return a generic message externally.

When recommending an application-facing error message (in remediation guidance, or when a finding's fix involves changing what an error response reveals), prefer a structured, three-part pattern over a bare generic string: **Error Detected** (what failed, in user-facing terms) + **Probable Cause** (a category, not internal detail -- e.g. "invalid input format", not the regex that rejected it) + **Suggested Action** (what the caller should do next). This gives callers and support teams enough to act on without leaking internals a generic "An error occurred" would also hide -- it is a usability improvement over a bare generic string, not a security control on its own, and never a substitute for the fail-closed and no-internal-detail rules above.
