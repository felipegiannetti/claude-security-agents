#!/usr/bin/env python3
"""Run Osv Scanner

Run OSV-Scanner against dependency manifests and emit normalized JSON results.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OSV-Scanner against dependency manifests and emit normalized JSON results.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
