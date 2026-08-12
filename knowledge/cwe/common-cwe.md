# Common CWEs — Quick Reference

Short descriptions for the CWEs most frequently produced by this project, per [cwe-mapping.json](cwe-mapping.json). Not exhaustive — for anything not listed, use the CWE ID and name directly from [cwe-mapping.json](cwe-mapping.json) or https://cwe.mitre.org/.

| CWE | Name | Typical Skill |
|---|---|---|
| CWE-22 | Path Traversal | `file-security-review` |
| CWE-78 | OS Command Injection | `injection-review` |
| CWE-79 | Cross-Site Scripting | `web-security-review` |
| CWE-89 | SQL Injection | `injection-review` |
| CWE-90 | LDAP Injection | `injection-review` |
| CWE-94 | Code Injection | `injection-review` |
| CWE-200 | Information Exposure | multiple |
| CWE-213 | Exposure of Sensitive Information Due to Incompatible Policies (used here for excessive data exposure) | `api-security-review` |
| CWE-259 | Use of Hard-coded Password | `secrets-detection` |
| CWE-269 | Improper Privilege Management | `business-logic-review` |
| CWE-306 | Missing Authentication for Critical Function | `auth-authz-review` |
| CWE-308 | Use of Single-factor Authentication | `auth-authz-review` |
| CWE-321 | Use of Hard-coded Cryptographic Key | `secrets-detection`, `cryptography-review` |
| CWE-326 | Inadequate Encryption Strength | `cryptography-review` |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | `cryptography-review` |
| CWE-338 | Use of Cryptographically Weak PRNG | `cryptography-review` |
| CWE-347 | Improper Verification of Cryptographic Signature | `auth-authz-review` (JWT) |
| CWE-352 | Cross-Site Request Forgery | `web-security-review` |
| CWE-362 | Race Condition | `business-logic-review` |
| CWE-384 | Session Fixation | `auth-authz-review` |
| CWE-434 | Unrestricted Upload of File with Dangerous Type | `file-security-review` |
| CWE-502 | Deserialization of Untrusted Data | `business-logic-review` / `injection-review` |
| CWE-601 | URL Redirection to Untrusted Site (Open Redirect) | `web-security-review` |
| CWE-611 | Improper Restriction of XML External Entity Reference | `injection-review` |
| CWE-613 | Insufficient Session Expiration | `auth-authz-review` |
| CWE-640 | Weak Password Recovery Mechanism | `auth-authz-review` |
| CWE-643 | XPath Injection | `injection-review` |
| CWE-668 | Exposure of Resource to Wrong Sphere (tenant isolation) | `business-logic-review` |
| CWE-693 | Protection Mechanism Failure | `web-security-review` (headers) |
| CWE-770 | Allocation of Resources Without Limits (rate limiting) | `api-security-review` |
| CWE-798 | Use of Hard-coded Credentials | `secrets-detection` |
| CWE-841 | Improper Enforcement of Behavioral Workflow | `business-logic-review` |
| CWE-862 | Missing Authorization | `auth-authz-review`, `api-security-review` |
| CWE-863 | Incorrect Authorization | `auth-authz-review` |
| CWE-915 | Improperly Controlled Modification of Dynamically-Determined Object Attributes (mass assignment) | `api-security-review` |
| CWE-916 | Use of Password Hash With Insufficient Computational Effort | `cryptography-review` |
| CWE-918 | Server-Side Request Forgery | `web-security-review` |
| CWE-942 | Permissive Cross-domain Policy (CORS) | `web-security-review` |
| CWE-943 | Improper Neutralization of Special Elements in Data Query Logic (NoSQL injection) | `injection-review` |
| CWE-1021 | Improper Restriction of Rendered UI Layers (Clickjacking) | `web-security-review` |
| CWE-1104 | Use of Unmaintained Third Party Components | `dependency-cve-check` |
| CWE-1336 | Improper Neutralization of Special Elements Used in a Template Engine (SSTI) | `injection-review` |
