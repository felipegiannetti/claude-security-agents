# NestJS Security

Extends [node-security.md](node-security.md) — NestJS runs on Express (or Fastify) under the hood but adds structural conventions worth checking specifically.

## Default Protections (when used as intended)

- **Guards** (`@UseGuards`, `CanActivate`) are NestJS's intended centralized mechanism for authentication/authorization — a good architectural sign per [security-architecture-smells.md](../../../skills/architecture-review/references/security-architecture-smells.md), *if* applied consistently (globally or via a base controller) rather than per-route with gaps.
- **Pipes** (`ValidationPipe` with `class-validator` DTOs) provide centralized input validation when enabled globally — check `main.ts` for `app.useGlobalPipes(new ValidationPipe())` and whether `whitelist: true`/`forbidNonWhitelisted: true` are set (these strip/reject unexpected fields, directly mitigating [mass-assignment.md](../../../skills/api-security-review/references/mass-assignment.md)).
- **Interceptors** are a common place for response shaping — check whether a serialization interceptor (`ClassSerializerInterceptor` with `@Exclude()` on sensitive entity fields) prevents [excessive-data-exposure.md](../../../skills/api-security-review/references/excessive-data-exposure.md), or whether entities are returned raw.

## Common Footguns

- **Guards applied per-controller but missed on a new module** — since Nest's DI-based module system makes it easy to add new controllers, confirm new modules actually import/apply the shared auth guard rather than assuming it's global.
- **DTOs without `class-validator` decorators** — a DTO class with no validation decorators provides no actual protection; the `ValidationPipe` only enforces what's declared.
- **Raw TypeORM/Prisma query methods** bypassing the parameterized query builder — same [SQL injection](../../../skills/injection-review/references/sql-injection.md) risk as any ORM's raw-query escape hatch.
- **GraphQL modules** (`@nestjs/graphql`) inherit the general [graphql-security.md](../../../skills/api-security-review/references/graphql-security.md) concerns — field-level authorization needs its own guards/decorators, not just the module-level ones.

## Architecture Notes

NestJS's module system (`@Module`) naturally supports the feature-first or domain-oriented layering patterns in [layering-patterns.md](../../../skills/architecture-review/references/layering-patterns.md) — assess whether modules are genuinely bounded (each module's providers/controllers cohesive to one domain) or whether cross-module imports have made the boundaries nominal only.
