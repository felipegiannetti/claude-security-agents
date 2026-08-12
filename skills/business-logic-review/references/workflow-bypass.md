# Workflow Bypass

**CWE-841**

## What to Look For

A multi-step process (onboarding, approval chain, checkout) where a later step doesn't re-verify that earlier required steps actually completed — letting an attacker call the later step's endpoint directly, skipping validation/approval/payment that the intended flow assumes happened first.

## Evidence to Look For

- Each step's endpoint checked independently: does step N verify step N-1's completion via server-side state, or does it only trust that the client navigated there in order (which the client fully controls)?
- State transitions enforced by a state machine / explicit status field with server-side transition validation, vs. implicit ordering assumed only by the UI.

## False-Positive Conditions

- Server-side state (e.g. an order status field) is checked at each step and a skipped prerequisite is rejected.
- The "skippable" step is genuinely optional by design, not a security control.

## Severity Notes

`high` to `critical` depending on what's bypassed — skipping payment in a checkout flow or skipping an approval gate for a privileged action are severe; skipping a cosmetic step is not a security finding at all.
