#!/usr/bin/env python3
"""Common

Shared helpers for scripts/ -- config loading, subprocess execution, and
repo-root resolution. Not a public entry point; imported by the other
scripts via sys.path manipulation (see any scripts/**/*.py for the pattern).
Kept small and dependency-light per CLAUDE.md's "prefer small focused files."
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def repo_root() -> Path:
    """Resolve the security-review-agent project root from any script under scripts/."""
    return Path(__file__).resolve().parents[2]


def load_yaml_config(relative_path: str) -> dict:
    """Load a YAML config file relative to the repo root. Returns {} if the
    file is missing or PyYAML isn't installed, rather than crashing --
    callers should apply their own sane defaults on top."""
    if yaml is None:
        print(
            "warning: pyyaml not installed (see scripts/requirements.txt); "
            "proceeding with empty config",
            file=sys.stderr,
        )
        return {}
    path = repo_root() / relative_path
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        print(f"warning: failed to parse {relative_path}: {exc}", file=sys.stderr)
        return {}


def run_tool(args: list[str], timeout: int = 300, cwd: Optional[str] = None) -> dict:
    """Run an external CLI tool and capture its result without raising --
    scanner/git tool failures should degrade that tool's contribution, not
    crash the pipeline (see workflow/stages/05_static_security_scanning.md
    "Success Criteria"). Returns a dict: {ok, returncode, stdout, stderr,
    error}. 'error' is set (and 'ok' is False) when the tool couldn't be
    invoked at all (not found, timed out)."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            check=False,
        )
        return {
            "ok": True,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error": None,
        }
    except FileNotFoundError:
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "error": f"tool not found: {args[0]} (is it installed and on PATH?)",
        }
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "error": f"tool timed out after {timeout}s: {' '.join(args)}",
        }


def print_json(data) -> None:
    print(json.dumps(data, indent=2))


def read_json_input(input_path: Optional[str]) -> object:
    text = Path(input_path).read_text(encoding="utf-8") if input_path else sys.stdin.read()
    return json.loads(text) if text.strip() else None
