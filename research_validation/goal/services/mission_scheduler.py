"""
Mission Scheduler Service
=========================
Manages mission queuing, priority ordering, concurrency throttling, and dependency gating.
"""

from typing import Dict, List, Optional
from research_validation.goal.models.mission import Mission
from research_validation.goal.models.mission_state import MissionState, StateTransitionRecord, MissionStateMachine
from research_validation.goal.models.goal import PriorityLevel
from research_validation.goal.interfaces.repository import IMissionRepository
from research_validation.goal.interfaces.event_bus import IEventBus
from research_validation.goal.interfaces.clock import IClock
from research_validation.goal.events.mission_events import MissionStateTransitionEvent


PRIORITY_WEIGHTS = {
    PriorityLevel.CRITICAL: 100,
    PriorityLevel.HIGH: 50,
    PriorityLevel.NORMAL: 20,
    PriorityLevel.LOW: 10,
    PriorityLevel.BACKGROUND: 1,
}


class MissionScheduler:
    """
    Schedules and throttles ready missions according to concurrency limits and priority queues.
    """

    def __init__(
        self,
        repository: IMissionRepository,
        event_bus: IEventBus,
        clock: IClock,
        max_concurrent_missions: int = 4,
    ):
        self.repo = repository
        self.event_bus = event_bus
        self.clock = clock
        self.max_concurrency = max_concurrent_missions

    def get_prioritized_queue(self) -> List[Mission]:
        """Returns pending READY_FOR_OBSERVATION missions ordered by priority weight."""
        ready = self.repo.list_missions(state=MissionState.READY_FOR_OBSERVATION.value)
        return sorted(ready, key=lambda m: PRIORITY_WEIGHTS.get(m.goal.priority, 0), reverse=True)

    def can_activate_mission(self) -> bool:
        """Verifies if system concurrency quota allows activating another mission."""
        active = self.repo.list_missions(state=MissionState.ACTIVE.value)
        return len(active) < self.max_concurrency

    def activate_next_mission(self) -> Optional[Mission]:
        """Activates the highest priority ready mission if concurrency permits."""
        if not self.can_activate_mission():
            return None

        queue = self.get_prioritized_queue()
        if not queue:
            return None

        mission = queue[0]
        now_str = self.clock.now_utc_iso()

        MissionStateMachine.assert_transition(mission.state, MissionState.ACTIVE)
        updated_transitions = list(mission.state_history) + [
            StateTransitionRecord(
                from_state=mission.state,
                to_state=MissionState.ACTIVE,
                timestamp_utc=now_str,
                actor="MISSION_SCHEDULER",
                rationale="Concurrency and priority criteria satisfied.",
            )
        ]

        activated = Mission(
            mission_id=mission.mission_id,
            goal_id=mission.goal_id,
            title=mission.title,
            description=mission.description,
            version=mission.version,
            state=MissionState.ACTIVE,
            goal=mission.goal,
            objectives=mission.objectives,
            execution_budget=mission.execution_budget,
            risk_profile=mission.risk_profile,
            metrics=mission.metrics,
            state_history=tuple(updated_transitions),
            created_at_utc=mission.created_at_utc,
            updated_at_utc=now_str,
            author=mission.author,
            previous_version_hash=mission.mission_digest_sha256,
            mission_digest_sha256="",
        )

        digest = activated.compute_digest()
        activated = Mission(
            mission_id=activated.mission_id,
            goal_id=activated.goal_id,
            title=activated.title,
            description=activated.description,
            version=activated.version,
            state=activated.state,
            goal=activated.goal,
            objectives=activated.objectives,
            execution_budget=activated.execution_budget,
            risk_profile=activated.risk_profile,
            metrics=activated.metrics,
            state_history=activated.state_history,
            created_at_utc=activated.created_at_utc,
            updated_at_utc=activated.updated_at_utc,
            author=activated.author,
            previous_version_hash=activated.previous_version_hash,
            mission_digest_sha256=digest,
        )

        self.repo.save_mission(activated)
        self.event_bus.publish(MissionStateTransitionEvent(
            event_id=f"evt_{activated.mission_id}_{len(updated_transitions)}",
            event_type="MissionStateTransition",
            aggregate_id=activated.mission_id,
            timestamp_utc=now_str,
            payload={"from_state": MissionState.READY_FOR_OBSERVATION.value, "to_state": MissionState.ACTIVE.value},
        ))

        return activated
