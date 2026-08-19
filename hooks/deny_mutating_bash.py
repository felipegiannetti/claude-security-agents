#!/usr/bin/env python3
"""Deny Mutating Bash -- PreToolUse hook for Bash and PowerShell tools.

Blocks mutating commands, but ONLY while one of this plugin's own
subagents (architecture-mapper, security-reviewer, security-verifier,
architecture-advisor, pentest-validator) is the one issuing the command --
never the user's main Claude Code session doing normal, unrelated work in
some other project. Installing this plugin must not turn off Bash/
PowerShell mutation for everything the user does afterward.

Pattern match, not a shell parser -- once scoped to our own agents,
over-block a read-only command rather than under-block a mutating one.
Not a sandbox: general-purpose interpreter invocation is a known gap this
revision specifically targets (see the interpreter-escape patterns below).
"""

import json
import re
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
        return False  # no subagent context -- this is the main session
    agent_type = (payload.get('agent_type') or '').lower()
    return any(name in agent_type for name in OUR_AGENT_NAMES)


_ANCHOR = r'(?:^|[;&|]\s*)'

DENY_PATTERNS = [
    r'\bgit\s+add\b',
    r'\bgit\s+commit\b',
    r'\bgit\s+push\b',
    r'\bgit\s+reset\b',
    r'\bgit\s+restore\b',
    r'\bgit\s+checkout\b',
    r'\bgit\s+switch\b',
    r'\bgit\s+clean\b',
    r'\bgit\s+(apply|merge|rebase|cherry-pick|revert|rm|mv)\b',
    r'\bgit\s+stash\s+(pop|apply|drop)\b',
    r'\brm\s',
    _ANCHOR + r'ri\s',
    r'\bremove-item\b',
    r'\bdel\s',
    r'\berase\s',
    r'\brd\s',
    r'\brmdir\b',
    r'\bclear-content\b',
    r'\bmv\s',
    r'\bmove-item\b',
    _ANCHOR + r'move\s',
    _ANCHOR + r'mi\s',
    r'\brename-item\b',
    _ANCHOR + r'ren\s',
    _ANCHOR + r'rni\s',
    r'\bcp\s',
    r'\bcopy-item\b',
    _ANCHOR + r'copy\s',
    _ANCHOR + r'cpi\s',
    r'\bmkdir\b',
    r'\btouch\s',
    r'\bnew-item\b',
    _ANCHOR + r'ni\s',
    r'\bset-content\b',
    r'\badd-content\b',
    r'\bout-file\b',
    r'\[(?:system\.io|io)\.file\]::(writealltext|appendalltext|copy|move|delete)',
    r'\[(?:system\.io|io)\.directory\]::(delete|move|createdirectory)',
    r'\btee\s+(-a\s+)?\S',
    r'\bdd\s+.*\bof=',
    r'\btruncate\s',
    r'\bsed\s+(-\S*i\S*|--in-place\S*)\b',
    r'>\|?>?\s*[\x27\x22]?[\w./-]+\.\w+',
    r'\b(curl|wget)\b.*\s(-o|--output|-O)\s',
    r'\biex\b',
    r'\binvoke-expression\b',
    r'-e(nc(odedcommand)?)?\s+[A-Za-z0-9+/=]{20,}',
    r'\b(python[0-9.]*|node|perl|ruby|php)\s+.*(-c|-e|-r|--eval)\b',
    r'\bstart-process\b',
    r'\bnpm\s+(install|uninstall|update)\b',
    r'\bnpx\s.*--fix\b',
    r'\byarn\s+(add|remove)\b',
    r'\bpnpm\s+(add|remove)\b',
    r'\bpip\s+(install|uninstall)\b',
    r'\bpoetry\s+(add|remove)\b',
    r'\bmvn\s+versions:',
    r'\bgradle\s.*--write-',
    r'\bsemgrep\s.*--autofix\b',
    r'\binstall-module\b',
    r'\binstall-package\b',
    r'\bdocker\s+(build|push)\b',
    r'\bkubectl\s+(apply|create|delete|edit|patch)\b',
    r'\bterraform\s+(apply|destroy)\b',
    r'\bgh\s+pr\s+(merge|create)\b',
    r'\bgh\s+release\s+create\b',
]

COMPILED = [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in DENY_PATTERNS]


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0  # can't identify the caller -- allow rather than block main-session work

    if not is_our_agent(payload):
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return 0
    for pattern in COMPILED:
        if pattern.search(command):
            msg = "Blocked: command matches a prohibited mutating pattern (" + pattern.pattern + "). Command was:" + chr(10) + command
            print(msg, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
