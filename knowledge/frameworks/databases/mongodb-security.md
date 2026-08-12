# MongoDB Security

Shared knowledge consumed by [injection-review](../../../skills/injection-review/SKILL.md) (specifically [nosql-injection.md](../../../skills/injection-review/references/nosql-injection.md)) when MongoDB is detected.

## What to Check

- **Query filters built from unvalidated request bodies** — the primary MongoDB-specific risk; see [nosql-injection.md](../../../skills/injection-review/references/nosql-injection.md) for the full operator-injection pattern (`{"$ne": null}` etc.).
- **`$where` operator / server-side JavaScript execution** — if reachable with attacker-influenced input, this is effectively [code injection](../../../skills/injection-review/references/code-injection.md), not just query manipulation; `$where` should generally be avoided entirely in application code.
- **Authentication enabled** — historically, MongoDB's default configuration allowed unauthenticated connections; confirm `--auth`/`security.authorization: enabled` is set and the deployment isn't relying on network isolation alone.
- **Network exposure** — MongoDB instances bound to `0.0.0.0` and exposed to the internet with no authentication have been a widely-exploited real-world misconfiguration; treat as `critical` if found (see [iac-misconfig-review](../../../skills/iac-misconfig-review/SKILL.md)).
- **Role-based access control granularity** — confirm the application's database user has only the roles it needs (e.g. `readWrite` on its own database) rather than `root`/`dbOwner` on the whole deployment.

## Common Footguns

- An ODM (Mongoose, etc.) with schema validation reduces operator-injection risk by enforcing field types, but confirm schema validation is actually strict (`strict: true`) rather than permissive.
- Aggregation pipelines built with string-concatenated stages from user input carry similar injection risk to raw query filters.
