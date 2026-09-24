"""
Reflection Metrics & Observability.
Collects telemetry, latencies, and counts for OpenTelemetry, Google Cloud Monitoring, and Cloud Logging.
"""

from typing import Any, Dict, List
from pydantic import BaseModel


class ReflectionMetrics(BaseModel):
    """Snapshot of aggregated reflection system metrics."""
    total_reflections_started: int = 0
    total_reflections_completed: int = 0
    total_reflections_failed: int = 0
    total_evaluations_executed: int = 0
    total_critiques_generated: int = 0
    total_learning_artifacts_created: int = 0
    total_recommendations_emitted: int = 0
    total_adaptation_proposals_created: int = 0
    average_reflection_duration_ms: float = 0.0
    average_evaluation_duration_ms: float = 0.0


class ReflectionMetricsCollector:
    """In-memory telemetry collector with Cloud Monitoring / OpenTelemetry telemetry counters."""

    def __init__(self):
        self._metrics = ReflectionMetrics()
        self._durations: List[float] = []

    def record_reflection_started(self) -> None:
        self._metrics.total_reflections_started += 1

    def record_reflection_completed(self, duration_ms: float) -> None:
        self._metrics.total_reflections_completed += 1
        self._durations.append(duration_ms)
        self._metrics.average_reflection_duration_ms = (
            sum(self._durations) / len(self._durations)
        )

    def record_reflection_failed(self) -> None:
        self._metrics.total_reflections_failed += 1

    def record_evaluation(self, dimension_count: int = 10) -> None:
        self._metrics.total_evaluations_executed += dimension_count

    def record_critique(self) -> None:
        self._metrics.total_critiques_generated += 1

    def record_artifacts(self, count: int) -> None:
        self._metrics.total_learning_artifacts_created += count

    def record_recommendations(self, count: int) -> None:
        self._metrics.total_recommendations_emitted += count

    def record_proposals(self, count: int) -> None:
        self._metrics.total_adaptation_proposals_created += count

    def get_metrics_snapshot(self) -> ReflectionMetrics:
        """Returns snapshot of current metrics."""
        return self._metrics.model_copy()

    def export_cloud_monitoring_format(self) -> Dict[str, Any]:
        """Formats metrics for Cloud Monitoring custom metrics API."""
        return {
            "custom.googleapis.com/agent/reflection/started_count": self._metrics.total_reflections_started,
            "custom.googleapis.com/agent/reflection/completed_count": self._metrics.total_reflections_completed,
            "custom.googleapis.com/agent/reflection/failed_count": self._metrics.total_reflections_failed,
            "custom.googleapis.com/agent/reflection/avg_duration_ms": self._metrics.average_reflection_duration_ms,
            "custom.googleapis.com/agent/reflection/artifacts_created": self._metrics.total_learning_artifacts_created,
            "custom.googleapis.com/agent/reflection/recommendations_emitted": self._metrics.total_recommendations_emitted,
        }
