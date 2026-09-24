"""
Agent Heartbeat Models.
Defines heartbeat telemetry emitted by active agents to track liveness and load.
"""

from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field


class AgentHeartbeat(BaseModel):
    """Heartbeat signal sent periodically by agents."""
    agent_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_task_count: int = Field(default=0, ge=0)
    cpu_utilization: float = Field(default=0.0, ge=0.0, le=1.0)
    memory_mb: float = Field(default=0.0, ge=0.0)

    model_config = {"frozen": True}
