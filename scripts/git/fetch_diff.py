#!/usr/bin/env python3
"""Fetch Diff

Fetch the diff for the current review (branch, PR, or commit range).
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch the diff for the current review (branch, PR, or commit range).")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
