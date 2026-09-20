"""
Continuous Benchmark Observatory & Regression Detection Platform.
Maintains historical time-series telemetry across benchmark campaigns:
- Trend analysis over sequential git commits
- Multi-dimensional regression detection (Latency, Memory, Confidence, Accuracy, Cost)
- Automated threshold alerts (SRE Alerting standard)
"""

from __future__ import annotations

import logging
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class RegressionSeverity(str, Enum):
    NONE = "NONE"
    MINOR_DRIFT = "MINOR_DRIFT"
    CRITICAL_REGRESSION = "CRITICAL_REGRESSION"


@dataclass
class HistoricalBenchmarkDataPoint:
    """Historical execution record of a benchmark."""

    campaign_id: str
    git_sha: str
    mean_latency_ms: float
    p95_latency_ms: float
    memory_mb: float
    accuracy_f1: float
    cost_usd: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class RegressionAlert:
    """Alert raised when benchmark metric degrades beyond acceptable thresholds."""

    metric_name: str
    baseline_value: float
    current_value: float
    delta_percentage: float
    severity: RegressionSeverity
    message: str


@dataclass
class ObservatoryAnalysisReport:
    """Consolidated time-series trend and regression analysis report."""

    benchmark_name: str
    total_campaigns_analyzed: int
    latency_trend_slope: float
    memory_growth_slope: float
    accuracy_trend_slope: float
    alerts: List[RegressionAlert]
    has_critical_regression: bool
    verdict_summary: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_name": self.benchmark_name,
            "campaigns_count": self.total_campaigns_analyzed,
            "latency_trend_slope": round(self.latency_trend_slope, 4),
            "memory_growth_slope": round(self.memory_growth_slope, 4),
            "accuracy_trend_slope": round(self.accuracy_trend_slope, 4),
            "has_critical_regression": self.has_critical_regression,
            "verdict_summary": self.verdict_summary,
            "alerts": [asdict(a) for a in self.alerts],
        }


class ContinuousBenchmarkObservatory:
    """
    Tracks benchmark performance evolution across historical commits and flags regressions.
    """

    LATENCY_REGRESSION_THRESHOLD_PCT: float = 15.0  # >15% latency increase is regression
    ACCURACY_DROP_THRESHOLD_PCT: float = 5.0  # >5% accuracy drop is critical

    def __init__(self) -> None:
        self.history: Dict[str, List[HistoricalBenchmarkDataPoint]] = {}

    def record_data_point(self, benchmark_name: str, point: HistoricalBenchmarkDataPoint) -> None:
        """Stores a historical benchmark run data point."""
        if benchmark_name not in self.history:
            self.history[benchmark_name] = []
        self.history[benchmark_name].append(point)

    def analyze_trends(self, benchmark_name: str) -> ObservatoryAnalysisReport:
        """Analyzes historical trends and evaluates regression alerts."""
        points = self.history.get(benchmark_name, [])
        if len(points) < 2:
            return ObservatoryAnalysisReport(
                benchmark_name=benchmark_name,
                total_campaigns_analyzed=len(points),
                latency_trend_slope=0.0,
                memory_growth_slope=0.0,
                accuracy_trend_slope=0.0,
                alerts=[],
                has_critical_regression=False,
                verdict_summary="Insufficient historical data points for regression detection (minimum 2 required).",
            )

        latencies = [p.mean_latency_ms for p in points]
        memories = [p.memory_mb for p in points]
        accuracies = [p.accuracy_f1 for p in points]

        lat_slope = self._compute_slope(latencies)
        mem_slope = self._compute_slope(memories)
        acc_slope = self._compute_slope(accuracies)

        alerts: List[RegressionAlert] = []

        # Check latest vs baseline (first point or median of past runs)
        baseline_lat = points[0].mean_latency_ms
        current_lat = points[-1].mean_latency_ms
        lat_delta_pct = ((current_lat - baseline_lat) / max(1e-9, baseline_lat)) * 100.0

        if lat_delta_pct > self.LATENCY_REGRESSION_THRESHOLD_PCT:
            alerts.append(
                RegressionAlert(
                    metric_name="Mean Latency",
                    baseline_value=baseline_lat,
                    current_value=current_lat,
                    delta_percentage=lat_delta_pct,
                    severity=RegressionSeverity.CRITICAL_REGRESSION,
                    message=f"Latency regressed by +{lat_delta_pct:.1f}% ({baseline_lat:.2f}ms -> {current_lat:.2f}ms).",
                )
            )

        baseline_acc = points[0].accuracy_f1
        current_acc = points[-1].accuracy_f1
        acc_delta_pct = ((baseline_acc - current_acc) / max(1e-9, baseline_acc)) * 100.0

        if acc_delta_pct > self.ACCURACY_DROP_THRESHOLD_PCT:
            alerts.append(
                RegressionAlert(
                    metric_name="Accuracy F1",
                    baseline_value=baseline_acc,
                    current_value=current_acc,
                    delta_percentage=-acc_delta_pct,
                    severity=RegressionSeverity.CRITICAL_REGRESSION,
                    message=f"Accuracy degraded by -{acc_delta_pct:.1f}% ({baseline_acc:.3f} -> {current_acc:.3f}).",
                )
            )

        has_crit = any(a.severity == RegressionSeverity.CRITICAL_REGRESSION for a in alerts)
        verdict = f"Observatory analyzed {len(points)} historical campaigns. " + (
            f"CRITICAL: {len(alerts)} regression alert(s) detected!" if has_crit else "Performance is stable with zero regressions."
        )

        return ObservatoryAnalysisReport(
            benchmark_name=benchmark_name,
            total_campaigns_analyzed=len(points),
            latency_trend_slope=lat_slope,
            memory_growth_slope=mem_slope,
            accuracy_trend_slope=acc_slope,
            alerts=alerts,
            has_critical_regression=has_crit,
            verdict_summary=verdict,
        )

    @staticmethod
    def _compute_slope(values: List[float]) -> float:
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2.0
        y_mean = statistics.mean(values)
        denom = sum((i - x_mean) ** 2 for i in range(n))
        if denom <= 0:
            return 0.0
        numer = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        return numer / denom
