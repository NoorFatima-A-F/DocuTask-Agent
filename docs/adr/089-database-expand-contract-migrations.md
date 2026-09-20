# 89. Zero-Downtime Database Expand-Contract Migration Architecture

Date: 2026-09-19

## Status
Accepted

## Context
Deploying application updates that require schema changes often risk downtime or broken backward compatibility with older application replicas still in service.

## Decision
We enforce the Expand-Contract pattern via `MigrationManager` and `ExpandContractValidator`.
- `EXPAND`: Add nullable columns or new tables without breaking existing queries. Destructive statements (`DROP COLUMN`, `DROP TABLE`) are blocked.
- `MIGRATE_DATA`: Asynchronously backfill data.
- `CONTRACT`: Safely clean up deprecated columns only after all older application versions are decommissioned.

## Consequences
- Zero-downtime rolling and canary updates operate safely alongside live database schemas.
- Dangerous DDL is intercepted prior to execution.
