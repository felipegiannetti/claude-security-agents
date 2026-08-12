#!/usr/bin/env python3
"""Generate Json

Generate the final JSON report from findings.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the final JSON report from findings.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
