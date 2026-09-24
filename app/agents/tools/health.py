"""
Tool Health Monitoring Subsystem.
Tracks heartbeat status, consecutive failure counters, and latency averages for tools and providers.
"""

from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field
from app.agents.tools.provider import ProviderStatus


class ToolHealthRecord(BaseModel):
    """Health status record for a single registered tool."""
    tool_id: str
    status: ProviderStatus = Field(default=ProviderStatus.HEALTHY)
    last_heartbeat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    consecutive_failures: int = Field(default=0, ge=0)
    total_calls: int = Field(default=0, ge=0)
    total_failures: int = Field(default=0, ge=0)


class ToolHealthMonitor:
    """Monitor tracking tool operational health."""

    def __init__(self):
        self._records: Dict[str, ToolHealthRecord] = {}

    def record_success(self, tool_id: str) -> None:
        """Records a successful tool execution."""
        rec = self._records.get(tool_id, ToolHealthRecord(tool_id=tool_id))
        self._records[tool_id] = ToolHealthRecord(
            tool_id=tool_id,
            status=ProviderStatus.HEALTHY,
            last_heartbeat=datetime.now(timezone.utc),
            consecutive_failures=0,
            total_calls=rec.total_calls + 1,
            total_failures=rec.total_failures
        )

    def record_failure(self, tool_id: str) -> None:
        """Records a tool execution failure."""
        rec = self._records.get(tool_id, ToolHealthRecord(tool_id=tool_id))
        new_failures = rec.consecutive_failures + 1
        status = ProviderStatus.UNAVAILABLE if new_failures >= 3 else ProviderStatus.DEGRADED

        self._records[tool_id] = ToolHealthRecord(
            tool_id=tool_id,
            status=status,
            last_heartbeat=datetime.now(timezone.utc),
            consecutive_failures=new_failures,
            total_calls=rec.total_calls + 1,
            total_failures=rec.total_failures + 1
        )

    def get_health(self, tool_id: str) -> ToolHealthRecord:
        """Retrieves current health record for tool."""
        return self._records.get(tool_id, ToolHealthRecord(tool_id=tool_id))
