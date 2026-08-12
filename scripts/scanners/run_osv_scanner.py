#!/usr/bin/env python3
"""Run OSV Scanner

Runs osv-scanner against dependency manifests/lockfiles in the review scope
and normalizes results to scan-result.schema.json. Feeds
scripts/scanners/check_kev.py for CISA KEV correlation.

Usage:
    run_osv_scanner.py --path <dir> [--output results.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def normalize(raw: dict) -> list[dict]:
    results = []
    # `raw.get("results", [])` is not enough -- osv-scanner v2 emits a
    # literal {"results": null} when it finds no package sources at all
    # (e.g. an empty directory, or the target wasn't a directory), and
    # .get()'s default only applies when the key is absent, not when
    # present with a None value.
    for result in raw.get("results") or []:
        source = (result.get("source") or {}).get("path")
        for pkg in result.get("packages", []) or []:
            package_info = pkg.get("package", {})
            for vuln in pkg.get("vulnerabilities", []) or []:
                cve = next(
                    (alias for alias in vuln.get("aliases", []) if str(alias).startswith("CVE-")),
                    vuln.get("id") if str(vuln.get("id", "")).startswith("CVE-") else None,
                )
                results.append({
                    "tool": "osv-scanner",
                    "rule_id": vuln.get("id"),
                    "title": vuln.get("summary") or vuln.get("id"),
                    "raw_severity": next(
                        (s.get("score") for s in vuln.get("severity", [])), None
                    ),
                    "file": source,
                    "cve": cve,
                    "package": package_info.get("name"),
                    "installed_version": package_info.get("version"),
                    "affected_range": ", ".join(
                        e.get("fixed", "unfixed")
                        for a in vuln.get("affected", [])
                        for e in (a.get("ranges", [{}])[0].get("events", []) if a.get("ranges") else [])
                        if "fixed" in e
                    ) or None,
                    "correlated": False,
                    "raw_output": vuln,
                })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--output", help="Write normalized JSON here instead of stdout")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/scanners.config.yaml").get("osv_scanner", {})
    if not cfg.get("enabled", True):
        common.print_json({"tool": "osv-scanner", "skipped": True, "reason": "disabled in config/scanners.config.yaml"})
        return 0

    # osv-scanner v2's CLI requires the "scan source" subcommand (the old
    # flat "osv-scanner --format json --recursive <path>" form from v1 is
    # no longer valid and silently walks the wrong root instead of erroring
    # clearly). --allow-no-lockfiles lets it still resolve versions from a
    # bare manifest (e.g. package.json) when no lockfile is present.
    run = common.run_tool(
        ["osv-scanner", "scan", "source", "--format", "json", "--recursive", "--allow-no-lockfiles", args.path],
        timeout=600,
    )

    # osv-scanner exits non-zero when vulnerabilities are found -- expected, not a failure.
    if not run["ok"]:
        print(f"warning: osv-scanner unavailable ({run['error']})", file=sys.stderr)
        common.print_json({"tool": "osv-scanner", "skipped": True, "reason": run["error"]})
        return 0

    try:
        raw = common.json.loads(run["stdout"] or "{}")
    except common.json.JSONDecodeError as exc:
        print(f"warning: could not parse osv-scanner output ({exc})", file=sys.stderr)
        common.print_json({"tool": "osv-scanner", "skipped": True, "reason": "unparseable output"})
        return 0

    normalized = normalize(raw)
    if args.output:
        Path(args.output).write_text(common.json.dumps(normalized, indent=2), encoding="utf-8")
    else:
        common.print_json(normalized)

    print(f"osv-scanner: {len(normalized)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
