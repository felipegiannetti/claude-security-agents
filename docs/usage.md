# Usage

## Prerequisites

- Python 3.10+ with `pip install -r scripts/requirements.txt` (PyYAML).
- For full static-scan coverage: Semgrep (`pip install semgrep`), Gitleaks, Trivy, and OSV-Scanner installed and on `PATH`. All four degrade gracefully (a `skipped` result, not a crash) if not installed -- see `docs/adding-scanners.md`.
- Claude Code, with this project loaded as a plugin (`.claude-plugin/plugin.json`) or as the active project.

## Running a Review

There is no single `review` command -- the pipeline is a sequence of agent invocations and script calls, driven by the orchestrating Claude Code session (you, talking to Claude, with this plugin loaded). A typical flow:

1. **Intake**: tell Claude the scope -- a repository path, a diff, or a PR.
2. Claude invokes `architecture-mapper` to build the architecture model (`schemas/architecture.schema.json`).
3. Attack surface mapping and static scanning run (the latter via `scripts/scanners/*.py`).
4. Claude invokes `security-reviewer`, which selects Skills per `workflow/routing_rules.yaml` and produces candidate findings.
5. Claude invokes `security-verifier` to independently challenge each candidate.
6. *(Optional, off by default)* If `config/pentest.config.yaml` is enabled with an authorized target, `pentest-validator` runs confirmation-only dynamic checks -- see `docs/usage.md#dynamic-validation` below.
7. `scripts/reporting/calculate_priorities.py` assigns priority to confirmed findings.
8. *(Optional)* Claude invokes `architecture-advisor` for the Software Architecture axis.
9. Remediation guidance is generated per confirmed finding.
10. `${CLAUDE_PLUGIN_ROOT}/scripts/reporting/generate_markdown.py` (and `generate_json.py`/`generate_sarif.py` as needed) produce the final report. Claude presents it directly in the conversation AND always saves it as a file automatically -- via `${CLAUDE_PLUGIN_ROOT}/scripts/reporting/resolve_report_path.py`, which always resolves to a location OUTSIDE the reviewed project (default `~/SecurityReviews/<project>-<timestamp>/`), never inside it, per `.claude/rules/security.md` "Absolute Read-Only Policy." Claude reports the exact path and attempts to open the file for you.

## Dynamic Validation (Optional)

Disabled by default. To enable it for a specific, explicitly authorized target:

1. Edit this plugin's own `config/pentest.config.yaml` (in the plugin's installation directory, never a file in whatever project you're reviewing): set `enabled: true` and add a `targets[]` entry with the exact URL, `environment` (`development`/`staging`/`homologation`; `production` requires `production_authorized: true`), and who authorized it.
2. `pentest-validator` will then confirm eligible findings (see `validation_scope.categories_eligible`) using only non-mutating `GET`/`HEAD`/`OPTIONS` requests -- see `agents/pentest-validator.md`.
3. For findings that would need a mutating request to confirm, `scripts/pentest/validate_finding.py` refuses automatically and produces a manual validation request instead -- see `docs/finding-model.md` and `scripts/pentest/generate_manual_validation_report.py`.

**Never** add a target that wasn't explicitly authorized by a human, and never infer one from application code/config.

## Running the Test Suite

See `docs/testing.md`.

## Verifying a Fresh Environment

Before relying on this in a real review, confirm your environment actually works end to end:

```bash
python --version                 # 3.10+
pip install -r scripts/requirements.txt
python tests/test_runner.py      # expect all automated cases to PASS or SKIP, never FAIL
```

A `FAIL` means either an environment problem or a real regression -- don't ignore it.
