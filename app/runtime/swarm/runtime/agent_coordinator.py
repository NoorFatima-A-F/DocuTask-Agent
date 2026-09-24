"""
AMCN-SIP Phase 13.8 - Agent Coordinator
Coordinates multi-agent task routing, dependency synchronization, distributed scheduling, and workload balancing.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid
from app.runtime.swarm.runtime.agent_registry import AgentRegistry
from app.runtime.swarm.runtime.agent_directory import AgentDirectory
from app.runtime.swarm.events.swarm_events import AgentLifecycleState


@dataclass
class SwarmCoordinatedTask:
    task_id: str
    mission_id: str
    description: str
    assigned_agent_id: str
    required_capability: str
    status: str  # ASSIGNED, EXECUTING, COMPLETED, FAILED
    priority: int = 1
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentCoordinator:
    """
    Coordinates execution graph across distributed autonomous agents.
    """

    def __init__(self, registry: AgentRegistry, directory: AgentDirectory):
        self.registry = registry
        self.directory = directory
        self._tasks: Dict[str, SwarmCoordinatedTask] = {}

    def route_and_assign_task(
        self,
        mission_id: str,
        description: str,
        required_capability: str,
        priority: int = 1,
        dependencies: Optional[List[str]] = None,
    ) -> SwarmCoordinatedTask:
        agent = self.directory.find_nearest_expert(required_capability)
        agent_id = agent.agent_id if agent else "agt-fallback-default"

        task_id = f"swm-tsk-{uuid.uuid4().hex[:8]}"
        task = SwarmCoordinatedTask(
            task_id=task_id,
            mission_id=mission_id,
            description=description,
            assigned_agent_id=agent_id,
            required_capability=required_capability,
            status="ASSIGNED",
            priority=priority,
            dependencies=dependencies or [],
        )

        self._tasks[task_id] = task

        if agent:
            self.registry.update_agent_state(agent.agent_id, AgentLifecycleState.ASSIGNED)
            agent.assigned_tasks_count += 1

        return task

    def mark_task_completed(self, task_id: str, success: bool = True):
        task = self._tasks.get(task_id)
        if task:
            task.status = "COMPLETED" if success else "FAILED"
            agent = self.registry.get_agent(task.assigned_agent_id)
            if agent:
                self.registry.update_agent_state(agent.agent_id, AgentLifecycleState.AVAILABLE)
                agent.completed_tasks_count += 1
                delta = 0.01 if success else -0.05
                self.registry.update_reputation(agent.agent_id, delta)

    def get_all_tasks(self) -> List[SwarmCoordinatedTask]:
        return list(self._tasks.values())
