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
- optional, disabled-by-default dynamic security validation against explicitly authorized targets;
- software architecture assessment and evidence-based structural recommendations;
- remediation prioritization;
- structured security reporting;
- regression and false-positive testing.

The primary objective is twofold: identify real, exploitable security vulnerabilities while minimizing false positives, and understand whether the system's own structure contributes to security risk, low maintainability, excessive coupling, or difficulty applying security controls. These are evaluated as two related but distinct axes -- see "Final Security Report".

The system must be reusable across different repositories, languages, frameworks, and application architectures. It does not have a favorite architecture or a default "correct" folder structure -- see [architecture-review skill](skills/architecture-review/SKILL.md).

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
- `architecture-advisor.md` -- software architecture assessment and recommendations. Strictly read-only, same as the three above.
- `pentest-validator.md` -- optional, disabled-by-default dynamic security validation. The **one** agent in this project that is not read-only against a running target (it remains strictly read-only against the analyzed *source repository*). Never active unless explicitly enabled and authorized -- see "Security Safety".

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
2. Software Context Discovery
3. Architecture Mapping
4. Attack Surface Mapping
5. Static Security Scanning
6. LLM Security Review
7. Data Flow Analysis
8. Security Triage
9. Independent Verification
10. Dynamic / Pentest Validation (optional -- see "Security Safety")
11. Security Prioritization
12. Architecture Assessment
13. Security Architecture Recommendations
14. Remediation Analysis
15. Final Report

Do not skip pipeline stages unless explicitly permitted by workflow configuration. Stage 10 is the one stage that is *always* skipped unless explicitly enabled and authorized -- skipping it is the safe default, not an exception to "don't skip stages."

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

- software context
- architecture
- attack surface
- scan result
- finding (includes the Static Analysis / Independent Verification / Dynamic Validation evidence layers)
- remediation
- architecture recommendation (`ARCH-*`, distinct from `finding`)
- final report (both axes: application security and software architecture)

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

Architecture recommendations (`ARCH-*`, produced by `architecture-advisor`) do not follow this lifecycle -- they are not vulnerabilities and are never "confirmed" or "rejected" in the same sense. They move from ASSESSED (a structural problem identified with evidence) to RECOMMENDED (a specific, justified recommendation with a priority). See "Final Security Report" for why the two are kept structurally separate.

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

## Dynamic Validation (Optional)

Some findings -- typically BOLA/IDOR, SSRF, authentication/authorization issues -- benefit from confirmation against a real, running instance of the application, beyond what static analysis and independent verification can establish from code alone. This is `pentest-validator`'s role, and it is optional and disabled by default.

A finding accumulates up to three independent evidence layers, tracked separately and never merged into a single number: **Static Analysis** (from `security-reviewer`), **Independent Verification** (from `security-verifier`), and **Dynamic Validation** (from `pentest-validator`, only when that stage actually ran). A finding with all three layers agreeing represents materially stronger evidence than one with static analysis alone -- but the absence of dynamic validation never counts against a finding; it simply means that layer wasn't attempted.

See "Security Safety" for the strict boundaries `pentest-validator` operates under.

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

The final security report has two axes, kept structurally and visually separate:

**Application Security** -- confirmed vulnerabilities (`SEC-*`). At minimum include: Executive Summary, Overall Risk, Finding Counts, Priority Overview, Confirmed Findings, Evidence, Attack Vectors, Data Flows, Exploitation Scenarios (and Dynamic Validation results when that layer was run), Business Impact, Consequences if Unresolved, Recommended Remediation, Remediation Effort, Verification Steps, Remediation Roadmap.

**Software Architecture** -- structural recommendations (`ARCH-*`), when `12_architecture_assessment` / `13_security_architecture_recommendations` ran. At minimum include: current-state summary, strengths, structural problems with evidence, security-relevant technical debt, recommended organization, architecture recommendations (with benefits, costs, risks, complexity, and a phased path -- never a single "rewrite everything" step), and an architecture roadmap.

A single **Final Conclusion** ties both axes together.

An imperfect architecture must never be presented as a vulnerability, and a vulnerability must never be softened into a mere architecture recommendation. See CLAUDE.md's Finding Lifecycle and Architecture recommendation lifecycle above, and [schemas/report.schema.json](schemas/report.schema.json) for the structural contract.

Reports should support structured output where possible.

Target formats:

- Markdown
- JSON
- SARIF (Application Security axis only -- SARIF has no meaningful representation for architecture recommendations)

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

### The Dynamic Validation Exception

`pentest-validator` (stage `10_dynamic_pentest_validation`) is a deliberate, narrowly-scoped exception to "read-only against everything" -- it is read-only against the analyzed *source repository* like every other agent, but it may send requests to a *running* application instance to confirm specific findings. This exception exists because dynamic confirmation genuinely strengthens evidence quality (see "Dynamic Validation" above), and it is bounded as follows, with no exceptions:

1. **Disabled by default.** `config/pentest.config.yaml` ships with `enabled: false` and an empty target list. Dynamic validation never runs unless a human has explicitly changed both.
2. **Allowlist only, never inferred.** A target must be listed verbatim in `config/pentest.config.yaml`. A URL appearing in the analyzed repository's code, configuration, or documentation is never treated as authorization to test it.
3. **Non-production by default.** An allowlist entry must be development, staging, or homologation unless it explicitly sets `production_authorized: true`.
4. **No destructive or disruptive action, ever**, regardless of authorization: no data deletion or alteration beyond the trivial minimum needed to observe a behavior, no denial-of-service, no persistence, no lateral movement beyond the single authorized target, no infrastructure changes, no bulk data extraction, no credential brute-forcing. See `agents/pentest-validator.md` for the full list.
5. **Confirmation-scoped, not exploratory.** Each test validates one specific claim from one specific finding -- never a broad scan of the target.

Tools like OWASP ZAP, Nuclei, the Burp Suite API, or custom HTTP validators may be integrated in the future, but any such integration is subject to every rule above without exception -- the gate is the point, not the specific tool.

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
