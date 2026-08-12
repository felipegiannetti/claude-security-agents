# MySQL Security

Shared knowledge consumed by [injection-review](../../../skills/injection-review/SKILL.md) and [iac-misconfig-review](../../../skills/iac-misconfig-review/SKILL.md) when MySQL/MariaDB is detected.

## What to Check

- **No native row-level security** — unlike Postgres, MySQL has no built-in RLS equivalent; tenant/ownership scoping must be enforced entirely at the application/query layer (every query manually scoped) or via views — making [tenant-isolation.md](../../../skills/business-logic-review/references/tenant-isolation.md) failures more likely if scoping isn't centralized in a shared data-access layer (see [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md)).
- **User privileges** — confirm the application's MySQL user doesn't have `GRANT OPTION`, `FILE`, or `SUPER` privileges it doesn't need; `FILE` in particular allows reading/writing files from within SQL (`LOAD_FILE()`, `INTO OUTFILE`), escalating a SQL injection's impact.
- **`LOAD DATA LOCAL INFILE`** — if enabled client-side, can be abused by a malicious server (or MITM) to read arbitrary files from the connecting client — verify this is disabled unless specifically required.
- **Network exposure and default accounts** — same concerns as Postgres: exposure to `0.0.0.0/0`, and any legacy default/blank-password accounts left enabled.

## Common Footguns

- Prepared statements (`?` placeholders, or an ORM's parameter binding) are the standard mitigation for [SQL injection](../../../skills/injection-review/references/sql-injection.md).
- Older MySQL versions/configurations using the legacy `mysql_native_password` auth plugin are weaker than `caching_sha2_password` — note as a hardening observation, not usually a standalone critical finding on its own.
- SSL/TLS not enforced (`require_secure_transport` off) — plaintext credentials/data in transit.
