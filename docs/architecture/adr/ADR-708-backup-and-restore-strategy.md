# ADR-708: Backup and Restore Strategy

## Status
Accepted

## Context
Enterprise customers require disaster recovery capabilities, point-in-time state capture, and the ability to restore accidentally deleted workspaces or configurations.

## Decision
1. Implement `TenantBackupRestoreEngine` generating encrypted, canonical JSON snapshot archives (`BackupSnapshot`).
2. Include SHA-256 integrity checksums and record counts on every snapshot.
3. Support granular restore scopes: `FULL_ORGANIZATION`, `WORKSPACE`, and `PROJECT`.
4. Validate checksums before applying any restore operation.

## Consequences
- **Positive**: Cryptographically verified restore workflows; portable tenant backups suitable for offline archiving.
- **Trade-off**: Large knowledge vector store backups require streaming serialization for high-volume tenants.
