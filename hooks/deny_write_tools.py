#!/usr/bin/env python3
"""Deny Write Tools -- PreToolUse hook for Edit/Write/NotebookEdit.

This plugin's own subagents (architecture-mapper, security-reviewer,
security-verifier, architecture-advisor, pentest-validator) must never
write to the repository they are analyzing -- see .claude/rules/security.md
"Absolute Read-Only Policy". That restriction applies ONLY while one of
those specific subagents is the one making the call. It must never block
the user's own main Claude Code session doing normal, unrelated work in
any other project -- installing this plugin must not turn off Edit/Write
globally for everything the user does afterward.

Claude Code includes agent_id/agent_type in the hook payload when a tool
call originates from a subagent invocation (absent for the main session).
Block only when agent_type identifies one of this plugin's own agents;
allow everything else, including calls with no agent context at all and
calls from a different, unrelated subagent -- ambiguous cases resolve to
allow, not block, since over-blocking normal work is the bug this exists
to fix, not a safe default to fall back on here.
"""

import json
import sys

OUR_AGENT_NAMES = (
    'architecture-mapper',
    'security-reviewer',
    'security-verifier',
    'architecture-advisor',
    'pentest-validator',
)


def is_our_agent(payload: dict) -> bool:
    agent_id = payload.get('agent_id')
    if not agent_id:
        return False  # no subagent context at all -- this is the main session
    agent_type = (payload.get('agent_type') or '').lower()
    return any(name in agent_type for name in OUR_AGENT_NAMES)


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or '{}')
    except json.JSONDecodeError:
        return 0  # can't identify the caller -- allow rather than block main-session work

    if is_our_agent(payload):
        print(
            'Blocked: this project is a read-only security review agent. '
            'Edit/Write/NotebookEdit against the analyzed repository are never permitted '
            '(see .claude/rules/security.md). Recommend the fix in the report instead.',
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())
