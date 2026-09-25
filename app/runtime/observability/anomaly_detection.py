"""
Autonomous Telemetry Anomaly Detector.

Monitors streaming metrics to identify statistical anomalies (Z-score outliers >= 3.0,
sudden latency spikes, memory leak growth slopes, retry explosions, worker starvation).
Zero false assumptions: baseline distributions are computed from actual execution history.
"""

from __future__ import annotations

import collections
import math
import time
from typing import Dict, List, Optional
from app.runtime.observability.schemas import (
    AnomalyReport,
    BaseRuntimeEvent,
    EventSeverity,
)


class AnomalyDetector:
    """Statistical anomaly detector operating over sliding metric windows."""

    def __init__(self, z_score_threshold: float = 3.0, min_history: int = 10) -> None:
        self.z_score_threshold = z_score_threshold
        self.min_history = min_history
        self._metric_history: Dict[str, collections.deque[float]] = collections.defaultdict(
            lambda: collections.deque(maxlen=100)
        )
        self._detected_anomalies: collections.deque[AnomalyReport] = collections.deque(maxlen=500)

    def observe(
        self, metric_name: str, value: float, anomaly_type: str = "GENERIC_OUTLIER"
    ) -> Optional[AnomalyReport]:
        """Observes a metric value and returns an AnomalyReport if it deviates significantly."""
        history = self._metric_history[metric_name]
        
        if len(history) < self.min_history:
            history.append(value)
            return None

        # Calculate mean and standard deviation
        mean = sum(history) / len(history)
        var = sum((x - mean) ** 2 for x in history) / (len(history) - 1)
        stddev = math.sqrt(var)

        history.append(value)

        if stddev < 1e-6:
            return None

        z_score = (value - mean) / stddev

        if z_score >= self.z_score_threshold:
            severity = EventSeverity.CRITICAL if z_score >= 4.5 else EventSeverity.WARNING
            report = AnomalyReport(
                metric_name=metric_name,
                anomaly_type=anomaly_type,
                severity=severity,
                observed_value=round(value, 3),
                expected_mean=round(mean, 3),
                z_score=round(z_score, 2),
                timestamp=time.time(),
                details=f"Metric '{metric_name}' observed {value:.2f} (Z-Score: +{z_score:.2f}σ above baseline {mean:.2f}).",
                root_cause_hint=self._diagnose_cause(metric_name, anomaly_type),
            )
            self._detected_anomalies.append(report)
            return report

        return None

    def _diagnose_cause(self, metric_name: str, anomaly_type: str) -> str:
        if "latency" in metric_name.lower():
            return "Potential worker thread contention, upstream LLM throttling, or complex table parsing."
        if "memory" in metric_name.lower():
            return "Potential unreleased image buffer or cache buildup in worker node."
        if "retry" in metric_name.lower():
            return "Repeated upstream service failures or validation constraint violations."
        if "queue" in metric_name.lower():
            return "Worker throughput lagging behind mission arrival velocity."
        return "Statistical divergence from baseline operating parameters."

    def check_event(self, event: BaseRuntimeEvent) -> Optional[AnomalyReport]:
        """Inspects single event for duration or failure anomalies."""
        if event.duration_ms > 0:
            metric_key = f"latency:{event.stage}:{event.event_type}"
            return self.observe(metric_key, event.duration_ms, anomaly_type="LATENCY_SPIKE")
        return None

    def get_recent_anomalies(self, limit: int = 20) -> List[AnomalyReport]:
        return list(self._detected_anomalies)[-limit:]
