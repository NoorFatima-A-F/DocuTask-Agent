"""
Agent Load Balancer.
Distributes incoming tasks across qualified agents using Round-Robin, Least-Loaded, or Weighted strategies.
"""

from enum import Enum
from typing import List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent


class LoadBalancingStrategy(str, Enum):
    """Load balancing algorithm."""
    ROUND_ROBIN = "ROUND_ROBIN"
    LEAST_LOADED = "LEAST_LOADED"
    CAPABILITY_WEIGHTED = "CAPABILITY_WEIGHTED"


class AgentLoadBalancer:
    """Balances task assignments across candidate agent pools."""

    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED):
        self.strategy = strategy
        self._round_robin_idx = 0

    def select_agent(self, candidates: List[Agent]) -> Optional[Agent]:
        """Selects target agent based on load balancing policy."""
        if not candidates:
            return None

        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            agent = candidates[self._round_robin_idx % len(candidates)]
            self._round_robin_idx += 1
            return agent

        if self.strategy == LoadBalancingStrategy.LEAST_LOADED:
            # Candidate with fewest current tasks
            return min(candidates, key=lambda a: len(a.current_tasks))

        if self.strategy == LoadBalancingStrategy.CAPABILITY_WEIGHTED:
            # Score = confidence / (1 + current_tasks)
            return max(
                candidates,
                key=lambda a: a.profile.capabilities.confidence_rating / (1 + len(a.current_tasks))
            )

        return candidates[0]
