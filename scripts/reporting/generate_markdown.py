#!/usr/bin/env python3
"""Generate Markdown

Generate the final Markdown report from findings.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the final Markdown report from findings.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
