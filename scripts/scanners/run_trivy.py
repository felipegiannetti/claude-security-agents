#!/usr/bin/env python3
"""Run Trivy

Run Trivy vulnerability/misconfig scanning and emit normalized JSON results.
"""

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Trivy vulnerability/misconfig scanning and emit normalized JSON results.")
    parser.parse_args()
    # TODO: implement
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
