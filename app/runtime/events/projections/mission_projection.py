"""
DocuTask Agent - Mission Read Projection Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any, Optional
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType


class MissionProjection:
    """
    Read Model Projection for Mission Lifecycles.
    Tracks active missions, task completion counters, and overall SLA metrics.
    """

    def __init__(self):
        self.missions: Dict[str, Dict[str, Any]] = {}
        self.total_missions_created: int = 0
        self.total_missions_completed: int = 0
        self.total_missions_failed: int = 0

    def apply_event(self, event: DomainEvent) -> None:
        """Applies a domain event to update the mission projection."""
        m_id = event.mission_id
        if m_id not in self.missions:
            self.missions[m_id] = {
                "mission_id": m_id,
                "status": "INITIALIZED",
                "goal": "",
                "created_at_utc": event.timestamp_utc,
                "completed_at_utc": None,
                "tasks_total": 0,
                "tasks_completed": 0,
                "tasks_failed": 0,
                "total_cost_usd": 0.0,
                "duration_seconds": 0.0,
                "correlation_id": event.correlation_id,
            }

        m_data = self.missions[m_id]

        if event.event_type == DomainEventType.MISSION_CREATED:
            m_data["status"] = "ACTIVE"
            m_data["goal"] = event.payload.get("goal", "")
            self.total_missions_created += 1

        elif event.event_type == DomainEventType.TASK_ASSIGNED:
            m_data["tasks_total"] += 1

        elif event.event_type == DomainEventType.TASK_COMPLETED:
            m_data["tasks_completed"] += 1

        elif event.event_type == DomainEventType.TASK_FAILED:
            m_data["tasks_failed"] += 1

        elif event.event_type == DomainEventType.MISSION_COMPLETED:
            m_data["status"] = "COMPLETED"
            m_data["completed_at_utc"] = event.timestamp_utc
            m_data["duration_seconds"] = event.payload.get("duration_seconds", round(event.timestamp_utc - m_data["created_at_utc"], 2))
            m_data["total_cost_usd"] = event.payload.get("total_cost_usd", 0.0)
            self.total_missions_completed += 1

        elif event.event_type == DomainEventType.MISSION_FAILED:
            m_data["status"] = "FAILED"
            m_data["completed_at_utc"] = event.timestamp_utc
            self.total_missions_failed += 1

    def get_mission_state(self, mission_id: str) -> Optional[Dict[str, Any]]:
        """Returns the read model for a single mission."""
        return self.missions.get(mission_id)

    def get_all_missions(self) -> List[Dict[str, Any]]:
        """Returns all mission read models."""
        return list(self.missions.values())

    def get_summary(self) -> Dict[str, Any]:
        """Returns aggregated mission lifecycle statistics."""
        return {
            "total_missions_created": self.total_missions_created,
            "total_missions_completed": self.total_missions_completed,
            "total_missions_failed": self.total_missions_failed,
            "active_missions_count": sum(1 for m in self.missions.values() if m["status"] == "ACTIVE"),
            "missions": list(self.missions.values())[-20:],
            "timestamp_utc": time.time(),
        }


# Global singleton mission projection
mission_projection = MissionProjection()
