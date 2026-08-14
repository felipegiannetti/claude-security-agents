#!/usr/bin/env python3
"""Run Semgrep

Runs Semgrep static analysis against the review scope and normalizes results
to scan-result.schema.json. Never invoked with --autofix (see
.claude/rules/security.md "Defensive Execution Policy").

Usage:
    run_semgrep.py --path <dir-or-file> [--config auto] [--output results.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def normalize_cwe(cwe) -> "str | None":
    """A rule's cwe metadata is sometimes a single string and sometimes a
    list of strings -- iterating a bare string with next(iter(...)) silently
    returns just its first character instead of the full identifier, so
    each shape needs its own explicit handling rather than one code path
    assuming a list."""
    if isinstance(cwe, str):
        return cwe
    if isinstance(cwe, list) and cwe:
        return cwe[0]
    return None


def normalize(raw: dict) -> list[dict]:
    results = []
    for r in raw.get("results") or []:
        start = r.get("start", {})
        end = r.get("end", {})
        extra = r.get("extra", {})
        results.append({
            "tool": "semgrep",
            "rule_id": r.get("check_id"),
            "title": extra.get("message", r.get("check_id", "")),
            "raw_severity": extra.get("severity"),
            "file": r.get("path"),
            "line_start": start.get("line"),
            "line_end": end.get("line"),
            "snippet": extra.get("lines"),
            "cwe": normalize_cwe((extra.get("metadata") or {}).get("cwe")),
            "correlated": False,
            "raw_output": r,
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--config", default=None, help="Semgrep config (default: from scanners.config.yaml, falls back to 'auto')")
    parser.add_argument("--output", help="Write normalized JSON here instead of stdout")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/scanners.config.yaml").get("semgrep", {})
    if not cfg.get("enabled", True):
        common.print_json({"tool": "semgrep", "skipped": True, "reason": "disabled in config/scanners.config.yaml"})
        return 0

    semgrep_config = args.config or cfg.get("config", "auto")
    run = common.run_tool(["semgrep", "scan", f"--config={semgrep_config}", "--json", "--quiet", args.path], timeout=600)

    if not run["ok"]:
        print(f"warning: semgrep unavailable ({run['error']})", file=sys.stderr)
        common.print_json({"tool": "semgrep", "skipped": True, "reason": run["error"]})
        return 0

    try:
        raw = common.json.loads(run["stdout"] or "{}")
    except common.json.JSONDecodeError as exc:
        print(f"warning: could not parse semgrep output ({exc})", file=sys.stderr)
        common.print_json({"tool": "semgrep", "skipped": True, "reason": "unparseable output"})
        return 0

    normalized = normalize(raw)
    if args.output:
        Path(args.output).write_text(common.json.dumps(normalized, indent=2), encoding="utf-8")
    else:
        common.print_json(normalized)

    print(f"semgrep: {len(normalized)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
