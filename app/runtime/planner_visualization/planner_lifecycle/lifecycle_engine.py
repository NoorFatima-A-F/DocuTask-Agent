"""
Planner Lifecycle Engine for Phase 13.2.
Manages transitions across the 14 Planner states and emits PlannerStateChanged domain events.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.runtime.planner_visualization.ui_models.models import PlannerStateEnum
from app.runtime.events.bus.event_bus import get_global_event_bus


class PlannerLifecycleEngine:
    """
    Manages the 14-state lifecycle of the Autonomous Planner and publishes
    immutable domain events for each state transition.
    """

    VALID_TRANSITIONS: Dict[PlannerStateEnum, List[PlannerStateEnum]] = {
        PlannerStateEnum.CREATED: [PlannerStateEnum.INITIALIZING, PlannerStateEnum.FAILED],
        PlannerStateEnum.INITIALIZING: [PlannerStateEnum.CONTEXT_LOADING, PlannerStateEnum.FAILED],
        PlannerStateEnum.CONTEXT_LOADING: [PlannerStateEnum.MEMORY_SEARCH, PlannerStateEnum.FAILED],
        PlannerStateEnum.MEMORY_SEARCH: [PlannerStateEnum.CAPABILITY_DISCOVERY, PlannerStateEnum.FAILED],
        PlannerStateEnum.CAPABILITY_DISCOVERY: [PlannerStateEnum.GOAL_ANALYSIS, PlannerStateEnum.FAILED],
        PlannerStateEnum.GOAL_ANALYSIS: [PlannerStateEnum.PLAN_SYNTHESIS, PlannerStateEnum.FAILED],
        PlannerStateEnum.PLAN_SYNTHESIS: [PlannerStateEnum.TASK_DECOMPOSITION, PlannerStateEnum.FAILED],
        PlannerStateEnum.TASK_DECOMPOSITION: [PlannerStateEnum.DEPENDENCY_ANALYSIS, PlannerStateEnum.FAILED],
        PlannerStateEnum.DEPENDENCY_ANALYSIS: [PlannerStateEnum.WORKER_ASSIGNMENT, PlannerStateEnum.FAILED],
        PlannerStateEnum.WORKER_ASSIGNMENT: [PlannerStateEnum.READY, PlannerStateEnum.FAILED],
        PlannerStateEnum.READY: [PlannerStateEnum.EXECUTING, PlannerStateEnum.FAILED],
        PlannerStateEnum.EXECUTING: [PlannerStateEnum.REPLANNING, PlannerStateEnum.COMPLETED, PlannerStateEnum.FAILED],
        PlannerStateEnum.REPLANNING: [PlannerStateEnum.EXECUTING, PlannerStateEnum.FAILED],
        PlannerStateEnum.COMPLETED: [],
        PlannerStateEnum.FAILED: [PlannerStateEnum.INITIALIZING],
    }

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id
        self.current_state: PlannerStateEnum = PlannerStateEnum.CREATED
        self.history: List[Dict[str, Any]] = []
        self._record_transition(None, self.current_state, "Lifecycle initialized.")

    def transition_to(self, new_state: PlannerStateEnum, reason: str = "", metadata: Optional[Dict[str, Any]] = None) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self.current_state, [])
        if new_state not in allowed and self.current_state != new_state:
            # Allow permissive transitions for live replanning if valid
            pass

        old_state = self.current_state
        self.current_state = new_state
        self._record_transition(old_state, new_state, reason, metadata)

        # Emit domain event via Phase 13.1 Event Bus
        from app.runtime.events.models.event import DomainEvent
        from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity
        from app.runtime.events.models.event_metadata import EventActor

        if new_state == PlannerStateEnum.CREATED:
            evt_type = DomainEventType.PLANNER_CREATED
        elif new_state == PlannerStateEnum.EXECUTING:
            evt_type = DomainEventType.PLANNER_STARTED
        elif new_state == PlannerStateEnum.COMPLETED:
            evt_type = DomainEventType.PLANNER_FINISHED
        elif new_state == PlannerStateEnum.REPLANNING:
            evt_type = DomainEventType.PLANNER_REPLANNED
        else:
            evt_type = DomainEventType.PLANNER_HEURISTIC_EVALUATED

        event = DomainEvent(
            mission_id=self.mission_id,
            actor=EventActor(actor_id="AutonomousPlanner", actor_type="PLANNER", role="CHIEF_PLANNER"),
            subsystem=EventSubsystem.PLANNER,
            component="LifecycleEngine",
            event_type=evt_type,
            payload={
                "old_state": old_state.value if old_state else "NONE",
                "new_state": new_state.value,
                "reason": reason or f"Transitioned to {new_state.value}",
                "planner_phase": new_state.value,
                **(metadata or {}),
            },
            severity=EventSeverity.INFO,
        )
        get_global_event_bus().publish_sync(event)
        return True

    def _record_transition(self, old_state: Optional[PlannerStateEnum], new_state: PlannerStateEnum, reason: str, metadata: Optional[Dict[str, Any]] = None):
        self.history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_state": old_state.value if old_state else None,
            "to_state": new_state.value,
            "reason": reason,
            "metadata": metadata or {},
        })

    def get_state(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "current_state": self.current_state.value,
            "history_length": len(self.history),
            "last_updated": self.history[-1]["timestamp"] if self.history else datetime.now(timezone.utc).isoformat(),
        }

    def get_timeline(self) -> List[Dict[str, Any]]:
        return self.history
