#!/usr/bin/env python3
"""Deduplicate Findings

Merges findings that share a root cause (same category + same rule/CWE)
across multiple call sites into a single finding with multiple locations,
per workflow/stages/08_security_triage.md. Two findings are considered the
same root cause only if category AND (cwe or rule-equivalent title) match --
same category alone is too coarse (e.g. two unrelated SQL injection sites
are still two distinct findings unless they share the exact same underlying
pattern/cause).

Usage:
    deduplicate_findings.py --input findings.json [--output deduped.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def dedup_key(finding: dict) -> tuple:
    return (finding.get("category"), finding.get("cwe"), finding.get("title"))


def merge(primary: dict, duplicate: dict) -> dict:
    locations = primary.get("locations") or ([primary["location"]] if primary.get("location") else [])
    dup_loc = duplicate.get("location")
    if dup_loc and dup_loc not in locations:
        locations.append(dup_loc)
    primary["locations"] = locations

    primary_evidence = primary.get("evidence") or []
    dup_evidence = duplicate.get("evidence") or []
    primary["evidence"] = primary_evidence + [e for e in dup_evidence if e not in primary_evidence]

    return primary


def deduplicate(findings: list[dict]) -> list[dict]:
    merged: dict[tuple, dict] = {}
    order: list[tuple] = []

    for finding in findings:
        key = dedup_key(finding)
        if key in merged:
            merged[key] = merge(merged[key], finding)
        else:
            merged[key] = dict(finding)
            order.append(key)

    return [merged[key] for key in order]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="Path to a JSON array of findings (default: stdin)")
    parser.add_argument("--output", help="Write deduplicated JSON here instead of stdout")
    args = parser.parse_args()

    findings = common.read_json_input(args.input) or []
    if not isinstance(findings, list):
        print("error: input must be a JSON array", file=sys.stderr)
        return 1

    result = deduplicate(findings)

    if args.output:
        Path(args.output).write_text(common.json.dumps(result, indent=2), encoding="utf-8")
    else:
        common.print_json(result)

    print(f"deduplicated {len(findings)} -> {len(result)} finding(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
