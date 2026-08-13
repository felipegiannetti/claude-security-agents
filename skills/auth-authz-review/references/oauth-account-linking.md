# OAuth / Identity Provider Account Linking

**CWE-287** (Improper Authentication, adjacent) -- extends [oauth-oidc.md](oauth-oidc.md) specifically for the account-linking step: mapping an external identity (corporate IdP, federated partner IdP) onto an existing internal account.

## What to Look For

- **Automatic linking by unverified email.** The most common real vulnerability here: the application receives an email claim from the IdP's token and automatically links/logs into whichever internal account has a matching email address, without confirming the IdP itself has verified that email. If any IdP in a multi-IdP setup allows a user to set an arbitrary, unverified email claim (common with some federated/partner IdPs, or a misconfigured OIDC provider), an attacker can register with a victim's email at the weaker IdP and be automatically linked into the victim's account at the relying application.
- **Cross-IdP identity confusion.** When multiple IdPs are supported (e.g. a corporate IdP for internal users and a federated IdP for external partners, as in the PDF's "usuários internos" / "usuários externos" split), check whether the linking logic distinguishes *which* IdP asserted the identity, not just the claimed identifier value -- an external, less-trusted IdP asserting the same email as an internal corporate account should not silently grant access to the internal account.
- **Manual linking with insufficient verification.** Where manual account linking exists (e.g. linking by a national ID number, as in the PDF's CPF example), confirm the linking step requires proof of ownership of both identities, not just knowledge of an identifier value that could be guessed or looked up.
- **Shared/non-individualized accounts with no responsible-party tracking.** Where a login represents a shared or role-based account rather than an individual, check whether the specific human operating it at any given time is recorded -- otherwise actions taken through the shared account aren't attributable to anyone, which is both an authorization and an audit gap (see `skills/logging-audit-review/references/audit-trail-integrity.md`).

## Evidence to Look For

- Account-linking code that queries `WHERE email = ?` using the IdP token's email claim, with no check of an `email_verified` claim (present in standard OIDC ID tokens) or equivalent.
- A single linking code path shared across multiple configured IdPs with no per-IdP trust level distinction.

## False-Positive Conditions

- The linking logic explicitly checks `email_verified: true` (or the equivalent for the specific IdP) before treating the email claim as authoritative.
- Only a single, fully-trusted corporate IdP is configured, and that IdP is confirmed to only assert verified emails by policy -- lower risk, but still worth noting if a second, less-trusted IdP could plausibly be added later without revisiting this logic.

## Severity Notes

Automatic linking on an unverified email claim, reachable from any configured IdP: `critical` -- this is a direct account-takeover path. Cross-IdP identity confusion allowing an external/partner identity to reach an internal account: `critical`. Manual linking with weak identifier-only verification: `high`.