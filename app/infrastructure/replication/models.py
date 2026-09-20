"""
Replication Domain Models & Enums.

Defines replication modes (SYNCHRONOUS, ASYNCHRONOUS, SEMI_SYNCHRONOUS),
lag metrics, stream states, and replication topology definitions.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ReplicationMode(str, enum.Enum):
    """Replication synchronization semantics."""
    SYNCHRONOUS = "SYNCHRONOUS"
    ASYNCHRONOUS = "ASYNCHRONOUS"
    SEMI_SYNCHRONOUS = "SEMI_SYNCHRONOUS"


class ReplicationLagMetric(BaseModel):
    """Telemetry tracking lag between primary and replica."""
    stream_id: str
    source_region: str
    target_region: str
    lag_seconds: float = Field(default=0.0, ge=0.0)
    byte_lag: int = Field(default=0, ge=0)
    unapplied_mutations: int = Field(default=0, ge=0)
    measured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReplicationStream(BaseModel):
    """Replication stream connecting data stores across regions."""
    stream_id: str
    source_region: str
    target_region: str
    dataset_name: str
    mode: ReplicationMode = ReplicationMode.ASYNCHRONOUS
    is_active: bool = True
    max_acceptable_lag_seconds: float = Field(default=60.0, ge=0.1)
    last_synced_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
