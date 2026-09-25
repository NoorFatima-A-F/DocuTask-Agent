"""Expand-Contract Schema Migration Safety Validator."""
import re
from ..core.exceptions import MigrationException
from .schema import MigrationPhase, SchemaMigration


class ExpandContractValidator:
    """Enforces zero-downtime database migration rules and backward compatibility."""

    DANGEROUS_EXPAND_PATTERNS = [
        re.compile(r"DROP\s+COLUMN", re.IGNORECASE),
        re.compile(r"DROP\s+TABLE", re.IGNORECASE),
        re.compile(r"ALTER\s+COLUMN.*SET\s+NOT\s+NULL", re.IGNORECASE),
        re.compile(r"RENAME\s+COLUMN", re.IGNORECASE),
    ]

    def validate_migration(self, migration: SchemaMigration) -> bool:
        """Validates that a schema migration follows expand/contract safety rules."""
        if migration.phase == MigrationPhase.EXPAND:
            for pattern in self.DANGEROUS_EXPAND_PATTERNS:
                if pattern.search(migration.up_sql):
                    raise MigrationException(
                        f"Unsafe EXPAND phase migration '{migration.name}': contains destructive operation "
                        f"({pattern.pattern}). Destructive operations must only run in CONTRACT phase."
                    )
            
            # Check for adding NOT NULL column without DEFAULT
            if re.search(r"ADD\s+COLUMN.*NOT\s+NULL", migration.up_sql, re.IGNORECASE):
                if not re.search(r"DEFAULT", migration.up_sql, re.IGNORECASE):
                    raise MigrationException(
                        f"Unsafe EXPAND phase migration '{migration.name}': Adding NOT NULL column requires a DEFAULT value."
                    )

        elif migration.phase == MigrationPhase.CONTRACT:
            if not migration.up_sql.strip():
                raise MigrationException(f"CONTRACT migration '{migration.name}' cannot have empty up_sql")

        if migration.is_reversible and not migration.down_sql:
            raise MigrationException(
                f"Migration '{migration.name}' marked as reversible but down_sql is missing"
            )

        return True
