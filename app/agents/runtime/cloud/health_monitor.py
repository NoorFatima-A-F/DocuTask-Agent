"""
Cloud Health Monitor for Enterprise Agent Operating System.
Provides Kubernetes/Cloud Run liveness (/healthz) and readiness (/readyz) probes.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.collaboration.agent_registry import AgentRegistry
from app.agents.events.event_bus import EnterpriseEventBus

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """System health check response."""

    status: str  # "HEALTHY", "DEGRADED", "UNHEALTHY"
    uptime_seconds: float
    healthy_agents_count: int
    unhealthy_agents_count: int
    event_bus_metrics: Dict[str, Any]
    details: Dict[str, Any] = field(default_factory=dict)


class CloudHealthMonitor:
    """Monitors process vitality, memory, event queues, and agent availability."""

    def __init__(
        self,
        event_bus: Optional[EnterpriseEventBus] = None,
        agent_registry: Optional[AgentRegistry] = None,
    ) -> None:
        self.event_bus = event_bus
        self.registry = agent_registry
        self.started_at = time.time()

    def check_liveness(self) -> Dict[str, str]:
        """Kubernetes /healthz probe: verifies process is alive."""
        return {"status": "UP", "timestamp": str(time.time())}

    def check_readiness(self) -> HealthStatus:
        """Kubernetes /readyz probe: verifies system dependencies and agent pools."""
        uptime = time.time() - self.started_at
        healthy_agents = 0
        unhealthy_agents = 0

        if self.registry:
            for profile in self.registry._agents.values():
                if profile.is_healthy:
                    healthy_agents += 1
                else:
                    unhealthy_agents += 1

        eb_metrics = self.event_bus.metrics if self.event_bus else {}
        dlq_size = eb_metrics.get("dlq_size", 0)

        # Status determination
        if unhealthy_agents > healthy_agents or dlq_size > 100:
            status = "DEGRADED"
        else:
            status = "HEALTHY"

        return HealthStatus(
            status=status,
            uptime_seconds=round(uptime, 2),
            healthy_agents_count=healthy_agents,
            unhealthy_agents_count=unhealthy_agents,
            event_bus_metrics=eb_metrics,
            details={"process_alive": True},
        )
