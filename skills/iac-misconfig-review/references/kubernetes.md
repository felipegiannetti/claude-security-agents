# Kubernetes

**CWE-16**

## What to Look For

- **Privileged containers / excessive capabilities**: `privileged: true`, or added Linux capabilities beyond what the workload needs — see [docker.md](docker.md), amplified at the orchestration level.
- **Host namespace sharing**: `hostNetwork`, `hostPID`, `hostIPC` set to true — breaks container isolation from the host.
- **Missing resource limits**: no CPU/memory limits, enabling a single compromised/misbehaving pod to exhaust node resources (a [rate-limiting.md](../../api-security-review/references/rate-limiting.md)-adjacent concern at the infrastructure level).
- **Overly broad RBAC**: a ServiceAccount bound to `cluster-admin` or a wildcard role when the workload needs a narrow set of permissions.
- **Secrets as plain environment variables** rather than mounted Kubernetes Secrets (or better, an external secret manager) — env vars are more easily leaked via logs, crash dumps, or child process inheritance.
- **No NetworkPolicy** — default-allow pod-to-pod communication means a compromised pod can reach anything in the cluster.

## False-Positive Conditions

- Privileged access/host namespace sharing is confirmed necessary for the workload's legitimate function (e.g. a node-monitoring daemonset) and scoped narrowly.

## Severity Notes

Privileged container or `cluster-admin` RBAC binding for a workload that doesn't need it: `high`. Missing NetworkPolicy / missing resource limits: `medium`, often better captured as an `ARCH-*` recommendation if it's a cluster-wide pattern rather than one workload.
