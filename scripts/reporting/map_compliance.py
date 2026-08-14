#!/usr/bin/env python3
"""Map Compliance

Deterministic enrichment: attaches MITRE ATT&CK technique(s), NIST CSF 2.0
function(s), and ISO/IEC 27001:2022 Annex A control(s) to each finding by
looking up its category in knowledge/mitre/attack-mapping.json,
knowledge/compliance/nist-mapping.json, and
knowledge/compliance/iso27001-mapping.json -- same pattern as
scripts/scanners/check_kev.py's CVE lookup. This script never invents a
technique or control ID: a category with no entry in a mapping file gets
no field for that framework, not a guessed one.

Framework alignment is additive context for the reader. It never changes
a finding's severity or priority, and a missing mapping is never evidence
that a finding has no attacker or compliance relevance -- it just means
this project has not mapped that category with enough confidence yet. See
knowledge/mitre/attack-overview.md and
knowledge/compliance/compliance-overview.md.

Usage: pass --input and --output flags (see argparse below), or use
stdin/stdout the same way check_kev.py does.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def load_mapping(path: str) -> dict:
    full_path = common.repo_root() / path
    if not full_path.exists():
        return {}
    try:
        data = json.loads(full_path.read_text(encoding="utf-8-sig"))
        return data.get("mappings", {})
    except json.JSONDecodeError:
        return {}


def attach_attack(finding: dict, mapping: dict) -> None:
    entry = mapping.get(finding.get("category"))
    if entry is None:
        return
    finding["mitre_attack"] = {
        "techniques": entry.get("techniques", []),
    }
    if "note" in entry:
        finding["mitre_attack"]["note"] = entry["note"]


def attach_compliance(finding, nist_mapping, iso_mapping, want_nist, want_iso):
    category = finding.get("category")
    mappings = {}
    if want_nist:
        nist_entry = nist_mapping.get(category)
        if nist_entry is not None:
            mappings["nist_csf"] = nist_entry.get("functions", [])
    if want_iso:
        iso_entry = iso_mapping.get(category)
        if iso_entry is not None:
            mappings["iso27001"] = iso_entry.get("controls", [])
    if mappings:
        finding["compliance_mappings"] = mappings


def read_findings(input_path):
    text = Path(input_path).read_text(encoding="utf-8-sig") if input_path else sys.stdin.read()
    text = text.lstrip(chr(65279))
    data = json.loads(text) if text.strip() else []
    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array of findings")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="Path to a JSON findings file (default: stdin)")
    parser.add_argument("--output", help="Path to write enriched JSON (default: stdout)")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/compliance.config.yaml")
    if not cfg.get("enabled", True):
        common.print_json({"tool": "map-compliance", "skipped": True, "reason": "disabled in config/compliance.config.yaml"})
        return 0

    frameworks = cfg.get("frameworks", {})
    want_attack = frameworks.get("mitre_attack", True)
    want_nist = frameworks.get("nist_csf", True)
    want_iso = frameworks.get("iso27001", True)
    mapping_files = cfg.get("mapping_files", {})

    attack_mapping = load_mapping(mapping_files.get("mitre_attack", "knowledge/mitre/attack-mapping.json")) if want_attack else {}
    nist_mapping = load_mapping(mapping_files.get("nist_csf", "knowledge/compliance/nist-mapping.json")) if want_nist else {}
    iso_mapping = load_mapping(mapping_files.get("iso27001", "knowledge/compliance/iso27001-mapping.json")) if want_iso else {}

    try:
        findings = read_findings(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 1

    enriched = []
    attack_count = 0
    compliance_count = 0
    for finding in findings:
        finding = dict(finding)
        if want_attack:
            before = finding.get("mitre_attack")
            attach_attack(finding, attack_mapping)
            if finding.get("mitre_attack") is not before:
                attack_count += 1
        if want_nist or want_iso:
            attach_compliance(finding, nist_mapping, iso_mapping, want_nist, want_iso)
            if "compliance_mappings" in finding:
                compliance_count += 1
        enriched.append(finding)

    output_text = json.dumps(enriched, indent=2)
    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text)

    summary = ("map-compliance: " + str(attack_count) + "/" + str(len(enriched))
        + " finding(s) got a MITRE technique mapping, " + str(compliance_count)
        + "/" + str(len(enriched)) + " got a compliance mapping")
    print(summary, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
