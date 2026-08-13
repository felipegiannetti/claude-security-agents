# Prioritization

`scripts/reporting/calculate_priorities.py` computes each confirmed finding's priority from `config/priority.config.yaml`. This document explains the formula so a priority number is never a black box.

## The Formula

1. Start from a severity base score: `critical=100, high=75, medium=50, low=25, informational=0`.
2. Apply weighted adjustments (see `config/priority.config.yaml` → `weights`):
   - **Exploitability** -- proof-of-concept available, trivial to exploit, or requires chained conditions.
   - **Exposure** -- internet-facing unauthenticated (+20), internet-facing authenticated (+10), internal-only (-10).
   - **Privileges required** -- none (+10), user (0), privileged/admin (-15).
   - **Affected data sensitivity** -- payment/credentials (+15), PII/health (+10).
   - **Blast radius** -- platform-wide (+25), multi-tenant (+15), single-tenant (0).
   - **Confidence** -- LOW findings get -25, which keeps low-confidence candidates out of P0/P1 regardless of severity.
   - **Remediation effort** -- trivial fixes get a small urgency boost (+10); large-effort fixes get -5. Cheap fixes have no excuse to sit in the backlog.
3. Bucket the resulting score into `P0` (>=90) through `P4` (<15) per `score_thresholds`.
4. Apply the **CISA KEV floor** last: a `kev.listed: true` finding is floored at `P1` (or `P0` if there's known ransomware campaign use) -- see `skills/dependency-cve-check/references/kev-correlation.md`. This is a floor, never a downgrade.

Some inputs (data sensitivity, blast radius, exploitability) are inferred from free-text finding fields via documented keyword heuristics when `priority_factors` isn't set explicitly -- see the script's own docstring for exactly which keywords. Prefer setting `priority_factors` explicitly when precision matters.

## Why Not Just Use Severity

CLAUDE.md is explicit that severity and priority are different questions. A `critical`-severity finding that needs privileged internal access and has no proof of concept might reasonably sit at `P2` while a `medium`-severity finding that's internet-facing, unauthenticated, and trivial to fix sits at `P0`.

## Architecture Recommendations Use a Different Scale

`ARCH-P0` through `ARCH-P3` (see `schemas/architecture-recommendation.schema.json`) is a structurally separate scale from `P0`-`P4` -- never conflate a "critical architectural risk" with a "P0 vulnerability." See `skills/architecture-review/SKILL.md`.
