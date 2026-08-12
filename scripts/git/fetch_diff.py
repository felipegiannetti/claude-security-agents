#!/usr/bin/env python3
"""Fetch Diff

Fetches the unified diff for the current review scope (working tree, or
between two refs) for 01_intake / diff-scoped reviews. Read-only.

Usage:
    fetch_diff.py --path <repo-dir> [--base <ref> --head <ref>] [--output diff.patch]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path")
    parser.add_argument("--base", help="Base ref (diff mode). If omitted, diffs the working tree against HEAD.")
    parser.add_argument("--head", default="HEAD", help="Head ref (diff mode, default HEAD)")
    parser.add_argument("--output", help="Write the diff here instead of stdout")
    args = parser.parse_args()

    git_args = ["diff", f"{args.base}...{args.head}"] if args.base else ["diff", "HEAD"]
    run = common.run_tool(["git", *git_args], cwd=args.path, timeout=60)

    if not run["ok"] or run["returncode"] != 0:
        print(f"error: git diff failed ({run.get('error') or run.get('stderr')})", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(run["stdout"], encoding="utf-8")
    else:
        print(run["stdout"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
