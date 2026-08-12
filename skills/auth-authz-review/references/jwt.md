# JWT

**CWE-347** (improper signature verification) and related · OWASP: Identification and Authentication Failures (A07:2021)

## What to Look For

- **Signature verification actually enforced.** Confirm the code path that validates an incoming JWT calls a verify function (not just decode) and that verification failure actually rejects the request rather than logging and continuing.
- **Algorithm confusion.** Confirm the verification call pins the expected algorithm (e.g. explicitly `RS256`) rather than trusting the algorithm named in the token's own header — a token with `alg: none`, or an RS256-verified token swapped to HS256 using the public key as an HMAC secret, are classic bypasses if the algorithm isn't pinned server-side.
- **Key handling.** Confirm the verification key (secret or public key) is not itself attacker-influenced (e.g. loaded from a `kid` header pointing to an attacker-controlled key source, or a JWKS URL that isn't pinned to a trusted issuer).
- **Claim validation.** Confirm `exp` (and `nbf`/`iat` where relevant) are checked and not ignored; confirm `aud`/`iss` are validated when the token could plausibly be issued for a different audience/issuer than expected.
- **Sensitive data in the payload.** JWT payloads are typically base64-encoded, not encrypted — confirm no secrets are placed in claims assuming confidentiality.

## False-Positive Conditions

- A well-maintained JWT library is used with algorithm explicitly pinned and signature verification confirmed enabled by configuration, not just by default assumption.
- Claims validation (`exp`, `aud`, `iss`) is delegated to and confirmed enforced by a framework's authentication middleware.

## Severity Notes

Algorithm confusion or missing signature verification: `critical` (full authentication bypass). Missing `exp` enforcement: `high` (extends token lifetime beyond intent). Missing `aud`/`iss` validation: severity depends on whether a plausible cross-service/cross-tenant token reuse scenario exists.
