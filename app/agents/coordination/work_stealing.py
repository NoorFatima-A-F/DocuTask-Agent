"""
Work Stealing Pool.
Enables idle agents to steal queued, unstarted tasks from overloaded peer queues to maximize cluster utilization.
"""

from typing import Dict, List, Optional
from uuid import UUID


class WorkStealingPool:
    """Manages per-agent pending task queues and enables work-stealing."""

    def __init__(self):
        self._queues: Dict[UUID, List[str]] = {}

    def register_agent_queue(self, agent_id: UUID) -> None:
        """Initializes task queue for an agent."""
        if agent_id not in self._queues:
            self._queues[agent_id] = []

    def enqueue_task(self, agent_id: UUID, task_id: str) -> None:
        """Enqueues task onto a specific agent's queue."""
        if agent_id not in self._queues:
            self._queues[agent_id] = []
        self._queues[agent_id].append(task_id)

    def steal_task(self, thief_agent_id: UUID) -> Optional[str]:
        """Attempts to steal a pending task from the agent with the largest queue."""
        eligible_targets = [
            (aid, q) for aid, q in self._queues.items()
            if aid != thief_agent_id and len(q) > 1  # Leave at least 1 task for the owner
        ]

        if not eligible_targets:
            return None

        # Pick queue with the most pending tasks
        target_aid, target_q = max(eligible_targets, key=lambda pair: len(pair[1]))
        stolen_task = target_q.pop()  # Steal from tail (LIFO)
        return stolen_task

    def queue_depth(self, agent_id: UUID) -> int:
        """Returns number of pending tasks for agent."""
        return len(self._queues.get(agent_id, []))
