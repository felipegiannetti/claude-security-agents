# Security Review Agent

## Project Purpose

Security Review Agent is an AI-assisted application security review system built for Claude Code.

The project combines:

- specialized AI agents;
- reusable security skills;
- deterministic security workflows;
- static analysis tools;
- secret scanning;
- dependency vulnerability scanning;
- architecture discovery;
- attack surface mapping;
- data-flow analysis;
- independent finding verification;
- remediation prioritization;
- structured security reporting;
- regression and false-positive testing.

The primary objective is to identify real, exploitable security vulnerabilities while minimizing false positives.

The system must be reusable across different repositories, languages, frameworks, and application architectures.

---

## Core Design Principle

Security findings must be evidence-driven, not checklist-driven.

Never classify suspicious code as a confirmed vulnerability without validating exploitability.

Whenever applicable, analysis should trace:

SOURCE
→ PARSING
→ TRANSFORMATION
→ VALIDATION
→ AUTHENTICATION
→ AUTHORIZATION
→ BUSINESS LOGIC
→ SINK

A finding should only be considered confirmed when the relevant execution path and security controls have been analyzed.

---

## Architecture

The project is organized into the following primary components:

### agents/

Contains Claude Code agents.

Initial agents:

- `architecture-mapper.md`
- `security-reviewer.md`
- `security-verifier.md`

Agents coordinate reasoning and security analysis.

Agents should not contain large security knowledge bases that belong in Skills or references.

### skills/

Contains reusable security capabilities following the Claude Code Skill structure.

Each Skill must have:

`skills/<skill-name>/SKILL.md`

Optional supporting material should live under:

`skills/<skill-name>/references/`

Skills contain specialized security methodologies and domain knowledge.

### workflow/

Defines the deterministic security review lifecycle.

The canonical pipeline is:

1. Intake
2. Architecture Discovery
3. Attack Surface Mapping
4. Static Scan
5. LLM Security Review
6. Data Flow Analysis
7. Triage
8. Independent Verification
9. Prioritization
10. Remediation Analysis
11. Final Report

Do not skip pipeline stages unless explicitly permitted by workflow configuration.

### knowledge/

Contains shared security knowledge used by multiple components.

Examples:

- OWASP references
- CWE mappings
- severity criteria
- priority criteria
- remediation criteria
- framework-specific security guidance

Do not duplicate shared knowledge across multiple Skills.

### prompts/

Contains reusable prompt fragments and output templates.

Agent identity and core agent behavior belong in `agents/`.

Task-specific reusable prompt material belongs in `prompts/`.

### scripts/

Contains deterministic tooling and integrations.

Examples:

- Semgrep
- Gitleaks
- Trivy
- OSV Scanner
- repository discovery
- report generation

Prefer deterministic scripts for operations that do not require LLM reasoning.

### schemas/

Contains structured contracts for internal data.

Important schemas include:

- architecture
- attack surface
- scan result
- finding
- remediation
- final report

Structured data should be preferred between pipeline stages whenever practical.

### config/

Contains configurable system behavior.

Configuration must be separated from security reasoning whenever possible.

Examples:

- scanner configuration
- severity thresholds
- priority rules
- remediation rules
- exclusions

### tests/

Contains security regression evaluations.

Every important vulnerability category should eventually include:

- vulnerable examples;
- safe examples;
- expected true positives;
- expected false positives.

Detection quality and false-positive rate are both first-class quality metrics.

### outputs/

Contains generated security reports.

Generated output must not be treated as source configuration.

### logs/

Contains runtime and diagnostic logs.

Logs must never intentionally contain secrets or sensitive source code unless explicitly required for debugging.

---

## Finding Lifecycle

A security issue progresses through the following states:

DETECTED
→ CANDIDATE
→ TRIAGED
→ VERIFIED
→ CONFIRMED

Only confirmed findings should appear as confirmed vulnerabilities in the final report.

If exploitability cannot be established, the finding must either:

- be rejected;
- remain informational;
- or explicitly indicate reduced confidence.

Never silently promote uncertain findings.

---

## Independent Verification

The Security Verifier exists to challenge findings produced by the Security Reviewer.

The verifier should actively attempt to disprove each candidate finding.

It must inspect:

- existing validation;
- authentication requirements;
- authorization checks;
- framework protections;
- sanitization;
- parameterization;
- data-flow reachability;
- environmental assumptions;
- attacker control of the source;
- actual reachability of the sink.

A finding surviving independent verification may be promoted to CONFIRMED.

---

## Severity and Priority

Severity and remediation priority are separate concepts.

Severity represents technical and business security impact.

Priority represents remediation urgency.

Prioritization should consider:

- severity;
- exploitability;
- exposure;
- authentication requirements;
- privileges required;
- affected data;
- business impact;
- blast radius;
- confidence;
- remediation effort.

Supported priorities:

- P0 — Immediate
- P1 — High
- P2 — Medium
- P3 — Low
- P4 — Informational

Do not assign priorities arbitrarily.

Use the project severity and priority configuration.

---

## Remediation Requirements

Every confirmed finding should provide actionable remediation guidance.

The system should explain:

- what is vulnerable;
- why it is vulnerable;
- where the issue exists;
- how an attacker could exploit it;
- realistic consequences if it remains unresolved;
- how it should be fixed;
- expected remediation effort;
- how the fix should be verified.

Remediation recommendations must be appropriate for the detected language and framework.

---

## Final Security Report

The final security report must contain both executive and technical information.

At minimum include:

- Executive Summary
- Overall Risk
- Finding Counts
- Priority Overview
- Confirmed Findings
- Evidence
- Attack Vectors
- Data Flows
- Exploitation Scenarios
- Business Impact
- Consequences if Unresolved
- Recommended Remediation
- Remediation Effort
- Verification Steps
- Remediation Roadmap
- Final Conclusion

Reports should support structured output where possible.

Target formats:

- Markdown
- JSON
- SARIF

---

## Development Rules

When modifying this repository:

1. Preserve separation between agents, Skills, workflow, knowledge, scripts, schemas, and configuration.
2. Avoid duplicating security knowledge.
3. Prefer small focused files over monolithic prompts.
4. Keep deterministic logic outside LLM prompts whenever practical.
5. Use structured schemas between pipeline stages when practical.
6. Every new finding type must define how false positives are evaluated.
7. Every important security capability should eventually include regression tests.
8. Never weaken verification requirements merely to increase finding count.
9. Prefer high-confidence findings over large quantities of speculative findings.
10. Keep the final report understandable by both engineers and decision-makers.

---

## Security Safety

This project is intended for defensive application security review.

Security tooling should default to analyzing code, configuration, dependencies, and local artifacts.

Do not introduce destructive behavior into scanners or agent workflows.

Do not automatically:

- modify analyzed repositories;
- delete files;
- push commits;
- publish packages;
- deploy applications;
- rotate credentials;
- perform destructive infrastructure actions.

Such actions require explicit user authorization and must remain outside the default review pipeline.

---

## Project Evolution

Before introducing a new major component, determine whether the capability belongs in:

- an Agent;
- a Skill;
- shared Knowledge;
- Workflow;
- a deterministic Script;
- Configuration;
- or a Schema.

Do not create new architectural layers unless existing layers cannot represent the requirement cleanly.

The architecture should remain modular, testable, reusable, and implementation-agnostic.
