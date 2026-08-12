---
name: secrets-detection
description: Detects hardcoded and leaked secrets - API keys, cloud credentials, database credentials, tokens, and private keys. Use when scanning source, config, or history for exposed credentials.
---

# Secrets Detection

Correlates [run_gitleaks.py](../../scripts/scanners/run_gitleaks.py) output with code context. Always runs regardless of routing (see [workflow/routing_rules.yaml](../../workflow/routing_rules.yaml) `always_run`).

- [API Keys](references/api-keys.md)
- [Cloud Credentials](references/cloud-credentials.md)
- [Database Credentials](references/database-credentials.md)
- [Tokens](references/tokens.md)
- [Private Keys](references/private-keys.md)

## Core Discipline

Never print a complete discovered secret — mask it (see `.claude/rules/security.md` "Secrets Handling", e.g. `AKIA****************`). A finding needs enough of the value shown to confirm the pattern, not the whole thing.

## False-Positive Conditions (General)

- **Placeholder/example values**: `example`, `changeme`, `xxxxxxxx`, `your-api-key-here`, or values in files clearly named `*.example`, `*.sample`, `*.template`.
- **Test-only fixtures**: values scoped to a test file, clearly fake (e.g. Stripe's published test-mode keys), or in `tests/fixtures/`.
- **Environment variable references**: `os.environ["API_KEY"]` is not a hardcoded secret — the secret isn't in the code.
- **Already-revoked credentials**: if determinable from context (e.g. a comment noting rotation), still worth flagging but at reduced severity/informational.

Each reference file below adds category-specific false-positive conditions on top of these.

## Output

A candidate finding conforming to [finding.schema.json](../../schemas/finding.schema.json), with the `evidence` snippet masked per above.
