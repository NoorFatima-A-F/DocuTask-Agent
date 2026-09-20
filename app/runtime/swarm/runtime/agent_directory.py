"""
AMCN-SIP Phase 13.8 - Agent Directory & Semantic Discovery
Semantic capability search, nearest expert matching, and replacement discovery.
"""

from typing import List, Optional
from app.runtime.swarm.runtime.agent_registry import AgentRegistry, SwarmAgentProfile
from app.runtime.swarm.events.swarm_events import AgentRoleType, AgentLifecycleState, AgentRole, AgentState


class AgentDirectory:
    """
    Finds best matching agents for tasks based on capability overlap, reputation score, and availability.
    """

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def find_nearest_expert(
        self,
        required_capability: str,
        preferred_role: Optional[AgentRoleType] = None,
        min_reputation: float = 0.80,
    ) -> Optional[SwarmAgentProfile]:
        candidates = self.registry.list_agents(role=preferred_role, capability=required_capability)
        if not candidates:
            # Fallback to any agent with capability regardless of role
            candidates = self.registry.list_agents(capability=required_capability)

        if not candidates:
            # Fallback to specialist or coordinator
            candidates = self.registry.list_agents(role=AgentRole.SPECIALIST) or self.registry.list_agents()

        # Filter by reputation and sort by availability + reputation
        eligible = [c for c in candidates if c.reputation_score >= min_reputation]
        if not eligible:
            eligible = candidates

        sorted_candidates = sorted(
            eligible,
            key=lambda a: (
                1 if a.state == AgentState.AVAILABLE else 0,
                a.reputation_score,
                -a.avg_latency_ms,
            ),
            reverse=True,
        )

        return sorted_candidates[0] if sorted_candidates else None

    def discover_agent(self, capability: str) -> Optional[SwarmAgentProfile]:
        return self.find_nearest_expert(capability)

    def fallback_discovery(self) -> Optional[SwarmAgentProfile]:
        agents = self.registry.list_agents()
        return agents[0] if agents else None

    def find_replacement(self, failed_agent_id: str) -> Optional[SwarmAgentProfile]:
        failed = self.registry.get_agent(failed_agent_id)
        if not failed:
            return None

        # Find agent with highest capability overlap
        other_agents = [a for a in self.registry.list_agents() if a.agent_id != failed_agent_id and a.state == AgentState.AVAILABLE]
        if not other_agents:
            other_agents = [a for a in self.registry.list_agents() if a.agent_id != failed_agent_id]

        if not other_agents:
            return None

        return other_agents[0]
