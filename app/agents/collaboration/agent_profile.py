"""Agent Profile Domain Model for Multi-Agent Collaboration.

Represents the capabilities, resource metrics, operational costs, and availability
of specialized agents within the Autonomous Operating System.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentProfile:
    """Enterprise profile defining agent traits, capacity, and operational cost."""

    agent_id: str
    role: str
    capabilities: List[str] = field(default_factory=list)
    cost_per_call: float = 0.001
    latency_p95_ms: float = 250.0
    confidence_rating: float = 0.95
    max_concurrency: int = 10
    current_load: int = 0
    is_healthy: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def can_accept_task(self) -> bool:
        """Determines if the agent has capacity to accept a new execution task."""
        return self.is_healthy and (self.current_load < self.max_concurrency)

    def increment_load(self) -> None:
        if not self.can_accept_task():
            raise RuntimeError(f"Agent {self.agent_id} cannot accept more load ({self.current_load}/{self.max_concurrency})")
        self.current_load += 1

    def decrement_load(self) -> None:
        self.current_load = max(0, self.current_load - 1)

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities or capability.lower() in self.role.lower()

    def update_heartbeat(self) -> None:
        self.last_heartbeat = time.time()
