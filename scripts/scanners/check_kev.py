#!/usr/bin/env python3
"""Check Kev

Cross-references CVE IDs found by dependency-cve-check (via run_osv_scanner.py)
against the CISA Known Exploited Vulnerabilities (KEV) catalog, and tags each
match with real-world exploitation evidence. This is enrichment, not a new
finding source: it never invents a vulnerability, it only adds an
"actively exploited in the wild" signal that the prioritization stage uses to
override pure-CVSS scoring (see workflow/stages/09_prioritization.md and
skills/dependency-cve-check/references/kev-correlation.md).

Usage:
    check_kev.py --input findings.json --output enriched.json
    cat findings.json | check_kev.py > enriched.json
    check_kev.py --cves CVE-2021-44228 CVE-2023-99999

Input format: a JSON array of finding objects. Any object containing a
top-level "cve" (string) and/or "cve_ids" (list of strings) field is checked;
other fields are passed through unchanged. Matches add a "kev" object:

    {
      "cve": "CVE-2021-44228",
      "kev": {
        "listed": true,
        "vendor_project": "Apache",
        "product": "Log4j2",
        "vulnerability_name": "Apache Log4j2 Remote Code Execution Vulnerability",
        "date_added": "2021-12-10",
        "due_date": "2021-12-24",
        "known_ransomware_campaign_use": "Known",
        "required_action": "..."
      }
    }

Findings with no CVE match get "kev": {"listed": false}. If the catalog can't
be fetched and no usable cache exists, findings are passed through with
"kev": {"listed": null, "lookup_status": "unavailable"} rather than failing
the pipeline -- KEV correlation is a priority signal, not a hard dependency.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

DEFAULT_FEED_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DEFAULT_CACHE_PATH = Path(__file__).resolve().parents[2] / "outputs" / ".cache" / "cisa_kev.json"
DEFAULT_CACHE_TTL_HOURS = 24
REQUEST_TIMEOUT_SECONDS = 15


def load_cache(cache_path: Path) -> Optional[dict]:
    if not cache_path.exists():
        return None
    try:
        return json.loads(cache_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def cache_is_fresh(cache_path: Path, ttl_hours: float) -> bool:
    if not cache_path.exists():
        return False
    age_seconds = time.time() - cache_path.stat().st_mtime
    return age_seconds < ttl_hours * 3600


def fetch_catalog(feed_url: str) -> dict:
    request = urllib.request.Request(feed_url, headers={"User-Agent": "security-review-agent/check_kev.py"})
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def save_cache(cache_path: Path, catalog: dict) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(catalog), encoding="utf-8")


def get_catalog(feed_url: str, cache_path: Path, ttl_hours: float, offline: bool) -> tuple[Optional[dict], str]:
    """Returns (catalog_or_None, lookup_status)."""
    if offline:
        cached = load_cache(cache_path)
        return (cached, "cache") if cached else (None, "unavailable")

    if cache_is_fresh(cache_path, ttl_hours):
        cached = load_cache(cache_path)
        if cached:
            return cached, "cache"

    try:
        catalog = fetch_catalog(feed_url)
        save_cache(cache_path, catalog)
        return catalog, "live"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"warning: could not fetch CISA KEV catalog ({exc}); falling back to cache", file=sys.stderr)
        cached = load_cache(cache_path)
        return (cached, "stale-cache") if cached else (None, "unavailable")


def build_index(catalog: dict) -> dict[str, dict]:
    return {
        entry["cveID"].upper(): entry
        for entry in catalog.get("vulnerabilities", [])
        if entry.get("cveID")
    }


def kev_record(entry: dict) -> dict:
    return {
        "listed": True,
        "vendor_project": entry.get("vendorProject"),
        "product": entry.get("product"),
        "vulnerability_name": entry.get("vulnerabilityName"),
        "date_added": entry.get("dateAdded"),
        "due_date": entry.get("dueDate"),
        "known_ransomware_campaign_use": entry.get("knownRansomwareCampaignUse"),
        "required_action": entry.get("requiredAction"),
    }


def extract_cve_ids(finding: dict) -> list[str]:
    ids = []
    if isinstance(finding.get("cve"), str):
        ids.append(finding["cve"])
    if isinstance(finding.get("cve_ids"), list):
        ids.extend(cve for cve in finding["cve_ids"] if isinstance(cve, str))
    return [cve.upper() for cve in ids]


def enrich_findings(findings: list[dict], index: Optional[dict[str, dict]], lookup_status: str) -> list[dict]:
    enriched = []
    for finding in findings:
        finding = dict(finding)
        cve_ids = extract_cve_ids(finding)

        if index is None:
            finding["kev"] = {"listed": None, "lookup_status": lookup_status}
        else:
            match = next((index[cve] for cve in cve_ids if cve in index), None)
            finding["kev"] = kev_record(match) if match else {"listed": False}

        enriched.append(finding)
    return enriched


def read_findings(input_path: Optional[str], raw_cves: Optional[list[str]]) -> list[dict]:
    if raw_cves:
        return [{"cve": cve} for cve in raw_cves]
    text = Path(input_path).read_text(encoding="utf-8-sig") if input_path else sys.stdin.read()
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
    parser.add_argument("--cves", nargs="+", help="Check specific CVE IDs directly instead of reading findings")
    parser.add_argument("--feed-url", default=DEFAULT_FEED_URL, help="CISA KEV JSON feed URL")
    parser.add_argument("--cache-file", default=str(DEFAULT_CACHE_PATH), help="Local cache path for the catalog")
    parser.add_argument("--cache-ttl-hours", type=float, default=DEFAULT_CACHE_TTL_HOURS)
    parser.add_argument("--offline", action="store_true", help="Never hit the network; use cache only")
    args = parser.parse_args()

    try:
        findings = read_findings(args.input, args.cves)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    catalog, lookup_status = get_catalog(
        args.feed_url, Path(args.cache_file), args.cache_ttl_hours, args.offline
    )
    index = build_index(catalog) if catalog else None

    enriched = enrich_findings(findings, index, lookup_status)
    output_text = json.dumps(enriched, indent=2)

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text)

    listed_count = sum(1 for f in enriched if f.get("kev", {}).get("listed"))
    print(f"KEV lookup status: {lookup_status}; {listed_count}/{len(enriched)} finding(s) actively exploited", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
