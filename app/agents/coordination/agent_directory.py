"""
Agent Directory.
Provides fast multi-index queries over agents by role, domain, skills, and availability.
"""

from typing import List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.lifecycle import AgentLifecycleState


class AgentDirectory:
    """Directory indexing agents across roles, skills, and states."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def find_by_role(self, role: str) -> List[Agent]:
        """Finds all agents with a matching role (e.g., supervisor, worker, specialist)."""
        all_agents = await self.registry.list_available()
        return [a for a in all_agents if a.profile.identity.role.lower() == role.lower()]

    async def find_by_domain(self, domain: str) -> List[Agent]:
        """Finds agents capable in a specific domain (e.g., financial, legal)."""
        all_agents = await self.registry.list_available()
        return [
            a for a in all_agents
            if domain.lower() in [d.lower() for d in a.profile.capabilities.execution_domains]
        ]

    async def find_by_skill(self, skill_name: str) -> List[Agent]:
        """Finds agents advertising a specific skill name."""
        all_agents = await self.registry.list_available()
        return [
            a for a in all_agents
            if any(s.name.lower() == skill_name.lower() for s in a.profile.capabilities.skills)
        ]
