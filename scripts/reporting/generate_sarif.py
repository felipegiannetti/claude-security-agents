#!/usr/bin/env python3
"""Generate SARIF

Converts the Application Security axis (CONFIRMED findings only) of a
report.schema.json document into SARIF 2.1.0, for CI/IDE integration. The
Software Architecture axis (ARCH-*) has no meaningful SARIF representation
and is intentionally omitted -- see workflow/stages/15_final_report.md.

Usage:
    generate_sarif.py --input report.json [--output report.sarif]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

SEVERITY_TO_SARIF_LEVEL = {
    "critical": "error", "high": "error", "medium": "warning",
    "low": "note", "informational": "note",
}


def finding_to_result(finding: dict) -> dict:
    location = finding.get("location") or {}
    return {
        "ruleId": finding.get("cwe") or finding.get("category") or finding.get("id"),
        "level": SEVERITY_TO_SARIF_LEVEL.get(finding.get("severity"), "warning"),
        "message": {"text": finding.get("title", "")},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": location.get("file", "")},
                    "region": {
                        "startLine": location.get("line_start") or 1,
                        "endLine": location.get("line_end") or location.get("line_start") or 1,
                    },
                }
            }
        ],
        "properties": {
            "securityReviewAgentId": finding.get("id"),
            "priority": finding.get("priority"),
            "confidence": finding.get("confidence"),
            "owaspCategory": finding.get("owasp_category"),
        },
    }


def build_sarif(report: dict) -> dict:
    findings = (report.get("application_security") or {}).get("confirmed_findings", [])
    rule_ids = sorted({f.get("cwe") or f.get("category") or f.get("id") for f in findings if f.get("id")})

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "security-review-agent",
                        "informationUri": "https://github.com/",
                        "version": (report.get("metadata") or {}).get("pipeline_version", "0.0.0"),
                        "rules": [{"id": rid} for rid in rule_ids],
                    }
                },
                "results": [finding_to_result(f) for f in findings],
            }
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Path to report.schema.json-shaped JSON (default: stdin)")
    parser.add_argument("--output", help="Write SARIF here instead of stdout")
    args = parser.parse_args()

    report = common.read_json_input(args.input) or {}
    sarif = build_sarif(report)

    output_text = common.json.dumps(sarif, indent=2)
    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
