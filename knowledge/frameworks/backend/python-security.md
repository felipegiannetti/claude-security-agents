# Python / Django / Flask Security

Shared knowledge consumed by [injection-review](../../../skills/injection-review/SKILL.md), [web-security-review](../../../skills/web-security-review/SKILL.md), and [auth-authz-review](../../../skills/auth-authz-review/SKILL.md) when Django or Flask is detected. See [fastapi-security.md](fastapi-security.md) for FastAPI specifically.

## Django Default Protections

- Django's ORM (`Model.objects.filter(...)`) parameterizes by default; the risk is `.raw()` and `extra()` with string-formatted input.
- Django templates auto-escape by default; `{{ value|safe }}` or `mark_safe()` are the explicit opt-outs — same pattern as every other templating footgun, treat every occurrence as a review point.
- CSRF middleware (`django.middleware.csrf.CsrfViewMiddleware`) is enabled by default for session-authenticated views.
- `django.contrib.auth` provides built-in password hashing (PBKDF2/Argon2 depending on config) — check `PASSWORD_HASHERS` hasn't been overridden with something weaker.

## Django Common Footguns

- **`@csrf_exempt`** on a view that's actually cookie-authenticated — see [csrf.md](../../../skills/web-security-review/references/csrf.md).
- **`DEBUG = True` in production** — leaks stack traces, settings, and internal paths to any error response.
- **Django REST Framework `ModelSerializer` exposing all fields** (`fields = "__all__"`) without an explicit allowlist — see [excessive-data-exposure.md](../../../skills/api-security-review/references/excessive-data-exposure.md) and [mass-assignment.md](../../../skills/api-security-review/references/mass-assignment.md).
- **Missing `permission_classes`** on a DRF viewset — defaults to `AllowAny` unless a global default or explicit class is set.

## Flask Default Protections

- Jinja2 (Flask's default template engine) auto-escapes by default — same `| safe` / `Markup()` opt-out risk as Django.
- Flask itself provides *no* built-in CSRF protection, session security hardening, or rate limiting — these require explicit extensions (`Flask-WTF` for CSRF, `Flask-Talisman` for headers, `Flask-Limiter` for rate limiting). Check whether they're actually present, similar to bare Express.

## Flask Common Footguns

- **`render_template_string()` with attacker-influenced *template* content** (not just template variables) — [SSTI](../../../skills/injection-review/references/template-injection.md), and Jinja2's expression language is powerful enough to reach code execution.
- **Session secret (`app.secret_key`) hardcoded or weakly generated** — Flask signs (not encrypts) session cookies with this key by default; a weak/leaked key allows session forgery.
- **`debug=True` in production** — Flask's debugger, if reachable, allows arbitrary code execution via its interactive console.

## Architecture Notes

Django's "batteries included" structure (apps, models, views, DRF serializers) maps onto a layered pattern by convention. Flask has no imposed structure at all — check whether the team has adopted a consistent pattern (blueprints, application factories) or whether the app is a single large file with no separation of concerns.
