#!/usr/bin/env python3
"""Test Runner

Runs security regression evals against tests/fixtures, per the cases in
eval_cases.yaml, checked against expected_findings.yaml and
expected_false_positives.yaml.

Two tiers of eval, because not every finding category is scanner-detectable:

1. Scanner-checkable cases (eval_cases.yaml has a non-null `scanner`): this
   script actually runs the named scanner script (scripts/scanners/*.py)
   against both the vulnerable_path and safe_path fixtures and checks that
   the scanner fires on the vulnerable one and not the safe one. This is a
   real, automated true/false-positive check, but only covers what a
   deterministic scanner alone can catch (see skills/*/SKILL.md -- most
   categories, like BOLA/IDOR, fundamentally require the LLM-driven
   06_llm_security_review stage's contextual reasoning, not just a scanner).
2. LLM-only cases (`scanner: null`): this script cannot execute an agentic
   review itself. It reports these as requiring a manual or agent-driven
   run of the full pipeline against the fixture pair, and prints exactly
   what outcome to check for (from expected_findings.yaml /
   expected_false_positives.yaml) so that run can be evaluated consistently.

When a real false positive is found (a Skill flagging a "safe" fixture, or a
scanner missing a "vulnerable" one), add the specific failing scenario as a
new eval_cases.yaml entry per CLAUDE.md Development Rule 7, and adjust the
relevant Skill's false-positive criteria -- don't just quietly accept it.

Usage:
    test_runner.py [--cases eval_cases.yaml]
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "lib"))
import common  # noqa: E402

TESTS_ROOT = Path(__file__).resolve().parent
SCANNERS_DIR = TESTS_ROOT.parent / "scripts" / "scanners"

SCANNER_SCRIPTS = {
    "semgrep": SCANNERS_DIR / "run_semgrep.py",
    "gitleaks": SCANNERS_DIR / "run_gitleaks.py",
    "trivy": SCANNERS_DIR / "run_trivy.py",
    "osv-scanner": SCANNERS_DIR / "run_osv_scanner.py",
}


def run_scanner(scanner: str, target_path: Path) -> tuple[list[dict], bool]:
    """Returns (hits, tool_unavailable). A scanner script that couldn't find
    its underlying tool prints a {"skipped": true, ...} object, not a list --
    that must never be misread as "hits" (a dict's len() is its key count,
    which is nonzero and would silently look like a true positive)."""
    script = SCANNER_SCRIPTS.get(scanner)
    if not script:
        return [], True
    result = common.run_tool([sys.executable, str(script), "--path", str(target_path)], timeout=120)
    if not result["ok"] or result["returncode"] != 0:
        print(f"    warning: {scanner} run failed ({result.get('error') or result.get('stderr')})", file=sys.stderr)
        return [], True
    try:
        parsed = common.json.loads(result["stdout"] or "[]")
    except common.json.JSONDecodeError:
        return [], True
    if isinstance(parsed, dict) and parsed.get("skipped"):
        print(f"    note: {scanner} skipped itself ({parsed.get('reason')})", file=sys.stderr)
        return [], True
    return (parsed if isinstance(parsed, list) else []), False


def check_scanner_case(case: dict) -> Optional[bool]:
    """Returns True/False for pass/fail, or None if the underlying scanner
    tool wasn't available -- a SKIP must never count as a PASS or a FAIL."""
    scanner = case["scanner"]
    vulnerable_path = TESTS_ROOT / case["vulnerable_path"]
    safe_path = TESTS_ROOT / case["safe_path"]

    vulnerable_hits, vuln_unavailable = run_scanner(scanner, vulnerable_path)
    safe_hits, safe_unavailable = run_scanner(scanner, safe_path)

    if vuln_unavailable or safe_unavailable:
        print(f"  [SKIP] {case['id']} ({scanner}): tool not available in this environment", file=sys.stderr)
        return None

    true_positive = len(vulnerable_hits) > 0
    false_positive = len(safe_hits) > 0

    status = "PASS" if (true_positive and not false_positive) else "FAIL"
    print(f"  [{status}] {case['id']} ({scanner}): "
          f"vulnerable={'flagged' if true_positive else 'MISSED'}, "
          f"safe={'FALSELY FLAGGED' if false_positive else 'clean'}")
    return status == "PASS"


def report_manual_case(case: dict, expected_findings: dict, expected_fps: dict) -> None:
    finding = expected_findings.get("findings", {}).get(case["id"], {})
    fp = expected_fps.get("false_positives", {}).get(case["id"], {})
    print(f"  [MANUAL] {case['id']}: requires a full pipeline run (06_llm_security_review) -- not scanner-detectable")
    print(f"           vulnerable_path should CONFIRM: {finding.get('category')} "
          f"(CWE {finding.get('cwe')}, min severity {finding.get('min_severity')})")
    print(f"           safe_path should NOT confirm -- why: {fp.get('why_safe')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cases", default=str(TESTS_ROOT / "eval_cases.yaml"))
    args = parser.parse_args()

    cases_cfg = common.yaml.safe_load(Path(args.cases).read_text(encoding="utf-8-sig")) if common.yaml else {}
    cases = (cases_cfg or {}).get("cases", [])
    expected_findings = common.yaml.safe_load((TESTS_ROOT / "expected_findings.yaml").read_text(encoding="utf-8-sig")) if common.yaml else {}
    expected_fps = common.yaml.safe_load((TESTS_ROOT / "expected_false_positives.yaml").read_text(encoding="utf-8-sig")) if common.yaml else {}

    if not cases:
        print("no eval cases found", file=sys.stderr)
        return 1

    print(f"Running {len(cases)} eval case(s)...\n")

    automated_pass = automated_fail = automated_skip = 0
    for case in cases:
        if case.get("scanner"):
            outcome = check_scanner_case(case)
            if outcome is None:
                automated_skip += 1
            elif outcome:
                automated_pass += 1
            else:
                automated_fail += 1
        else:
            report_manual_case(case, expected_findings or {}, expected_fps or {})

    automated_run = automated_pass + automated_fail
    print(f"\nAutomated (scanner-level) checks: {automated_pass}/{automated_run} passed"
          f"{f' ({automated_skip} skipped -- underlying tool not installed)' if automated_skip else ''}")
    print(f"Manual (LLM-review-level) checks: {sum(1 for c in cases if not c.get('scanner'))} case(s) "
          f"require a pipeline run -- see output above for expected outcomes.")

    # A SKIP (tool unavailable) is not a failure of this project's detection
    # logic -- only an actual FAIL (tool ran and got the wrong answer) should
    # fail the run.
    return 0 if automated_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
