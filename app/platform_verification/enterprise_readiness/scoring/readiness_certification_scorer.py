"""Automated Readiness Certification Scorer (3H.3.11).

Calculates a 6-dimension weighted quality score:
1. Dependency Detection Accuracy (Weight 25%)
2. Traffic Safety (Weight 20%)
3. Startup Correctness (Weight 15%)
4. Failure Handling (Weight 15%)
5. Recovery Validation (Weight 15%)
6. Observability (Weight 10%)
"""

from ..domain.models import (
    ReadinessCertificationScorecard,
    ReadinessCertificationTier,
    ReadinessContractReport,
    DependencyReadinessReport,
    DatabaseReadinessReport,
    QueueReadinessReport,
    WorkerReadinessReport,
    AIProviderReadinessReport,
    StartupReadinessReport,
    FailureSimulationReport,
    OrchestrationReport,
    ReadinessMetricsReport,
)
from ..domain.interfaces import IReadinessCertificationScorer


class ReadinessCertificationScorer(IReadinessCertificationScorer):
    """Calculates weighted readiness certification score."""

    def score_readiness(
        self,
        contract_rep: ReadinessContractReport,
        dep_rep: DependencyReadinessReport,
        db_rep: DatabaseReadinessReport,
        queue_rep: QueueReadinessReport,
        worker_rep: WorkerReadinessReport,
        ai_rep: AIProviderReadinessReport,
        startup_rep: StartupReadinessReport,
        sim_rep: FailureSimulationReport,
        orch_rep: OrchestrationReport,
        obs_rep: ReadinessMetricsReport,
    ) -> ReadinessCertificationScorecard:
        # 1. Dependency Detection Accuracy (25%)
        dep_score = 100.0
        if not dep_rep.critical_dependencies_healthy:
            dep_score -= 30.0
        if db_rep.status != "READY":
            dep_score -= 20.0
        if queue_rep.status != "READY":
            dep_score -= 20.0
        if worker_rep.status != "READY":
            dep_score -= 20.0

        # 2. Traffic Safety (20%)
        # Pre-init blocked, contract zero leaks, orchestrator traffic removed on failure
        traffic_score = 100.0
        if not startup_rep.pre_initialization_traffic_blocked:
            traffic_score -= 40.0
        if not contract_rep.zero_sensitive_leak:
            traffic_score -= 30.0
        if not orch_rep.traffic_removed_on_failure:
            traffic_score -= 30.0

        # 3. Startup Correctness (15%)
        # 7-step sequence successful, TTR <= 5.0s
        startup_score = 100.0
        if not startup_rep.all_steps_successful:
            startup_score -= 40.0
        if startup_rep.time_to_ready_seconds > startup_rep.ttr_threshold_seconds:
            startup_score -= 20.0

        # 4. Failure Handling (15%)
        # Simulated failures detected without crashes, false positives = 0%
        fail_score = 100.0
        if sim_rep.passed_simulations < sim_rep.total_simulations:
            fail_score -= (sim_rep.total_simulations - sim_rep.passed_simulations) * 25.0
        if sim_rep.false_positive_rate_pct > 0.0:
            fail_score -= 20.0

        # 5. Recovery Validation (15%)
        # Recovery time <= 3.0s, traffic restored after recovery
        rec_score = 100.0
        if sim_rep.mean_recovery_time_seconds > 3.0:
            rec_score -= 20.0
        if not orch_rep.traffic_restored_on_recovery:
            rec_score -= 30.0

        # 6. Observability (10%)
        # Prometheus metrics exposed, Grafana dashboards ready
        obs_score = 100.0
        if obs_rep.metrics_count < 6:
            obs_score -= 25.0
        if not obs_rep.service_readiness_dashboard_ready or not obs_rep.dependency_dashboard_ready:
            obs_score -= 25.0

        # Clamp individual scores [0.0, 100.0]
        dep_score = max(0.0, min(100.0, dep_score))
        traffic_score = max(0.0, min(100.0, traffic_score))
        startup_score = max(0.0, min(100.0, startup_score))
        fail_score = max(0.0, min(100.0, fail_score))
        rec_score = max(0.0, min(100.0, rec_score))
        obs_score = max(0.0, min(100.0, obs_score))

        # Weighted calculation
        overall = (
            dep_score * 0.25
            + traffic_score * 0.20
            + startup_score * 0.15
            + fail_score * 0.15
            + rec_score * 0.15
            + obs_score * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = ReadinessCertificationTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = ReadinessCertificationTier.PRODUCTION_READY
            verdict = "PROVISIONALLY_CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = ReadinessCertificationTier.NEEDS_IMPROVEMENT
            verdict = "ACTION_REQUIRED"
            passed = False
        else:
            tier = ReadinessCertificationTier.FAILED
            verdict = "FAILED"
            passed = False

        return ReadinessCertificationScorecard(
            dependency_detection_score=dep_score,
            traffic_safety_score=traffic_score,
            startup_correctness_score=startup_score,
            failure_handling_score=fail_score,
            recovery_validation_score=rec_score,
            observability_score=obs_score,
            overall_readiness_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
        )
