#!/usr/bin/env python3
"""Detect Entrypoints

Heuristic entry-point detection (HTTP route decorators/registrations) across
common frameworks, for agents/architecture-mapper.md and
04_attack_surface_mapping. Grep-based and intentionally approximate --
architecture-mapper must confirm each hit by reading the actual handler, not
trust this listing as final.

Usage:
    detect_entrypoints.py --path <dir>
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

# (file glob, regex, framework label) -- regex captures the route path where possible.
PATTERNS = [
    ("*.py", re.compile(r'@app\.(?:route|get|post|put|delete|patch)\(\s*["\']([^"\']+)'), "Flask/FastAPI"),
    ("*.py", re.compile(r'@router\.(?:get|post|put|delete|patch)\(\s*["\']([^"\']+)'), "FastAPI router"),
    ("*.py", re.compile(r'path\(\s*["\']([^"\']*)["\']'), "Django urls.py"),
    ("*.js", re.compile(r'\.(?:get|post|put|delete|patch)\(\s*["\']([^"\']+)'), "Express/Node"),
    ("*.ts", re.compile(r'\.(?:get|post|put|delete|patch)\(\s*["\']([^"\']+)'), "Express/Node (TS)"),
    ("*.ts", re.compile(r'@(?:Get|Post|Put|Delete|Patch)\(\s*["\']?([^"\')\s]*)'), "NestJS"),
    ("*.java", re.compile(r'@(?:GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\(\s*["\']([^"\']+)'), "Spring"),
]

EXCLUDE_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path)
    entry_points = []

    for glob, pattern, framework in PATTERNS:
        for file in root.rglob(glob):
            if any(part in EXCLUDE_DIRS for part in file.parts):
                continue
            try:
                lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, start=1):
                match = pattern.search(line)
                if match:
                    entry_points.append({
                        "type": "rest",
                        "path_or_command": match.group(1) or "(dynamic)",
                        "file": str(file),
                        "line": i,
                        "detected_via": framework,
                    })

    common.print_json({"entry_points": entry_points})
    return 0


if __name__ == "__main__":
    sys.exit(main())
