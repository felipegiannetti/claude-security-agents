# Stage 12: Architecture Assessment

## Purpose

Evaluate whether the system's current structure is appropriate for what it actually is (per `02_software_context_discovery`) — not against a universal "best" architecture. This stage produces an evidence-based assessment; it does not yet produce recommendations (that's `13_security_architecture_recommendations`) — assessment and recommendation are kept separate so the "what is" isn't pre-biased by "what I'd change."

## Agent

[architecture-advisor](../../agents/architecture-advisor.md)

## Inputs

- Architecture model from `03_architecture_mapping`.
- Software context from `02_software_context_discovery`.
- Confirmed security findings from `09_independent_verification` / `10_dynamic_pentest_validation` — structural root causes behind multiple findings are architecturally relevant signal.

## Process

See [architecture-advisor.md](../../agents/architecture-advisor.md): evaluate layering and separation of concerns, module boundaries, monolith-vs-services fit for the actual context, and scan for security architecture smells (authorization scattered across controllers, direct multi-layer database access, circular dependencies, scattered credentials, duplicated security logic, missing integration gateway, excessive frontend trust, overly broad service privileges, undefined internal trust).

## Outputs

- An architecture assessment: current-state summary, strengths (name them — an assessment that's only criticism isn't credible), structural problems with evidence, and security-relevant technical debt. No recommendations yet — those are scoped to `13_security_architecture_recommendations`.

## Success Criteria

- Every problem cited has supporting evidence (file references, not general impressions).
- The assessment explicitly considers whether the current structure fits the system's actual scale/criticality/team shape from `02_software_context_discovery` — "this could theoretically be cleaner" is not the same finding as "this is causing real problems for a system like this one."
