# ADR-099: Zero-Downtime Database Migrations with Online Expand-Contract

## Status
Accepted

## Context
Traditional monolithic schema migrations that execute destructive DDL (e.g. `DROP COLUMN`, `ALTER TABLE NOT NULL`) cause table locks and service outages during rolling deployments.

## Decision
1. Decouple database migrations into 5 online phases: `EXPAND` -> `DUAL_WRITE` -> `BACKFILL` -> `READ_NEW` -> `CONTRACT`.
2. `MigrationSafetyValidator` enforces that destructive DDL is strictly prohibited during `EXPAND` and `DUAL_WRITE` phases.
3. Code changes and database migrations are released in separate compatible steps.

## Consequences
- Enables true zero-downtime rolling and canary deployments with backward-compatible schemas.
