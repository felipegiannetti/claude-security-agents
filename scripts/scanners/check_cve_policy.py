#!/usr/bin/env python3
"""Check Cve Policy

Flags dependency CVEs that meet a configurable "recent and severe" policy,
independent of CISA KEV listing status (see scripts/scanners/check_kev.py).
KEV correlation answers "is this being actively exploited right now" -- a
narrow, high-confidence signal that most CVEs will never trigger. This
script answers a broader, proactive question: "is this a severe
vulnerability that was disclosed recently enough that exploit tooling is
plausibly circulating, whether or not CISA has confirmed active
exploitation yet." See skills/dependency-cve-check/references/cve-policy.md.

Policy (config/scanners.config.yaml -> cve_policy):
    min_severity: the minimum CVSS severity rating (low|medium|high|critical)
        that qualifies for a policy flag.
    max_age_days: only CVEs first published within this many days are
        flagged -- an old medium-severity CVE with no exploitation history
        is exactly the kind of stale, low-signal finding this policy should
        NOT surface.

Input format: a JSON array of finding objects as produced by
run_osv_scanner.py (each with a "raw_output" field holding the full OSV
vulnerability record). Any object without a usable "raw_output" is passed
through with a "no-osv-record" reason. Matches add a "cve_policy" object:

    {
      "cve_policy": {
        "flagged": true,
        "severity_rating": "high",
        "cvss_score": 8.1,
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N",
        "published": "2026-02-14T00:00:00Z",
        "age_days": 92,
        "policy": {"min_severity": "medium", "max_age_days": 365}
      }
    }

Findings with no determinable severity get "cve_policy":
{"flagged": false, "reason": "severity-undetermined"} rather than a silent
false -- undetermined severity is not evidence of low severity, so it must
never be conflated with a genuine below-threshold rating.

Usage:
    check_cve_policy.py --input findings.json --output enriched.json
    cat findings.json | check_cve_policy.py > enriched.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

SEVERITY_ORDER = ["low", "medium", "high", "critical"]

# CVSS v3.0/3.1 base-score metric weights (see first.org CVSS v3.1
# specification section 7.4). Implemented locally rather than via a
# dependency -- this is a small, stable, spec-fixed formula.
AV_WEIGHTS = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AC_WEIGHTS = {"L": 0.77, "H": 0.44}
UI_WEIGHTS = {"N": 0.85, "R": 0.62}
CIA_WEIGHTS = {"N": 0.0, "L": 0.22, "H": 0.56}
PR_WEIGHTS_UNCHANGED = {"N": 0.85, "L": 0.62, "H": 0.27}
PR_WEIGHTS_CHANGED = {"N": 0.85, "L": 0.68, "H": 0.5}

DATABASE_SEVERITY_MAP = {
    "LOW": "low",
    "MODERATE": "medium",
    "MEDIUM": "medium",
    "HIGH": "high",
    "CRITICAL": "critical",
}


def parse_cvss_v3_vector(vector: str) -> Optional[float]:
    """Computes the CVSS v3.0/3.1 base score from a vector string. Returns
    None (never a guessed number) if a required metric is missing."""
    parts = {}
    for segment in vector.split("/"):
        if ":" not in segment:
            continue
        key, _, value = segment.partition(":")
        parts[key] = value

    try:
        av, ac, pr, ui, s = parts["AV"], parts["AC"], parts["PR"], parts["UI"], parts["S"]
        c, i, a = parts["C"], parts["I"], parts["A"]
    except KeyError:
        return None

    scope_changed = s == "C"
    pr_weights = PR_WEIGHTS_CHANGED if scope_changed else PR_WEIGHTS_UNCHANGED

    try:
        av_w, ac_w, ui_w = AV_WEIGHTS[av], AC_WEIGHTS[ac], UI_WEIGHTS[ui]
        pr_w = pr_weights[pr]
        c_w, i_w, a_w = CIA_WEIGHTS[c], CIA_WEIGHTS[i], CIA_WEIGHTS[a]
    except KeyError:
        return None

    iss = 1 - ((1 - c_w) * (1 - i_w) * (1 - a_w))
    if scope_changed:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)
    else:
        impact = 6.42 * iss

    if impact <= 0:
        return 0.0

    exploitability = 8.22 * av_w * ac_w * pr_w * ui_w
    raw = (impact + exploitability) * (1.08 if scope_changed else 1.0)
    capped = min(raw, 10.0)

    # CVSS "Roundup" per spec: ceiling to one decimal place, done via
    # integer math to avoid float-rounding surprises at exact boundaries.
    int_score = int(round(capped * 100000))
    if int_score % 10000 == 0:
        return int_score / 100000
    return (int_score // 10000 + 1) / 10.0


def rating_from_score(score: float) -> str:
    if score == 0.0:
        return "none"
    if score < 4.0:
        return "low"
    if score < 7.0:
        return "medium"
    if score < 9.0:
        return "high"
    return "critical"


def determine_severity(vuln: dict) -> tuple:
    """Returns (rating_or_None, score_or_None, vector_or_None). Prefers an
    explicit database_specific.severity (common on GHSA-sourced advisories,
    reflecting the advisory publisher's own triage) over computing a CVSS
    base score from a vector, since the publisher's rating already accounts
    for context a bare vector doesn't capture."""
    db_severity = (vuln.get("database_specific") or {}).get("severity")
    if isinstance(db_severity, str) and db_severity.upper() in DATABASE_SEVERITY_MAP:
        return DATABASE_SEVERITY_MAP[db_severity.upper()], None, None

    for entry in vuln.get("severity", []) or []:
        if entry.get("type") == "CVSS_V3":
            vector = entry.get("score")
            if isinstance(vector, str) and vector.startswith("CVSS:3"):
                score = parse_cvss_v3_vector(vector)
                if score is not None:
                    return rating_from_score(score), score, vector

    return None, None, None


def parse_published(vuln: dict) -> Optional[datetime]:
    raw = vuln.get("published")
    if not isinstance(raw, str):
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def evaluate_policy(finding: dict, min_severity: str, max_age_days: int, now: datetime) -> dict:
    vuln = finding.get("raw_output")
    if not isinstance(vuln, dict):
        return {"flagged": False, "reason": "no-osv-record"}

    rating, score, vector = determine_severity(vuln)
    if rating is None:
        return {"flagged": False, "reason": "severity-undetermined"}
    if rating == "none":
        return {"flagged": False, "reason": "severity-none", "severity_rating": rating}

    published = parse_published(vuln)
    if published is None:
        return {
            "flagged": False,
            "reason": "publish-date-unknown",
            "severity_rating": rating,
            "cvss_score": score,
            "cvss_vector": vector,
        }

    age_days = (now - published).days
    meets_severity = SEVERITY_ORDER.index(rating) >= SEVERITY_ORDER.index(min_severity)
    meets_age = 0 <= age_days <= max_age_days

    return {
        "flagged": bool(meets_severity and meets_age),
        "severity_rating": rating,
        "cvss_score": score,
        "cvss_vector": vector,
        "published": vuln.get("published"),
        "age_days": age_days,
        "policy": {"min_severity": min_severity, "max_age_days": max_age_days},
    }


def enrich_findings(findings: list, min_severity: str, max_age_days: int) -> list:
    now = datetime.now(timezone.utc)
    enriched = []
    for finding in findings:
        finding = dict(finding)
        finding["cve_policy"] = evaluate_policy(finding, min_severity, max_age_days, now)
        enriched.append(finding)
    return enriched


def read_findings(input_path: Optional[str]) -> list:
    text = Path(input_path).read_text(encoding="utf-8-sig") if input_path else sys.stdin.read()
    text = text.lstrip("\ufeff")
    data = json.loads(text) if text.strip() else []
    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]
    if not isinstance(data, list):
        raise ValueError("input must be a JSON array of findings (or an object with a top-level 'findings' array)")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="Path to a JSON findings file (default: stdin)")
    parser.add_argument("--output", help="Path to write enriched JSON (default: stdout)")
    parser.add_argument("--min-severity", choices=SEVERITY_ORDER, help="Override config/scanners.config.yaml cve_policy.min_severity")
    parser.add_argument("--max-age-days", type=int, help="Override config/scanners.config.yaml cve_policy.max_age_days")
    args = parser.parse_args()

    cfg = common.load_yaml_config("config/scanners.config.yaml").get("cve_policy", {})
    if not cfg.get("enabled", True):
        common.print_json({"tool": "check-cve-policy", "skipped": True, "reason": "disabled in config/scanners.config.yaml"})
        return 0

    min_severity = args.min_severity or cfg.get("min_severity", "medium")
    max_age_days = args.max_age_days if args.max_age_days is not None else cfg.get("max_age_days", 365)

    try:
        findings = read_findings(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    enriched = enrich_findings(findings, min_severity, max_age_days)
    output_text = json.dumps(enriched, indent=2)

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text)

    flagged_count = sum(1 for f in enriched if f.get("cve_policy", {}).get("flagged"))
    print(
        f"CVE policy: min_severity={min_severity} max_age_days={max_age_days}; "
        f"{flagged_count}/{len(enriched)} finding(s) flagged",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())