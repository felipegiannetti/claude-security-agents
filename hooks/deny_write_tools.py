#!/usr/bin/env python3
"""Deny Write Tools

PreToolUse hook for Edit/Write/NotebookEdit. This plugin's agents are
strictly read-only against the analyzed repository (see
.claude/rules/security.md "Absolute Read-Only Policy") -- this hook enforces
that at the tool layer, not just in agent prompts, so a prompt-injection or a
model mistake can't silently bypass it.

Exit code 2 blocks the tool call in Claude Code; stderr is surfaced back to
the model as the reason. Exit code 0 allows.

Wire this up from settings.json, e.g.:
    "PreToolUse": [
      {"matcher": "Edit|Write|NotebookEdit",
       "hooks": [{"type": "command", "command": "python hooks/deny_write_tools.py"}]}
    ]
"""

import sys


def main() -> int:
    print(
        "Blocked: this project is a read-only security review agent. "
        "Edit/Write/NotebookEdit against the analyzed repository are never permitted "
        "(see .claude/rules/security.md). Recommend the fix in the report instead.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
