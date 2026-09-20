"""
Agent Health Monitor.
Tracks agent liveness from heartbeats and flags degraded or hung agents.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.coordination.heartbeat import AgentHeartbeat


class AgentHealthStatus:
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNRESPONSIVE = "UNRESPONSIVE"


class AgentHealthMonitor:
    """Monitors heartbeat timestamps to detect unresponsive or degraded agents."""

    def __init__(self, timeout_seconds: float = 30.0):
        self.timeout_seconds = timeout_seconds
        self._last_heartbeats: Dict[UUID, AgentHeartbeat] = {}

    def record_heartbeat(self, heartbeat: AgentHeartbeat) -> None:
        """Records latest heartbeat."""
        self._last_heartbeats[heartbeat.agent_id] = heartbeat

    def get_agent_health(self, agent_id: UUID) -> str:
        """Determines health status of an agent."""
        hb = self._last_heartbeats.get(agent_id)
        if not hb:
            return AgentHealthStatus.UNRESPONSIVE

        now = datetime.now(timezone.utc).timestamp()
        diff = now - hb.timestamp.timestamp()
        if diff > self.timeout_seconds:
            return AgentHealthStatus.UNRESPONSIVE
        if hb.active_task_count > 10 or hb.cpu_utilization > 0.9:
            return AgentHealthStatus.DEGRADED
        return AgentHealthStatus.HEALTHY
