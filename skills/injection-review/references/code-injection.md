# Code Injection

**CWE-94** · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data reaching a code evaluator — `eval`-family functions, dynamic `Function`/lambda construction from a string, dynamic module/class loading driven by user input, or deserialization of a format that can construct arbitrary objects/execute code on load (see also [insecure-deserialization](../../business-logic-review/references/state-manipulation.md) for the object-graph angle; this reference covers the injection angle specifically).

## Source-to-Sink Checklist

1. Confirm the evaluator genuinely executes the string/data as code (vs., e.g., a restricted expression-only evaluator with no side-effect capability).
2. Confirm attacker-influenced data reaches it, even partially — code injection often only needs to control a fragment of the evaluated expression, not the whole thing.
3. For deserialization-based code execution: confirm the deserializer used is one capable of instantiating arbitrary types/invoking constructors/callbacks from the serialized data (this varies significantly by language/library — check the specific one in use, don't assume).

## False-Positive Conditions

- **No user input reaches the evaluator at all** — the evaluated string/data is entirely code-defined.
- **A restricted/sandboxed evaluator** genuinely limits what can be expressed (verify the sandbox's actual guarantees — many "sandboxed" eval implementations have known escapes; don't take the label at face value without checking which specific mechanism is used).
- **Deserialization using a safe, schema-bound format/mode** (e.g. a deserializer restricted to a known safe type allowlist) rather than one that allows arbitrary type resolution.

## Severity Notes

Default `critical` per `config/severity.config.yaml` — code injection is remote code execution by definition.
