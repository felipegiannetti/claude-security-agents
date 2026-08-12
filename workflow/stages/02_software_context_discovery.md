# Stage 02: Software Context Discovery

## Purpose

Understand what the software is *for* before evaluating how it's built. Architecture and security recommendations that ignore business context are generic advice, not analysis — a payment system and an internal admin tool warrant very different levels of rigor even with identical code patterns. This stage produces the context that `12_architecture_assessment` and `13_security_architecture_recommendations` are evaluated against, and that shapes how much weight `04_attack_surface_mapping` gives to different entry points.

## Inputs

- The review scope from `01_intake`.
- Repository-level signals: README, docs/, package metadata/description, domain terminology in code (entity/model names), CI/deployment configuration.
- Optional: context supplied directly by the requester (business domain, expected users, criticality) when available — prefer this over inference when it's given.

## Process

1. Infer the business domain and system purpose from documentation and domain terminology — do not guess beyond what's evidenced; mark anything uncertain as such.
2. Estimate expected scale/volume and criticality (e.g. "handles payments" or "internal-only, low user count") from evidence: infra sizing config, rate limits, error budgets, SLA references, compliance mentions (PCI, HIPAA, SOC2, GDPR).
3. Identify the user base: public internet users, authenticated customers, internal staff, other systems (machine-to-machine).
4. Note any explicit or implied compliance/regulatory context, since it materially changes both security priority and architectural recommendations (e.g. data residency requirements affect data-store recommendations).

## Outputs

- A software context record conforming to [software-context.schema.json](../../schemas/software-context.schema.json): domain, purpose, user base, expected scale, criticality, compliance context — each with a confidence level and supporting evidence.

## Success Criteria

- Every claim is either evidenced or explicitly marked as an inference with stated uncertainty — this context will be used to justify architecture recommendations later, so an unfounded assumption here propagates.
- `12_architecture_assessment` should never need to ask "why does this matter for a system like this" — this stage already answered it.
