# Monolith vs. Microservices

The default recommendation for most small-to-medium applications is a well-structured **modular monolith** — clear internal module boundaries, without the operational overhead of distributed systems. Microservices solve organizational and scaling problems that most applications don't actually have yet; recommending them without evidence of those specific problems is a common and costly overreach.

## Signals That Favor a Modular Monolith

- Single team, or a small number of teams that still communicate easily.
- Uniform or unclear scaling needs across the system's components.
- Domain boundaries are still evolving/unclear — splitting into services locks in boundaries that are expensive to redraw later; a monolith's internal module boundaries are cheap to redraw by comparison.
- Limited operational maturity for distributed systems (observability, service discovery, distributed tracing, deployment automation) — microservices without this maturity trade code-level complexity for operational complexity, often a net loss.
- Low-to-moderate traffic/scale where a single deployable easily meets performance and availability needs.

## Signals That Favor Evolving Toward Services

- Genuinely independent business domains with different teams owning each, wanting independent release cadence.
- Meaningfully uneven scaling needs between components (e.g. one component needs 50x the compute of the rest) where scaling the whole monolith to serve one hot path wastes resources.
- A real need for operational/security isolation between components (e.g. a component handling payment data warranting a harder boundary and separate deployment/patching cadence than the rest).
- Extensive external integrations that benefit from being isolated behind a dedicated service (reducing blast radius if a third-party dependency misbehaves).
- The team has already demonstrated the operational maturity to run distributed systems (existing service mesh, tracing, on-call practices).

## What a Recommendation Must Include

Never recommend a migration without:

1. **Which specific signal(s) above apply**, with evidence — not "microservices are more scalable" as a general claim.
2. **Benefits** specific to this system (not generic microservices marketing).
3. **Costs**: operational overhead, distributed-systems failure modes (partial failure, network calls where there used to be function calls, data consistency across service boundaries), team/process changes required.
4. **Security implications specifically**: services can enable tighter least-privilege boundaries and isolate blast radius — but they also multiply the attack surface (more network-exposed interfaces, more inter-service trust boundaries to define and secure, more places secrets/credentials need to be managed) if not deliberately designed for it.
5. **A phased path** (see [layering-patterns.md](layering-patterns.md) and `agents/architecture-advisor.md`): bounded contexts identified → internal modules separated → interfaces defined between them → cross-module dependencies reduced → *then* evaluate extraction, module by module, only where the signals above genuinely apply to that specific module.

## Explicit Non-Goals

This Skill does not exist to justify a "microservices" recommendation as a default outcome, nor to universally discourage it. A small internal tool recommended to stay a modular monolith, and a payments platform with independent scaling domains recommended for a phased service extraction, are both correct outputs of the same methodology.
