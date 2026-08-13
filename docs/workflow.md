# Workflow

The review pipeline is deterministic and sequential -- 15 stages, defined in `workflow/pipeline.yaml`, documented individually in `workflow/stages/`. No stage is skipped except stage 10, which is skipped by default and only runs when explicitly enabled and authorized.

## The Stages

| # | Stage | Agent | Notes |
|---|---|---|---|
| 01 | Intake | -- | Resolve scope: full repo, diff, or PR. |
| 02 | Software Context Discovery | -- | Business domain, criticality, users -- shapes everything downstream. |
| 03 | Architecture Mapping | `architecture-mapper` | Languages, frameworks, entry points, trust boundaries. |
| 04 | Attack Surface Mapping | -- | Rank entry points by risk. |
| 05 | Static Security Scanning | -- | Semgrep, Gitleaks, Trivy, OSV-Scanner, CISA KEV correlation. |
| 06 | LLM Security Review | `security-reviewer` | Skill-guided analysis; produces `CANDIDATE` findings. |
| 07 | Data Flow Analysis | -- | Deepens an incomplete source-to-sink trace on demand. |
| 08 | Security Triage | -- | Dedup, normalize, assign preliminary severity. |
| 09 | Independent Verification | `security-verifier` | Actively tries to disprove each candidate. |
| 10 | Dynamic / Pentest Validation | `pentest-validator` | **Optional, off by default.** |
| 11 | Security Prioritization | -- | `calculate_priorities.py`, KEV-floor overrides applied. |
| 12 | Architecture Assessment | `architecture-advisor` | Current-state evaluation, no recommendations yet. |
| 13 | Security Architecture Recommendations | `architecture-advisor` | `ARCH-*` records. |
| 14 | Remediation Analysis | -- | Actionable, text-only guidance per confirmed finding. |
| 15 | Final Report | -- | Dual-axis Markdown/JSON/SARIF output. |

## Why This Shape

The split between "candidate" (06), "verified" (09), and "prioritized" (11) exists so that no single pass has to be simultaneously creative (find things) and skeptical (disprove things) -- see CLAUDE.md's Core Design Principle. Splitting architecture assessment (12) from recommendations (13) similarly keeps "what is" from being pre-biased by "what I'd change."

## Routing

`workflow/routing_rules.yaml` decides which Skills apply during stage 06, based on file patterns, detected frameworks, and entry-point types from the architecture model. `secure-code-review` and `secrets-detection` always run regardless of routing.

## Running It

There's no single "run the pipeline" command -- stages with an agent are invoked as that agent; stages without one run in the orchestrating Claude Code session using the corresponding `prompts/*.md` fragment and `scripts/` tooling. See `docs/usage.md` for a walkthrough.
