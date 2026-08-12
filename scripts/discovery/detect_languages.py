#!/usr/bin/env python3
"""Detect Languages

Detect programming languages present in the codebase.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect programming languages present in the codebase.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
