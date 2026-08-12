# Race Conditions

**CWE-362**

## What to Look For

A check-then-act sequence on a shared resource (balance check then deduct, stock check then reserve, single-use coupon check then redeem) with no atomicity guarantee — allowing concurrent requests to both pass the check before either has acted, producing an inconsistent result (double-spend, over-redemption, overselling).

## Evidence to Look For

- The check and the act are separate operations (separate queries/statements) rather than a single atomic operation (e.g. a database `UPDATE ... WHERE balance >= amount` that atomically checks and acts, vs. a `SELECT` followed by a separate `UPDATE`).
- No locking, transaction isolation, or idempotency key protecting the sequence.

## False-Positive Conditions

- The operation is confirmed wrapped in a database transaction with an isolation level (or explicit row lock) that prevents the race in practice.
- An idempotency key or unique constraint at the database level prevents the abusive outcome even if the application-level check has a gap.

## Severity Notes

`high` when exploitable for financial gain (double-spend, coupon abuse) or resource exhaustion; `medium` for lower-stakes inconsistencies.
