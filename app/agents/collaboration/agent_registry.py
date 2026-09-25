"""Agent Registry for Multi-Agent Collaboration Engine.

Maintains the authoritative live catalog of all registered agent instances,
their active states, capacity, and health monitoring.
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional

from app.agents.collaboration.agent_profile import AgentProfile

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Central registry tracking active agent profiles and live health status."""

    def __init__(self, heartbeat_timeout_seconds: float = 60.0) -> None:
        self._profiles: Dict[str, AgentProfile] = {}
        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds

    def register(self, profile: AgentProfile) -> None:
        profile.update_heartbeat()
        self._profiles[profile.agent_id] = profile
        logger.info("Registered agent %s (%s)", profile.agent_id, profile.role)

    def deregister(self, agent_id: str) -> bool:
        if agent_id in self._profiles:
            del self._profiles[agent_id]
            logger.info("Deregistered agent %s", agent_id)
            return True
        return False

    def get(self, agent_id: str) -> Optional[AgentProfile]:
        profile = self._profiles.get(agent_id)
        if profile:
            self._check_health(profile)
        return profile

    def list_all(self) -> List[AgentProfile]:
        time.time()
        for p in self._profiles.values():
            self._check_health(p)
        return list(self._profiles.values())

    def find_by_capability(self, capability: str) -> List[AgentProfile]:
        return [
            p for p in self.list_all()
            if p.has_capability(capability) and p.is_healthy
        ]

    def record_heartbeat(self, agent_id: str) -> bool:
        profile = self._profiles.get(agent_id)
        if profile:
            profile.update_heartbeat()
            profile.is_healthy = True
            return True
        return False

    def _check_health(self, profile: AgentProfile) -> None:
        if (time.time() - profile.last_heartbeat) > self.heartbeat_timeout_seconds:
            profile.is_healthy = False
