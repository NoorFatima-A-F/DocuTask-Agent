"""
Reputation Engine for Dynamic Agent Reputation System.
Calculates mathematical reputation scores, dynamically modulates agent confidence ratings,
and refines multi-agent negotiation bids based on historical performance.
"""

from __future__ import annotations

import logging
from typing import Optional

from app.agents.collaboration.agent_profile import AgentProfile
from app.agents.collaboration.agent_registry import AgentRegistry
from app.agents.collaboration.reputation.performance_tracker import PerformanceTracker

logger = logging.getLogger(__name__)


class ReputationEngine:
    """Computes mathematical agent reputation and synchronizes with the collaboration framework."""

    def __init__(
        self,
        performance_tracker: Optional[PerformanceTracker] = None,
        registry: Optional[AgentRegistry] = None,
    ) -> None:
        self.tracker = performance_tracker or PerformanceTracker()
        self.registry = registry

    def compute_reputation_score(self, agent_id: str, baseline_latency_ms: float = 300.0) -> float:
        """
        Computes normalized reputation score in [0.0, 1.0]:
        Score = 0.40 * SuccessRate + 0.25 * Accuracy + 0.20 * Efficiency + 0.15 * Reliability - Penalties
        """
        metrics = self.tracker.get_metrics(agent_id)
        if metrics.total_invocations == 0:
            # Default prior for uninvoked agents
            return 0.95

        success_rate = metrics.success_rate
        accuracy = metrics.average_accuracy

        # Efficiency: ratio of baseline latency to actual latency, clamped to [0, 1]
        avg_lat = metrics.average_latency_ms
        efficiency = min(1.0, baseline_latency_ms / avg_lat) if avg_lat > 0 else 1.0

        # Reliability: penalize human overrides and reflection failures
        override_rate = metrics.total_human_overrides / metrics.total_invocations
        penalty_rate = metrics.total_reflection_penalties / metrics.total_invocations
        reliability = max(0.0, 1.0 - (override_rate * 0.5 + penalty_rate * 0.3))

        raw_score = (
            0.40 * success_rate
            + 0.25 * accuracy
            + 0.20 * efficiency
            + 0.15 * reliability
        )

        score = max(0.0, min(1.0, raw_score))
        return round(score, 4)

    def sync_agent_profile(self, agent_id: str) -> Optional[AgentProfile]:
        """Recalculates reputation and synchronizes AgentProfile.confidence_rating in AgentRegistry."""
        if not self.registry:
            return None

        profile = self.registry.get(agent_id)
        if not profile:
            return None

        new_reputation = self.compute_reputation_score(agent_id, baseline_latency_ms=profile.latency_p95_ms)
        old_rating = profile.confidence_rating
        profile.confidence_rating = new_reputation

        # Automatically mark unhealthy if reputation plummets below 0.50
        if new_reputation < 0.50:
            profile.is_healthy = False
            logger.warning("Agent %s marked unhealthy due to low reputation score: %.2f", agent_id, new_reputation)
        elif not profile.is_healthy and new_reputation >= 0.70:
            profile.is_healthy = True
            logger.info("Agent %s restored to healthy status with reputation score: %.2f", agent_id, new_reputation)

        logger.debug("Updated reputation for agent %s: %.3f -> %.3f", agent_id, old_rating, new_reputation)
        return profile

    def adjust_bid_confidence(self, agent_id: str, proposed_confidence: float) -> float:
        """Modulates a proposed negotiation bid confidence using historical reputation."""
        reputation = self.compute_reputation_score(agent_id)
        # Weighted blend between agent's self-reported bid and empirical reputation
        adjusted = 0.30 * proposed_confidence + 0.70 * reputation
        return round(max(0.1, min(1.0, adjusted)), 4)
