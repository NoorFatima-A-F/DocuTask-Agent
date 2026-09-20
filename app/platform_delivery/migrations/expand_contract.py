"""Zero-Downtime Expand-Contract Database Migration Framework (Req 46, 47)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import re


class ExpandContractPhase(str, Enum):
    """Phases for non-breaking schema evolution (Req 46)."""
    EXPAND = "EXPAND"               # Add columns/tables, ensure backwards-compatible writes
    MIGRATE_DATA = "MIGRATE_DATA"   # Backfill historical rows asynchronously
    CONTRACT = "CONTRACT"           # Drop legacy columns/constraints after old app replicas decommissioned


@dataclass
class MigrationStep:
    version: str
    name: str
    phase: ExpandContractPhase
    up_sql: str
    down_sql: Optional[str] = None
    applied_at: Optional[datetime] = None


class MigrationSafetyValidator:
    """Blocks destructive DDL in active deployment windows (Req 47)."""

    DESTRUCTIVE_PATTERNS = [
        re.compile(r"DROP\s+COLUMN", re.IGNORECASE),
        re.compile(r"DROP\s+TABLE", re.IGNORECASE),
        re.compile(r"RENAME\s+COLUMN", re.IGNORECASE),
        re.compile(r"ALTER\s+COLUMN.*SET\s+NOT\s+NULL", re.IGNORECASE),
    ]

    @classmethod
    def validate_step(cls, step: MigrationStep) -> bool:
        if step.phase == ExpandContractPhase.EXPAND:
            for pat in cls.DESTRUCTIVE_PATTERNS:
                if pat.search(step.up_sql):
                    raise ValueError(
                        f"Migration Safety Violation: Destructive operation '{pat.pattern}' forbidden in EXPAND phase."
                    )
        return True
