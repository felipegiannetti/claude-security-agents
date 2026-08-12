# Layering Patterns

Three common organizational patterns, and when each genuinely fits. None is "the" correct pattern — the right choice depends on team structure, domain complexity, and how the codebase is actually navigated day to day.

## Technical Layering (`controller/service/repository/model/dto/...`)

```
src/
├── controller/
├── service/
├── repository/
├── model/
├── dto/
├── mapper/
├── security/
├── validation/
├── exception/
├── config/
└── integration/
```

Fits well when: the team is small-to-medium and works across the whole codebase rather than owning specific business domains; the domain is not yet complex enough to warrant domain boundaries; the stack/framework conventions already expect this shape (common in Spring, many Rails/Django-influenced structures).

Security value: a dedicated `security/` layer centralizes authentication/authorization instead of letting it leak into individual controllers; `dto/` prevents direct entity exposure (and mass assignment, when entities would otherwise be bound directly to request bodies); `validation/` makes input handling consistent instead of ad hoc per-endpoint; `repository/` bounds direct database access to one layer.

Weakness at scale: as the codebase grows, a change to one business feature touches files scattered across every top-level folder, and it becomes hard to see where one feature's boundary ends and another's begins — which is exactly when authorization and validation start being applied inconsistently.

## Domain-Oriented Layering (`domain/application/infrastructure/presentation`)

```
src/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

Fits well when: the business domain itself is complex enough to benefit from being modeled independent of frameworks and delivery mechanisms (hexagonal/clean-architecture style); the team wants domain logic to be testable without spinning up infrastructure; there's a real need to swap infrastructure (a database, a queue) without touching business rules.

Security value: business rules (including authorization *decisions*, as opposed to authorization *enforcement*) live in `domain/`/`application/` independent of transport — so a security rule expressed once applies whether the entry point is HTTP, a queue consumer, or a CLI. `infrastructure/` becomes the natural place to enforce that all external calls (including database access) go through one audited boundary.

Weakness: more upfront structure and more indirection than a small application needs; can be over-applied as a "best practice" to systems with genuinely simple domains, adding ceremony without corresponding benefit.

## Feature-First Layering

```
src/
├── authentication/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── dto/
│   └── security/
├── users/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   └── dto/
└── payments/
    ├── controller/
    ├── service/
    ├── repository/
    └── dto/
```

Fits well when: the system has genuinely distinct business domains that rarely need to reach into each other's internals; different people/teams own different features; the system is a plausible future candidate for splitting into independent services and internal module boundaries would double as future service boundaries.

Security value: a change to one feature's authorization logic is visibly scoped to that feature's folder — it's much harder for an authorization check to be "missed" 27 controllers away because there's no single "controllers" bucket to lose track of. Blast radius of a bug is easier to reason about because the module boundary is also (ideally) a trust/ownership boundary.

Weakness: cross-cutting concerns (a shared `security/` mechanism, shared validation) can end up duplicated per feature unless deliberately factored out into a shared module — which reintroduces some of technical layering's centralization benefit for the pieces that should stay centralized (see [security-architecture-smells.md](security-architecture-smells.md) on duplicated security logic).

## How to Choose

Don't pick based on trend. Evaluate against the actual system: team structure and ownership, domain complexity, how often changes cross today's folder boundaries in practice (check git history for files that change together across "unrelated" folders — that's often the real signal), and whether the system is a realistic future services-split candidate. A recommendation to move from one pattern to another must name which of these specifically motivates the change.
