#!/usr/bin/env python3
"""Test Runner

Runs the security review pipeline against tests/fixtures and checks results
against expected_findings.yaml and expected_false_positives.yaml, per the
cases enumerated in eval_cases.yaml.
"""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run security review regression evals.")
    parser.add_argument("--cases", default="eval_cases.yaml")
    parser.parse_args()
    # TODO: implement
    return 0


if __name__ == "__main__":
    sys.exit(main())
