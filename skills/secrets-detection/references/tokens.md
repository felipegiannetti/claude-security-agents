# Tokens

**CWE-798**

## What to Look For

Hardcoded session tokens, personal access tokens (GitHub/GitLab-style), CI/CD pipeline tokens, or pre-generated JWTs committed to source, CI configuration, or scripts. Distinct from [jwt.md](../../auth-authz-review/references/jwt.md), which covers JWT *verification logic* rather than a specific leaked token value.

## Category-Specific Notes

- A CI/CD pipeline token (e.g. embedded in a workflow file instead of using the platform's secret store) is a common and high-impact case — it often grants write access to the repository or deployment pipeline itself.
- Check token expiration if determinable — a long-lived or non-expiring token found hardcoded is higher severity than a clearly short-lived one.

## Severity Notes

`critical` for a token granting write/deploy access; `high` for a token granting read access to sensitive systems.
