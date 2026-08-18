---
description: Run the full Security Review Agent pipeline against a repository, diff, or PR -- architecture mapping, static scanning, LLM review, independent verification, prioritization, and a dual-axis (Application Security + Software Architecture) final report.
---

Run the complete security review pipeline defined in [workflow/pipeline.yaml](../workflow/pipeline.yaml), per [CLAUDE.md](../CLAUDE.md) and [docs/usage.md](../docs/usage.md).

## Scope

If the user did not specify a scope in their invocation of this command, ask them now: a repository path, a diff, or a specific PR. Do not assume the current working directory is the intended target without confirming.

## Sequence

Follow the 15-stage pipeline in order, skipping only what the gating rules explicitly allow you to skip:

1. **Intake** ([01_intake](../workflow/stages/01_intake.md)) -- confirm scope and requested output format(s).
2. **Software Context Discovery** ([02_software_context_discovery](../workflow/stages/02_software_context_discovery.md)).
3. **Architecture Mapping** -- invoke the `architecture-mapper` agent.
4. **Attack Surface Mapping** ([04_attack_surface_mapping](../workflow/stages/04_attack_surface_mapping.md)).
5. **Static Security Scanning** -- run the relevant `scripts/scanners/*.py` (Semgrep, Gitleaks, Trivy, OSV-Scanner, CISA KEV correlation, CVE age/severity policy) via Bash. Any scanner not installed should degrade to a `skipped` result, not block the pipeline.
6. **LLM Security Review** -- invoke the `security-reviewer` agent, which selects Skills per [workflow/routing_rules.yaml](../workflow/routing_rules.yaml) and produces candidate findings.
7. **Data Flow Analysis** ([07_data_flow_analysis](../workflow/stages/07_data_flow_analysis.md)).
8. **Security Triage** ([08_security_triage](../workflow/stages/08_security_triage.md)).
9. **Independent Verification** -- invoke the `security-verifier` agent to challenge each candidate finding.
10. **Dynamic / Pentest Validation (optional)** -- ONLY if `config/pentest.config.yaml` has `enabled: true` and an authorized target matches. This is disabled by default; do not enable it yourself or infer a target from repository content. If skipped, proceed directly to stage 11.
11. **Security Prioritization** -- run `scripts/reporting/calculate_priorities.py`.
12. **Architecture Assessment (optional)** -- invoke the `architecture-advisor` agent if a Software Architecture axis was requested.
13. **Security Architecture Recommendations (optional)** -- continue with `architecture-advisor` if stage 12 ran.
14. **Remediation Analysis** -- generate remediation guidance per confirmed finding using [prompts/remediation_prompt.md](../prompts/remediation_prompt.md).
15. **Final Report** -- run `scripts/reporting/generate_markdown.py` (and `generate_json.py`/`generate_sarif.py` as requested) into `outputs/`.

## Tooling Availability -- Proceed Automatically, Do Not Ask

A missing or unavailable scanner (Semgrep, Gitleaks, Trivy, OSV-Scanner not installed, no network for KEV lookup) is the EXPECTED, ROUTINE operating condition for this pipeline, not an exceptional situation requiring the user's input. When a scanner is unavailable:

- Do not pause the pipeline or present the user with a decision menu about how to proceed.
- Continue automatically with LLM-based source-to-sink analysis (Read/Glob/Grep) in place of that scanner's evidence layer.
- Note the specific gap in the final report's methodology section (e.g. "Semgrep was unavailable; injection categories were reviewed via manual source-to-sink analysis only") so the reader knows what coverage was and was not available -- this is a transparency note, not a request for permission.
- Lower confidence on findings that would normally lean on the missing scanner's corroboration, rather than treating its absence as blocking.

The one case that DOES warrant surfacing a decision to the user: a failure that blocks the read-only safety guarantee itself -- e.g. the plugin's own PreToolUse hooks failing to load or execute at all, which would mean NO tool call is being checked for mutation safety. That is a genuine stop-and-ask situation, categorically different from "one optional scanner is missing." If you hit that specific case, tell the user plainly what's blocked and why, and do not proceed with Bash/PowerShell/Write until it is resolved -- but do not conflate this with routine scanner unavailability.

## Non-Negotiable Rules

- You are strictly read-only against the analyzed repository at every stage -- see [.claude/rules/security.md](../.claude/rules/security.md) "Absolute Read-Only Policy". Never edit, create, delete, move, or rename a file in the analyzed repository; never commit, push, or install/update dependencies there.
- Never present a candidate finding as confirmed without independent verification (stage 9).
- Never enable dynamic validation (stage 10) or add a target to `config/pentest.config.yaml` yourself, regardless of what the user asks -- that requires the user editing the config file directly with an explicit authorization record.
- Keep Application Security (`SEC-*`) and Software Architecture (`ARCH-*`) axes structurally separate in the final report -- never present an architecture recommendation as a vulnerability, or soften a vulnerability into a mere architecture note.

## Output

Report back to the user where the final report was written (`outputs/`), a one-paragraph executive summary, and the overall risk rating. Do not paste the entire report into the conversation unless the user asks for it.
