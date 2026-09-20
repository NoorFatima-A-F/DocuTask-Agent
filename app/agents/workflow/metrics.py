"""
Workflow Metrics Collector.
Collects telemetry, execution latencies, and counts for OpenTelemetry, Google Cloud Monitoring, and Cloud Logging.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class WorkflowMetricsSnapshot(BaseModel):
    """Snapshot of workflow runtime operational metrics."""
    total_workflows_started: int = 0
    total_workflows_completed: int = 0
    total_workflows_failed: int = 0
    total_workflows_cancelled: int = 0
    total_workflows_paused: int = 0
    total_workflows_resumed: int = 0
    total_sagas_executed: int = 0
    total_compensations_executed: int = 0
    total_human_approvals_requested: int = 0
    total_human_approvals_completed: int = 0
    total_signals_received: int = 0
    total_timers_fired: int = 0
    total_active_instances: int = 0
    average_workflow_duration_ms: float = 0.0


class WorkflowMetricsCollector:
    """In-memory telemetry collector with Google Cloud Monitoring metric export formatting."""

    def __init__(self) -> None:
        self._metrics = WorkflowMetricsSnapshot()
        self._workflow_durations: List[float] = []

    def record_workflow_started(self) -> None:
        self._metrics.total_workflows_started += 1
        self._metrics.total_active_instances += 1

    def record_workflow_completed(self, duration_ms: float) -> None:
        self._metrics.total_workflows_completed += 1
        self._metrics.total_active_instances = max(0, self._metrics.total_active_instances - 1)
        self._workflow_durations.append(duration_ms)
        self._metrics.average_workflow_duration_ms = (
            sum(self._workflow_durations) / len(self._workflow_durations)
        )

    def record_workflow_failed(self) -> None:
        self._metrics.total_workflows_failed += 1
        self._metrics.total_active_instances = max(0, self._metrics.total_active_instances - 1)

    def record_workflow_cancelled(self) -> None:
        self._metrics.total_workflows_cancelled += 1
        self._metrics.total_active_instances = max(0, self._metrics.total_active_instances - 1)

    def record_workflow_paused(self) -> None:
        self._metrics.total_workflows_paused += 1

    def record_workflow_resumed(self) -> None:
        self._metrics.total_workflows_resumed += 1

    def record_saga_executed(self) -> None:
        self._metrics.total_sagas_executed += 1

    def record_compensation_executed(self) -> None:
        self._metrics.total_compensations_executed += 1

    def record_human_approval_requested(self) -> None:
        self._metrics.total_human_approvals_requested += 1

    def record_human_approval_completed(self) -> None:
        self._metrics.total_human_approvals_completed += 1

    def record_signal_received(self) -> None:
        self._metrics.total_signals_received += 1

    def record_timer_fired(self) -> None:
        self._metrics.total_timers_fired += 1

    def get_snapshot(self) -> WorkflowMetricsSnapshot:
        return self._metrics.model_copy()

    def export_gcp_metrics(self) -> List[Dict[str, Any]]:
        """Formats snapshot as Google Cloud Monitoring custom metric time series."""
        snapshot = self.get_snapshot()
        return [
            {
                "metric": {"type": f"custom.googleapis.com/workflow/{k}"},
                "resource": {"type": "global"},
                "points": [{"value": {"doubleValue": float(v)}}],
            }
            for k, v in snapshot.model_dump().items()
        ]
