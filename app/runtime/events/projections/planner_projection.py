"""
DocuTask Agent - Planner Read Projection Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any, Optional
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType


class PlannerProjection:
    """
    Read Model Projection for Planner Activities.
    Derived purely from immutable DomainEvents; never modifies runtime.
    """

    def __init__(self):
        self.state: str = "IDLE"
        self.active_mission_id: Optional[str] = None
        self.total_plans_generated: int = 0
        self.total_replans_executed: int = 0
        self.current_goal: Optional[str] = None
        self.generated_tasks_count: int = 0
        self.estimated_cost_usd: float = 0.0
        self.critical_path_ms: float = 0.0
        self.recent_planner_events: List[Dict[str, Any]] = []
        self.replan_history: List[Dict[str, Any]] = []
        self.last_updated_utc: float = time.time()

    def apply_event(self, event: DomainEvent) -> None:
        """Applies a single domain event to update the read projection."""
        event_dict = event.to_dict()
        self.recent_planner_events.append(event_dict)
        if len(self.recent_planner_events) > 50:
            self.recent_planner_events.pop(0)

        self.last_updated_utc = event.timestamp_utc

        if event.event_type == DomainEventType.PLANNER_STARTED:
            self.state = "PLANNING"
            self.active_mission_id = event.mission_id
            self.current_goal = event.payload.get("goal")

        elif event.event_type == DomainEventType.PLANNER_FINISHED:
            self.state = "EXECUTION_READY"
            self.total_plans_generated += 1
            self.generated_tasks_count = event.payload.get("generated_task_count", 0)
            self.estimated_cost_usd = event.payload.get("estimated_cost_usd", 0.0)
            self.critical_path_ms = event.payload.get("critical_path_latency_ms", 0.0)

        elif event.event_type == DomainEventType.PLANNER_REPLANNED:
            self.total_replans_executed += 1
            self.replan_history.append({
                "timestamp_utc": event.timestamp_utc,
                "reason": event.payload.get("replan_reason"),
                "mutated_nodes": event.payload.get("mutated_node_ids", []),
            })

        elif event.event_type == DomainEventType.PLANNER_FAILED:
            self.state = "FAILED"

    def get_projection_state(self) -> Dict[str, Any]:
        """Returns the serializable read model."""
        return {
            "state": self.state,
            "active_mission_id": self.active_mission_id,
            "total_plans_generated": self.total_plans_generated,
            "total_replans_executed": self.total_replans_executed,
            "current_goal": self.current_goal,
            "generated_tasks_count": self.generated_tasks_count,
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
            "critical_path_ms": round(self.critical_path_ms, 2),
            "replan_history": self.replan_history[-10:],
            "recent_events_count": len(self.recent_planner_events),
            "last_updated_utc": self.last_updated_utc,
        }


# Global singleton planner projection
planner_projection = PlannerProjection()
