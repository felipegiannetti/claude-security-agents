#!/usr/bin/env python3
"""Detect Dependencies

Enumerates dependency manifest/lockfile locations per ecosystem, for handoff
to dependency-cve-check / run_osv_scanner.py. Does not resolve versions
itself -- that's the scanner's job; this only locates the manifests.

Usage:
    detect_dependencies.py --path <dir>
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

MANIFEST_PATTERNS = {
    "npm": (["package.json"], ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"]),
    "pip": (["requirements*.txt", "pyproject.toml", "Pipfile"], ["poetry.lock", "Pipfile.lock"]),
    "maven": (["pom.xml"], []),
    "gradle": (["build.gradle", "build.gradle.kts"], ["gradle.lockfile"]),
    "nuget": (["*.csproj"], ["packages.lock.json"]),
}

EXCLUDE_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path)
    dependencies = []

    for ecosystem, (manifest_globs, lockfile_names) in MANIFEST_PATTERNS.items():
        for pattern in manifest_globs:
            for manifest in root.rglob(pattern):
                if any(part in EXCLUDE_DIRS for part in manifest.parts):
                    continue
                lockfile = next(
                    (str(manifest.parent / lf) for lf in lockfile_names if (manifest.parent / lf).exists()),
                    None,
                )
                dependencies.append({
                    "ecosystem": ecosystem,
                    "manifest_file": str(manifest),
                    "lockfile": lockfile,
                })

    common.print_json({"dependencies": dependencies})
    return 0


if __name__ == "__main__":
    sys.exit(main())
