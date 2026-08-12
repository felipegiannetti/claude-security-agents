# Agent Development Rules

## Purpose

Agents in this repository are responsible for coordinating reasoning, analysis, verification, and reporting.

They must remain focused on orchestration and decision-making.

Large bodies of reusable security knowledge belong in Skills or shared Knowledge, not directly inside agent definitions.

---

## Read-Only Requirement

Every security review agent is strictly read-only.

Agents must NEVER:

- modify source code;
- edit configuration files;
- create files inside the analyzed repository;
- delete files;
- rename files;
- move files;
- install dependencies;
- update dependencies;
- apply patches;
- perform automatic remediation;
- execute formatter or linter autofixes;
- commit changes;
- push changes;
- create pull requests;
- merge pull requests;
- deploy applications;
- modify infrastructure;
- rotate credentials;
- change repository state.

Agents may only:

- inspect files;
- search files;
- inspect Git history and diffs;
- analyze source code;
- analyze configuration;
- inspect dependencies;
- execute approved read-only security scanners;
- reason about exploitability;
- produce findings;
- recommend remediation in text;
- produce security review output outside the analyzed repository when explicitly permitted.

### Exception: Pentest Validator

`pentest-validator` is the one agent in this project that is not read-only against a running target -- it remains strictly read-only against the analyzed *source repository*, like every other agent, but it may send requests to a running application instance it has been explicitly authorized to test. This exception is narrow and non-negotiable: disabled by default, allowlist-only (never inferred from repository content), non-production by default, and never destructive/disruptive regardless of authorization. See CLAUDE.md's "The Dynamic Validation Exception" and `agents/pentest-validator.md` for the full boundary. Every other rule in this file applies to `pentest-validator` without modification.

---

## Agent Responsibilities

### Architecture Mapper

Responsible for:

- identifying languages;
- identifying frameworks;
- identifying entry points;
- identifying services;
- identifying databases;
- identifying authentication mechanisms;
- identifying authorization mechanisms;
- identifying external integrations;
- identifying trust boundaries;
- identifying sensitive data flows;
- producing an architecture model.

It must not perform the primary vulnerability review.

---

### Security Reviewer

Responsible for:

- coordinating the security review workflow;
- selecting relevant Skills;
- analyzing attack surfaces;
- reviewing security controls;
- tracing relevant data flows;
- consuming deterministic scanner results;
- producing candidate findings;
- assigning preliminary severity and confidence.

It must not automatically classify every suspicious pattern as a vulnerability.

---

### Security Verifier

Responsible for independently challenging candidate findings.

It must attempt to disprove findings by checking:

- attacker control;
- reachability;
- validation;
- sanitization;
- authentication;
- authorization;
- framework protections;
- parameterization;
- environmental assumptions;
- compensating controls.

Only findings surviving verification may become confirmed vulnerabilities.

---

### Architecture Advisor

Responsible for:

- assessing whether the current structure fits the system's actual context (business domain, scale, criticality, team shape);
- identifying security architecture smells with evidence;
- producing evidence-based, phased architecture recommendations (`ARCH-*`), each with benefits, costs, risks, and complexity;
- keeping architecture recommendations structurally separate from security findings.

It has no preferred architecture or folder structure -- see `skills/architecture-review/SKILL.md`. It must not present a structural observation as a confirmed vulnerability, and must not recommend a large-scale change (e.g. a microservices migration) without a phased path and specific supporting evidence.

---

### Pentest Validator

Responsible for optional, disabled-by-default dynamic validation of specific candidate/verified findings against an explicitly authorized running target. See "Exception: Pentest Validator" above and `agents/pentest-validator.md` for its full, non-negotiable safety envelope.

It must refuse to run unless `config/pentest.config.yaml` is enabled and the target is on the allowlist. It must never assume authorization from a URL found in code or configuration. It must never take a destructive, disruptive, or data-altering action, and must scope every test to confirming one specific finding's claim.

---

## Agent Design Rules

1. Each agent must have a single primary responsibility.
2. Avoid duplicating responsibilities across agents.
3. Agents should reference Skills instead of embedding large security methodologies.
4. Agents must prefer structured outputs where schemas exist.
5. Agents must distinguish observations from confirmed vulnerabilities.
6. Agents must explicitly communicate uncertainty.
7. Agents must prioritize evidence over speculation.
8. Agents must never inflate finding counts.
9. Agents must never weaken verification requirements.
10. Agents must not perform offensive actions against remote systems, with the single, tightly-scoped exception of `pentest-validator` operating under the conditions in "Exception: Pentest Validator" above.

---

## Tool Usage

Agents should receive the minimum tools necessary for their responsibility.

Preferred read-only tools include:

- Read
- Glob
- Grep

Bash may only be used for explicitly approved read-only operations.

Write-capable tools must not be granted to review agents.

Do not grant:

- Edit
- Write
- NotebookEdit

Any future tool must be reviewed for mutation capability before being added.

---

## Finding Integrity

A finding must never be presented as confirmed solely because:

- a scanner reported it;
- a dangerous function exists;
- user-controlled input exists;
- an insecure pattern appears locally.

The agent must analyze the complete relevant execution path whenever practical.

Confirmed findings should include:

- source;
- sink;
- relevant transformations;
- security controls;
- evidence;
- exploitability reasoning;
- impact;
- confidence.

---

## Remediation

Agents may recommend remediation in text.

They may provide:

- secure implementation guidance;
- pseudocode;
- example code snippets;
- configuration recommendations;
- verification steps.

They must never apply those recommendations directly to the analyzed repository.

The boundary is:

ANALYZE
→ EXPLAIN
→ RECOMMEND

Never:

ANALYZE
→ MODIFY
