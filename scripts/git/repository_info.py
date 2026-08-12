#!/usr/bin/env python3
"""Repository Info

Collects read-only repository metadata for 01_intake: remote URL, default
branch, current commit, and top contributors. Uses only non-mutating git
commands (see .claude/rules/security.md "Defensive Execution Policy").

Usage:
    repository_info.py [--path <repo-dir>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def git(args: list[str], cwd: str) -> str:
    result = common.run_tool(["git", *args], cwd=cwd, timeout=30)
    return result["stdout"].strip() if result["ok"] and result["returncode"] == 0 else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path")
    args = parser.parse_args()

    remote = git(["remote", "get-url", "origin"], args.path)
    default_branch = git(["symbolic-ref", "refs/remotes/origin/HEAD"], args.path).replace("refs/remotes/origin/", "")
    current_branch = git(["branch", "--show-current"], args.path)
    commit = git(["rev-parse", "HEAD"], args.path)
    top_contributors_raw = git(["shortlog", "-sn", "--all", "-n", "10"], args.path)
    contributors = [
        {"count": int(line.split(maxsplit=1)[0]), "name": line.split(maxsplit=1)[1]}
        for line in top_contributors_raw.splitlines()
        if line.strip()
    ]

    common.print_json({
        "remote": remote or None,
        "default_branch": default_branch or None,
        "current_branch": current_branch or None,
        "commit": commit or None,
        "top_contributors": contributors,
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
