"""
DAG Projection Read Model for Phase 13.2.
Maintains the live projected DAG state constructed from incoming Domain Events.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.runtime.planner_visualization.ui_models.models import (
    PlannerDAGSnapshot,
    PlannerDAGNode,
    PlannerDAGEdge,
    TaskExecutionState,
    PlannerStateEnum,
)
from app.runtime.events.bus.subscriber import EventSubscriber
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import EventSubsystem, DomainEventType


class DAGProjection(EventSubscriber):
    """
    Event-driven read projection that reconstructs the live DAG state in memory.
    """

    def __init__(self, mission_id: str = "mission-001"):
        super().__init__(
            subscriber_id=f"DAGProjection-{mission_id}",
            handler=self.on_event,
            subsystems={EventSubsystem.PLANNER, EventSubsystem.WORKER_POOL},
        )
        self.mission_id = mission_id
        self.version = 1
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.state = PlannerStateEnum.READY.value
        self.events_processed = 0

    async def on_event(self, event: DomainEvent) -> None:
        self.events_processed += 1
        payload = event.payload

        if event.event_type == DomainEventType.PLANNER_STARTED:
            self.state = PlannerStateEnum.EXECUTING.value
        elif event.event_type == DomainEventType.TASK_ASSIGNED:
            task_id = payload.get("task_id")
            if task_id and task_id in self.nodes:
                self.nodes[task_id]["state"] = TaskExecutionState.RUNNING.value
                self.nodes[task_id]["assigned_worker"] = payload.get("worker_id")
        elif event.event_type == DomainEventType.TASK_COMPLETED:
            task_id = payload.get("task_id")
            if task_id and task_id in self.nodes:
                self.nodes[task_id]["state"] = TaskExecutionState.COMPLETED.value
        elif event.event_type == DomainEventType.PLANNER_REPLANNED:
            self.version = payload.get("new_plan_version", self.version + 1)

    def get_projection(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "version": self.version,
            "state": self.state,
            "events_processed": self.events_processed,
            "nodes_count": len(self.nodes),
            "edges_count": len(self.edges),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
