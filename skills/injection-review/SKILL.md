---
name: injection-review
description: Reviews for injection vulnerabilities - SQL, NoSQL, command, code, template, LDAP, and XPath injection. Use when user input reaches a query, shell command, interpreter, or template engine.
---

# Injection Review

Builds on [secure-code-review](../secure-code-review/SKILL.md) — apply that Skill's source-sink and false-positive methodology to each category below rather than pattern-matching on syntax alone.

- [SQL Injection](references/sql-injection.md)
- [NoSQL Injection](references/nosql-injection.md)
- [Command Injection](references/command-injection.md)
- [Code Injection](references/code-injection.md)
- [Template Injection](references/template-injection.md)
- [LDAP / XPath Injection](references/ldap-xpath-injection.md)

## When to Use

Whenever the architecture model or attack surface map shows user input reaching a query engine, a shell/process execution call, a code evaluator (`eval`-family), a template renderer, or a directory/XML query interface — routed here per [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml).

## Shared Pattern Across All Injection Types

Every injection vulnerability is a case where attacker data and the *interpreter's control-plane* (the syntax that decides what the interpreter does, not just what data it processes) end up mixed in the same string/structure, and the interpreter can't tell the difference. The fix is always some form of keeping data and control-plane separated — parameterization, safe APIs, or strict allowlisting when parameterization isn't available (e.g. dynamic identifiers). Keep this unifying idea in mind: it's what makes "is this actually exploitable" tractable across very different-looking sinks (a SQL driver, a shell, a template engine).

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json). CWE and category should match the specific injection type (e.g. CWE-89 for SQL injection, CWE-78 for OS command injection) — see [knowledge/cwe/cwe-mapping.json](../../knowledge/cwe/cwe-mapping.json).
