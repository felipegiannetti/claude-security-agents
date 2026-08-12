# Webhook Security

Covers both directions: receiving webhooks (inbound) and sending them (outbound, see [ssrf.md](../../web-security-review/references/ssrf.md) for the outbound-URL angle).

## What to Look For (Inbound)

- **Signature verification**: confirm incoming webhook payloads are verified against a shared secret/signature (e.g. HMAC of the payload) before being trusted — an unverified webhook endpoint lets anyone who finds the URL submit fake events.
- **Replay protection**: confirm a timestamp/nonce check prevents a captured, valid webhook payload from being replayed.
- **Payload treated as untrusted input**: webhook payload fields still need the same source-sink discipline as any other external input (see [secure-code-review](../../secure-code-review/SKILL.md)) — a "trusted" webhook source doesn't mean its content is safe to use unsanitized in a query/command/template.

## False-Positive Conditions

- Signature verification confirmed present and actually enforced (rejects on mismatch, not just logs).
- The webhook endpoint's actions are genuinely low-impact even if spoofed.

## Severity Notes

Missing signature verification on a webhook triggering a sensitive action (order fulfillment, payment status change, account state change): `high` to `critical`.
