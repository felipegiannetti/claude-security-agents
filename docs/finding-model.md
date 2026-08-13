# The Finding Model

Every vulnerability finding in this project conforms to `schemas/finding.schema.json`. This document explains the shape and why it looks the way it does.

## Lifecycle

```
CANDIDATE -> TRIAGED -> CONFIRMED
                      -> REJECTED
                      -> NEEDS_MORE_EVIDENCE
```

Only `CONFIRMED` findings appear as confirmed vulnerabilities in the final report. A `REJECTED` finding is not a failure of the process -- CLAUDE.md is explicit that "a rejected false positive is a successful verification result."

## Three Independent Evidence Layers

A finding can carry up to three, tracked separately and never merged into one number:

1. **Static Analysis** -- `security-reviewer`'s scanner correlation + source-to-sink reasoning (stage 06).
2. **Independent Verification** -- `security-verifier`'s attempt to disprove it by re-deriving the claim from code alone (stage 09). Populates the `verification` field.
3. **Dynamic Validation** -- `pentest-validator`'s optional, disabled-by-default confirmation against a running, authorized target (stage 10). Populates the `dynamic_validation` field. Absence means "not attempted," never "failed."

## Severity vs. Priority vs. Confidence

Three separate axes, easy to conflate:

- **Severity** -- technical/business impact. See `config/severity.config.yaml`.
- **Priority** (`P0`-`P4`) -- remediation urgency. A function of severity *plus* exploitability, exposure, privileges required, data sensitivity, blast radius, confidence, and remediation effort -- see `config/priority.config.yaml`'s `weights`. A trivial-effort critical finding and a large-effort critical finding are not automatically the same priority.
- **Confidence** (`HIGH`/`MEDIUM`/`LOW`) -- how much of the claimed path was actually confirmed vs. assumed. See `knowledge/standards/confidence-matrix.yaml`.

## Source-to-Sink Fields

`source`, `sink`, and `data_flow` follow the model from CLAUDE.md's Core Design Principle:

```
SOURCE -> PARSING -> TRANSFORMATION -> VALIDATION -> AUTHENTICATION -> AUTHORIZATION -> BUSINESS LOGIC -> SINK
```

Each `data_flow` step has a `confirmed` boolean -- whether that step was actually read in code (`true`) or inferred (`false`). This is what lets `confidence` be an honest, auditable value instead of a vibe.

## Dependency Findings: the `kev` Field

For `vulnerable-dependency` findings, the `kev` field (populated by `scripts/scanners/check_kev.py`) records CISA KEV correlation -- whether the CVE is actively exploited in the wild. This affects *priority*, not severity -- see `skills/dependency-cve-check/references/kev-correlation.md`.

## Cross-Referencing Architecture Recommendations

`related_architecture_recommendations` links a finding to `ARCH-*` records (see `schemas/architecture-recommendation.schema.json`) whose implementation would address the finding's structural root cause. This is informational only -- fixing the architecture is never a substitute for fixing the individual finding.
