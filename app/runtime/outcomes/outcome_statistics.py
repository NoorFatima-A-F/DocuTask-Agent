"""
Outcome Verification Engine - Outcome Statistics
Maintains sliding-window aggregations and accuracy trends across observed executions.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from app.runtime.outcomes.outcome_collector import MissionOutcomeRecord


@dataclass
class WindowStatisticsSummary:
    total_samples: int
    sla_compliance_rate: float
    success_rate: float
    mean_accuracy_error: float
    mean_latency_error_ms: float
    mean_cost_error_usd: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class OutcomeStatisticsTracker:
    """Tracks running statistics on predicted vs observed accuracy across all missions."""

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self._records: List[MissionOutcomeRecord] = []

    def record_outcome(self, record: MissionOutcomeRecord) -> None:
        self._records.append(record)
        if len(self._records) > self.max_history:
            self._records.pop(0)

    def compute_window_statistics(self, records: Optional[List[MissionOutcomeRecord]] = None) -> WindowStatisticsSummary:
        target = records if records is not None else self._records
        n = len(target)
        if n == 0:
            return WindowStatisticsSummary(
                total_samples=0,
                sla_compliance_rate=1.0,
                success_rate=1.0,
                mean_accuracy_error=0.0,
                mean_latency_error_ms=0.0,
                mean_cost_error_usd=0.0,
            )

        sla_ok = sum(1 for r in target if r.is_sla_compliant)
        succ_ok = sum(1 for r in target if r.is_success)

        acc_errs = [abs(r.accuracy_residual) for r in target]
        lat_errs = [abs(r.latency_residual) for r in target]
        cost_errs = [abs(r.predicted_cost_usd - r.observed_cost_usd) for r in target]

        return WindowStatisticsSummary(
            total_samples=n,
            sla_compliance_rate=round(sla_ok / n, 4),
            success_rate=round(succ_ok / n, 4),
            mean_accuracy_error=round(sum(acc_errs) / n, 4),
            mean_latency_error_ms=round(sum(lat_errs) / n, 2),
            mean_cost_error_usd=round(sum(cost_errs) / n, 5),
        )

    def get_aggregate_summary(self) -> Dict[str, Any]:
        n = len(self._records)
        if n == 0:
            return {
                "total_verified_missions": 0,
                "overall_sla_compliance_rate": 1.0,
                "overall_success_rate": 1.0,
                "mean_absolute_errors": {},
            }

        sla_ok = sum(1 for r in self._records if r.is_sla_compliant)
        succ_ok = sum(1 for r in self._records if r.is_success)

        dims = ["latency_ms", "cost_usd", "accuracy", "ocr_confidence", "expected_utility"]
        mae_by_dim = {}
        for dim in dims:
            errors = [r.dimension_pairs[dim].absolute_error for r in self._records if dim in r.dimension_pairs]
            if errors:
                mae_by_dim[dim] = round(sum(errors) / len(errors), 4)

        return {
            "total_verified_missions": n,
            "overall_sla_compliance_rate": round(sla_ok / n, 4),
            "overall_success_rate": round(succ_ok / n, 4),
            "mean_absolute_errors": mae_by_dim,
            "recent_records": [r.to_dict() for r in reversed(self._records[-10:])],
        }


outcome_statistics_tracker = OutcomeStatisticsTracker()
