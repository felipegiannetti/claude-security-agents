#!/usr/bin/env python3
"""Normalize Findings

Normalizes scan results (scan-result.schema.json, from scripts/scanners/*.py)
and/or candidate findings from security-reviewer into a single consistent
shape conforming to finding.schema.json, for 08_security_triage.

This does NOT decide severity or correlate with code context -- that already
happened (severity: 07/08_security_triage via calculate rules below is
applied here only as a starting default; correlation is security-reviewer's
job in 06_llm_security_review). This script's job is shape consistency:
every input record, regardless of source, comes out with the same fields.

Usage:
    normalize_findings.py --input findings.json [--output normalized.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def normalize_one(record: dict) -> dict:
    """Map a loosely-shaped candidate/scan-result record onto the fields
    finding.schema.json expects, filling in safe defaults for anything
    missing rather than dropping the record."""
    normalized = {
        "id": record.get("id") or record.get("rule_id") or "UNASSIGNED",
        "status": record.get("status", "CANDIDATE"),
        "title": record.get("title") or record.get("category") or "Untitled finding",
        "category": record.get("category") or record.get("rule_id") or "uncategorized",
        "confidence": record.get("confidence", "LOW"),
        "location": record.get("location") or {
            "file": record.get("file"),
            "line_start": record.get("line_start") or record.get("line"),
            "line_end": record.get("line_end"),
        },
    }
    # Carry through any already-well-shaped optional fields without altering them.
    for key in (
        "severity", "priority", "priority_factors", "cwe", "owasp_category",
        "source", "sink", "data_flow", "evidence", "attack_vector",
        "exploitation_scenario", "attacker_prerequisites", "technical_impact",
        "business_impact", "consequences_if_unresolved", "kev", "verification",
        "dynamic_validation", "false_positive_analysis", "remediation",
        "related_architecture_recommendations", "locations",
    ):
        if key in record:
            normalized[key] = record[key]

    severity_cfg = common.load_yaml_config("config/severity.config.yaml")
    if "severity" not in normalized:
        default_severity = severity_cfg.get("category_base_severity", {}).get(normalized["category"])
        if default_severity:
            normalized["severity"] = default_severity

    cwe_map_path = common.repo_root() / "knowledge" / "cwe" / "cwe-mapping.json"
    try:
        cwe_map = common.json.loads(cwe_map_path.read_text(encoding="utf-8"))
    except (OSError, common.json.JSONDecodeError):
        cwe_map = {}
    if "cwe" not in normalized and normalized["category"] in cwe_map:
        normalized["cwe"] = cwe_map[normalized["category"]]

    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="Path to a JSON array of raw records (default: stdin)")
    parser.add_argument("--output", help="Write normalized JSON here instead of stdout")
    args = parser.parse_args()

    records = common.read_json_input(args.input) or []
    if not isinstance(records, list):
        print("error: input must be a JSON array", file=sys.stderr)
        return 1

    normalized = [normalize_one(r) for r in records]

    if args.output:
        Path(args.output).write_text(common.json.dumps(normalized, indent=2), encoding="utf-8")
    else:
        common.print_json(normalized)
    return 0


if __name__ == "__main__":
    sys.exit(main())
