"""
Platform Reliability, Availability, MTBF, and MTTR Evaluator.
"""

from app.performance_verification.domain.models import ReliabilityMetric


class PlatformReliabilityEvaluator:
    """Calculates enterprise reliability metrics from production execution telemetry."""

    @staticmethod
    def evaluate_reliability(
        total_requests: int = 50000,
        failed_requests: int = 2,
        unplanned_downtime_sec: float = 3.15,
        total_window_sec: float = 2592000.0,  # 30 days
        incident_count: int = 1,
    ) -> ReliabilityMetric:
        availability_pct = ((total_window_sec - unplanned_downtime_sec) / total_window_sec) * 100.0
        error_rate_pct = (failed_requests / total_requests) * 100.0 if total_requests > 0 else 0.0

        # MTBF in hours = total operational hours / failures
        total_hours = total_window_sec / 3600.0
        mtbf_hours = total_hours / max(1, incident_count)

        # MTTR in milliseconds = (downtime in ms) / incidents
        mttr_ms = (unplanned_downtime_sec * 1000.0) / max(1, incident_count)

        target_avail = 99.90
        sla_met = availability_pct >= target_avail and error_rate_pct < 0.10

        return ReliabilityMetric(
            availability_pct=availability_pct,
            mtbf_hours=mtbf_hours,
            mttr_ms=mttr_ms,
            error_rate_pct=error_rate_pct,
            total_requests_evaluated=total_requests,
            sla_availability_target_pct=target_avail,
            sla_met=sla_met,
        )
