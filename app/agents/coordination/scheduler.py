"""
Distributed Agent Scheduler.
Determines task allocation order, priority matching, and execution windows across distributed agents.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_selector import AgentSelector
from app.agents.coordination.capability_matcher import CapabilityRequirement


class ScheduledTaskItem(BaseModel):
    """Task scheduled for allocation to an agent."""
    task_id: str
    task_name: str
    priority: int = Field(default=1, ge=1, le=10)
    required_skills: List[str] = Field(default_factory=list)
    assigned_agent_id: Optional[UUID] = None

    model_config = {"frozen": True}


class DistributedAgentScheduler:
    """Schedules tasks across candidate agents considering priority and capability constraints."""

    def __init__(self, selector: Optional[AgentSelector] = None):
        self.selector = selector or AgentSelector()

    def schedule_tasks(
        self,
        tasks: List[ScheduledTaskItem],
        available_agents: List[Agent]
    ) -> List[ScheduledTaskItem]:
        """Schedules tasks ordered by priority (highest first) and binds to optimal agents."""
        # Sort tasks by descending priority
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        scheduled: List[ScheduledTaskItem] = []

        for t in sorted_tasks:
            req = CapabilityRequirement(required_skills=t.required_skills)
            agent = self.selector.select_agent(req, available_agents)
            scheduled.append(t.model_copy(update={"assigned_agent_id": agent.agent_id}))

        return scheduled
