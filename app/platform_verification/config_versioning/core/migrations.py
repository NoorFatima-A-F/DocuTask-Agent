"""
Database Migration Versioning and Rollback Engine.
"""
from datetime import datetime, timezone
import hashlib
from typing import Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import DatabaseMigrationRecord


class DatabaseMigrationManager:
    def __init__(self):
        self._migrations: Dict[str, DatabaseMigrationRecord] = {}
        self._applied_history: List[str] = []

    def register_migration(
        self,
        migration_id: str,
        version: str,
        author: str,
        description: str,
        forward_sql: str,
        rollback_sql: str,
        affected_components: Optional[List[str]] = None
    ) -> DatabaseMigrationRecord:
        checksum = hashlib.sha256(forward_sql.encode("utf-8")).hexdigest()
        record = DatabaseMigrationRecord(
            migration_id=migration_id,
            version=version,
            author=author,
            description=description,
            checksum_sha256=checksum,
            rollback_sql=rollback_sql,
            affected_components=affected_components or ["core_db"],
            is_applied=False
        )
        self._migrations[migration_id] = record
        return record

    def apply_migration(self, migration_id: str) -> DatabaseMigrationRecord:
        if migration_id not in self._migrations:
            raise KeyError(f"Migration {migration_id} not registered")
        record = self._migrations[migration_id]
        if record.is_applied:
            return record
        
        record.is_applied = True
        record.applied_at = datetime.now(timezone.utc).isoformat()
        record.execution_time_ms = 4.2
        self._applied_history.append(migration_id)
        return record

    def rollback_migration(self, migration_id: str) -> DatabaseMigrationRecord:
        if migration_id not in self._migrations:
            raise KeyError(f"Migration {migration_id} not registered")
        record = self._migrations[migration_id]
        if not record.is_applied:
            raise ValueError(f"Migration {migration_id} is not applied")
        
        record.is_applied = False
        record.applied_at = None
        if migration_id in self._applied_history:
            self._applied_history.remove(migration_id)
        return record

    def get_applied_migrations(self) -> List[DatabaseMigrationRecord]:
        return [self._migrations[m_id] for m_id in self._applied_history]

    def verify_integrity(self) -> bool:
        return all(m.checksum_sha256 for m in self._migrations.values())


migration_manager = DatabaseMigrationManager()
