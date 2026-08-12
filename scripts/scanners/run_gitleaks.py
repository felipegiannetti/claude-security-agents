#!/usr/bin/env python3
"""Run Gitleaks

Runs Gitleaks secret detection against the review scope and normalizes
results to scan-result.schema.json. Secret values are masked in the
normalized output -- see .claude/rules/security.md "Secrets Handling".

Usage:
    run_gitleaks.py --path <dir> [--output results.json]
"""

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def mask(secret: str) -> str:
    if not secret:
        return secret
    if len(secret) <= 8:
        return "*" * len(secret)
    return secret[:4] + "*" * (len(secret) - 4)


def normalize(raw: list[dict]) -> list[dict]:
    results = []
    for r in raw:
        results.append({
            "tool": "gitleaks",
            "rule_id": r.get("RuleID"),
            "title": r.get("Description"),
            "raw_severity": "high",  # gitleaks doesn't emit severity; secrets default high
            "file": r.get("File"),
            "line_start": r.get("StartLine"),
            "line_end": r.get("EndLine"),
            "snippet": mask(r.get("Secret", "")),
            "correlated": False,
            "raw_output": {k: (mask(v) if k == "Secret" else v) for k, v in r.items()},
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--output", help="Write normalized JSON here instead of stdout")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/scanners.config.yaml").get("gitleaks", {})
    if not cfg.get("enabled", True):
        common.print_json({"tool": "gitleaks", "skipped": True, "reason": "disabled in config/scanners.config.yaml"})
        return 0

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        report_path = tmp.name

    run = common.run_tool(
        ["gitleaks", "detect", "--source", args.path, "--report-format", "json", "--report-path", report_path, "--no-git"],
        timeout=600,
    )

    if not run["ok"]:
        print(f"warning: gitleaks unavailable ({run['error']})", file=sys.stderr)
        common.print_json({"tool": "gitleaks", "skipped": True, "reason": run["error"]})
        return 0

    # gitleaks exits non-zero when leaks are found -- that's expected, not a failure.
    try:
        report_text = Path(report_path).read_text(encoding="utf-8") if Path(report_path).exists() else "[]"
        raw = common.json.loads(report_text or "[]")
    except common.json.JSONDecodeError as exc:
        print(f"warning: could not parse gitleaks output ({exc})", file=sys.stderr)
        common.print_json({"tool": "gitleaks", "skipped": True, "reason": "unparseable output"})
        return 0
    finally:
        Path(report_path).unlink(missing_ok=True)

    normalized = normalize(raw)
    if args.output:
        Path(args.output).write_text(common.json.dumps(normalized, indent=2), encoding="utf-8")
    else:
        common.print_json(normalized)

    print(f"gitleaks: {len(normalized)} result(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
