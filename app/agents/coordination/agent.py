"""
Agent Domain Aggregate.
Encapsulates an agent instance, its current lifecycle state, active workloads, and operational history.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.coordination.agent_profile import AgentProfile
from app.agents.coordination.lifecycle import AgentLifecycleState


class Agent(BaseModel):
    """
    Agent Domain Entity / Aggregate.
    Represents an active, registered, or assigned agent in the multi-agent cluster.
    """
    profile: AgentProfile
    state: AgentLifecycleState = Field(default=AgentLifecycleState.CREATED)
    current_tasks: List[str] = Field(default_factory=list)
    active_leases: List[str] = Field(default_factory=list)
    completed_task_count: int = Field(default=0, ge=0)
    failed_task_count: int = Field(default=0, ge=0)
    reputation_score: float = Field(default=1.0, ge=0.0, le=1.0)
    last_heartbeat_timestamp: float = 0.0

    @property
    def agent_id(self) -> UUID:
        return self.profile.identity.agent_id

    @property
    def name(self) -> str:
        return self.profile.identity.name

    def transition_to(self, new_state: AgentLifecycleState) -> "Agent":
        """Deterministic state transition."""
        return self.model_copy(update={"state": new_state})

    def assign_task(self, task_id: str) -> "Agent":
        """Assigns a task and transitions to ASSIGNED or EXECUTING."""
        new_tasks = [*self.current_tasks, task_id]
        return self.model_copy(update={
            "current_tasks": new_tasks,
            "state": AgentLifecycleState.ASSIGNED
        })

    def complete_task(self, task_id: str, success: bool = True) -> "Agent":
        """Removes task and updates task counts and state."""
        new_tasks = [t for t in self.current_tasks if t != task_id]
        new_state = AgentLifecycleState.AVAILABLE if not new_tasks else AgentLifecycleState.EXECUTING
        new_comp = self.completed_task_count + (1 if success else 0)
        new_fail = self.failed_task_count + (0 if success else 1)
        total = new_comp + new_fail
        rep = (new_comp / total) if total > 0 else 1.0

        return self.model_copy(update={
            "current_tasks": new_tasks,
            "state": new_state,
            "completed_task_count": new_comp,
            "failed_task_count": new_fail,
            "reputation_score": rep
        })
