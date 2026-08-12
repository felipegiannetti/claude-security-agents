# OWASP Top 10 (2021) — Mapping Reference

Used to populate `finding.schema.json`'s `owasp_category` field. This is a categorization aid, not a review checklist — do not review "for the OWASP Top 10" as a goal in itself; review for real, evidenced vulnerabilities and map them to a category afterward where one applies clearly. Not every finding maps cleanly to exactly one category.

| Category | Covers (in this project) |
|---|---|
| A01:2021 – Broken Access Control | `broken-object-level-authorization`, `broken-function-level-authorization` — see `skills/auth-authz-review/references/access-control.md`, `skills/api-security-review/references/bola-idor.md` |
| A02:2021 – Cryptographic Failures | Weak encryption, weak hashing, insecure password storage, insecure random generation — see `skills/cryptography-review/` |
| A03:2021 – Injection | SQL/NoSQL/command/code/template/LDAP/XPath injection, XSS — see `skills/injection-review/`, `skills/web-security-review/references/xss.md` |
| A04:2021 – Insecure Design | Findings whose root cause is a missing security control by design, not an implementation bug — often overlaps with `skills/architecture-review/` recommendations, but a *specific exploitable instance* is still filed as a `SEC-*` finding here, not only as an `ARCH-*` recommendation |
| A05:2021 – Security Misconfiguration | CORS misconfiguration, missing security headers, IaC misconfiguration — see `skills/web-security-review/`, `skills/iac-misconfig-review/` |
| A06:2021 – Vulnerable and Outdated Components | Dependency CVEs — see `skills/dependency-cve-check/` |
| A07:2021 – Identification and Authentication Failures | JWT, OAuth/OIDC, session management, password reset, MFA — see `skills/auth-authz-review/` |
| A08:2021 – Software and Data Integrity Failures | Insecure deserialization, unsigned/unverified update or CI/CD artifact handling |
| A09:2021 – Security Logging and Monitoring Failures | Missing/insufficient logging of security-relevant events — typically an `ARCH-*` or low-severity hardening observation rather than a standalone critical finding |
| A10:2021 – Server-Side Request Forgery (SSRF) | See `skills/web-security-review/references/ssrf.md` |

See also [owasp-api-top10.md](owasp-api-top10.md) for API-specific categories that don't map cleanly onto the general Top 10 (e.g. mass assignment, excessive data exposure).
