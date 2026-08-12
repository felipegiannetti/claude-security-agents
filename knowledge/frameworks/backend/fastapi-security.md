# FastAPI Security

Extends [python-security.md](python-security.md).

## Default Protections (when used as intended)

- **Pydantic models** as request bodies provide automatic type validation and reject unexpected fields when configured with `model_config = ConfigDict(extra="forbid")` (Pydantic v2) — directly mitigates [mass-assignment.md](../../../skills/api-security-review/references/mass-assignment.md), but only if that config is actually set; the default (`extra="ignore"`) silently drops unexpected fields rather than rejecting them, which is safer than binding them but still worth confirming.
- **Separate response models** (`response_model=...`) let FastAPI filter the returned object to only declared fields — check whether endpoints actually declare one or return raw ORM/DB objects, which risks [excessive-data-exposure.md](../../../skills/api-security-review/references/excessive-data-exposure.md).
- **`Depends()`-based dependency injection** is FastAPI's idiomatic place to centralize authentication/authorization (e.g. a shared `get_current_user` dependency) — a good sign per [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md), if consistently applied across routers.

## Common Footguns

- **SQLAlchemy raw SQL** (`text()` with string-formatted input, or `.execute(f"...")`) reintroduces [SQL injection](../../../skills/injection-review/references/sql-injection.md) despite FastAPI's own request validation being solid.
- **Async endpoints calling blocking I/O directly** — not a security issue per se, but a blocking call in an `async def` route can starve the event loop, which is a resource-exhaustion/availability concern worth noting alongside [rate-limiting.md](../../../skills/api-security-review/references/rate-limiting.md) if it's reachable with attacker-controlled volume.
- **`Depends()` dependency present but not actually applied** to every router/route — FastAPI doesn't enforce a dependency is used; a new router added without the shared auth dependency is a silent gap, same risk pattern as NestJS guards.
- **CORS `allow_origins=["*"]` combined with `allow_credentials=True`** — invalid per spec but check for the reflected-origin workaround pattern, see [cors.md](../../../skills/web-security-review/references/cors.md).

## Architecture Notes

FastAPI's router-based structure supports feature-first organization well (one router module per domain) — evaluate whether routers are organized by domain or all dumped into a single `main.py`, and whether the `Depends()`-based auth pattern is genuinely centralized or reimplemented per router.
