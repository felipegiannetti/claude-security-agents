# Docker

**CWE-16** (misconfiguration)

## What to Look For

- Container running as root (no `USER` directive, or explicitly `USER root`) — raises impact of any code-execution finding inside the container.
- Secrets baked into image layers (`ARG`/`ENV` with credentials, or a `COPY` of a secrets file) — persists in image history even if later "removed" in a subsequent layer.
- Base images pinned to `latest` or unpinned — unpredictable/unreviewed content on rebuild; also relevant to [dependency-cve-check](../../dependency-cve-check/SKILL.md) since the base image's own OS packages carry CVE exposure.
- Overly broad `COPY . .` pulling unintended files (`.git`, `.env`, credentials) into the image.
- Exposed unnecessary ports / debug interfaces left enabled in a production image.

## False-Positive Conditions

- Root user is confirmed necessary for a specific, justified reason and the container is otherwise sandboxed (rare — treat root-by-default as the finding unless clearly justified).
- The image is build-time only and never runs as a live container (e.g. a builder stage in a multi-stage build).

## Severity Notes

Secrets in image layers: `high` to `critical` (image may be pushed to a registry others can pull). Root user alone: `low`, escalating with additional risky capabilities (see `agents/architecture-advisor.md`'s smell about overly broad privileges).
