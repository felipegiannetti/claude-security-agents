#!/usr/bin/env python3
"""Normalize Findings

Normalize findings from all sources into the shared finding schema.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize findings from all sources into the shared finding schema.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
