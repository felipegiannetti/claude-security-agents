# LDAP / XPath Injection

**CWE-90** (LDAP) **/ CWE-643** (XPath) · OWASP: Injection (A03:2021)

## What to Look For

Attacker-influenced data reaching an LDAP filter or an XPath query in a form that lets it alter the filter/query's logical structure — the same underlying pattern as SQL injection, applied to directory-query and XML-query languages respectively. Common in authentication flows that query a directory service (LDAP) or systems parsing/querying XML documents/config with user-influenced XPath expressions.

## Source-to-Sink Checklist

**LDAP:**
1. Confirm the value reaches a filter string built by concatenation rather than through the LDAP library's parameterized/escaped filter construction API.
2. Check specifically whether this filter is used for an authentication or authorization decision — LDAP injection in an auth filter (e.g. `(&(uid=<input>)(password=<input>))`) can produce an authentication bypass, not just a filter-logic anomaly.

**XPath:**
1. Confirm the value reaches an XPath expression string built by concatenation rather than a parameterized XPath API (where the underlying library supports one).
2. Check what the query controls — authentication/authorization decisions against an XML-based user store, or data retrieval where an attacker could widen the query to access unauthorized nodes.

## False-Positive Conditions

- **Parameterized/escaped filter or query construction** is used (most modern LDAP and XPath libraries offer an escaping or parameter-binding API — check whether the specific call site uses it).
- **Strict allowlist validation** constrains the value before it's used (e.g. validating a username against an expected character set before building the filter).
- **The filter/query is entirely code-defined**, with user input never reaching the filter/query string.

## Severity Notes

Default `high` per `config/severity.config.yaml`; escalate to `critical` when the injected filter/query gates authentication or authorization.
