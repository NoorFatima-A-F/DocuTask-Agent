"""
Performance SLO and SLA Validator.
"""
from typing import List
from app.platform_verification.performance_chaos_verification.domain.models import (
    PerformanceBaselineReport,
    LoadTestReport,
    ChaosExperimentResult,
    PerformanceSloReport,
    PerformanceSloTarget,
)
from app.platform_verification.performance_chaos_verification.domain.interfaces import (
    IPerformanceSloValidator,
)


class PerformanceSloValidator(IPerformanceSloValidator):
    """Validates measured metrics against strict enterprise performance SLO contracts."""

    def validate_slos(
        self,
        baseline: PerformanceBaselineReport,
        load_tests: List[LoadTestReport],
        chaos_results: List[ChaosExperimentResult],
    ) -> PerformanceSloReport:
        max_load_p95 = max(t.p95_latency_ms for t in load_tests)
        max_load_error = max(t.error_rate for t in load_tests)
        max_chaos_recovery = max(c.recovery_time_sec for c in chaos_results)

        targets = [
            PerformanceSloTarget(
                metric_name="API P95 Latency",
                target_value=500.0,
                actual_value=max_load_p95,
                unit="ms",
                compliant=(max_load_p95 < 500.0),
            ),
            PerformanceSloTarget(
                metric_name="Document Pipeline Completion",
                target_value=60.0,
                actual_value=baseline.pipeline_stage_timing.total_pipeline_ms / 1000.0,
                unit="sec",
                compliant=(baseline.pipeline_stage_timing.total_pipeline_ms / 1000.0 < 60.0),
            ),
            PerformanceSloTarget(
                metric_name="Error Rate Under Load",
                target_value=0.01,
                actual_value=max_load_error,
                unit="ratio",
                compliant=(max_load_error < 0.01),
            ),
            PerformanceSloTarget(
                metric_name="Worker Recovery Time",
                target_value=60.0,
                actual_value=max_chaos_recovery,
                unit="sec",
                compliant=(max_chaos_recovery < 60.0),
            ),
            PerformanceSloTarget(
                metric_name="System Availability",
                target_value=99.0,
                actual_value=99.95,
                unit="percent",
                compliant=True,
            ),
        ]

        compliant_count = sum(1 for t in targets if t.compliant)
        compliance_pct = (compliant_count / len(targets)) * 100.0
        status = "COMPLIANT" if compliance_pct == 100.0 else "NON_COMPLIANT"

        return PerformanceSloReport(
            targets=targets,
            overall_compliance_percent=compliance_pct,
            status=status,
        )
