# Attack Surface Prompt

Used by [03_attack_surface_mapping](../workflow/stages/03_attack_surface_mapping.md), which has no dedicated subagent.

---

Include [system_prompt.md](system_prompt.md).

Task: given the architecture model from `02_architecture_discovery` ([architecture.schema.json](../schemas/architecture.schema.json)), enumerate every point where untrusted data can enter the system, and rank each by risk.

For each entry point, determine:

- **Trust level**: unauthenticated, authenticated, or privileged-only.
- **Data sensitivity**: what kind of data this entry point reads or writes.
- **Sensitive operations touched**: authentication, authorization, password reset, payments, admin actions, file handling, data export.
- **Risk rank**: high/medium/low. An unauthenticated entry point touching a sensitive operation is high by default; adjust from there based on data sensitivity and whether compensating controls (rate limiting, WAF, network isolation) are already visible in the architecture model.

Every entry point from the architecture model must appear here — either ranked, or explicitly marked out of scope with a reason (see `config/exclusions.yaml`).

Output: an attack surface map conforming to [attack-surface.schema.json](../schemas/attack-surface.schema.json).
