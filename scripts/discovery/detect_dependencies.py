#!/usr/bin/env python3
"""Detect Dependencies

Enumerate direct and transitive dependencies.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Enumerate direct and transitive dependencies.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
