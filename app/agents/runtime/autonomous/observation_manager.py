"""
Observation Manager for Autonomous Runtime Brain.
Synthesizes environmental states, task graph outputs, error signals, and system telemetry into structured observations.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.workflow.task_graph.dynamic_task_graph import NodeState

logger = logging.getLogger(__name__)


@dataclass
class Observation:
    """A synthesized snapshot of execution environment and progress."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    execution_id: str = ""
    completed_task_count: int = 0
    pending_task_count: int = 0
    failed_task_count: int = 0
    current_wave_tasks: List[str] = field(default_factory=list)
    available_outputs: Dict[str, Any] = field(default_factory=dict)
    active_errors: List[str] = field(default_factory=list)
    has_blocking_errors: bool = False
    is_work_complete: bool = False


class ObservationManager:
    """Collects, aggregates, and filters observations across the agent environment."""

    def observe(self, context: RuntimeContext) -> Observation:
        """Constructs an Observation from the current runtime context and task graph."""
        graph = context.task_graph

        if not graph:
            return Observation(
                execution_id=context.execution_id,
                active_errors=list(context.errors_encountered),
                has_blocking_errors=len(context.errors_encountered) > 0,
                is_work_complete=False,
            )

        completed = sum(1 for s in graph._states.values() if s == NodeState.COMPLETED)
        failed = sum(1 for s in graph._states.values() if s == NodeState.FAILED)
        pending = sum(1 for s in graph._states.values() if s in (NodeState.PENDING, NodeState.READY, NodeState.RUNNING))

        ready_tasks = graph.get_ready_tasks()
        ready_ids = [t.task_id for t in ready_tasks]

        is_complete = graph.is_completed()
        has_blocking = failed > 0 and len(ready_ids) == 0 and not is_complete

        obs = Observation(
            execution_id=context.execution_id,
            completed_task_count=completed,
            pending_task_count=pending,
            failed_task_count=failed,
            current_wave_tasks=ready_ids,
            available_outputs=dict(graph._outputs),
            active_errors=list(context.errors_encountered),
            has_blocking_errors=has_blocking,
            is_work_complete=is_complete,
        )

        logger.debug(
            "Observed context %s: completed=%d, ready=%d, failed=%d, complete=%s",
            context.execution_id,
            completed,
            len(ready_ids),
            failed,
            is_complete,
        )
        return obs
