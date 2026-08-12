# Open Redirect

**CWE-601** · OWASP: (folds into A01:2021 Broken Access Control / used as a component of phishing and OAuth attacks)

## What to Look For

Attacker-influenced data (typically a `redirect`/`next`/`returnUrl`/`continue` query parameter) used directly as the target of a server-issued redirect, without validating that the target stays within the application's own domain.

## What This Enables

Rarely high-impact alone, but a common building block: phishing (a link to the trusted domain that redirects to an attacker's lookalike login page), and — notably — a component of OAuth `redirect_uri` attacks (see [oauth-oidc.md](../../auth-authz-review/references/oauth-oidc.md)) where an open redirect on the legitimate domain can sometimes satisfy a loosely-validated `redirect_uri` allowlist check.

## False-Positive Conditions

- **Relative-path-only redirects** — the redirect target is validated/constrained to a relative path (no scheme/host), which structurally can't redirect off-domain.
- **Allowlist of exact permitted destinations**, validated against the actual resolved target (not just a `startswith` check on a string, which can be bypassed with e.g. `https://trusted.com.attacker.com`).
- **No user-influenced redirect target at all** — the destination is entirely code-defined per route.

## Severity Notes

Default `low` per `config/severity.config.yaml` in isolation. Escalate to `medium`/`high` when it's chainable with another issue (OAuth flow, or the application context makes phishing impact especially high per `02_software_context_discovery`).
