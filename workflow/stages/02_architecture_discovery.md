# Stage 02: Architecture Discovery

## Purpose

Build the architectural context that every later stage depends on. No vulnerability should be analyzed without understanding the system it lives in (see CLAUDE.md's Core Design Principle).

## Agent

[architecture-mapper](../../agents/architecture-mapper.md)

## Inputs

- The review scope from `01_intake`.
- For diff/PR scope: the full repository is still available for context, even though only changed files are the primary review target — architectural context should not be limited to just the diff.

## Process

See [architecture-mapper.md](../../agents/architecture-mapper.md) for the full discovery methodology (languages, frameworks, entry points, data stores, auth/authz mechanisms, integrations, infrastructure, dependencies, sensitive data, trust boundaries, existing security controls).

## Outputs

- An architecture model conforming to [architecture.schema.json](../../schemas/architecture.schema.json).
- A short prose summary of anything architecturally notable for the reviewer to pay attention to.

## Success Criteria

- Every entry point, data store, and trust boundary later referenced by a finding can be traced back to this model.
- Claims in the model are backed by cited files, not inference alone.
