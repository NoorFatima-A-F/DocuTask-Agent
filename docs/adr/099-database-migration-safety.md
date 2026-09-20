# 99. Zero-Downtime Database Expand-Contract Migration Architecture

Date: 2026-09-20

## Status
Accepted

## Context
Deploying software releases that introduce database schema changes risks production downtime and query failures when older application replicas are still serving traffic.

## Decision
We enforce the three-phase Expand-Contract pattern via `MigrationCoordinator`:
1. `EXPAND`: Add backwards-compatible nullable columns/tables; dual-write in application layer. Destructive DDL (`DROP COLUMN`, `DROP TABLE`) is blocked by `MigrationSafetyValidator`.
2. `MIGRATE_DATA`: Asynchronously backfill historical rows.
3. `CONTRACT`: Safely drop deprecated columns only after all older application versions have been decommissioned.

## Consequences
- Guarantees zero-downtime rolling and canary deployments across mixed-version cluster environments.
- Protects database data integrity against accidental destructive schema alterations.
