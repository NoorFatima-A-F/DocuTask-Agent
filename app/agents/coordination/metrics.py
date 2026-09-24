"""
Coordination Metrics Collector.
Collects telemetry, latencies, and counts for OpenTelemetry, Google Cloud Monitoring, and Cloud Logging.
"""

from typing import Any, Dict, List
from pydantic import BaseModel


class CoordinationMetricsSnapshot(BaseModel):
    """Snapshot of multi-agent coordination metrics."""
    total_delegations_started: int = 0
    total_delegations_completed: int = 0
    total_delegations_failed: int = 0
    total_messages_routed: int = 0
    total_negotiation_rounds: int = 0
    total_consensus_rounds: int = 0
    total_conflicts_resolved: int = 0
    total_active_teams: int = 0
    average_delegation_latency_ms: float = 0.0


class CoordinationMetricsCollector:
    """In-memory telemetry collector with Cloud Monitoring custom metric export."""

    def __init__(self):
        self._metrics = CoordinationMetricsSnapshot()
        self._delegation_durations: List[float] = []

    def record_delegation_started(self) -> None:
        self._metrics.total_delegations_started += 1

    def record_delegation_completed(self, duration_ms: float) -> None:
        self._metrics.total_delegations_completed += 1
        self._delegation_durations.append(duration_ms)
        self._metrics.average_delegation_latency_ms = (
            sum(self._delegation_durations) / len(self._delegation_durations)
        )

    def record_delegation_failed(self) -> None:
        self._metrics.total_delegations_failed += 1

    def record_message_routed(self) -> None:
        self._metrics.total_messages_routed += 1

    def record_negotiation(self) -> None:
        self._metrics.total_negotiation_rounds += 1

    def record_consensus(self) -> None:
        self._metrics.total_consensus_rounds += 1

    def record_conflict_resolved(self) -> None:
        self._metrics.total_conflicts_resolved += 1

    def set_active_teams(self, count: int) -> None:
        self._metrics.total_active_teams = count

    def get_snapshot(self) -> CoordinationMetricsSnapshot:
        return self._metrics.model_copy()

    def export_cloud_monitoring(self) -> Dict[str, Any]:
        """Formats metrics for Cloud Monitoring custom metrics API."""
        return {
            "custom.googleapis.com/agent/coordination/delegations_completed": self._metrics.total_delegations_completed,
            "custom.googleapis.com/agent/coordination/delegations_failed": self._metrics.total_delegations_failed,
            "custom.googleapis.com/agent/coordination/messages_routed": self._metrics.total_messages_routed,
            "custom.googleapis.com/agent/coordination/avg_delegation_latency_ms": self._metrics.average_delegation_latency_ms,
            "custom.googleapis.com/agent/coordination/active_teams": self._metrics.total_active_teams
        }
