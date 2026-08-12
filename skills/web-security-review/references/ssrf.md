# Server-Side Request Forgery (SSRF)

**CWE-918** · OWASP: Server-Side Request Forgery (A10:2021)

## What to Look For

Attacker-influenced data controlling (fully or partially — including just the host/port) a URL that the *server* then fetches — webhooks, URL preview/unfurling features, image/file fetch-by-URL, PDF/document generation from a URL, "import from URL" features, and integrations that build outbound request URLs from configuration/data an attacker can influence.

## Source-to-Sink Checklist

1. Confirm the destination URL/host is attacker-influenced, even partially (e.g. only the path is user-controlled but the host is fixed is *not* SSRF; the host being user-controlled or user-influenced *is*).
2. Confirm what the server does with the response — SSRF impact ranges from blind (no response returned to attacker) to full response reflection, which materially changes exploitability and impact.
3. Check specifically for access to internal-only targets: cloud metadata endpoints (a classic high-impact SSRF target), internal service ports, `localhost`/loopback, private IP ranges, and internal DNS names.
4. Check for allowlist/blocklist bypass techniques if a filter exists: DNS rebinding, redirects (does the fetch follow redirects to a disallowed target after passing the initial check?), alternate IP representations (decimal/octal/hex encoding), and IPv6 equivalents of blocked IPv4 ranges.

## False-Positive Conditions

- **Strict destination allowlist** validated against the *resolved* IP (not just the input hostname, which can be resolved differently at fetch time — see DNS rebinding above) and enforced with no redirect-following past the check.
- **Network-level egress restriction** confirmed to block internal targets regardless of application-level validation (a genuine compensating control — but application-level validation should still be recommended per defense-in-depth, at lower priority).
- **The "URL" is entirely code-defined**, with user input only selecting from a small set of pre-approved, hardcoded targets (e.g. an enum, not a raw string).

## Severity Notes

Unrestricted SSRF reaching cloud metadata endpoints or internal admin interfaces: `critical`. SSRF restricted to external targets only (no internal network reach) but still attacker-directed: `medium` to `high` depending on what the response is used for.
