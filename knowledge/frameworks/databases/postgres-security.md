# PostgreSQL Security

Shared knowledge consumed by [injection-review](../../../skills/injection-review/SKILL.md) and [iac-misconfig-review](../../../skills/iac-misconfig-review/SKILL.md) when PostgreSQL is detected.

## What to Check

- **Row-Level Security (RLS)** — Postgres supports enforcing tenant/ownership scoping at the database level (`CREATE POLICY ... USING (tenant_id = current_setting('app.tenant_id'))`). If present, this is a strong, centralized [tenant-isolation.md](../../../skills/business-logic-review/references/tenant-isolation.md) control worth noting as a positive architectural signal — but confirm the session variable it depends on (`app.tenant_id`) is actually set correctly on every connection and can't be influenced by the application layer's own bugs.
- **Role privileges** — an application's database role should not be `SUPERUSER` or own the schema it operates on; least-privilege roles limit blast radius if the application layer is compromised (see [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md) "overly broad privileges").
- **`pg_hba.conf` / network exposure** — confirm the database isn't reachable from untrusted networks (`0.0.0.0/0` in a cloud security group, or `trust`/`md5` auth method accepting connections from broad CIDR ranges) — see [iac-misconfig-review](../../../skills/iac-misconfig-review/SKILL.md).
- **`dblink`/`pg_read_file`/`COPY ... TO/FROM PROGRAM`** — functions capable of filesystem access or command execution from within SQL; if reachable via an injection point, they escalate a SQL injection's impact to file read/write or code execution.

## Common Footguns

- Prepared statements (`$1`, `$2` placeholders, or an ORM's parameter binding) are the standard mitigation for [SQL injection](../../../skills/injection-review/references/sql-injection.md) — the driver/ORM in use determines whether this is automatic; verify the specific call site.
- SSL/TLS not enforced for connections (`sslmode=disable` or unset) — credentials and data travel in plaintext over the network.
