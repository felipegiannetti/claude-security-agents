# Stage 13: Security Architecture Recommendations

## Purpose

Turn the assessment from `12_architecture_assessment` into concrete, justified recommendations — each with benefits, costs, risks, complexity introduced, and the specific criteria that justify it. Never a bare "migrate to microservices" or "add a service layer" without the reasoning behind it.

## Agent

[architecture-advisor](../../agents/architecture-advisor.md)

## Inputs

- The architecture assessment from `12_architecture_assessment`.
- Software context from `02_software_context_discovery`.

## Process

For each structural problem worth addressing, produce a recommendation per [architecture-recommendation.schema.json](../../schemas/architecture-recommendation.schema.json): what to change, why (tied to a specific assessed problem, not a generic best practice), benefits, costs, risks, complexity introduced, and — critically — a phased path rather than a single big-bang change. A monolith-to-modular evolution is proposed as: identify bounded contexts → separate internal modules → define interfaces between them → reduce cross-module dependencies → *only then* evaluate extracting an independent service, and only for the modules where the evidence (uneven scale, independent teams, genuine isolation need) supports it.

Assign priority: `ARCH-P0` (critical architectural risk) through `ARCH-P3` (optional optimization) — a distinct scale from the security `P0`–`P4` used for vulnerabilities, never conflated with it.

## Outputs

- A list of `ARCH-NNN` recommendations, each conforming to [architecture-recommendation.schema.json](../../schemas/architecture-recommendation.schema.json).
- Where a recommendation would also reduce a specific security finding's root cause (e.g. centralizing authorization would prevent the class of bug behind several `SEC-*` findings), the recommendation references those finding IDs — but the finding stays `CONFIRMED`/`SEC-*` in its own right; fixing the architecture is not itself the finding's remediation.

## Success Criteria

- No recommendation is a bare architectural preference — each is tied to evidence from `12_architecture_assessment` and context from `02_software_context_discovery`.
- Recommendations are phased/gradual by default; a full rewrite or a full microservices migration is only proposed when the evidence genuinely supports it, and even then as a multi-step roadmap, not a single leap.
- Security Findings (`SEC-*`) and Architecture Recommendations (`ARCH-*`) remain clearly distinguishable in the output — see [15_final_report.md](15_final_report.md).
