---
name: logging-audit-review
description: Reviews security logging and audit trail adequacy - authentication/session/failed-attempt logging, sensitive data leaking into logs, audit trail integrity (including impersonation/"login as" tracking), and error correlation (trace IDs). The dedicated owner of OWASP A09:2021 - Security Logging and Monitoring Failures, which previously had no Skill covering it directly.
---

# Logging & Audit Review

Builds on [secure-code-review](../secure-code-review/SKILL.md). Unlike most Skills, this one produces findings about *absence* (a missing log) as often as about *presence* (a log that leaks something it shouldn't) -- both are equally real findings, not just hardening notes.

- [Insufficient Logging](references/insufficient-logging.md)
- [Sensitive Data in Logs](references/sensitive-data-in-logs.md)
- [Audit Trail Integrity](references/audit-trail-integrity.md)
- [Error Correlation](references/error-correlation.md)

## When to Use

Whenever the architecture model shows authentication, session management, or privileged/administrative actions (see [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml)) -- these are exactly the events that must be logged for incident response and compliance audits to be possible after the fact.

## Core Discipline

A missing log is invisible until the moment it's needed -- during an actual incident, when it's too late to add it. Evaluate logging coverage against a concrete question: "if this specific action turned out to be malicious, could the team reconstruct who did what, when, and from where, after the fact?" If the answer is no for a security-relevant action (login, failed login, permission change, privileged action, data export, impersonation), that's a finding.

Equally, logging is not an unconditional good -- a log that captures a password, a session token, or other sensitive data has turned the logging system itself into a new sensitive-data store, often with weaker access controls than the primary datastore. See [sensitive-data-in-logs.md](references/sensitive-data-in-logs.md).

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json). Common categories: `insufficient-security-logging`, `sensitive-data-exposure-in-logs`, `missing-audit-trail`, `insufficient-error-correlation`.