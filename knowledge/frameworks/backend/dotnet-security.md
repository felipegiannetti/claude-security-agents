# .NET / ASP.NET Core Security

Shared knowledge consumed by [injection-review](../../../skills/injection-review/SKILL.md), [auth-authz-review](../../../skills/auth-authz-review/SKILL.md), and [api-security-review](../../../skills/api-security-review/SKILL.md) when ASP.NET Core is detected.

## Default Protections

- Entity Framework Core parameterizes LINQ queries by default; the risk is `FromSqlRaw`/`ExecuteSqlRaw` with string-interpolated input (use `FromSqlInterpolated`/`ExecuteSqlInterpolated` or explicit parameters instead — these are safe; the raw string-formatting variants are not).
- Razor views HTML-encode by default (`@value`); `@Html.Raw()` is the explicit opt-out — same pattern as every other templating footgun.
- ASP.NET Core's Antiforgery middleware provides CSRF protection when `[ValidateAntiForgeryToken]`/`[AutoValidateAntiforgeryToken]` is applied — check it's actually wired for cookie-authenticated state-changing endpoints.
- ASP.NET Core Identity provides built-in password hashing (PBKDF2 by default) and account lockout.

## Common Footguns

- **`[Authorize]` present but no specific policy/role** — confirms authentication only, not authorization; check whether a privileged action needs `[Authorize(Roles = "Admin")]` or an explicit policy and whether it's actually applied — same authentication-vs-authorization distinction as everywhere else.
- **Model binding without `[Bind]` allowlist or a separate DTO** — binding request data directly onto an EF entity risks [mass-assignment.md](../../../skills/api-security-review/references/mass-assignment.md).
- **`XmlSerializer`/`DataContractSerializer` deserializing untrusted XML** without disabling DTD/external entity resolution — [XXE](../../../skills/injection-review/references/ldap-xpath-injection.md)-adjacent risk (see CWE-611 in [common-cwe.md](../../cwe/common-cwe.md)).
- **`BinaryFormatter` deserialization of untrusted data** — a well-known .NET insecure-deserialization vector (Microsoft itself has deprecated `BinaryFormatter` for this reason); any use on attacker-influenced input is a strong signal, see [state-manipulation.md](../../../skills/business-logic-review/references/state-manipulation.md).
- **Connection strings / secrets in `appsettings.json`** committed to source rather than `appsettings.Development.json` (gitignored) + environment variables or a secret manager (Azure Key Vault, `dotnet user-secrets` for local dev) — see [database-credentials.md](../../../skills/secrets-detection/references/database-credentials.md).

## Architecture Notes

ASP.NET Core's controller/service/repository conventions map onto the technical-layering pattern. Minimal APIs (`app.MapGet(...)` style) trade that structure for terseness — check whether authorization/validation logic is centralized via filters/`Results` conventions or duplicated inline per endpoint.
