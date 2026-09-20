"""Time-series aggregation, window comparison, and trend detection."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from .metrics import MetricValue, MetricTrend, MetricPeriod
from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter, TimeBucketSummary


class TimeSeriesAggregator:
    """Aggregates metrics across time windows and computes trend deltas."""

    @staticmethod
    def get_time_bounds(period: MetricPeriod, now: Optional[datetime] = None) -> tuple[datetime, datetime]:
        current = now or datetime.now(timezone.utc)
        if period == MetricPeriod.LAST_HOUR:
            return current - timedelta(hours=1), current
        elif period == MetricPeriod.LAST_24_HOURS:
            return current - timedelta(days=1), current
        elif period == MetricPeriod.LAST_7_DAYS:
            return current - timedelta(days=7), current
        elif period == MetricPeriod.LAST_30_DAYS:
            return current - timedelta(days=30), current
        elif period == MetricPeriod.LAST_90_DAYS:
            return current - timedelta(days=90), current
        return current - timedelta(days=30), current

    @staticmethod
    def compare_periods(
        current_val: float, previous_val: float, is_lower_better: bool = False
    ) -> tuple[float, MetricTrend]:
        if previous_val == 0.0:
            change_pct = 0.0
        else:
            change_pct = ((current_val - previous_val) / previous_val) * 100.0

        if abs(change_pct) < 1.0:
            trend = MetricTrend.STABLE
        elif change_pct > 25.0 and is_lower_better:
            trend = MetricTrend.CRITICAL_SPIKE
        elif (change_pct > 0 and not is_lower_better) or (change_pct < 0 and is_lower_better):
            trend = MetricTrend.IMPROVING
        else:
            trend = MetricTrend.DEGRADING

        return round(change_pct, 2), trend
