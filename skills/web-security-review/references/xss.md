# Cross-Site Scripting (XSS)

**CWE-79** · OWASP: Injection (A03:2021)

## Variants

- **Stored**: attacker input is persisted (database, file) and later rendered to other users without proper escaping.
- **Reflected**: attacker input from the current request (query param, form field) is rendered directly back in the response.
- **DOM-based**: client-side JavaScript takes data from an attacker-influenced source (URL, `document.referrer`, `postMessage`) and writes it into the DOM via an unsafe sink, with no server round-trip involved.

## What to Look For

- **Sink type**: does the rendering path use an explicit "trust this as HTML/markup" API (e.g. a template engine's raw/unescaped output directive, `dangerouslySetInnerHTML`-style APIs, direct DOM `innerHTML` assignment) rather than the framework's default auto-escaping text output?
- **Attacker-influenced source reaching that sink** — trace per [source-sink-analysis.md](../../secure-code-review/references/source-sink-analysis.md), including stored-XSS paths where the source was user input from a *previous* request now read back from storage.
- **Context-appropriate escaping**: HTML-escaping alone doesn't protect an attribute, URL, or `<script>` context — confirm the escaping matches where the value actually lands.

## False-Positive Conditions

- **Framework default auto-escaping** is used (no explicit "trust as raw HTML" opt-out at that call site).
- **Content Security Policy** with a strict, non-`unsafe-inline` script-src meaningfully reduces (though doesn't always eliminate) impact — note as a compensating control, not an automatic dismissal.
- **The rendered value is genuinely static/code-defined**, not user-influenced.
- **Sanitization library applied** with a configuration that actually strips dangerous markup/attributes for the rendering context in use.

## Severity Notes

Stored XSS: `high` (broader victim reach, persists). Reflected/DOM XSS: `medium` (typically requires social engineering to deliver the crafted link) — escalate to `high` if it can lead to session/credential theft in a sensitive application, per `02_software_context_discovery` context.
