# Sensitive Data in Logs

**CWE-532** (Insertion of Sensitive Information into Log File) · OWASP A09:2021

## What to Look For

Logging statements (application logs, access logs, error logs, third-party logging/APM service calls) that include:

- Passwords, tokens, session IDs, API keys, or other credentials -- even when logging a "failed login attempt" or an error, the credential value itself must never be included.
- Full request/response bodies logged indiscriminately (`log.info(req.body)` / `log.debug(response)`-style calls) -- these frequently capture whatever sensitive fields the endpoint happens to handle, without the developer having deliberately chosen to log them.
- Personally identifiable information beyond what's operationally necessary (full card numbers, government ID numbers, health data) in plaintext.

This is functionally a [secrets-detection](../../secrets-detection/SKILL.md)-adjacent concern, but the mechanism is different: `secrets-detection` looks for a credential hardcoded in *source*; this looks for a credential (or other sensitive value) flowing into a *logging sink at runtime* -- the log files/log aggregation service become a new, often less-protected copy of the sensitive data.

## Evidence to Look For

- A log statement whose argument is the entire request/response object, a whole user/entity object, or a caught exception's full context, rather than an explicit, deliberate list of safe fields.
- Log statements inside authentication/password-reset/payment code paths specifically -- these are the highest-risk locations for this pattern.

## False-Positive Conditions

- The logging call explicitly allowlists safe fields (e.g. `log.info({userId, action})`) rather than logging an entire object.
- The value is masked/redacted before logging (e.g. the same masking discipline described in `.claude/rules/security.md` "Secrets Handling" -- `AKIA****...` rather than the full value) and the masking is confirmed to actually execute on the code path in question, not just exist as an unused utility function.
- Logs are confirmed to go only to a tightly access-controlled, encrypted-at-rest destination AND the specific value is operationally necessary there (rare -- treat as an exception requiring explicit justification, not a default).

## Severity Notes

Credentials or tokens logged in plaintext: `high` -- log files/aggregation services are frequently more broadly accessible (to support/ops/monitoring teams, third-party log-aggregation vendors) than the primary datastore, meaningfully widening exposure. Broader PII over-logging: `medium`.