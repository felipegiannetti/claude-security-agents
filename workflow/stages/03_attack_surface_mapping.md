# Stage 03: Attack Surface Mapping

## Purpose

Identify every point where untrusted data can enter the system, and rank them by risk, so later analysis is directed at the highest-value targets instead of scanning uniformly.

## Prompt

[attack_surface_prompt.md](../../prompts/attack_surface_prompt.md) — this stage has no dedicated subagent; it runs in the orchestrating context using the architecture model as input.

## Inputs

- The architecture model from `02_architecture_discovery` ([architecture.schema.json](../../schemas/architecture.schema.json)).

## Process

1. Enumerate untrusted-input entry points from the architecture model's entry points and trust boundaries: REST/GraphQL/WebSocket endpoints, webhook receivers, file uploads, HTTP parameters/cookies/headers, message queue consumers, third-party integration callbacks, admin interfaces.
2. Flag entry points that touch sensitive operations as higher risk: authentication, authorization, password reset, payments, admin/privileged actions, file handling, data export.
3. Note which entry points are unauthenticated vs. authenticated vs. privileged-only — unauthenticated entry points touching sensitive operations are the highest-priority targets.
4. Cross-reference against `config/exclusions.yaml` and the review scope — an entry point outside scope is documented but not analyzed further.

## Outputs

- An attack surface map conforming to [attack-surface.schema.json](../../schemas/attack-surface.schema.json): each entry point with its trust level, data sensitivity, and a preliminary risk rank.

## Success Criteria

- Every entry point in the architecture model is either represented here or explicitly excluded with a reason.
- High-risk entry points (unauthenticated + sensitive operation) are clearly distinguishable from routine ones, so `05_llm_review` can prioritize its attention.
