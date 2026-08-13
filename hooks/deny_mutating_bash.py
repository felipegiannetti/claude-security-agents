#!/usr/bin/env python3
"""Deny Mutating Bash

PreToolUse hook for the Bash tool. Reads the pending tool call as JSON from
stdin (Claude Code's hook contract: {"tool_name": "Bash", "tool_input":
{"command": "...", ...}, ...}) and blocks commands that could mutate the
analyzed repository, git state, installed packages, or external
infrastructure -- mirroring the deny list in .claude/settings.json and
.claude/rules/security.md "Defensive Execution Policy".

This is a second, independent enforcement layer: even if settings.json's deny
list were misconfigured or bypassed, this hook still inspects the literal
command string. It is deliberately conservative (pattern match, not a full
shell parser) -- prefer over-blocking a legitimate read-only command
(the agent can rephrase it) over under-blocking a mutating one.

Exit code 2 blocks the tool call; stderr is surfaced back to the model as the
reason. Exit code 0 allows. Any error parsing stdin fails closed (blocks).

Wire this up from settings.json, e.g.:
    "PreToolUse": [
      {"matcher": "Bash",
       "hooks": [{"type": "command", "command": "python hooks/deny_mutating_bash.py"}]}
    ]
"""

import json
import re
import sys

# Each pattern is matched case-insensitively against the full command string.
# Keep in sync with the deny list in .claude/settings.json.
DENY_PATTERNS = [
    r"\bgit\s+add\b",
    r"\bgit\s+commit\b",
    r"\bgit\s+push\b",
    r"\bgit\s+reset\b",
    r"\bgit\s+restore\b",
    r"\bgit\s+checkout\b",
    r"\bgit\s+switch\b",
    r"\bgit\s+clean\b",
    r"\brm\s",
    r"\bmv\s",
    r"\bcp\s",
    r"\bmkdir\b",
    r"\btouch\s",
    r"\bnpm\s+(install|uninstall|update)\b",
    r"\bnpx\s.*--fix\b",
    r"\byarn\s+(add|remove)\b",
    r"\bpnpm\s+(add|remove)\b",
    r"\bpip\s+(install|uninstall)\b",
    r"\bpoetry\s+(add|remove)\b",
    r"\bmvn\s+versions:",
    r"\bgradle\s.*--write-",
    r"\bsemgrep\s.*--autofix\b",
    r"\bdocker\s+(build|push)\b",
    r"\bkubectl\s+(apply|create|delete|edit|patch)\b",
    r"\bterraform\s+(apply|destroy)\b",
    r"\bgh\s+pr\s+(merge|create)\b",
    r"\bgh\s+release\s+create\b",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in DENY_PATTERNS]


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        print("Blocked: could not parse hook input; failing closed.", file=sys.stderr)
        return 2

    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return 0

    for pattern in COMPILED:
        if pattern.search(command):
            print(
                f"Blocked: command matches a prohibited mutating pattern ({pattern.pattern}). "
                "This plugin is strictly read-only against the analyzed repository "
                "(see .claude/rules/security.md). Command was:\n"
                f"  {command}",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())