# Error Correlation

**CWE-390** (Detection of Error Condition Without Action, adjacent) · OWASP A09:2021

## What to Look For

- **No trace/correlation ID.** When an error occurs, is there a unique identifier (trace ID, request ID, correlation ID) generated at the start of the request and included in both the log entry and, where appropriate, the user-facing error response -- so a user-reported issue ("I got an error at 3pm") can actually be located in the logs? Without one, correlating a specific user complaint to a specific log entry among thousands becomes guesswork.
- **Errors logged with insufficient context.** A caught exception logged as just a message string, with no request path, user identity (where safe), or stack trace, is hard to act on during triage.
- **User-facing error messages that leak internals instead of surfacing a trace ID.** This is the flip side of `knowledge/standards/secure-coding-standard.md` "Errors Don't Leak Internals" -- the fix for over-informative errors is not to say nothing useful, it's to show the user a generic message *plus* a trace ID they can reference, while the actual detail goes to the log. See `prompts/remediation_prompt.md` for the suggested error-message pattern (what happened, likely cause, suggested action -- without a stack trace or internal identifiers).

## Evidence to Look For

- Global error-handling middleware (or its absence) and whether it generates/propagates a correlation ID.
- Catch blocks that log `error.message` alone rather than the structured context needed to act on it.

## False-Positive Conditions

- Correlation IDs are generated and propagated by infrastructure (e.g. an API gateway, a tracing system like OpenTelemetry) not visible in the application code under review -- note this as "not confirmable from this codebase" rather than asserting a confirmed gap, same discipline as other infrastructure-dependent checks in this project.
- The application is small/internal enough (per `02_software_context_discovery`) that this is better captured as an `ARCH-*` hardening recommendation than a standalone finding.

## Severity Notes

Typically `low` to `informational` on its own -- this is primarily an operational/incident-response quality concern, not a directly exploitable vulnerability. Escalate toward `medium` only when combined with genuinely leaked sensitive error detail (see `knowledge/standards/secure-coding-standard.md`), where the finding is really about the leak, with poor correlation as a contributing factor.