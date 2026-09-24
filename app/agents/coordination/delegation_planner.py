"""
Delegation Planner.
Plans task assignments across candidate agents according to delegation mode and capability matching.
"""

from typing import List, Optional
from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_selector import AgentSelector
from app.agents.coordination.capability_matcher import CapabilityRequirement
from app.agents.coordination.delegation import DelegationRequest, DelegationTask
from app.agents.coordination.delegation_policy import DelegationPolicy


class DelegationPlanner:
    """Calculates optimal agent assignments for requested delegation tasks."""

    def __init__(
        self,
        selector: Optional[AgentSelector] = None,
        policy: Optional[DelegationPolicy] = None
    ):
        self.selector = selector or AgentSelector()
        self.policy = policy or DelegationPolicy()

    def plan_delegation(
        self,
        request: DelegationRequest,
        available_agents: List[Agent]
    ) -> List[DelegationTask]:
        """Assigns primary and fallback agents to each task in the delegation request."""
        planned_tasks: List[DelegationTask] = []

        for task in request.tasks:
            req = CapabilityRequirement(required_skills=task.required_skills)
            best_agent = self.selector.select_agent(req, available_agents)

            # Find fallback agent if allowed
            fallback_agent_id = None
            if self.policy.allow_fallback and len(available_agents) > 1:
                other_candidates = [a for a in available_agents if a.agent_id != best_agent.agent_id]
                if other_candidates:
                    try:
                        fallback = self.selector.select_agent(req, other_candidates)
                        fallback_agent_id = fallback.agent_id
                    except Exception:
                        fallback_agent_id = None

            planned_tasks.append(
                task.model_copy(update={
                    "assigned_agent_id": best_agent.agent_id,
                    "fallback_agent_id": fallback_agent_id,
                    "delegation_depth": task.delegation_depth + 1
                })
            )

        return planned_tasks
