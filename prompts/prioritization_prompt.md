# Prioritization Prompt

`11_security_prioritization` is a deterministic calculation ([calculate_priorities.py](../scripts/reporting/calculate_priorities.py) against [priority.config.yaml](../config/priority.config.yaml)), not an LLM judgment call — priority should be reproducible, not vibes-based. This prompt is for the narrow follow-up task of turning the computed score into a short, readable justification for the report.

---

Task: given a `CONFIRMED` finding with its computed `priority` and `priority_factors` ([finding.schema.json](../schemas/finding.schema.json)), write one or two sentences explaining *why* it landed at that priority — referencing the specific factors that moved the score (e.g. "P0 despite medium technical severity, because it's unauthenticated, internet-facing, and the fix is trivial" or "P2 despite critical severity, because exploitation requires an already-privileged internal account and no proof of concept was confirmed").

Do not re-derive the priority yourself or override the computed value — explain the number that `calculate_priorities.py` already produced. If the explanation doesn't make sense given the factors, that's a signal to check the calculation/config, not to substitute your own judgment silently.
