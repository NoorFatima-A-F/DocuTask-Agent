"""
Heartbeat Aggregator & Lag Tracker.

Monitors periodic heartbeats from nodes, clusters, and distributed services,
tracking telemetry drift, lease validity, and identifying expired/unresponsive entities.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.health.heartbeat")


class HeartbeatSignal(BaseModel):
    """Heartbeat signal sent by a distributed entity."""
    entity_id: str
    entity_type: str = Field(default="service", description="node, cluster, worker, service, etc.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: float = Field(default=30.0, ge=0.01)
    cpu_usage_percent: Optional[float] = None
    memory_usage_percent: Optional[float] = None
    active_connections: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HeartbeatStatus(BaseModel):
    """Evaluation of an entity's heartbeat state."""
    entity_id: str
    entity_type: str
    last_seen: datetime
    age_seconds: float
    is_alive: bool
    is_stale: bool
    lag_seconds: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class HeartbeatAggregator:
    """
    Centralized collector and evaluator for heartbeats across all platform subsystems.
    """

    def __init__(self, default_stale_threshold_seconds: float = 15.0) -> None:
        self.default_stale_threshold_seconds = default_stale_threshold_seconds
        self._signals: Dict[str, HeartbeatSignal] = {}
        self._received_at: Dict[str, float] = {}

    def record_heartbeat(self, signal: HeartbeatSignal) -> HeartbeatStatus:
        """Process incoming heartbeat signal."""
        now = time.time()
        self._signals[signal.entity_id] = signal
        self._received_at[signal.entity_id] = now

        return self.get_status(signal.entity_id)

    def get_status(self, entity_id: str) -> Optional[HeartbeatStatus]:
        """Evaluate heartbeat status for a specific entity."""
        signal = self._signals.get(entity_id)
        if not signal:
            return None

        received_at = self._received_at.get(entity_id, 0.0)
        age = max(0.0, time.time() - received_at)
        is_alive = age <= signal.ttl_seconds
        is_stale = age > self.default_stale_threshold_seconds

        # Lag between signal origin timestamp and local reception
        signal_epoch = signal.timestamp.timestamp()
        lag = max(0.0, received_at - signal_epoch)

        return HeartbeatStatus(
            entity_id=signal.entity_id,
            entity_type=signal.entity_type,
            last_seen=datetime.fromtimestamp(received_at, tz=timezone.utc),
            age_seconds=age,
            is_alive=is_alive,
            is_stale=is_stale,
            lag_seconds=lag,
            metadata=signal.metadata,
        )

    def get_all_statuses(self) -> List[HeartbeatStatus]:
        statuses = []
        for entity_id in list(self._signals.keys()):
            st = self.get_status(entity_id)
            if st:
                statuses.append(st)
        return statuses

    def get_dead_entities(self) -> List[HeartbeatStatus]:
        """Find entities whose TTL has expired."""
        return [st for st in self.get_all_statuses() if not st.is_alive]

    def remove_entity(self, entity_id: str) -> bool:
        if entity_id in self._signals:
            del self._signals[entity_id]
            self._received_at.pop(entity_id, None)
            return True
        return False
