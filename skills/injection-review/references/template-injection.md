# Server-Side Template Injection (SSTI)

**CWE-1336** · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data used as (or concatenated into) a *template string itself* — not just a value substituted into a template — before being rendered by a server-side template engine. This is distinct from XSS: SSTI means the attacker's input is interpreted as template syntax, which in many template engines allows arbitrary code execution, not just HTML injection.

## Source-to-Sink Checklist

1. Confirm the render call's *template* argument (not just its data/context argument) includes attacker-influenced content — e.g. a user-supplied string passed directly as the template to render, or string-built templates that embed user input into the template markup itself.
2. Confirm which template engine is in use and whether it's a "logic-less" engine (limited expression capability) or a full-featured one (often capable of arbitrary code execution via its expression syntax).
3. Distinguish from safe usage: passing user data as a *variable* into a pre-defined, code-authored template is normal and safe — the risk is specifically when user data becomes part of the template's own syntax.

## False-Positive Conditions

- **User input only ever populates template variables**, never the template string/markup itself.
- **Templates are entirely pre-defined and stored as static application assets**, with no user-influenced construction of template content.
- **A logic-less templating mode is enforced** that structurally cannot evaluate arbitrary expressions (verify this is actually the mode in use, not just theoretically available).

## Severity Notes

Default `critical` per `config/severity.config.yaml` when the template engine's expression language allows code execution (common); `high` if the engine is confirmed logic-less and impact is limited to information disclosure via template internals.
