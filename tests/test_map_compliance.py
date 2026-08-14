#!/usr/bin/env python3
"""Test Map Compliance

Regression check for scripts/reporting/map_compliance.py -- confirms the
deterministic lookup returns the EXACT expected technique/control IDs for
a handful of core categories, and confirms an unmapped category gets no
fabricated field. This guards against the specific failure mode the
deterministic-lookup design exists to prevent: a hallucinated MITRE
ATT&CK/NIST/ISO identifier silently ending up in a report.

Usage: test_map_compliance.py (no arguments, plain asserts, exit 0/1)
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / 'scripts' / 'reporting' / 'map_compliance.py'

SAMPLE_FINDINGS = [
    {'id': 'SEC-001', 'category': 'sql-injection'},
    {'id': 'SEC-002', 'category': 'weak-cryptography'},
    {'id': 'SEC-003', 'category': 'hardcoded-credential-live'},
    {'id': 'SEC-004', 'category': 'this-category-does-not-exist'},
]

EXPECTED_ATTACK_IDS = {
    'sql-injection': ['T1190'],
    'weak-cryptography': None,
    'hardcoded-credential-live': ['T1552.001', 'T1190'],
    'this-category-does-not-exist': None,
}

EXPECTED_NIST_IDS = {
    'sql-injection': ['PR.PS'],
    'weak-cryptography': ['PR.DS'],
    'hardcoded-credential-live': ['PR.AA', 'PR.DS'],
    'this-category-does-not-exist': None,
}

EXPECTED_ISO_IDS = {
    'sql-injection': ['A.8.28'],
    'weak-cryptography': ['A.8.24'],
    'hardcoded-credential-live': ['A.8.12', 'A.8.24'],
    'this-category-does-not-exist': None,
}


def main() -> int:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(SAMPLE_FINDINGS),
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        print('FAIL: map_compliance.py exited', result.returncode, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1

    enriched = json.loads(result.stdout)
    by_category = {f['category']: f for f in enriched}

    failures = []
    for category, expected in EXPECTED_ATTACK_IDS.items():
        finding = by_category[category]
        actual = [t['id'] for t in finding.get('mitre_attack', {}).get('techniques', [])] or None
        if actual != expected:
            failures.append('ATT&CK mismatch for ' + category + ': expected ' + str(expected) + ', got ' + str(actual))

    for category, expected in EXPECTED_NIST_IDS.items():
        finding = by_category[category]
        actual = [c['id'] for c in finding.get('compliance_mappings', {}).get('nist_csf', [])] or None
        if actual != expected:
            failures.append('NIST mismatch for ' + category + ': expected ' + str(expected) + ', got ' + str(actual))

    for category, expected in EXPECTED_ISO_IDS.items():
        finding = by_category[category]
        actual = [c['id'] for c in finding.get('compliance_mappings', {}).get('iso27001', [])] or None
        if actual != expected:
            failures.append('ISO mismatch for ' + category + ': expected ' + str(expected) + ', got ' + str(actual))

    if failures:
        print('FAIL:')
        for f in failures:
            print('  -', f)
        return 1

    print('PASS: all', len(SAMPLE_FINDINGS), 'sample categories matched expected framework mappings exactly')
    return 0


if __name__ == '__main__':
    sys.exit(main())
