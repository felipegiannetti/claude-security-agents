# Security Architecture Smells

Structural patterns that make security controls harder to apply correctly and consistently — distinct from a specific vulnerability. A smell is a risk factor and a candidate `ARCH-*` recommendation; it is not, by itself, a `SEC-*` finding. If a smell has actually produced a confirmed exploitable instance somewhere in the code, that instance is a separate `SEC-*` finding that references the smell, not the other way around.

## No Clear Module Boundaries

Symptom: any part of the codebase can import/call any other part with no enforced boundary. Risk: a security control added "at the boundary" doesn't actually bound anything, because there effectively isn't one — code can route around it by calling internals directly.

## Authorization Implemented Individually Per Controller

Symptom: the same "does this user own this resource" logic re-implemented (often slightly differently) in dozens of handlers instead of a shared mechanism (middleware, guard, policy engine, service-layer check). Risk: it only takes one handler to skip or subtly get the check wrong to produce a BOLA/IDOR — and with dozens of independent implementations, that's a probability question, not an "if." This is one of the most common root causes behind a cluster of related authorization findings.

## Direct Database Access From Multiple Layers

Symptom: controllers, services, and even presentation-layer code all query the database directly, rather than going through a single data-access layer. Risk: query construction (and therefore injection risk, and access-control-at-the-query-level) is duplicated everywhere instead of centralized where it can be reviewed and hardened once.

## Circular Dependencies Between Modules

Symptom: module A depends on module B which depends on module A. Risk: not directly a vulnerability, but it defeats the purpose of having module boundaries at all — you can't reason about or isolate one module's trust level from another's, and it makes any later attempt at service extraction or privilege separation much harder.

## Credentials/Secrets Handling Scattered Across the Application

Symptom: no single, consistent mechanism for accessing secrets — some read directly from environment variables inline, some from config files, some hardcoded, in many different places. Risk: inconsistent handling makes it easy for one of those many places to leak a secret into logs, error messages, or version control; also makes credential rotation operationally painful, which discourages rotating them at all.

## Duplicated Security Logic

Symptom: more than one implementation of "the same" security mechanism (e.g. two different JWT validation code paths, two different password-hashing call sites with different parameters). Risk: the implementations drift; a fix applied to one path doesn't reach the other.

## No Gateway/Boundary Layer for External Integrations

Symptom: many different parts of the codebase call third-party APIs directly, each with its own error handling, retry logic, and credential usage. Risk: a compromised or misbehaving third-party dependency has a much larger blast radius, and there's no single place to apply rate limiting, circuit breaking, or response validation against a potentially hostile external actor.

## Excessive Trust in Frontend-Supplied Data or Frontend-Enforced Rules

Symptom: authorization or business-rule decisions that are only enforced in client-side code, with the backend trusting whatever the client sends (e.g. a "isAdmin" flag accepted from the request body). Risk: trivially bypassed by anyone who can craft their own request — this is often the direct cause of a `SEC-*` broken-authorization finding, and the smell is the systemic pattern behind it.

## Services/Components With Overly Broad Privileges

Symptom: a service account, API key, or database role used by a component has far more access than that component's actual function requires (e.g. a read-only reporting service using a database credential with write access to every table). Risk: compromise of that one component has a blast radius equal to everything its credentials *could* touch, not just what it *needs* to touch.

## Undefined Trust Level for Internal Communication

Symptom: internal service-to-service or module-to-module calls are treated as inherently trusted, with no authentication/authorization between them, on the assumption that "it's internal." Risk: this assumption breaks the moment any single internal component is compromised or any network boundary assumption turns out to be wrong (e.g. a misconfigured network policy, a compromised adjacent tenant in shared infrastructure) — internal trust boundaries deserve the same explicit definition as external ones, proportionate to the system's actual risk profile.

---

Each smell found should be evidenced with specific file/module references (see `12_architecture_assessment`) and, if recommended for remediation, turned into a justified, phased `ARCH-*` recommendation (see `13_security_architecture_recommendations`) — never presented as a vulnerability on its own.
