"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Observability.
Captures real-time telemetry: invocation counters, latency percentiles, error rates, retries, and costs.
"""

from __future__ import annotations

from datetime import datetime
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.models import ExecutionResult

logger = logging.getLogger(__name__)


class ConnectorMetricsSummary(BaseModel):
    """Aggregated operational telemetry for an individual connector."""
    connector_id: str
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_retries: int = 0
    total_cost_usd: float = 0.0
    avg_latency_ms: float = 0.0
    last_success_at: Optional[datetime] = None
    last_failure_at: Optional[datetime] = None
    error_counts: Dict[str, int] = Field(default_factory=dict)


class ConnectorObservability:
    """
    Central telemetry collector for all connector operations.
    """

    def __init__(self):
        self._summaries: Dict[str, ConnectorMetricsSummary] = {}
        self._latency_samples: Dict[str, List[float]] = {}

    def _get_or_create(self, connector_id: str) -> ConnectorMetricsSummary:
        if connector_id not in self._summaries:
            self._summaries[connector_id] = ConnectorMetricsSummary(connector_id=connector_id)
            self._latency_samples[connector_id] = []
        return self._summaries[connector_id]

    def record_execution(self, result: ExecutionResult, retry_count: int = 0) -> None:
        """Records an execution outcome and updates operational metrics."""
        summary = self._get_or_create(result.connector_id)
        summary.total_calls += 1
        summary.total_retries += retry_count
        summary.total_cost_usd += result.cost_usd

        self._latency_samples[result.connector_id].append(result.latency_ms)
        # Keep sliding window of 100 samples
        if len(self._latency_samples[result.connector_id]) > 100:
            self._latency_samples[result.connector_id].pop(0)

        samples = self._latency_samples[result.connector_id]
        summary.avg_latency_ms = sum(samples) / len(samples) if samples else 0.0

        if result.status == "SUCCESS":
            summary.successful_calls += 1
            summary.last_success_at = result.timestamp
        else:
            summary.failed_calls += 1
            summary.last_failure_at = result.timestamp
            err_key = result.error or "UNKNOWN_ERROR"
            summary.error_counts[err_key] = summary.error_counts.get(err_key, 0) + 1

    def get_summary(self, connector_id: str) -> Optional[ConnectorMetricsSummary]:
        """Returns metrics summary for a specific connector."""
        return self._summaries.get(connector_id)

    def get_all_summaries(self) -> Dict[str, ConnectorMetricsSummary]:
        """Returns all connector metrics summaries."""
        return dict(self._summaries)
