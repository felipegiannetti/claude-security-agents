# SQL Injection

**CWE-89** · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data (HTTP parameters, headers, body fields, or stored data that originated from user input) reaching a SQL query in a way that lets it alter the query's structure — not just its data values. Common sink shapes: string concatenation/formatting building a query string, an ORM's raw/native query escape hatch, dynamic construction of identifiers (table/column names) that can't be parameterized the normal way.

## Source-to-Sink Checklist

1. Identify the exact value and confirm it's attacker-influenced (not a server-generated ID or enum).
2. Confirm it reaches a query execution call — trace through any wrapper/repository functions.
3. Confirm the query is built by concatenation/formatting rather than parameter binding at that exact call site.
4. Confirm there's no intermediate validation that would constrain the value to a safe shape (e.g. strict integer parsing before use, when the value is meant to be numeric).

## False-Positive Conditions

- **Prepared statements / parameterized queries**: the value is passed as a bind parameter, not concatenated into the SQL string — even if the code *looks* similar to unsafe concatenation at a glance, check exactly how the value reaches the driver.
- **ORM parameterization**: the ORM's standard query builder methods (not its raw-SQL escape hatch) are used.
- **Safe dynamic identifiers**: when a table/column name must be dynamic, an allowlist of known-safe identifiers (not the raw value) determines what's actually used.
- **Value never reaches this code path**: dead code, disabled feature, unreachable branch.

## Severity Notes

Default `critical` per `config/severity.config.yaml` — actual severity may be lower if exploitation requires already-privileged access or the affected data is non-sensitive, but this is rare for SQL injection given how directly it typically maps to a critical technical impact (full read/write on the underlying data, and depending on the DB, potentially further access).
