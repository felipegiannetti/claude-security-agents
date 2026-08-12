# Stage 09: Independent Verification

## Purpose

Independently challenge every triaged finding. This is the stage that separates this project's findings from raw scanner output — nothing reaches the final report as a confirmed vulnerability without surviving an adversarial second pass (see CLAUDE.md's Independent Verification and [security-verifier.md](../../agents/security-verifier.md)).

## Agent

[security-verifier](../../agents/security-verifier.md)

## Inputs

- `TRIAGED` findings from `08_security_triage`.
- The architecture model (for authentication/authorization/framework context).

## Process

See [security-verifier.md](../../agents/security-verifier.md) in full: attacker control, reachability, authentication/authorization validation, framework and compensating controls, scanner correlation, dependency version verification, severity/confidence review.

## Outputs

- Each finding transitions to one of: `CONFIRMED`, `REJECTED`, or `NEEDS_MORE_EVIDENCE`, with verification evidence and, for rejections, an explicit rejection reason.
- Findings that could benefit from real-world confirmation (e.g. a BOLA/IDOR, SSRF, or auth/authz finding where static evidence alone leaves residual doubt) are flagged as dynamic-validation candidates for `10_dynamic_pentest_validation` — that stage only runs if it's also enabled and authorized per `config/pentest.config.yaml`; it is never assumed.

## Success Criteria

- Every `CONFIRMED` finding has a verified attack path, not just a restated candidate claim.
- Every `REJECTED` finding has a documented reason, so patterns of false positives can be fed back into the relevant Skill's false-positive criteria over time (see [testing.md](../../.claude/rules/testing.md)).
