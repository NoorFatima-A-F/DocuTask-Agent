"""
Automated Quality, Performance, and Cost Regression Detection Engine.
"""
from __future__ import annotations
import uuid
from typing import Dict, List
from app.platform_verification.evaluation_engine.domain.models import (
    MetricResult,
    RegressionAlert,
    RegressionCategory,
    Severity,
    MetricCategory,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IRegressionDetector


class RegressionDetector(IRegressionDetector):
    """Monitors metrics against baselines and emits automated regression alerts."""

    def __init__(
        self,
        quality_drop_threshold_pct: float = 2.0,
        perf_latency_spike_threshold_pct: float = 20.0,
        cost_spike_threshold_pct: float = 25.0,
    ) -> None:
        self.quality_threshold = quality_drop_threshold_pct
        self.perf_threshold = perf_latency_spike_threshold_pct
        self.cost_threshold = cost_spike_threshold_pct

    def check_regressions(
        self, candidate_results: List[MetricResult], baseline_results: List[MetricResult]
    ) -> List[RegressionAlert]:
        baseline_map: Dict[str, MetricResult] = {m.metric_id: m for m in baseline_results}
        alerts: List[RegressionAlert] = []

        for candidate in candidate_results:
            if candidate.metric_id not in baseline_map:
                continue

            base = baseline_map[candidate.metric_id]
            if base.raw_value == 0:
                continue

            delta_pct = ((candidate.raw_value - base.raw_value) / base.raw_value) * 100.0

            # 1. Quality Regression (e.g., accuracy, precision drops)
            if candidate.category in [MetricCategory.FUNCTIONAL_CORRECTNESS, MetricCategory.AI_QUALITY]:
                if delta_pct < -self.quality_threshold:
                    alerts.append(
                        RegressionAlert(
                            alert_id=f"REG-Q-{uuid.uuid4().hex[:6].upper()}",
                            metric_id=candidate.metric_id,
                            metric_name=candidate.metric_name,
                            category=RegressionCategory.QUALITY,
                            baseline_value=base.raw_value,
                            candidate_value=candidate.raw_value,
                            delta_percentage=round(delta_pct, 2),
                            threshold_percentage=self.quality_threshold,
                            severity=Severity.HIGH,
                            message=f"Quality regression detected in {candidate.metric_name}: dropped by {abs(delta_pct):.2f}% (from {base.raw_value} to {candidate.raw_value}).",
                        )
                    )

            # 2. Performance Latency Spike
            elif candidate.category == MetricCategory.PERFORMANCE and "latency" in candidate.metric_id:
                if delta_pct > self.perf_threshold:
                    alerts.append(
                        RegressionAlert(
                            alert_id=f"REG-P-{uuid.uuid4().hex[:6].upper()}",
                            metric_id=candidate.metric_id,
                            metric_name=candidate.metric_name,
                            category=RegressionCategory.PERFORMANCE,
                            baseline_value=base.raw_value,
                            candidate_value=candidate.raw_value,
                            delta_percentage=round(delta_pct, 2),
                            threshold_percentage=self.perf_threshold,
                            severity=Severity.HIGH,
                            message=f"Performance regression detected in {candidate.metric_name}: latency spiked by +{delta_pct:.2f}% (from {base.raw_value}ms to {candidate.raw_value}ms).",
                        )
                    )

            # 3. Cost Spike
            elif candidate.category == MetricCategory.PERFORMANCE and "cost" in candidate.metric_id:
                if delta_pct > self.cost_threshold:
                    alerts.append(
                        RegressionAlert(
                            alert_id=f"REG-C-{uuid.uuid4().hex[:6].upper()}",
                            metric_id=candidate.metric_id,
                            metric_name=candidate.metric_name,
                            category=RegressionCategory.COST,
                            baseline_value=base.raw_value,
                            candidate_value=candidate.raw_value,
                            delta_percentage=round(delta_pct, 2),
                            threshold_percentage=self.cost_threshold,
                            severity=Severity.MEDIUM,
                            message=f"Cost regression detected in {candidate.metric_name}: cost increased by +{delta_pct:.2f}% (from ${base.raw_value} to ${candidate.raw_value}).",
                        )
                    )

        return alerts
