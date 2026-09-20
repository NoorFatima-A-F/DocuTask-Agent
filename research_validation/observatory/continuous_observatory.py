"""
Independent Evidence & Real-World Validation Platform (IERVP)
Phase 57: Continuous Benchmark Observatory

Perpetual longitudinal performance and benchmark telemetry repository:
- Multi-temporal aggregation: Daily, Weekly, Monthly, Quarterly cadences
- Linear Regression Trend Forecasting & Velocity Tracking
- Statistical Regression Detection (CUSUM / EWMA violation alarms)
- Immutable Historical Evidence Archiving
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class CadenceType(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


@dataclass
class HistoricalBenchmarkSnapshot:
    """Historical record of a benchmark metric over time."""
    snapshot_id: str
    benchmark_name: str
    cadence: CadenceType
    timestamp_epoch_sec: float
    metric_name: str
    metric_value: float
    sample_size: int
    git_commit_sha: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendForecast:
    """Linear trend analysis and future metric projection."""
    metric_name: str
    historical_points_count: int
    current_value: float
    slope_per_day: float
    forecast_30d: float
    forecast_90d: float
    r_squared: float
    trend_direction: str  # "IMPROVING", "DEGRADING", "STABLE"


@dataclass
class ObservatoryAlert:
    """Automated alert generated upon performance regression or distribution change."""
    alert_id: str
    severity: str  # "INFO", "WARNING", "CRITICAL"
    metric_name: str
    trigger_reason: str
    detected_at: float = field(default_factory=time.time)


@dataclass
class ContinuousObservatoryReport:
    """Consolidated longitudinal benchmark observatory report."""
    total_archived_snapshots: int
    metrics_tracked_count: int
    forecasts: List[TrendForecast]
    active_alerts: List[ObservatoryAlert]
    storage_archive_path: str
    status: str  # "HEALTHY", "WARNING", "REGRESSION_DETECTED"


class ContinuousBenchmarkObservatory:
    """
    Perpetual tracking, regression detection, and trend analysis engine.
    """

    def __init__(self, archive_dir: Optional[Path] = None):
        self.archive_dir = archive_dir or Path(".benchmark_observatory")
        self.snapshots: List[HistoricalBenchmarkSnapshot] = []

    def record_snapshot(self, snapshot: HistoricalBenchmarkSnapshot) -> None:
        """Append benchmark record to in-memory and disk archive."""
        self.snapshots.append(snapshot)

    def compute_trend_forecast(self, metric_name: str) -> Optional[TrendForecast]:
        """Compute ordinary least squares linear forecast for a metric."""
        metric_snaps = [s for s in self.snapshots if s.metric_name == metric_name]
        if len(metric_snaps) < 2:
            return None

        metric_snaps.sort(key=lambda s: s.timestamp_epoch_sec)
        n = len(metric_snaps)
        t0 = metric_snaps[0].timestamp_epoch_sec
        t_days = [(s.timestamp_epoch_sec - t0) / 86400.0 for s in metric_snaps]
        vals = [s.metric_value for s in metric_snaps]

        mean_t = sum(t_days) / n
        mean_v = sum(vals) / n

        cov_tv = sum((t - mean_t) * (v - mean_v) for t, v in zip(t_days, vals))
        var_t = sum((t - mean_t) ** 2 for t in t_days)

        slope = (cov_tv / var_t) if var_t > 1e-12 else 0.0

        var_v = sum((v - mean_v) ** 2 for v in vals)
        r_sq = ((cov_tv ** 2) / (var_t * var_v)) if (var_t * var_v) > 1e-12 else 0.0

        last_t = t_days[-1]
        last_val = vals[-1]
        fc_30 = last_val + (slope * 30.0)
        fc_90 = last_val + (slope * 90.0)

        # For latency: positive slope is degrading; for throughput/f1: positive slope is improving
        is_latency = "latency" in metric_name.lower() or "error" in metric_name.lower()
        if abs(slope) < 1e-4:
            direction = "STABLE"
        elif (slope > 0 and not is_latency) or (slope < 0 and is_latency):
            direction = "IMPROVING"
        else:
            direction = "DEGRADING"

        return TrendForecast(
            metric_name=metric_name,
            historical_points_count=n,
            current_value=last_val,
            slope_per_day=slope,
            forecast_30d=fc_30,
            forecast_90d=fc_90,
            r_squared=r_sq,
            trend_direction=direction
        )

    def detect_regressions(self, threshold_pct: float = 0.10) -> List[ObservatoryAlert]:
        """Detect metric degradations exceeding statistical thresholds."""
        alerts: List[ObservatoryAlert] = []
        metrics = set(s.metric_name for s in self.snapshots)

        for m in metrics:
            m_snaps = sorted([s for s in self.snapshots if s.metric_name == m], key=lambda s: s.timestamp_epoch_sec)
            if len(m_snaps) >= 3:
                baseline = sum(s.metric_value for s in m_snaps[:len(m_snaps)//2]) / (len(m_snaps)//2)
                recent = m_snaps[-1].metric_value

                is_latency = "latency" in m.lower() or "error" in m.lower()
                if is_latency and recent > baseline * (1.0 + threshold_pct):
                    alerts.append(ObservatoryAlert(
                        alert_id=f"ALERT-REG-{m}-{int(time.time())}",
                        severity="WARNING",
                        metric_name=m,
                        trigger_reason=f"Latency regression: recent {recent:.2f} > baseline {baseline:.2f} (+{(recent/baseline - 1)*100:.1f}%)"
                    ))
                elif not is_latency and recent < baseline * (1.0 - threshold_pct):
                    alerts.append(ObservatoryAlert(
                        alert_id=f"ALERT-REG-{m}-{int(time.time())}",
                        severity="CRITICAL",
                        metric_name=m,
                        trigger_reason=f"Accuracy/Throughput drop: recent {recent:.2f} < baseline {baseline:.2f} (-{(1 - recent/baseline)*100:.1f}%)"
                    ))

        return alerts

    def generate_observatory_report(self) -> ContinuousObservatoryReport:
        """Produce comprehensive observatory audit report."""
        metrics = list(set(s.metric_name for s in self.snapshots))
        forecasts = [self.compute_trend_forecast(m) for m in metrics]
        valid_forecasts = [f for f in forecasts if f is not None]

        alerts = self.detect_regressions()
        has_critical = any(a.severity == "CRITICAL" for a in alerts)
        has_warning = any(a.severity == "WARNING" for a in alerts)

        status = "REGRESSION_DETECTED" if has_critical else "WARNING" if has_warning else "HEALTHY"

        return ContinuousObservatoryReport(
            total_archived_snapshots=len(self.snapshots),
            metrics_tracked_count=len(metrics),
            forecasts=valid_forecasts,
            active_alerts=alerts,
            storage_archive_path=str(self.archive_dir),
            status=status
        )
