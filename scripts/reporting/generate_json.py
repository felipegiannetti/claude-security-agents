#!/usr/bin/env python3
"""Generate JSON

Assembles the final report.schema.json-shaped document from its component
parts (metadata, executive summary prose, prioritized findings, and
optionally architecture assessment/recommendations) for 15_final_report.
Prose fields (executive_summary.overview, final_conclusion, etc.) are
expected to already be filled in by the pipeline's LLM stages -- this script
only assembles and validates shape, it does not generate prose.

Usage:
    generate_json.py --metadata metadata.json --executive-summary summary.json
                      --findings findings.json [--architecture architecture.json]
                      --final-conclusion "..." [--output report.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
from calculate_security_posture import compute as compute_posture  # noqa: E402


def load(path: str | None) -> dict:
    if not path:
        return {}
    return common.json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--executive-summary", required=True)
    parser.add_argument("--findings", required=True, help="JSON array of findings, priority already assigned")
    parser.add_argument("--architecture", help="architecture assessment + recommendations JSON, if that stage ran")
    parser.add_argument("--final-conclusion", default="")
    parser.add_argument("--output", help="Write report JSON here instead of stdout")
    args = parser.parse_args()

    metadata = load(args.metadata)
    executive_summary = load(args.executive_summary)
    findings = common.json.loads(Path(args.findings).read_text(encoding="utf-8"))
    architecture = load(args.architecture) if args.architecture else None

    posture = compute_posture(findings)

    report = {
        "metadata": {
            **metadata,
            "dynamic_validation_performed": any(
                (f.get("dynamic_validation") or {}).get("performed") for f in findings
            ),
        },
        "executive_summary": {
            **executive_summary,
            "overall_risk": executive_summary.get("overall_risk") or posture["overall_risk"],
            "security_posture_score": posture["security_posture_score"],
        },
        "application_security": {
            "finding_counts": posture["finding_counts"],
            "confirmed_findings": [f for f in findings if f.get("status") == "CONFIRMED"],
            "remediation_roadmap": {
                "immediate": [f["id"] for f in findings if f.get("priority") == "P0"],
                "short_term": [f["id"] for f in findings if f.get("priority") == "P1"],
                "medium_term": [f["id"] for f in findings if f.get("priority") in ("P2", "P3")],
                "hardening": [f["id"] for f in findings if f.get("priority") == "P4"],
            },
        },
        "final_conclusion": args.final_conclusion,
    }
    if architecture:
        report["software_architecture"] = architecture

    output_text = common.json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
