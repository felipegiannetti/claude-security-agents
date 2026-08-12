# Architecture Prompt

Standalone prompt for running architecture discovery outside the full pipeline — e.g. "just map this repo's architecture" without a full review. For the full methodology used in `02_architecture_discovery`, see [agents/architecture-mapper.md](../agents/architecture-mapper.md); this is the condensed version for a narrower, one-off invocation.

---

Include [system_prompt.md](system_prompt.md).

Task: build an architecture model of the target repository (or the specified subset of it) sufficient to support a later security review. Do not flag vulnerabilities — note architecturally notable characteristics as observations only.

Cover, citing evidence for each: languages and frameworks in use; components/services and how they communicate; entry points (REST/GraphQL/WebSocket/webhook/CLI/queue-consumer/admin); data stores and what each holds; authentication and authorization mechanisms and where each is enforced; external integrations; infrastructure/IaC; dependencies (ecosystem + manifest location); where sensitive data lives; trust boundaries; existing security controls already in place.

Output: an architecture model conforming to [architecture.schema.json](../schemas/architecture.schema.json), plus a short prose summary of anything unusual worth a reviewer's attention.
