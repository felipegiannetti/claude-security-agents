# OWASP API Security Top 10 (2023) — Mapping Reference

Used alongside [owasp-top10.md](owasp-top10.md) for API-specific findings — see `skills/api-security-review/`.

| Category | Covers (in this project) |
|---|---|
| API1:2023 – Broken Object Level Authorization | See `skills/api-security-review/references/bola-idor.md` |
| API2:2023 – Broken Authentication | See `skills/auth-authz-review/` |
| API3:2023 – Broken Object Property Level Authorization | Excessive data exposure + mass assignment — see `skills/api-security-review/references/excessive-data-exposure.md`, `mass-assignment.md` |
| API4:2023 – Unrestricted Resource Consumption | Missing rate limiting / pagination limits — see `skills/api-security-review/references/rate-limiting.md` |
| API5:2023 – Broken Function Level Authorization | See `skills/api-security-review/references/broken-function-authorization.md` |
| API6:2023 – Unrestricted Access to Sensitive Business Flows | Often surfaces as a `business-logic-review` finding (e.g. workflow-bypass) rather than a pure API-layer issue — cross-reference both Skills |
| API7:2023 – Server Side Request Forgery | See `skills/web-security-review/references/ssrf.md` |
| API8:2023 – Security Misconfiguration | See `skills/web-security-review/`, `skills/iac-misconfig-review/` |
| API9:2023 – Improper Inventory Management | Undocumented/shadow API versions and endpoints — typically surfaces during `04_attack_surface_mapping` as a coverage gap rather than a single finding; escalate to an `ARCH-*` recommendation if systemic |
| API10:2023 – Unsafe Consumption of APIs | Applies the same source-sink discipline to data received *from* third-party APIs as to direct user input — a third-party API response is still an untrusted source unless proven otherwise |

See `skills/api-security-review/references/graphql-security.md` and `webhook-security.md` for protocol-specific concerns that cut across several of the categories above.
