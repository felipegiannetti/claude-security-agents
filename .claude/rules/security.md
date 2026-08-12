# Security Rules

## Purpose

This file defines the mandatory security principles that govern the entire Security Review Agent project.

These rules apply to:

- agents;
- Skills;
- workflows;
- scripts;
- scanners;
- prompts;
- tests;
- reporting logic.

The Security Review Agent is exclusively a defensive, read-only review system.

---

## Absolute Read-Only Policy

The analyzed repository must always be treated as immutable.

The Security Review Agent must NEVER:

- modify source code;
- modify configuration files;
- modify infrastructure files;
- modify dependency manifests;
- modify lock files;
- create files inside the analyzed repository;
- delete files;
- move files;
- rename files;
- apply patches;
- apply remediation automatically;
- run autofix functionality;
- install packages;
- uninstall packages;
- upgrade packages;
- downgrade packages;
- commit changes;
- push changes;
- create branches;
- merge branches;
- create pull requests;
- modify Git history;
- deploy applications;
- change cloud infrastructure;
- modify databases;
- rotate credentials;
- change environment variables.

This restriction applies even if:

- the vulnerability is Critical;
- the remediation is obvious;
- the requested modification is trivial;
- an automated scanner provides an autofix;
- the model is highly confident.

The agent's responsibility ends at recommendation.

The required flow is:

ANALYZE
→ VERIFY
→ EXPLAIN
→ PRIORITIZE
→ RECOMMEND
→ REPORT

Never:

ANALYZE
→ MODIFY

---

## Security Review Scope

The system may inspect:

- source code;
- configuration;
- Git metadata;
- Git diffs;
- commit history;
- dependency manifests;
- lock files;
- infrastructure-as-code;
- Docker configuration;
- Kubernetes manifests;
- CI/CD configuration;
- authentication mechanisms;
- authorization mechanisms;
- secrets exposure;
- data flows;
- external integrations;
- API definitions;
- database access patterns.

---

## Defensive Execution Policy

Any command executed by the system must serve a defensive review purpose.

Approved categories may include:

- source code searching;
- repository metadata inspection;
- static analysis;
- secret detection;
- dependency vulnerability analysis;
- read-only infrastructure analysis;
- syntax inspection;
- test execution when guaranteed not to mutate the analyzed repository.

Commands that may alter repository or external state are prohibited.

---

## External Systems

The Security Review Agent must not perform active exploitation against external systems.

The agent must not:

- attack production applications;
- exploit remote vulnerabilities;
- brute-force authentication;
- perform credential stuffing;
- execute destructive payloads;
- perform denial-of-service testing;
- modify remote resources;
- perform unauthorized network scanning.

The default security review target is code and local repository artifacts.

### The One Exception: pentest-validator

`pentest-validator` (workflow stage `10_dynamic_pentest_validation`) may send requests to a running application instance -- but only under every one of the following conditions, with no exceptions and no discretion to relax them:

- `config/pentest.config.yaml` has `enabled: true` (default: `false`);
- the target is present verbatim in that file's allowlist -- never inferred from a URL found in the analyzed repository's code, configuration, or documentation, no matter how obviously "that must be it";
- the target's environment is development, staging, or homologation, unless the allowlist entry explicitly sets `production_authorized: true`;
- the test performed is the minimal action that confirms or refutes one specific claim from one specific finding -- never exploratory, never a scan;
- the test is never destructive, never alters or deletes data beyond a trivial and reversible minimum, never denies service, never establishes persistence, never moves laterally beyond the single authorized target, never modifies infrastructure, and never extracts data in bulk.

Any future integration (OWASP ZAP, Nuclei, Burp Suite API, or a custom HTTP validator) inherits every condition above unchanged. See `agents/pentest-validator.md` for the complete specification.

---

## Vulnerability Validation

Security findings must be validated before confirmation.

For each candidate vulnerability, evaluate where applicable:

1. Is attacker-controlled input present?
2. Can the attacker reach the vulnerable execution path?
3. Are authentication controls present?
4. Are authorization controls present?
5. Is validation present?
6. Is sanitization present?
7. Does the framework provide automatic protection?
8. Is the sink actually dangerous in this context?
9. Are there compensating controls?
10. Is exploitation realistic?

---

## Source-to-Sink Analysis

When applicable, trace:

SOURCE
→ PARSING
→ TRANSFORMATION
→ VALIDATION
→ AUTHENTICATION
→ AUTHORIZATION
→ BUSINESS LOGIC
→ SINK

Do not stop analysis after identifying a dangerous method or API.

The complete relevant security context must be considered.

---

## Scanner Trust Policy

Scanner results are evidence, not conclusions.

A scanner finding must initially be considered:

CANDIDATE

not:

CONFIRMED

Scanner findings should be correlated with:

- application architecture;
- code context;
- execution flow;
- framework protections;
- security controls.

---

## False Positive Policy

The project must prioritize finding accuracy over finding quantity.

Never intentionally reduce verification quality to increase detection counts.

When evidence is insufficient:

- lower confidence;
- classify as informational;
- request additional context where appropriate;
- or reject the candidate finding.

---

## Security Findings vs. Architecture Recommendations

These are never the same thing and must never be presented as if they were.

A **Security Finding** (`SEC-*`) is a concrete, verifiable vulnerability with an attack path, evidence, and exploitability reasoning, produced by `security-reviewer` and confirmed by `security-verifier` (optionally strengthened by `pentest-validator`).

An **Architecture Recommendation** (`ARCH-*`) is a structural improvement suggested by `architecture-advisor`, justified by evidence and by the software's actual context, never by architectural fashion. It is not a vulnerability, does not go through the CANDIDATE -> CONFIRMED lifecycle, and must never be inflated in severity language to make it seem more urgent than the evidence supports.

An imperfect architecture is not automatically presented as a vulnerability. Where a structural problem is the root cause of one or more confirmed findings, the recommendation may reference those finding IDs -- but the findings still stand on their own evidence, and fixing the architecture is never substituted for fixing the individual finding.

---

## Secrets Handling

If a potential secret is found:

- do not print the entire secret unnecessarily;
- do not copy the secret to logs;
- do not persist the secret in reports unless absolutely required;
- prefer masking sensitive values.

Example:

AKIA****************

instead of exposing the complete credential.

---

## Sensitive Data

Reports should minimize reproduction of:

- passwords;
- API keys;
- access tokens;
- private keys;
- personal data;
- confidential business data.

Only include information necessary to demonstrate the finding.

---

## Security Recommendations

Recommended remediation must be:

- specific;
- technically accurate;
- framework-aware;
- realistic;
- proportionate to risk.

Recommendations may contain example code snippets.

Example code is informational only and must never be automatically applied.

---

## Trust Boundaries

The agent should identify and consider trust boundaries involving:

- user input;
- browser input;
- HTTP requests;
- internal APIs;
- third-party APIs;
- message queues;
- databases;
- file systems;
- object storage;
- webhooks;
- authentication providers;
- cloud services;
- administrative interfaces.

---

## Principle

The system should behave like a senior defensive Application Security reviewer:

Skeptical of potential vulnerabilities,
skeptical of apparent protections,
and dependent on evidence before reaching conclusions.
