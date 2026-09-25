"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Registry.
Provides centralized agent registration, capability matching, skill discovery,
version management, compatibility verification, and health tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import logging

from app.agents.domain.agent_entity import Agent, AgentLifecycleState, AgentType

logger = logging.getLogger(__name__)


@dataclass
class AgentHealthStatus:
    """Tracks operational health and telemetry for registered agents."""
    agent_id: str
    is_healthy: bool = True
    last_heartbeat: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_latency_ms: float = 0.0
    error_count: int = 0


class AgentRegistry:
    """
    Central repository for discovering, indexing, versioning, and matching
    autonomous agents across the enterprise platform.
    """

    def __init__(self):
        self._agents: Dict[str, Agent] = {}  # agent_id -> Agent
        self._versions: Dict[str, Dict[str, Agent]] = {}  # agent_name -> {version: Agent}
        self._health: Dict[str, AgentHealthStatus] = {}

    def register(self, agent: Agent) -> Agent:
        """Registers a new agent or updates an existing registered agent."""
        self._agents[agent.id] = agent
        
        if agent.name not in self._versions:
            self._versions[agent.name] = {}
        self._versions[agent.name][agent.version] = agent

        if agent.id not in self._health:
            self._health[agent.id] = AgentHealthStatus(agent_id=agent.id)

        logger.info(f"Registered Agent: {agent.name} v{agent.version} [ID: {agent.id}, Type: {agent.type}]")
        return agent

    def get(self, agent_id: str) -> Optional[Agent]:
        """Retrieves an agent by its unique identifier."""
        return self._agents.get(agent_id)

    def get_by_name_and_version(self, name: str, version: Optional[str] = None) -> Optional[Agent]:
        """Retrieves an agent by name and specific version, or the latest version."""
        if name not in self._versions:
            return None
        versions_map = self._versions[name]
        if not versions_map:
            return None
        if version:
            return versions_map.get(version)
        # Return latest registered version
        sorted_versions = sorted(versions_map.keys())
        return versions_map[sorted_versions[-1]]

    def find_capable_agents(
        self,
        capability: Optional[str] = None,
        skill: Optional[str] = None,
        agent_type: Optional[AgentType | str] = None,
        organization_id: Optional[str] = None,
        only_active: bool = True,
    ) -> List[Agent]:
        """
        Discovers and returns all agents matching the requested capability, skill, or type.
        """
        results: List[Agent] = []
        for agent in self._agents.values():
            if organization_id and agent.organization_id != organization_id:
                continue

            if only_active and agent.status in [
                AgentLifecycleState.FAILED,
                AgentLifecycleState.CANCELLED,
                AgentLifecycleState.ARCHIVED,
            ]:
                continue

            if agent_type:
                target_type = agent_type.value if isinstance(agent_type, AgentType) else str(agent_type)
                current_type = agent.type.value if isinstance(agent.type, AgentType) else str(agent.type)
                if target_type.lower() != current_type.lower():
                    continue

            if capability and capability.lower() not in [c.lower() for c in agent.capabilities]:
                continue

            if skill and skill.lower() not in [s.lower() for s in agent.skills]:
                continue

            results.append(agent)

        return results

    def find_best_agent(
        self,
        capability: Optional[str] = None,
        skill: Optional[str] = None,
        agent_type: Optional[AgentType | str] = None,
        organization_id: Optional[str] = None,
    ) -> Optional[Agent]:
        """
        Finds the single best candidate agent based on health, capability match,
        and success rate.
        """
        candidates = self.find_capable_agents(
            capability=capability,
            skill=skill,
            agent_type=agent_type,
            organization_id=organization_id,
            only_active=True,
        )
        if not candidates:
            return None

        # Sort candidates by health and completion stats
        def score(a: Agent) -> float:
            h = self._health.get(a.id)
            if not h or not h.is_healthy:
                return -1.0
            total = h.total_tasks_completed + h.total_tasks_failed
            if total == 0:
                return 1.0  # Fresh agent
            return h.total_tasks_completed / total

        candidates.sort(key=score, reverse=True)
        return candidates[0]

    def validate_compatibility(
        self,
        agent: Agent,
        required_capabilities: List[str],
        required_skills: List[str]
    ) -> bool:
        """Validates whether an agent satisfies a set of required capabilities and skills."""
        agent_caps = {c.lower() for c in agent.capabilities}
        agent_skills = {s.lower() for s in agent.skills}

        for rc in required_capabilities:
            if rc.lower() not in agent_caps:
                return False

        for rs in required_skills:
            if rs.lower() not in agent_skills:
                return False

        return True

    def record_heartbeat(self, agent_id: str, is_healthy: bool = True) -> None:
        """Records a liveness heartbeat and health status for an agent."""
        if agent_id in self._health:
            self._health[agent_id].last_heartbeat = datetime.now(timezone.utc)
            self._health[agent_id].is_healthy = is_healthy

    def record_task_outcome(self, agent_id: str, success: bool, latency_ms: float = 0.0) -> None:
        """Updates health and operational metrics for an agent."""
        if agent_id in self._health:
            h = self._health[agent_id]
            if success:
                h.total_tasks_completed += 1
            else:
                h.total_tasks_failed += 1
                h.error_count += 1
            # Rolling latency
            if h.average_latency_ms == 0.0:
                h.average_latency_ms = latency_ms
            else:
                h.average_latency_ms = (h.average_latency_ms * 0.9) + (latency_ms * 0.1)

    def list_all(self, organization_id: Optional[str] = None) -> List[Agent]:
        """Lists all registered agents, optionally filtered by organization."""
        if organization_id:
            return [a for a in self._agents.values() if a.organization_id == organization_id]
        return list(self._agents.values())

    def clear(self) -> None:
        """Clears all registered agents (primarily for test teardown)."""
        self._agents.clear()
        self._versions.clear()
        self._health.clear()
