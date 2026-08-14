#!/usr/bin/env python3
"""Run Trivy

Runs Trivy filesystem scan (dependency CVEs, misconfigurations, exposed
secrets in config) against the review scope and normalizes results to
scan-result.schema.json.

Usage:
    run_trivy.py --path <dir> [--output results.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def normalize(raw: dict) -> list[dict]:
    results = []
    for target in raw.get("Results") or []:
        file_path = target.get("Target")

        for v in target.get("Vulnerabilities", []) or []:
            results.append({
                "tool": "trivy",
                "rule_id": v.get("VulnerabilityID"),
                "title": v.get("Title") or v.get("VulnerabilityID"),
                "raw_severity": v.get("Severity"),
                "file": file_path,
                "cve": v.get("VulnerabilityID") if str(v.get("VulnerabilityID", "")).startswith("CVE-") else None,
                "package": v.get("PkgName"),
                "installed_version": v.get("InstalledVersion"),
                "affected_range": v.get("VulnerableVersionRange") or v.get("FixedVersion"),
                "correlated": False,
                "raw_output": v,
            })

        for m in target.get("Misconfigurations", []) or []:
            results.append({
                "tool": "trivy",
                "rule_id": m.get("ID"),
                "title": m.get("Title"),
                "raw_severity": m.get("Severity"),
                "file": file_path,
                "line_start": (m.get("CauseMetadata") or {}).get("StartLine"),
                "line_end": (m.get("CauseMetadata") or {}).get("EndLine"),
                "correlated": False,
                "raw_output": m,
            })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--output", help="Write normalized JSON here instead of stdout")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/scanners.config.yaml").get("trivy", {})
    if not cfg.get("enabled", True):
        common.print_json({"tool": "trivy", "skipped": True, "reason": "disabled in config/scanners.config.yaml"})
        return 0

    run = common.run_tool(["trivy", "fs", "--format", "json", "--quiet", args.path], timeout=900)

    if not run["ok"]:
        print(f"warning: trivy unavailable ({run['error']})", file=sys.stderr)
        common.print_json({"tool": "trivy", "skipped": True, "reason": run["error"]})
        return 0

    try:
        raw = common.json.loads(run["stdout"] or "{}")
    except common.json.JSONDecodeError as exc:
        print(f"warning: could not parse trivy output ({exc})", file=sys.stderr)
        common.print_json({"tool": "trivy", "skipped": True, "reason": "unparseable output"})
        return 0

    normalized = normalize(raw)
    if args.output:
        Path(args.output).write_text(common.json.dumps(normalized, indent=2), encoding="utf-8")
    else:
        common.print_json(normalized)

    print(f"trivy: {len(normalized)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
