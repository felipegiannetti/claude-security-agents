# Tenant Isolation

**CWE-668**

Relevant for any multi-tenant application (SaaS with multiple customer organizations sharing infrastructure). A tenant-isolation failure is a specific, high-blast-radius flavor of [bola-idor.md](../../api-security-review/references/bola-idor.md): instead of one user reaching another user's data, one *tenant* reaches another *tenant's* entire dataset.

## What to Look For

- **Tenant scoping applied inconsistently**: some queries scope by `tenant_id`/`organization_id`, others (especially newer or less-reviewed endpoints, background jobs, admin tooling, and reporting/export features) don't.
- **Tenant ID sourced from client-controlled input** (a request parameter or JWT claim the client can influence) rather than derived server-side from the authenticated session.
- **Shared resources leaking across tenants**: caches, search indexes, or file storage keyed without tenant scoping.

## False-Positive Conditions

- Tenant scoping is enforced at a single, centralized data-access layer (e.g. ORM-level default scoping, a query-building base class) applied uniformly, rather than repeated per-query — see `skills/architecture-review/references/security-architecture-smells.md` for why centralization matters here specifically.
- The resource is intentionally cross-tenant (e.g. shared reference data with no per-tenant sensitivity).

## Severity Notes

`critical` — a confirmed cross-tenant data leak is one of the highest-blast-radius finding types in a multi-tenant system, by definition affecting many customers at once.
