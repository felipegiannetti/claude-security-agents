#!/usr/bin/env python3
"""Calculate Priorities

Calculate finding priority from severity, confidence, and exploitability.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate finding priority from severity, confidence, and exploitability.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
