# Adding a Deterministic Scanner

Follow this when integrating a new external tool into `scripts/scanners/`.

## Conventions Every Scanner Script Follows

Look at `scripts/scanners/run_semgrep.py` or `run_trivy.py` as the reference implementation. Every scanner script:

1. Is a standalone CLI: `argparse`, `--path` for the scan target, `--output` (default stdout).
2. Reads its enabled/disabled state and any tool-specific options from `config/scanners.config.yaml` via `scripts/lib/common.load_yaml_config`.
3. Invokes the external tool via `scripts/lib/common.run_tool`, never a raw `subprocess.run` call -- this gets you the "tool not found" / timeout handling for free.
4. **Degrades, never crashes**, if the tool isn't installed or the run fails: prints a `{"tool": "...", "skipped": true, "reason": "..."}` object and exits 0. A missing scanner should reduce coverage, not break the pipeline.
5. Normalizes native tool output into `scan-result.schema.json` shape -- see each script's `normalize()` function.
6. **Never runs in autofix mode.** No `--fix`, `--autofix`, or equivalent flag, ever -- see `.claude/rules/security.md` "Defensive Execution Policy."
7. If the tool's output could contain secrets (like Gitleaks), mask them before they leave the script -- see `run_gitleaks.py`'s `mask()`.

## Steps

1. Add the tool to `scripts/requirements.txt` if it's pip-installable, or note the external install method (winget/apt/brew) if it's a standalone binary -- see the comment block at the top of `requirements.txt` for the existing pattern.
2. Write `scripts/scanners/run_<tool>.py` following the conventions above.
3. Add a config block to `config/scanners.config.yaml`.
4. Reference it from `workflow/stages/05_static_security_scanning.md`.
5. **Verify the tool's actual current CLI** before assuming a syntax -- tool CLIs change between major versions (this project already hit this once: `osv-scanner` v2 requires a `scan source` subcommand that v1's flat flag syntax doesn't have, and it fails by silently scanning the wrong root rather than erroring clearly). Run the tool directly first, don't just trust its `--help` from memory or documentation that might be for an older version.
6. Test against a real installed instance of the tool -- `tests/test_runner.py` will report `[SKIP]` (not pass or fail) if the tool isn't installed in the current environment, which is correct but means you must install the tool locally at least once to confirm your integration actually works, not just that it degrades gracefully.

## What NOT to Add Here

Anything requiring judgment about whether a hit is a real vulnerability belongs in a Skill's false-positive analysis (`security-reviewer` correlates scanner output with code context in stage 06), not in the scanner script itself. The scanner script's job ends at producing evidence.
