#!/usr/bin/env python3
"""Detect Languages

Heuristic language detection by file extension footprint -- a starting
hypothesis for agents/architecture-mapper.md, which should verify against
actual imports/config rather than trust this alone (see
agents/architecture-mapper.md "Languages & Frameworks").

Usage:
    detect_languages.py --path <dir>
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

EXTENSION_LANGUAGE = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".java": "Java", ".kt": "Kotlin",
    ".go": "Go", ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".rs": "Rust",
    ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++", ".swift": "Swift",
    ".scala": "Scala", ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell",
    ".tf": "Terraform", ".yaml": "YAML", ".yml": "YAML",
}

DEFAULT_EXCLUDE_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path)
    counts: Counter = Counter()
    total_files = 0

    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if any(part in DEFAULT_EXCLUDE_DIRS for part in file.parts):
            continue
        total_files += 1
        lang = EXTENSION_LANGUAGE.get(file.suffix.lower())
        if lang:
            counts[lang] += 1

    ranked = counts.most_common()
    languages = []
    for i, (lang, count) in enumerate(ranked):
        languages.append({
            "name": lang,
            "role": "primary" if i == 0 else "secondary",
            "evidence": [f"{count} file(s) with matching extension"],
        })

    common.print_json({"languages": languages, "files_scanned": total_files})
    return 0


if __name__ == "__main__":
    sys.exit(main())
