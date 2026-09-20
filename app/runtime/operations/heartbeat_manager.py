"""
AMAEOP Pillar 4 - Heartbeat & Liveness Monitor
Tracks periodic heartbeats from worker departments, detects stalled operations, and triggers failover.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class DepartmentHeartbeat:
    department_id: str
    last_heartbeat_timestamp: float
    active_operations_count: int
    is_responsive: bool
    missed_heartbeats_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HeartbeatManager:
    """Monitors heartbeat liveliness across all departments with dead-man timers."""

    def __init__(self, timeout_seconds: float = 30.0):
        self.timeout_seconds = timeout_seconds
        self.heartbeats: Dict[str, DepartmentHeartbeat] = {}
        self._seed_heartbeats()

    def _seed_heartbeats(self):
        depts = ["dept_executive", "dept_ocr", "dept_extraction", "dept_validation", "dept_memory", "dept_research", "dept_governance", "dept_qa"]
        for d in depts:
            self.heartbeats[d] = DepartmentHeartbeat(
                department_id=d,
                last_heartbeat_timestamp=time.time(),
                active_operations_count=2,
                is_responsive=True,
                missed_heartbeats_count=0,
            )

    def record_heartbeat(self, department_id: str, active_ops: int = 1) -> DepartmentHeartbeat:
        hb = DepartmentHeartbeat(
            department_id=department_id,
            last_heartbeat_timestamp=time.time(),
            active_operations_count=active_ops,
            is_responsive=True,
            missed_heartbeats_count=0,
        )
        self.heartbeats[department_id] = hb
        return hb

    def check_liveness(self) -> Dict[str, Any]:
        now = time.time()
        stalled = []
        healthy = []

        for d_id, hb in self.heartbeats.items():
            if now - hb.last_heartbeat_timestamp > self.timeout_seconds:
                hb.is_responsive = False
                hb.missed_heartbeats_count += 1
                stalled.append(d_id)
            else:
                hb.is_responsive = True
                healthy.append(d_id)

        return {
            "all_departments_healthy": len(stalled) == 0,
            "healthy_count": len(healthy),
            "stalled_departments": stalled,
            "heartbeats": [hb.to_dict() for hb in self.heartbeats.values()],
        }


heartbeat_manager = HeartbeatManager()
