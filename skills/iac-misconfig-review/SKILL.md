---
name: iac-misconfig-review
description: Reviews infrastructure-as-code misconfigurations across Docker, Kubernetes, Terraform, AWS, Azure, and GCP. Use when reviewing IaC files or cloud resource definitions.
---

# IaC Misconfiguration Review

Correlates [run_trivy.py](../../scripts/scanners/run_trivy.py) misconfiguration output with the actual deployment context. Findings here often overlap with [architecture-review](../architecture-review/SKILL.md)'s trust-boundary concerns — a systemic IaC pattern (e.g. every service granted admin-equivalent cloud permissions) may warrant an `ARCH-*` recommendation in addition to (not instead of) specific `SEC-*` findings for concretely dangerous instances.

- [Docker](references/docker.md)
- [Kubernetes](references/kubernetes.md)
- [Terraform](references/terraform.md)
- [AWS](references/aws.md)
- [Azure](references/azure.md)
- [GCP](references/gcp.md)

## Core Discipline

An IaC finding needs to say what's actually deployed with it, not just "this setting is insecure in the abstract" — e.g. a container running as root is a `low` observation on its own, but `high`/`critical` if that container also has a mounted host path or elevated capabilities, since the combination is what enables actual container-escape impact.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json).
