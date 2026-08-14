#!/usr/bin/env python3
"""Calculate Priorities

Implements the weighted priority calculation from config/priority.config.yaml
for 11_security_prioritization. Priority is a function of severity plus
exploitability/exposure/privileges/data-sensitivity/blast-radius/confidence/
effort modifiers -- never severity alone (see CLAUDE.md "Severity and
Priority"). Applies the CISA KEV floor overrides last.

Several inputs (data sensitivity, blast radius, exploitability) are inferred
from free-text finding fields via keyword heuristics, since finding.schema.json
intentionally keeps those fields as prose for readability -- this script
documents exactly which keywords it looks for so the heuristic is auditable,
not a black box. Prefer setting `priority_factors` explicitly on the finding
(security-reviewer/security-verifier's job) over relying on the heuristic
when precision matters.

Usage:
    calculate_priorities.py --input findings.json [--output prioritized.json]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

SEVERITY_BASE = {"critical": 100, "high": 75, "medium": 50, "low": 25, "informational": 0}

DATA_SENSITIVITY_KEYWORDS = {
    "payment_or_credentials": ["payment", "credential", "credit card", "bank"],
    "pii_or_health": ["pii", "personal data", "health", "medical"],
}

BLAST_RADIUS_KEYWORDS = {
    "platform_wide": ["platform-wide", "all users", "all tenants", "system-wide"],
    "multi_tenant": ["multiple users", "multiple tenants", "cross-tenant", "multi-tenant"],
}

EXPLOITABILITY_KEYWORDS = {
    "proof_of_concept_available": ["proof of concept", "poc confirmed", "reproduced"],
    "trivial_to_exploit": ["trivial", "single request", "no special tooling"],
    "requires_chained_conditions": ["requires chaining", "chained with", "combined with another"],
}


def keyword_match(text: str, keyword_map: dict) -> list[str]:
    text_lower = (text or "").lower()
    return [key for key, keywords in keyword_map.items() if any(k in text_lower for k in keywords)]


def score_finding(finding: dict, weights: dict) -> tuple[int, dict]:
    severity = finding.get("severity", "informational")
    score = SEVERITY_BASE.get(severity, 0)
    applied = {"severity_base": score}

    prereqs = finding.get("attacker_prerequisites") or {}
    exposure_weights = weights.get("exposure", {})
    if prereqs.get("network_position") == "internet":
        key = "internet_facing_unauthenticated" if not prereqs.get("authentication_required") else "internet_facing_authenticated"
    else:
        key = "internal_only"
    delta = exposure_weights.get(key, 0)
    score += delta
    applied["exposure"] = {key: delta}

    priv_weights = weights.get("privileges_required", {})
    priv = prereqs.get("privileges_required") or "user"
    priv_key = "none" if priv == "none" else ("user" if priv == "user" else "privileged_or_admin")
    delta = priv_weights.get(priv_key, 0)
    score += delta
    applied["privileges_required"] = {priv_key: delta}

    conf_weights = weights.get("confidence", {})
    confidence = finding.get("confidence", "LOW")
    delta = conf_weights.get(confidence, 0)
    score += delta
    applied["confidence"] = {confidence: delta}

    effort_weights = weights.get("remediation_effort", {})
    effort = (finding.get("remediation") or {}).get("effort")
    if effort:
        delta = effort_weights.get(effort, 0)
        score += delta
        applied["remediation_effort"] = {effort: delta}

    combined_text = " ".join(filter(None, [
        finding.get("business_impact"), finding.get("technical_impact"),
        (finding.get("priority_factors") or {}).get("blast_radius"),
        (finding.get("priority_factors") or {}).get("exploitability"),
    ]))

    data_matches = keyword_match(combined_text, DATA_SENSITIVITY_KEYWORDS)
    data_weights = weights.get("affected_data_sensitivity", {})
    for match in data_matches:
        delta = data_weights.get(match, 0)
        score += delta
        applied.setdefault("affected_data_sensitivity", {})[match] = delta

    blast_matches = keyword_match(combined_text, BLAST_RADIUS_KEYWORDS)
    blast_weights = weights.get("blast_radius", {})
    for match in blast_matches:
        delta = blast_weights.get(match, 0)
        score += delta
        applied.setdefault("blast_radius", {})[match] = delta

    exploit_matches = keyword_match(combined_text, EXPLOITABILITY_KEYWORDS)
    exploit_weights = weights.get("exploitability", {})
    for match in exploit_matches:
        delta = exploit_weights.get(match, 0)
        score += delta
        applied.setdefault("exploitability", {})[match] = delta

    return score, applied


def score_to_priority(score: int, thresholds: dict) -> str:
    for level in ("P0", "P1", "P2", "P3", "P4"):
        if score >= thresholds.get(level, 0):
            return level
    return "P4"


def apply_kev_override(priority: str, finding: dict, kev_overrides: dict, order: list[str]) -> tuple[str, bool]:
    if not kev_overrides.get("enabled"):
        return priority, False
    kev = finding.get("kev") or {}
    if not kev.get("listed"):
        return priority, False

    floor = kev_overrides.get("listed_priority_floor", "P1")
    if kev.get("known_ransomware_campaign_use"):
        floor = kev_overrides.get("known_ransomware_campaign_use_priority_floor", "P0")

    if order.index(floor) < order.index(priority):
        return floor, True
    return priority, False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="Path to a JSON array of CONFIRMED findings (default: stdin)")
    parser.add_argument("--output", help="Write prioritized JSON here instead of stdout")
    args = parser.parse_args()

    findings = common.read_json_input(args.input) or []
    if not isinstance(findings, list):
        print("error: input must be a JSON array", file=sys.stderr)
        return 1

    cfg = common.load_yaml_config("config/priority.config.yaml")
    weights = cfg.get("weights", {})
    thresholds = cfg.get("score_thresholds", {"P0": 90, "P1": 65, "P2": 40, "P3": 15, "P4": 0})
    kev_overrides = cfg.get("kev_overrides", {})
    order = ["P0", "P1", "P2", "P3", "P4"]

    for finding in findings:
        score, applied = score_finding(finding, weights)
        priority = score_to_priority(score, thresholds)
        priority, kev_applied = apply_kev_override(priority, finding, kev_overrides, order)

        finding["priority"] = priority
        finding["priority_factors"] = {
            **(finding.get("priority_factors") or {}),
            "computed_score": score,
            "score_breakdown": applied,
            "kev_override_applied": kev_applied,
        }

    if args.output:
        Path(args.output).write_text(common.json.dumps(findings, indent=2), encoding="utf-8")
    else:
        common.print_json(findings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
