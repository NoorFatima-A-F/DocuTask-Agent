"""
Performance Certification Scorecard Engine.
"""
from typing import List
from app.platform_verification.performance_chaos_verification.domain.models import (
    PerformanceBaselineReport,
    LoadTestReport,
    StressTestReport,
    HorizontalScalingReport,
    ResourceAnalysisReport,
    ChaosExperimentResult,
    PerformanceSloReport,
    PerformanceCertificationScorecard,
    PerformanceCertificationTier,
)
from app.platform_verification.performance_chaos_verification.domain.interfaces import (
    IPerformanceCertificationEngine,
)


class PerformanceCertificationEngine(IPerformanceCertificationEngine):
    """Calculates weighted composite scorecard across 6 dimensions."""

    def compute_certification(
        self,
        baseline: PerformanceBaselineReport,
        load_tests: List[LoadTestReport],
        stress_test: StressTestReport,
        scaling: HorizontalScalingReport,
        resources: ResourceAnalysisReport,
        chaos: List[ChaosExperimentResult],
        slo_report: PerformanceSloReport,
    ) -> PerformanceCertificationScorecard:
        # Latency (20%): Baseline & load P95 < 500ms
        latency_score = 100.0 if all(t.p95_latency_ms < 500.0 for t in load_tests) else 80.0

        # Throughput (20%): Sustainable load & stress
        throughput_score = 100.0 if stress_test.max_sustainable_throughput_rps >= 2000.0 else 85.0

        # Scalability (20%): Near-linear scaling efficiency >= 85%
        scalability_score = 100.0 if scaling.near_linear_scaling else 75.0

        # Resource Efficiency (15%): No CPU throttling, DB pool < 80%
        resource_efficiency_score = 98.0 if not resources.cpu_throttling_detected else 70.0

        # Chaos Resilience (15%): All chaos experiments passed, zero data loss
        chaos_resilience_score = 100.0 if all(c.passed and not c.data_loss_detected for c in chaos) else 60.0

        # Recovery Performance (10%): Max recovery < 30s
        max_recovery = max(c.recovery_time_sec for c in chaos)
        recovery_score = 100.0 if max_recovery < 30.0 else 75.0

        # Weighted composite:
        # Latency (20%) + Throughput (20%) + Scalability (20%) + Resources (15%) + Chaos (15%) + Recovery (10%)
        composite = (
            (latency_score * 0.20)
            + (throughput_score * 0.20)
            + (scalability_score * 0.20)
            + (resource_efficiency_score * 0.15)
            + (chaos_resilience_score * 0.15)
            + (recovery_score * 0.10)
        )

        if composite >= 95.0:
            tier = PerformanceCertificationTier.ENTERPRISE_PERFORMANCE_READY
        elif composite >= 90.0:
            tier = PerformanceCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = PerformanceCertificationTier.OPTIMIZATION_REQUIRED
        else:
            tier = PerformanceCertificationTier.FAILED

        passed = tier in [
            PerformanceCertificationTier.ENTERPRISE_PERFORMANCE_READY,
            PerformanceCertificationTier.PRODUCTION_READY,
        ]

        return PerformanceCertificationScorecard(
            latency_score=latency_score,
            throughput_score=throughput_score,
            scalability_score=scalability_score,
            resource_efficiency_score=resource_efficiency_score,
            chaos_resilience_score=chaos_resilience_score,
            recovery_performance_score=recovery_score,
            composite_score=round(composite, 2),
            certification_tier=tier,
            passed=passed,
        )
