---
name: architecture-review
description: Software architecture and security-architecture review methodology — evaluating layering, module boundaries, and monolith-vs-services fit against actual system context, and identifying security architecture smells. Backs agents/architecture-advisor.md for workflow stages 12_architecture_assessment and 13_security_architecture_recommendations. Not a vulnerability-detection skill — its output is ARCH-* recommendations, never SEC-* findings.
---

# Architecture Review

This Skill has no favorite architecture. Its purpose is to evaluate whether a system's structure serves its actual context well, and — only when evidence supports it — recommend a specific, justified evolution. See references below for the detailed methodology:

- [Layering Patterns](references/layering-patterns.md) — common organizational patterns and when each fits.
- [Monolith Vs Microservices](references/monolith-vs-microservices.md) — decision criteria, not a default answer.
- [Security Architecture Smells](references/security-architecture-smells.md) — structural patterns that make security harder to get right, independent of any specific vulnerability.

## When to Use

During `12_architecture_assessment` and `13_security_architecture_recommendations`, always in combination with `02_software_context_discovery` output — a structural observation without context ("controllers are large") is not yet an assessment ("controllers are large *and* this is causing measurable authorization inconsistency across a system with N independent teams").

## Evidence Requirements

Every architectural claim needs a file reference. "This seems coupled" is not evidence; "OrderController directly constructs SQL queries and also contains payment-provider API calls" is.

## False-Positive / Overreach Conditions

An architecture recommendation is inappropriate (not just unnecessary — actively wrong to make) when:

- the "problem" is a reasonable tradeoff for the system's actual scale (e.g. a shared database access pattern in a 3-developer internal tool is not the same problem it would be in a 200-engineer platform);
- the recommended pattern would introduce more operational complexity than the system's team/ops maturity can currently support;
- the recommendation is a stylistic preference (e.g. folder-naming convention) with no security or maintainability consequence — don't manufacture urgency for taste.

## Output

`12_architecture_assessment` produces an assessment (current state, strengths, problems with evidence, security-relevant technical debt) — no recommendations. `13_security_architecture_recommendations` produces `ARCH-NNN` records conforming to [architecture-recommendation.schema.json](../../schemas/architecture-recommendation.schema.json): what, why, security implications, benefits/costs/risks/complexity, a phased path, and an `ARCH-P0`–`ARCH-P3` priority — a scale distinct from vulnerability priority.
