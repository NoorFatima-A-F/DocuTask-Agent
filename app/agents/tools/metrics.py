"""
Tool Operational Metrics Collector.
Tracks tool execution metrics including total calls, latency, cost, and token usage.
"""

from typing import Dict
from pydantic import BaseModel, Field


class ToolMetricRecord(BaseModel):
    """Execution metrics for a specific tool."""
    tool_id: str
    total_calls: int = Field(default=0, ge=0)
    total_cost_usd: float = Field(default=0.0, ge=0.0)
    total_latency_ms: float = Field(default=0.0, ge=0.0)
    total_tokens: int = Field(default=0, ge=0)


class ToolMetricsCollector:
    """Collector tracking tool performance metrics."""

    def __init__(self):
        self._metrics: Dict[str, ToolMetricRecord] = {}

    def record_execution(
        self,
        tool_id: str,
        latency_ms: float,
        cost_usd: float = 0.0,
        tokens: int = 0
    ) -> None:
        """Records a completed tool execution."""
        rec = self._metrics.get(tool_id, ToolMetricRecord(tool_id=tool_id))
        self._metrics[tool_id] = ToolMetricRecord(
            tool_id=tool_id,
            total_calls=rec.total_calls + 1,
            total_cost_usd=rec.total_cost_usd + cost_usd,
            total_latency_ms=rec.total_latency_ms + latency_ms,
            total_tokens=rec.total_tokens + tokens
        )

    def get_metrics(self, tool_id: str) -> ToolMetricRecord:
        """Retrieves performance metrics record for tool."""
        return self._metrics.get(tool_id, ToolMetricRecord(tool_id=tool_id))
