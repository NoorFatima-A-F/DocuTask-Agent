"""
Agent Task Dispatcher.
Dispatches scheduled task assignments to target agents, managing handshakes and acknowledgments.
"""

from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.scheduler import ScheduledTaskItem


class AgentTaskDispatcher:
    """Dispatches scheduled tasks to destination agents."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def dispatch_task(self, task: ScheduledTaskItem) -> bool:
        """Dispatches a single scheduled task to its assigned agent."""
        if not task.assigned_agent_id:
            return False

        agent = await self.registry.get_by_id(task.assigned_agent_id)
        if not agent or not agent.state.is_operational():
            return False

        updated = agent.assign_task(task.task_id)
        await self.registry.update_agent(updated)
        return True
