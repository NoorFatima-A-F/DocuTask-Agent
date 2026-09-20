"""
AOIS-HROP Phase 13.7 - Runtime Heartbeat
Enterprise heartbeat with periodic pulse emissions and sub-second timestamp tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class HeartbeatPulse:
    pulse_id: str
    sequence_number: int
    timestamp_utc: str
    liveness_status: str
    active_workers_count: int
    system_load_pct: float
    health_index: float
    node_id: str = "cluster-primary-master"


class RuntimeHeartbeat:
    """
    Maintains autonomous liveness pulses and detects missing heartbeats.
    """

    def __init__(self, node_id: str = "cluster-primary-master"):
        self.node_id = node_id
        self._sequence: int = 0
        self._pulses: List[HeartbeatPulse] = []
        self._last_pulse_time: Optional[datetime] = None

    def emit_pulse(
        self,
        workers: int = 8,
        load_pct: float = 28.5,
        health_index: float = 98.5,
    ) -> HeartbeatPulse:
        self._sequence += 1
        now = datetime.now(timezone.utc)
        self._last_pulse_time = now

        pulse = HeartbeatPulse(
            pulse_id=f"pulse-{uuid.uuid4().hex[:8]}",
            sequence_number=self._sequence,
            timestamp_utc=now.isoformat(),
            liveness_status="ALIVE_OPTIMAL",
            active_workers_count=workers,
            system_load_pct=load_pct,
            health_index=health_index,
            node_id=self.node_id,
        )

        self._pulses.append(pulse)
        if len(self._pulses) > 500:
            self._pulses.pop(0)

        return pulse

    def get_latest_pulse(self) -> HeartbeatPulse:
        if not self._pulses:
            return self.emit_pulse()
        return self._pulses[-1]

    def is_heartbeat_fresh(self, max_interval_seconds: float = 10.0) -> bool:
        if not self._last_pulse_time:
            return False
        delta = (datetime.now(timezone.utc) - self._last_pulse_time).total_seconds()
        return delta <= max_interval_seconds

    def get_recent_pulses(self, limit: int = 20) -> List[HeartbeatPulse]:
        return self._pulses[-limit:]
