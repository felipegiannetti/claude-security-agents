# Stage 08: Verification

## Purpose

Independently challenge every triaged finding. This is the stage that separates this project's findings from raw scanner output — nothing reaches the final report as a confirmed vulnerability without surviving an adversarial second pass (see CLAUDE.md's Independent Verification and [security-verifier.md](../../agents/security-verifier.md)).

## Agent

[security-verifier](../../agents/security-verifier.md)

## Inputs

- `TRIAGED` findings from `07_triage`.
- The architecture model (for authentication/authorization/framework context).

## Process

See [security-verifier.md](../../agents/security-verifier.md) in full: attacker control, reachability, authentication/authorization validation, framework and compensating controls, scanner correlation, dependency version verification, severity/confidence review.

## Outputs

- Each finding transitions to one of: `CONFIRMED`, `REJECTED`, or `NEEDS_MORE_EVIDENCE`, with verification evidence and, for rejections, an explicit rejection reason.

## Success Criteria

- Every `CONFIRMED` finding has a verified attack path, not just a restated candidate claim.
- Every `REJECTED` finding has a documented reason, so patterns of false positives can be fed back into the relevant Skill's false-positive criteria over time (see [testing.md](../../.claude/rules/testing.md)).
