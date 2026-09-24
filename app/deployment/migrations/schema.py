"""Schema Migration Models and Expand-Contract Phases."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class MigrationPhase(str, Enum):
    """Zero-downtime expand/contract schema evolution phases."""
    EXPAND = "EXPAND"               # Add new nullable columns / new tables / dual-write targets
    MIGRATE_DATA = "MIGRATE_DATA"   # Backfill historical data in background
    CONTRACT = "CONTRACT"           # Drop old deprecated columns / drop legacy constraints


@dataclass
class SchemaMigration:
    """Represents a database schema migration step."""
    version: str
    name: str
    phase: MigrationPhase
    up_sql: str
    down_sql: Optional[str] = None
    migration_id: Optional[str] = None
    is_reversible: bool = True
    description: str = ""
    applied_at: Optional[datetime] = None
    execution_time_ms: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.migration_id:
            self.migration_id = f"mig-{self.version}-{self.name.lower().replace(' ', '_')}"
        if self.down_sql is None:
            self.is_reversible = False
