#!/usr/bin/env python3
"""Calculate Security Posture

Computes an overall security posture score (0-100) and risk rating from the
confirmed finding set, for 15_final_report's executive summary. The score is
a deliberately simple, explainable deduction model -- not a black box --
so the accompanying narrative (written by the report stage, not this script)
can explain exactly what drove it.

Usage:
    calculate_security_posture.py --input findings.json
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

# Points deducted per confirmed finding, by priority. Deliberately front-loaded
# on P0/P1 -- a handful of P0s should dominate the score the way they'd
# dominate a human reviewer's risk judgment.
DEDUCTIONS = {"P0": 25, "P1": 12, "P2": 5, "P3": 2, "P4": 0}

RISK_THRESHOLDS = [
    (0, "critical"),
    (40, "high"),
    (70, "medium"),
    (85, "low"),
]


def compute(findings: list[dict]) -> dict:
    score = 100
    counts_by_priority = {p: 0 for p in DEDUCTIONS}
    counts_by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0, "informational": 0}

    for finding in findings:
        if finding.get("status") != "CONFIRMED":
            continue
        priority = finding.get("priority", "P4")
        severity = finding.get("severity", "informational")
        counts_by_priority[priority] = counts_by_priority.get(priority, 0) + 1
        counts_by_severity[severity] = counts_by_severity.get(severity, 0) + 1
        score -= DEDUCTIONS.get(priority, 0)

    score = max(0, min(100, score))

    overall_risk = "low"
    for threshold, label in RISK_THRESHOLDS:
        if score >= threshold:
            overall_risk = label

    return {
        "security_posture_score": score,
        "overall_risk": overall_risk,
        "finding_counts": {
            "by_priority": counts_by_priority,
            "by_severity": counts_by_severity,
            "rejected_as_false_positive": sum(1 for f in findings if f.get("status") == "REJECTED"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Path to a JSON array of findings (default: stdin)")
    args = parser.parse_args()

    findings = common.read_json_input(args.input) or []
    if not isinstance(findings, list):
        print("error: input must be a JSON array", file=sys.stderr)
        return 1

    common.print_json(compute(findings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
