# MITRE ATT&CK Mapping

## What this is

[MITRE ATT&CK](https://attack.mitre.org/) is a public, freely-licensed (CC BY-SA 4.0) knowledge base of adversary tactics and techniques observed in real intrusions. It is fundamentally an **adversary-behavior model**, not a vulnerability taxonomy -- it describes what an attacker *does*, not what a piece of code is *wrong* in the way CWE does. That distinction matters for how this mapping should be read.

## How it is produced here

`knowledge/mitre/attack-mapping.json` maps a `finding.schema.json` `category` string to one or more ATT&CK technique IDs, looked up deterministically by `scripts/reporting/map_compliance.py` -- the same pattern as `scripts/scanners/check_kev.py`'s CVE lookup. This is a deliberate design choice: asking an LLM to recall an ATT&CK technique ID from memory during a review is a known way to get a plausible-looking but wrong ID. A fixed lookup table, reviewed once by a human and then reused deterministically, removes that failure mode entirely.

## Why it is not exhaustive

The mapping file only covers **categories with a high-confidence, defensible technique match** -- currently 15 of this project's ~45 finding categories. Most map to **T1190 (Exploit Public-Facing Application)**, which is the correct, MITRE-documented technique for exploiting an application-layer weakness in an Internet-facing system; MITRE's own T1190 description explicitly names SQL injection, cross-site scripting, cross-site request forgery, and remote file inclusion as examples of this technique, so that mapping is not a stretch.

A handful of categories are deliberately **absent** from the mapping file rather than forced into a weak match -- `weak-cryptography` is the clearest example. ATT&CK's Enterprise matrix has a technique for an adversary *actively downgrading* strong encryption (T1600, Weaken Encryption), but no technique for "the application shipped with weak encryption baked in" -- that is a design weakness with real consequences, but it is not adversary *behavior*, so forcing a T1600 label onto it would misrepresent what ATT&CK actually measures. When a category has no defensible mapping, `map_compliance.py` omits the field entirely rather than guessing -- absence of a `mitre_attack` field means "not yet mapped," never "this finding has no attacker relevance."

## Expanding the mapping

Adding a new category: confirm the technique against the current ATT&CK Enterprise matrix directly (technique numbering and sub-techniques do change between MITRE revisions), add the entry to `attack-mapping.json` with the same `{id, name, tactic}` shape, and prefer omission over a low-confidence guess. A `note` field is available on any entry to record a condition under which a technique should or should not be attached (see `ssrf`, `authentication-bypass`, and `vulnerable-dependency` in the current file for examples) -- these notes exist because ATT&CK technique attachment sometimes depends on what the specific finding's evidence actually shows, not just its category.

## On CrowdStrike and other threat-intel sources

CrowdStrike (and other threat-intel vendors) publish research that is explicitly organized around MITRE ATT&CK -- adversary profiles, campaign write-ups, and their annual Global Threat Report all reference specific technique IDs. That public research is a legitimate **citation source** for writing informed, current context into this file or into a specific finding's exploitation narrative (e.g. "T1190-based exploitation of public-facing applications remains among the most commonly observed initial-access vectors per public industry reporting").

It is explicitly **not** a live data integration. Unlike the CISA KEV catalog (`scripts/scanners/check_kev.py`), which has a free public JSON feed this project polls directly, CrowdStrike's detailed adversary intelligence (Falcon Intelligence) is a paid, licensed product this project has no credentials for and no right to poll programmatically. Any reference to CrowdStrike research in this project's output must be a citation to their public material, never a claim of a live feed that does not exist.

## Relationship to CWE and OWASP

CWE (`knowledge/cwe/cwe-mapping.json`) answers "what kind of weakness is this, in the code." OWASP Top 10 answers "which well-known risk category does this fall under, for a broad audience." MITRE ATT&CK answers "what would an attacker actually be doing if they exploited this." All three can be populated on the same finding without conflict -- they are different lenses on the same underlying issue, not competing classifications.
