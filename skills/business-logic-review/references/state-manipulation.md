# State Manipulation

**CWE-502**-adjacent (when the mechanism is deserialization) and general workflow-state tampering.

## What to Look For

- **Client-trusted state**: any value that represents application state (price, permission flag, workflow stage, quantity) accepted from the client and used without server-side re-derivation or validation — the general pattern behind [payment-security.md](payment-security.md)'s price-tampering case and [workflow-bypass.md](workflow-bypass.md)'s stage-skipping case.
- **Insecure deserialization of client-supplied state**: state passed as a serialized blob (a "cart token," a signed-but-not-verified state object, a serialized object in a hidden form field/cookie) that's deserialized without verifying integrity — if the deserializer can construct arbitrary types, this escalates to [code-injection.md](../../injection-review/references/code-injection.md)'s territory; if it's just data tampering, it's a business-logic integrity issue.
- **Client-side-only enforcement of state transitions** (disabled buttons, hidden form fields) with no server-side equivalent check.

## False-Positive Conditions

- State is either recomputed server-side from authoritative data, or transmitted in a form the server cryptographically verifies (signed/MACed) before trusting.
- The deserializer used is restricted to safe, schema-bound types incapable of arbitrary object construction.

## Severity Notes

`critical` when it enables code execution (insecure deserialization) or financial manipulation; `high` for other integrity-affecting state tampering.
