# Data Flow Analysis

How to trace a value from source to sink and represent what was actually confirmed, per the model in CLAUDE.md's Core Design Principle:

```
SOURCE → PARSING → TRANSFORMATION → VALIDATION → AUTHENTICATION → AUTHORIZATION → BUSINESS LOGIC → SINK
```

Not every step applies to every finding — a stored XSS path may have no `AUTHENTICATION` step at all, for instance. Include only the steps that are actually relevant to the specific path, but don't skip a step that *is* relevant just because it's inconvenient to check.

## How to Trace

1. Start at the source. Identify the exact variable/field and where it's first read.
2. Follow it through the call chain: does it get reassigned, wrapped, parsed, concatenated with other data, passed as a parameter to another function?
3. At each hop, note whether validation, sanitization, encoding, or a type constraint is applied — and whether that operation actually changes whether the eventual sink is safe (e.g. HTML-escaping a value that's later used in a SQL query doesn't help).
4. Note where authentication/authorization checks occur in the call chain, if this path is behind one.
5. Stop at the sink and confirm the final form of the value matches what you traced — not what you assumed based on the variable name.

## Representing Confirmation Honestly

Each step in [finding.schema.json](../../../schemas/finding.schema.json)'s `data_flow` array has a `confirmed` boolean. Use it accurately:

- `confirmed: true` — you read the actual code at this step and verified the claim.
- `confirmed: false` — you're asserting this step based on framework knowledge, convention, or inference, not a direct read.

A finding with several `confirmed: false` steps isn't disqualified — but its `confidence` should reflect that, and it's a strong candidate for `07_data_flow_analysis` to resolve the specific gap rather than `08_security_triage` waving it through.

## Cross-File and Cross-Service Tracing

Data flow often crosses file boundaries (controller → service → repository) and sometimes service boundaries (an internal API call, a message queue). Use `Grep`/`Glob` to follow the value across files rather than assuming continuity. For cross-service flows, the architecture model's entry points and trust boundaries tell you whether the receiving side re-validates or implicitly trusts the caller — don't assume trust without evidence either way.

## When Tracing Stalls

If you can't find where a value goes after a certain point (dynamic dispatch, reflection, a call into a dependency you can't inspect), say so explicitly in the finding rather than guessing the sink is reached. This is exactly the kind of gap `NEEDS_MORE_EVIDENCE` exists for.
