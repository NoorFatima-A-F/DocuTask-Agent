"""Enterprise Database Migration Manager."""
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from ..core.exceptions import MigrationException
from .schema import MigrationPhase, SchemaMigration
from .validation import ExpandContractValidator


class MigrationManager:
    """Manages versioned, zero-downtime database migrations across clusters and tenants."""

    def __init__(
        self,
        validator: Optional[ExpandContractValidator] = None,
        sql_executor: Optional[Callable[[str], bool]] = None,
    ):
        self.validator = validator or ExpandContractValidator()
        self.sql_executor = sql_executor or (lambda sql: True)
        self._migrations: Dict[str, SchemaMigration] = {}
        self._applied: Dict[str, List[str]] = {}  # target (env or tenant) -> list of applied migration_ids

    def register_migration(self, migration: SchemaMigration) -> SchemaMigration:
        """Registers and validates a migration definition."""
        self.validator.validate_migration(migration)
        self._migrations[migration.migration_id] = migration
        return migration

    def get_migration(self, migration_id: str) -> Optional[SchemaMigration]:
        """Fetches migration by ID."""
        return self._migrations.get(migration_id)

    def list_migrations(self, phase: Optional[MigrationPhase] = None) -> List[SchemaMigration]:
        """Lists registered migrations, optionally filtered by phase."""
        migs = list(self._migrations.values())
        if phase:
            migs = [m for m in migs if m.phase == phase]
        return sorted(migs, key=lambda m: m.version)

    def get_applied_migrations(self, target: str) -> List[SchemaMigration]:
        """Returns list of applied migrations for a target."""
        applied_ids = self._applied.get(target, [])
        return [self._migrations[mid] for mid in applied_ids if mid in self._migrations]

    def get_pending_migrations(self, target: str) -> List[SchemaMigration]:
        """Returns list of unapplied registered migrations for a target."""
        applied_ids = set(self._applied.get(target, []))
        all_sorted = self.list_migrations()
        return [m for m in all_sorted if m.migration_id not in applied_ids]

    def apply_migration(self, target: str, migration_id: str) -> SchemaMigration:
        """Executes up_sql and marks migration as applied."""
        mig = self.get_migration(migration_id)
        if not mig:
            raise MigrationException(f"Migration '{migration_id}' not found")

        applied_list = self._applied.setdefault(target, [])
        if migration_id in applied_list:
            raise MigrationException(f"Migration '{migration_id}' has already been applied to target '{target}'")

        start = datetime.now(timezone.utc)
        try:
            self.sql_executor(mig.up_sql)
            duration_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000.0
            mig.applied_at = datetime.now(timezone.utc)
            mig.execution_time_ms = round(duration_ms, 2)
            applied_list.append(migration_id)
            return mig
        except Exception as e:
            raise MigrationException(f"Failed executing up_sql for migration '{migration_id}': {e}") from e

    def rollback_migration(self, target: str, migration_id: str) -> SchemaMigration:
        """Executes down_sql and removes migration from applied list."""
        mig = self.get_migration(migration_id)
        if not mig:
            raise MigrationException(f"Migration '{migration_id}' not found")
        if not mig.is_reversible or not mig.down_sql:
            raise MigrationException(f"Migration '{migration_id}' is not reversible")

        applied_list = self._applied.get(target, [])
        if migration_id not in applied_list:
            raise MigrationException(f"Migration '{migration_id}' is not currently applied to target '{target}'")

        try:
            self.sql_executor(mig.down_sql)
            applied_list.remove(migration_id)
            return mig
        except Exception as e:
            raise MigrationException(f"Failed executing down_sql for migration '{migration_id}': {e}") from e
