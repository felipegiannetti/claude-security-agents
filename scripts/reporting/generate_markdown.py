#!/usr/bin/env python3
"""Generate Markdown

Deterministically renders a report.schema.json-shaped document (prose fields
already filled in by the pipeline's LLM stages -- this script formats, it
does not write prose) into the Markdown structure defined by
prompts/report_template.md and prompts/finding_template.md, for
15_final_report.

Usage:
    generate_markdown.py --input report.json [--output report.md]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

PRIORITY_LABELS = {"P0": "Immediate", "P1": "High", "P2": "Medium", "P3": "Low", "P4": "Informational"}


def render_finding(f: dict) -> str:
    loc = f.get("location") or {}
    lines = [
        f"### {f.get('id', '?')} — {f.get('title', '')}",
        "",
        "| | |",
        "|---|---|",
        f"| **Severity** | {f.get('severity', '')} |",
        f"| **Priority** | {f.get('priority', '')} — {PRIORITY_LABELS.get(f.get('priority'), '')} |",
        f"| **Confidence** | {f.get('confidence', '')} |",
        f"| **Category** | {f.get('category', '')} |",
    ]
    if f.get("cwe"):
        lines.append(f"| **CWE** | {f['cwe']} |")
    if f.get("owasp_category"):
        lines.append(f"| **OWASP** | {f['owasp_category']} |")
    lines.append(f"| **Location** | `{loc.get('file', '')}:{loc.get('line_start', '')}` |")
    lines.append("")

    if f.get("evidence"):
        lines.append("**Evidence**")
        lines.append("")
        for ev in f["evidence"]:
            lines.append("```")
            lines.append(ev.get("snippet", ""))
            lines.append("```")
        lines.append("")

    if f.get("attack_vector"):
        lines += ["**Attack Vector**", "", f["attack_vector"], ""]
    if f.get("exploitation_scenario"):
        lines += ["**Exploitation Scenario**", "", f["exploitation_scenario"], ""]

    remediation = f.get("remediation") or {}
    if remediation:
        lines += ["**Remediation**", "", remediation.get("summary", ""), "", remediation.get("fix_guidance", "")]
        if remediation.get("effort"):
            lines += ["", f"Estimated effort: {remediation['effort']}"]
        if remediation.get("verification_steps"):
            lines += ["", "**Verification Steps**", ""]
            lines += [f"- [ ] {step}" for step in remediation["verification_steps"]]
        lines.append("")

    layers = ["**Evidence Layers**", ""]
    layers.append(f"- Static Analysis: candidate identified by security-reviewer")
    verification = f.get("verification") or {}
    if verification.get("exploitability_conclusion"):
        layers.append(f"- Independent Verification: {verification['exploitability_conclusion']}")
    dynamic = f.get("dynamic_validation") or {}
    if dynamic.get("performed"):
        layers.append(f"- Dynamic Validation: {dynamic.get('result')} — {dynamic.get('observation', '')}")
    lines += layers + [""]

    if f.get("related_architecture_recommendations"):
        lines += ["**Related Architecture Recommendations**", ""]
        lines += [f"- {rid}" for rid in f["related_architecture_recommendations"]]
        lines.append("")

    return "\n".join(lines)


def render_recommendation(r: dict) -> str:
    lines = [
        f"### {r.get('id', '?')} — {r.get('title', '')}",
        "",
        f"**Priority:** {r.get('priority', '')}  ",
        f"**Category:** {r.get('category', '')}",
        "",
        "**Assessed Problem**", "", r.get("assessed_problem", ""), "",
        "**Recommendation**", "", r.get("recommendation", ""), "",
        "**Rationale**", "", r.get("rationale", ""), "",
    ]
    if r.get("security_implications"):
        lines += ["**Security Implications**", "", r["security_implications"], ""]
    if r.get("benefits"):
        lines += ["**Benefits**", ""] + [f"- {b}" for b in r["benefits"]] + [""]
    if r.get("costs"):
        lines += ["**Costs**", ""] + [f"- {c}" for c in r["costs"]] + [""]
    if r.get("phased_path"):
        lines += ["**Phased Path**", ""]
        lines += [f"{step.get('step')}. {step.get('description')}" for step in r["phased_path"]]
        lines.append("")
    return "\n".join(lines)


def render(report: dict) -> str:
    metadata = report.get("metadata", {})
    exec_summary = report.get("executive_summary", {})
    app_sec = report.get("application_security", {})
    arch = report.get("software_architecture")

    parts = [
        "# Security Review Report",
        "",
        f"*Generated {metadata.get('generated_at', '')} · {metadata.get('repository', '')} · "
        f"scope: {metadata.get('review_scope', '')}*",
        "",
        "## Executive Summary",
        "",
        exec_summary.get("overview", ""),
        "",
        f"**Overall Risk: {exec_summary.get('overall_risk', '')}**",
        "",
        f"Security posture score: {exec_summary.get('security_posture_score', 'N/A')}/100",
        "",
        "---",
        "",
        "# Part 1 — Application Security",
        "",
        "## Confirmed Findings",
        "",
    ]

    findings = sorted(
        app_sec.get("confirmed_findings", []),
        key=lambda f: (f.get("priority", "P4"), f.get("severity", "")),
    )
    for f in findings:
        parts.append(render_finding(f))
        parts.append("---")
        parts.append("")

    roadmap = app_sec.get("remediation_roadmap", {})
    parts += [
        "## Remediation Roadmap",
        "",
        "### Immediate (P0)", "", *[f"- {i}" for i in roadmap.get("immediate", [])], "",
        "### Short-Term (P1)", "", *[f"- {i}" for i in roadmap.get("short_term", [])], "",
        "### Medium-Term (P2–P3)", "", *[f"- {i}" for i in roadmap.get("medium_term", [])], "",
        "### Hardening (P4)", "", *[f"- {i}" for i in roadmap.get("hardening", [])], "",
        "---",
        "",
    ]

    if arch:
        parts += [
            "# Part 2 — Software Architecture",
            "",
            "## Current State",
            "",
            arch.get("current_state_summary", ""),
            "",
        ]
        if arch.get("strengths"):
            parts += ["**Strengths**", ""] + [f"- {s}" for s in arch["strengths"]] + [""]
        if arch.get("structural_problems"):
            parts += ["**Structural Problems**", ""] + [f"- {s}" for s in arch["structural_problems"]] + [""]
        parts += ["## Architecture Recommendations", ""]
        for r in arch.get("recommendations", []):
            parts.append(render_recommendation(r))
            parts.append("---")
            parts.append("")

    parts += [
        "## Final Conclusion",
        "",
        report.get("final_conclusion", ""),
    ]

    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Path to report.schema.json-shaped JSON (default: stdin)")
    parser.add_argument("--output", help="Write Markdown here instead of stdout")
    args = parser.parse_args()

    report = common.read_json_input(args.input) or {}
    markdown = render(report)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
