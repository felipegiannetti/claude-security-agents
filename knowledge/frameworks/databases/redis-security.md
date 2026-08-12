# Redis Security

Shared knowledge consumed by [architecture-mapper](../../../agents/architecture-mapper.md) and [iac-misconfig-review](../../../skills/iac-misconfig-review/SKILL.md) when Redis is detected -- typically used as a cache, session store, or queue rather than a primary datastore, which changes what matters most.

## What to Check

- **Authentication** — Redis has no authentication enabled by default in many versions/configurations (`requirepass` unset); an exposed, unauthenticated Redis instance allows full read/write of its contents and, in older versions, has been used as a pivot for remote code execution (via `CONFIG SET`/`MODULE LOAD` abuse). Treat an internet-exposed, unauthenticated Redis instance as `critical`.
- **Network exposure** — Redis is designed to be used within a trusted network; confirm it isn't bound to `0.0.0.0` and reachable from the internet or from untrusted network segments.
- **Session store usage** — if Redis backs session storage, review [session-management.md](../../../skills/auth-authz-review/references/session-management.md) concerns through the lens of "who else can read/write this store" — Redis access effectively equals session-hijacking capability.
- **Cached sensitive data** — confirm data cached in Redis (e.g. serialized user objects) doesn't include secrets/credentials that would otherwise never be persisted in a general-purpose store, and that appropriate TTLs limit exposure window.
- **`EVAL`/Lua scripting with attacker-influenced arguments** — Redis Lua scripting can be a code-injection-adjacent risk if script content or unescaped arguments are attacker-influenced.

## Architecture Notes

Redis often sits behind an application as an implementation detail (cache, rate-limit counter, queue) — when mapping architecture, still record it as a data store with its own trust boundary and confirm its exposure isn't broader than the application layer that's supposed to be its only client.
