# Database Credentials

**CWE-798**

## What to Look For

Database connection strings/passwords hardcoded in source or config files, especially production connection strings committed alongside development ones. Check ORM configuration files, `.env` files committed by mistake, and Docker Compose files.

## Category-Specific Notes

- A `.env` file committed to version control (even if `.gitignore` supposedly excludes future ones) is a strong signal — check git history for it, not just the current tree.
- Distinguish a production connection string from a local development default (e.g. `localhost` with a well-known default password) — both are worth noting, but severity differs sharply.

## Severity Notes

`critical` for production database credentials; `low` to `informational` for a clearly local-only development default.
