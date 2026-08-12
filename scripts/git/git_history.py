#!/usr/bin/env python3
"""Git History

Inspects git history for a specific file (or file:line range via blame) to
aid triage -- e.g. when a finding was introduced, or who last touched a
suspicious line. Read-only.

Usage:
    git_history.py --path <repo-dir> --file <relative-path> [--blame] [--limit 10]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path")
    parser.add_argument("--file", required=True, help="File to inspect, relative to --path")
    parser.add_argument("--blame", action="store_true", help="Show blame instead of commit log")
    parser.add_argument("--limit", type=int, default=10, help="Max commits to show (log mode)")
    args = parser.parse_args()

    if args.blame:
        run = common.run_tool(["git", "blame", "--line-porcelain", args.file], cwd=args.path, timeout=60)
    else:
        run = common.run_tool(
            ["git", "log", f"-{args.limit}", "--follow", "--format=%H|%an|%ad|%s", "--date=iso", "--", args.file],
            cwd=args.path,
            timeout=60,
        )

    if not run["ok"] or run["returncode"] != 0:
        print(f"warning: git history lookup failed ({run.get('error') or run.get('stderr')})", file=sys.stderr)
        common.print_json({"file": args.file, "entries": []})
        return 0

    if args.blame:
        common.print_json({"file": args.file, "blame_raw": run["stdout"]})
        return 0

    entries = []
    for line in run["stdout"].splitlines():
        if not line.strip():
            continue
        parts = line.split("|", maxsplit=3)
        if len(parts) == 4:
            entries.append({"commit": parts[0], "author": parts[1], "date": parts[2], "message": parts[3]})

    common.print_json({"file": args.file, "entries": entries})
    return 0


if __name__ == "__main__":
    sys.exit(main())
