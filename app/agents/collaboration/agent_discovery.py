"""Agent Discovery Service for Multi-Agent Collaboration.

Performs dynamic discovery and multi-objective ranking of candidate agents
for tasks based on confidence, cost, latency, and real-time operational load.
"""

from __future__ import annotations

from typing import List, Optional

from app.agents.collaboration.agent_profile import AgentProfile
from app.agents.collaboration.agent_registry import AgentRegistry


class AgentDiscoveryService:
    """Discovers best available agents matching capability criteria."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def discover_best_agent(
        self,
        capability: str,
        max_cost: Optional[float] = None,
        max_latency_ms: Optional[float] = None,
        min_confidence: float = 0.85,
    ) -> Optional[AgentProfile]:
        """Find the optimal agent matching capability and constraints."""
        candidates = self.registry.find_by_capability(capability)
        if not candidates:
            return None

        # Filter by hard constraints and availability
        valid: List[AgentProfile] = []
        for c in candidates:
            if not c.can_accept_task():
                continue
            if c.confidence_rating < min_confidence:
                continue
            if max_cost is not None and c.cost_per_call > max_cost:
                continue
            if max_latency_ms is not None and c.latency_p95_ms > max_latency_ms:
                continue
            valid.append(c)

        if not valid:
            # Relax soft constraints if needed, or pick best available
            valid = [c for c in candidates if c.can_accept_task()]
            if not valid:
                return None

        # Multi-factor score:
        # Score = 0.4 * confidence + 0.25 * (1 - cost/max_cost) + 0.2 * (1 - latency/max_lat) + 0.15 * (1 - load/max_load)
        def rank_score(agent: AgentProfile) -> float:
            conf_part = agent.confidence_rating * 40.0
            cost_part = max(0.0, 25.0 - (agent.cost_per_call * 1000.0))
            lat_part = max(0.0, 20.0 - (agent.latency_p95_ms / 50.0))
            load_factor = (agent.max_concurrency - agent.current_load) / max(1, agent.max_concurrency)
            load_part = load_factor * 15.0
            return conf_part + cost_part + lat_part + load_part

        return max(valid, key=rank_score)
