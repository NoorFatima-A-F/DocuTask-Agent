"""
Event Controller for Autonomous Runtime Brain.
Bridges runtime state machine events, task progress, and anomaly signals to the EnterpriseEventBus.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.agents.events.event_bus import EnterpriseEventBus
from app.agents.events.event_types import (
    AgentCompletedEvent,
    AgentFailedEvent,
    GoalReceivedEvent,
    PlanOptimizedEvent,
    PlanningStartedEvent,
    ReflectionCritiqueCompletedEvent,
    StateTransitionEvent,
)
from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.runtime.autonomous.state_machine import AutonomousState

logger = logging.getLogger(__name__)


class EventController:
    """Publishes runtime lifecycle events to the central asynchronous event bus."""

    def __init__(self, event_bus: Optional[EnterpriseEventBus] = None) -> None:
        self.event_bus = event_bus or EnterpriseEventBus()

    async def emit_state_transition(
        self,
        from_state: AutonomousState,
        to_state: AutonomousState,
        context: RuntimeContext,
    ) -> None:
        """Publishes a state transition event."""
        evt = StateTransitionEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            from_state=from_state.value,
            to_state=to_state.value,
            payload={"iteration": context.iteration_count},
        )
        await self.event_bus.publish(evt)

    async def emit_goal_received(self, goal_text: str, context: RuntimeContext) -> None:
        evt = GoalReceivedEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            payload={"goal_text": goal_text},
        )
        await self.event_bus.publish(evt)

    async def emit_plan_optimized(self, strategy: str, score: float, context: RuntimeContext) -> None:
        evt = PlanOptimizedEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            payload={"strategy": strategy, "score": score},
        )
        await self.event_bus.publish(evt)

    async def emit_reflection_completed(
        self,
        overall_score: float,
        passed: bool,
        context: RuntimeContext,
    ) -> None:
        evt = ReflectionCritiqueCompletedEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            overall_score=overall_score,
            passed=passed,
            payload={"errors": list(context.errors_encountered)},
        )
        await self.event_bus.publish(evt)

    async def emit_completion(self, context: RuntimeContext) -> None:
        evt = AgentCompletedEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            payload={"elapsed_seconds": context.elapsed_time_seconds()},
        )
        await self.event_bus.publish(evt)

    async def emit_failure(self, error: str, context: RuntimeContext) -> None:
        evt = AgentFailedEvent(
            execution_id=context.execution_id,
            document_id=context.document_id,
            payload={"error": error},
        )
        await self.event_bus.publish(evt)
