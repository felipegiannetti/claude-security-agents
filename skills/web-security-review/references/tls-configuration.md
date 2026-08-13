# TLS Configuration

**CWE-295** (improper certificate validation) / **CWE-326** (inadequate encryption strength) / **CWE-319** (cleartext transmission) · OWASP: Cryptographic Failures (A02:2021)

## What to Look For

Unlike most findings in this Skill, TLS configuration is as much an
infrastructure/deployment concern as a code concern — treat findings here as
frequently belonging in the Architecture axis (`ARCH-*`, hardening
recommendation) rather than the Application Security axis (`SEC-*`,
confirmed vulnerability), unless the misconfiguration is directly expressed
in application code (e.g. a hardcoded HTTP URL, or certificate validation
explicitly disabled in an HTTP client).

- **Self-signed or untrusted certificates accepted in production code paths.**
  Look for HTTP client configuration that disables certificate verification
  (`rejectUnauthorized: false` in Node, `verify=False` in Python `requests`,
  `InsecureSkipVerify: true` in Go, a custom `TrustManager` that accepts
  everything in Java) — this is a direct MITM-enabler, not a hardening note,
  and should be a confirmed `SEC-*` finding when found in application code
  that talks to any external or untrusted-network endpoint.
- **Weak or deprecated TLS protocol versions.** TLS 1.0/1.1 and SSLv3 are
  deprecated and have known weaknesses (BEAST, POODLE, and others); flag
  explicit protocol pinning to these versions, or a server/client
  configuration that doesn't enforce a TLS 1.2+ floor.
- **Weak cipher suites.** Explicit allowance of RC4, 3DES, export-grade, or
  NULL ciphers, or a cipher list that doesn't prioritize forward-secrecy
  (ECDHE/DHE) suites.
- **Non-standard ports for TLS-protected services** are not a vulnerability
  by themselves (security by obscurity doesn't help or hurt directly), but
  note them as an architecture observation when they diverge from documented
  infrastructure conventions — they can indicate an undocumented service or
  a misconfigured proxy/load-balancer, which is a discovery-quality issue
  for `03_architecture_mapping`/`13_security_architecture_recommendations`
  more than a security finding on its own.
- **Plaintext fallback.** A server or client that will silently downgrade to
  HTTP if HTTPS negotiation fails, rather than failing closed.

## False-Positive Conditions

- Certificate validation is disabled only in test/local-development
  configuration, gated behind an environment check that can't reach
  production (e.g. `if (process.env.NODE_ENV === "test")`) — confirm the
  gate is genuine and not trivially bypassable before downgrading; note the
  scope explicitly either way.
- TLS termination happens at a load balancer/reverse proxy/CDN not visible
  in the repository, and internal (post-termination) traffic stays within a
  trusted private network boundary — note as "not confirmable from this
  codebase; recommend verifying infrastructure-level TLS termination policy"
  rather than a confirmed finding, per the same pattern as
  [security-headers.md](security-headers.md).
- A pinned older TLS version is required for compatibility with a specific,
  named legacy integration partner and is scoped narrowly to that one
  connection — this is a real risk tradeoff, not a false positive, but
  should be reported as a scoped, justified exception rather than a blanket
  "weak TLS" finding across the whole application.

## Severity Notes

- Disabled certificate validation reachable from application code handling
  any real network traffic: `high` to `critical` per
  `config/severity.config.yaml`, depending on what data crosses that
  connection (credentials/PII/financial data pushes toward critical).
- Deprecated protocol versions or weak ciphers, with no evidence of
  exploitation path beyond the protocol weakness itself: `medium`.
- Non-standard ports and infrastructure-level TLS observations that
  couldn't be confirmed from the codebase: treat as `ARCH-*` hardening
  recommendations (P4-adjacent) rather than confirmed findings, per
  `13_security_architecture_recommendations`.