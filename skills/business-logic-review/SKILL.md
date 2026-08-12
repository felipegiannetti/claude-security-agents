---
name: business-logic-review
description: Reviews business-logic flaws - race conditions, workflow bypass, payment security, privilege escalation, tenant isolation, and state manipulation. Use for logic that isn't a classic OWASP vulnerability class but can still be abused.
---

# Business Logic Review

This category has no universal pattern to search for — unlike injection or XSS, business logic flaws are specific to *this application's* rules. Requires the software context ([02_software_context_discovery](../../workflow/stages/02_software_context_discovery.md)) and architecture model more than any other Skill: you can't spot a workflow bypass without first understanding what the workflow is supposed to enforce.

- [Race Conditions](references/race-conditions.md)
- [Workflow Bypass](references/workflow-bypass.md)
- [Payment Security](references/payment-security.md)
- [Privilege Escalation](references/privilege-escalation.md)
- [Tenant Isolation](references/tenant-isolation.md)
- [State Manipulation](references/state-manipulation.md)

## Core Discipline

For each business process (checkout, approval workflow, account upgrade, multi-step onboarding), ask: what invariant is this process supposed to enforce, and is that invariant checked at every step where it could be violated — not just the "front door"? A common pattern: a check enforced in step 1 of a multi-step flow but not re-verified in step 3, letting an attacker skip directly to step 3.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json). These findings often need an especially concrete `exploitation_scenario` since the vulnerability class name alone (e.g. "workflow bypass") doesn't convey the specific abuse the way "SQL injection" does.
