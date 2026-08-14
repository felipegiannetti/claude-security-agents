# Creating a New Skill

Follow this when adding coverage for a vulnerability category or domain the existing 13 Skills don't cover well.

## 1. Confirm It's Actually a New Skill

Check `.claude/rules/skills.md` "Skill Scope" first -- a Skill should have one coherent domain (`injection-review`, not `everything-security-review`). If what you're adding is really a new reference file for an existing domain (e.g. a new injection variant), add it to that Skill's `references/` instead of creating a new Skill.

## 2. Directory Structure

```
skills/<skill-name>/
├── SKILL.md
└── references/
    └── <topic>.md
```

## 3. Write SKILL.md

Include, per the pattern every existing Skill follows:
- Frontmatter: `name`, `description` (specific enough that routing/selection can rely on it).
- A one-line link list to each reference file.
- "When to Use" -- what triggers this Skill (file patterns, frameworks, entry-point types).
- "Core Discipline" -- the 2-4 sentence version of what makes this domain's analysis different from a generic pattern match.
- "Output" -- confirm it emits `finding.schema.json`-shaped candidates.

## 4. Write Reference Files

Each reference file (one per sub-topic, e.g. `sql-injection.md` under `injection-review`) should have, at minimum:
- **CWE / OWASP mapping** at the top.
- **What to Look For** -- concrete source-sink checklist, not just a definition.
- **False-Positive Conditions** -- explicit, specific conditions that would make this NOT exploitable. This section is mandatory -- see CLAUDE.md Development Rule 6 ("every new finding type must define how false positives are evaluated").
- **Severity Notes** -- default severity and what shifts it.

## 5. Wire It In

- Add the category(ies) to `config/severity.config.yaml` → `category_base_severity` and `config/remediation.config.yaml` → `category_default_effort`.
- Add the CWE mapping to `knowledge/cwe/cwe-mapping.json`.
- Add routing rules to `workflow/routing_rules.yaml` if the Skill should trigger on specific file patterns/frameworks/entry-point types.
- Reference the new Skill from `agents/security-reviewer.md`'s Skill list.

## 6. Add Test Fixtures

Per `.claude/rules/testing.md`: a vulnerable/safe pair under `tests/fixtures/<category>/`, wired into `tests/eval_cases.yaml`, `tests/expected_findings.yaml`, and `tests/expected_false_positives.yaml`. If a deterministic scanner reliably catches the vulnerable case and not the safe one, set `scanner:` to that tool in `eval_cases.yaml` for an automated check; otherwise leave it `null` and document the expected pipeline-run outcome (most categories genuinely need the LLM review stage -- see `tests/test_runner.py`'s docstring for why).

## 7. Validate

Run `python tests/test_runner.py` and confirm your new case appears and, if scanner-checkable, passes.
