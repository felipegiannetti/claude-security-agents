#!/usr/bin/env python3
"""Changed Files

List files changed in the current review scope.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="List files changed in the current review scope.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
