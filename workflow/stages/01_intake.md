# Stage 01: Intake

## Purpose

Establish the exact scope of the review before any analysis begins. An undefined scope is the most common cause of an unfocused, low-signal review.

## Inputs

- A target: full repository path/URL, a diff/patch, a PR reference, or a specific branch/commit range.
- Optional: explicit inclusion/exclusion paths, priority areas the requester wants covered, and the intended report format(s) (Markdown / JSON / SARIF).

## Process

1. Resolve the target using `scripts/git/repository_info.py` (remote, default branch, current commit) and, if scope is a diff/PR, `scripts/git/fetch_diff.py` + `scripts/git/changed_files.py`.
2. Apply `config/exclusions.yaml` to drop vendored/generated/build paths from scope.
3. Classify the review type: `full-repository`, `diff`, or `pull-request`. This determines whether `02_architecture_discovery` builds a full model or an incremental one anchored on `architecture.schema.json` from a prior run if available.
4. Record the scope decision — this is what every later stage's "in scope" / "out of scope" judgment is measured against.

## Outputs

- A review scope record: target type, resolved repository metadata, included/excluded paths, changed files (if applicable), requested output formats.

## Success Criteria

- Scope is unambiguous enough that a file either is or is not part of this review, with no stage needing to re-derive it.
