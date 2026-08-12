#!/usr/bin/env python3
"""Changed Files

Lists files changed in the current review scope (working tree changes, or a
diff between two refs), filtered against config/exclusions.yaml. Read-only.

Usage:
    changed_files.py --path <repo-dir> [--base <ref> --head <ref>]
"""

import argparse
import fnmatch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def is_excluded(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, p) for p in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path")
    parser.add_argument("--base", help="Base ref (diff mode). If omitted, lists working-tree changes.")
    parser.add_argument("--head", default="HEAD", help="Head ref (diff mode, default HEAD)")
    args = parser.parse_args()

    if args.base:
        git_args = ["diff", "--name-only", f"{args.base}...{args.head}"]
    else:
        git_args = ["diff", "--name-only", "HEAD"]

    run = common.run_tool(["git", *git_args], cwd=args.path, timeout=30)
    if not run["ok"] or run["returncode"] != 0:
        print(f"warning: git diff failed ({run.get('error') or run.get('stderr')})", file=sys.stderr)
        common.print_json({"files": []})
        return 0

    files = [f for f in run["stdout"].splitlines() if f.strip()]

    exclusions = common.load_yaml_config("config/exclusions.yaml").get("paths", [])
    in_scope = [f for f in files if not is_excluded(f, exclusions)]
    excluded = [f for f in files if is_excluded(f, exclusions)]

    common.print_json({"files": in_scope, "excluded": excluded})
    return 0


if __name__ == "__main__":
    sys.exit(main())
