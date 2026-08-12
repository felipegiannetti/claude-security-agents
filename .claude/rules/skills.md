# Skill Development Rules

## Purpose

Skills provide reusable, specialized security knowledge and review procedures.

Each Skill should represent a clear security capability or domain.

Examples:

- authentication review;
- authorization review;
- injection analysis;
- API security;
- secrets detection;
- dependency vulnerability analysis;
- cryptography review;
- infrastructure-as-code review.

---

## Directory Structure

Every Skill must follow:

skills/<skill-name>/
├── SKILL.md
└── references/

The `references/` directory is optional.

Use references when detailed supporting knowledge would make `SKILL.md` unnecessarily large.

---

## SKILL.md Responsibilities

`SKILL.md` should define:

- the purpose of the Skill;
- when it should be used;
- what security questions it should answer;
- what evidence should be collected;
- how potential vulnerabilities should be validated;
- common false-positive conditions;
- expected outputs.

Avoid placing large reference material directly in `SKILL.md`.

---

## Skill Scope

Skills must be focused.

Prefer:

auth-authz-review
api-security-review
injection-review

instead of:

everything-security-review

A Skill should have one coherent security domain.

---

## Read-Only Policy

All Skills inherit the project's strict read-only policy.

Skills must NEVER instruct an agent to:

- edit source code;
- modify configuration;
- create files in the analyzed repository;
- install packages;
- update dependencies;
- apply fixes;
- execute autofix;
- commit;
- push;
- deploy;
- modify infrastructure.

Skills may explain or recommend remediation, but never execute it.

---

## Evidence Requirements

Skills should favor evidence-driven analysis.

Potential vulnerabilities should be evaluated using relevant context such as:

- attacker-controlled sources;
- validation;
- sanitization;
- encoding;
- authentication;
- authorization;
- framework behavior;
- dangerous sinks;
- execution reachability;
- environmental constraints.

Avoid purely pattern-based conclusions when additional context is available.

---

## False Positive Analysis

Every Skill responsible for vulnerability detection must define likely false-positive conditions.

Examples:

A SQL injection Skill should check for:

- prepared statements;
- ORM parameterization;
- query builders with safe binding.

An XSS Skill should check for:

- contextual escaping;
- framework auto-escaping;
- sanitization;
- trusted static content.

An authorization Skill should check for:

- resource ownership checks;
- service-layer authorization;
- middleware;
- policy engines.

---

## References

Detailed information should live in:

skills/<skill-name>/references/

Examples:

skills/auth-authz-review/references/jwt.md

skills/injection-review/references/sql-injection.md

skills/web-security-review/references/ssrf.md

References should contain specialized knowledge that supports the Skill without bloating its main instructions.

---

## Shared Knowledge

Do not duplicate globally reusable information across Skills.

Shared material belongs under:

knowledge/

Examples:

- OWASP mappings;
- CWE mappings;
- severity standards;
- priority rules;
- framework guidance.

Skills may instruct agents to consult shared knowledge when needed.

---

## Output

Skills should produce structured security observations whenever practical.

A vulnerability-related Skill should provide enough information to populate fields such as:

- title;
- category;
- location;
- evidence;
- source;
- sink;
- attack vector;
- exploitability;
- severity;
- confidence;
- remediation recommendation.

The Skill should not generate the final executive report unless it is specifically a reporting Skill.

---

## Development Principles

1. Keep Skills modular.
2. Avoid overlapping Skills.
3. Avoid duplicated knowledge.
4. Prefer references for detailed material.
5. Include false-positive criteria.
6. Preserve read-only behavior.
7. Prefer security reasoning over keyword matching.
8. Keep outputs compatible with project schemas.
9. Do not depend on a specific project architecture unless the Skill is explicitly framework-specific.
10. Keep Skills reusable across repositories.
