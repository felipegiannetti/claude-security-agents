#!/usr/bin/env python3
"""Resolve Report Path

Deterministically computes and creates the directory where a completed
review's report should be saved -- always OUTSIDE the analyzed project,
per CLAUDE.md's Absolute Read-Only Policy, which forbids creating any
file inside the analyzed repository. A fixed, predictable base location
(not a value the model picks per run) means every review's output ends
up somewhere the user can find consistently, and two reviews of the same
or different projects never collide.

Usage:
    resolve_report_path.py --project-name my-app
    # prints the absolute path to the created directory, e.g.:
    # e.g. (Windows) C:/Users/you/SecurityReviews/my-app-20260819-143022
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

DEFAULT_BASE_DIR_NAME = 'SecurityReviews'


def sanitize(name: str) -> str:
    name = (name or '').strip() or 'project'
    cleaned = re.sub(r'[^A-Za-z0-9._-]+', '-', name).strip('-')
    return cleaned or 'project'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project-name', required=True, help='Name of the project being reviewed, used in the folder name')
    parser.add_argument('--base-dir', default=None, help='Override the base directory (default: ~/SecurityReviews)')
    args = parser.parse_args()

    base = Path(args.base_dir) if args.base_dir else Path.home() / DEFAULT_BASE_DIR_NAME
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    target = base / (sanitize(args.project_name) + '-' + timestamp)
    target.mkdir(parents=True, exist_ok=True)
    print(str(target))
    return 0


if __name__ == '__main__':
    sys.exit(main())
