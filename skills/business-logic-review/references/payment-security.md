# Payment Security

Combines several other references applied to the highest-stakes business flow in most applications that have one.

## What to Look For

- **Price/amount determined client-side**: the server trusts a price, quantity, or total submitted by the client rather than recalculating it server-side from authoritative data — see [state-manipulation.md](state-manipulation.md).
- **Payment confirmation not independently verified**: the application marks an order as paid based on a client-side redirect/callback parameter rather than a server-to-server webhook verified per [webhook-security.md](../../api-security-review/references/webhook-security.md).
- **Race conditions on balance/inventory**: see [race-conditions.md](race-conditions.md).
- **Currency/rounding manipulation**: negative quantities, currency confusion, or rounding exploited across many small transactions.

## False-Positive Conditions

- Price/total is always recalculated server-side from the authoritative product/pricing data, with client input used only to select *which* items, never their price.
- Payment status is confirmed only via a signature-verified server-to-server webhook, never a client-controlled parameter.

## Severity Notes

`critical` for any path allowing an attacker to pay less than the correct amount, or to mark an order paid without actually paying.
