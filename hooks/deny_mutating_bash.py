#!/usr/bin/env python3
"""Deny Mutating Bash -- PreToolUse hook for Bash and PowerShell tools.
Blocks mutating commands against the analyzed repository. Second layer
on top of settings.json deny list. Pattern match, not a shell parser --
over-block a read-only command rather than under-block a mutating one.
Not a sandbox: general-purpose interpreter invocation is a known gap this
revision specifically targets (see the interpreter-escape patterns below).
"""

import json
import re
import sys

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
    r'>\|?>?\s*[\x27\x22]?[\w./-]+\.\w+',
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
        print("Blocked: could not parse hook input; failing closed.", file=sys.stderr)
        return 2
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
