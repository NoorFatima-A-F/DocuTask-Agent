"""
Readiness Quality Scorer (Part 3H.3.2.14).
Evaluates the 6 core dimensions of readiness verification and computes weighted scorecard:
1. Dependency Detection: 25%
2. Failure Accuracy: 20%
3. Policy Correctness: 20%
4. Kubernetes Compatibility: 15%
5. Security: 10%
6. Observability: 10%
"""
from typing import Dict, Any
from app.platform_verification.readiness_engine.domain.models import (
    DatabaseReadinessReport,
    QueueReadinessReport,
    StorageReadinessReport,
    AIProviderReadinessReport,
    WorkerReadinessReport,
    DependencyMatrixReport,
    ReadinessEvaluationResult,
    FailureSimulationReport,
    KubernetesCompatibilityReport,
    ReadinessSecurityReport,
    ReadinessScorecard,
    ReadinessTier,
)


class ReadinessQualityScorer:
    """
    Computes weighted composite readiness quality scorecard.
    """

    def compute_scorecard(
        self,
        db_report: DatabaseReadinessReport,
        queue_report: QueueReadinessReport,
        storage_report: StorageReadinessReport,
        ai_report: AIProviderReadinessReport,
        worker_report: WorkerReadinessReport,
        matrix_report: DependencyMatrixReport,
        eval_result: ReadinessEvaluationResult,
        sim_report: FailureSimulationReport,
        k8s_report: KubernetesCompatibilityReport,
        sec_report: ReadinessSecurityReport,
        observability_valid: bool = True,
    ) -> ReadinessScorecard:
        # 1. Dependency Detection (25%)
        # Checks: DB transaction & pool, Redis queue pressure, Storage lifecycle, AI quota, Worker status
        dep_points = 0.0
        if db_report.transaction_supported and db_report.schema_compatible:
            dep_points += 20.0
        if queue_report.ping_pong_ok and queue_report.queue_state_readable:
            dep_points += 20.0
        if storage_report.integrity_verified and storage_report.cleanup_verified:
            dep_points += 20.0
        if ai_report.authenticated and ai_report.response_valid:
            dep_points += 20.0
        if worker_report.registered and worker_report.can_process_tasks:
            dep_points += 20.0
        dep_score = min(100.0, dep_points)

        # 2. Failure Accuracy (20%)
        # All 4 failure simulation scenarios executed and accurately classified
        if sim_report.total_scenarios >= 4 and sim_report.all_scenarios_passed:
            fail_score = 100.0
        else:
            fail_score = (sim_report.passed_scenarios / max(1, sim_report.total_scenarios)) * 100.0

        # 3. Policy Correctness (20%)
        # Declarative policy classification: critical, important, optional, traffic actions mapped
        pol_points = 0.0
        if matrix_report.critical_dependencies_count >= 3:
            pol_points += 40.0
        if matrix_report.important_dependencies_count >= 1:
            pol_points += 30.0
        if matrix_report.passed and eval_result.service == "docutask-api":
            pol_points += 30.0
        policy_score = min(100.0, pol_points)

        # 4. Kubernetes Compatibility (15%)
        # Fast response (<100ms), deterministic code, no side effects
        k8s_points = 0.0
        if k8s_report.readiness_probe_path == "/ready" and k8s_report.fast_response:
            k8s_points += 50.0
        if k8s_report.deterministic_response and k8s_report.no_side_effects and k8s_report.passed:
            k8s_points += 50.0
        k8s_score = min(100.0, k8s_points)

        # 5. Security (10%)
        sec_score = 100.0 if sec_report.passed and sec_report.total_leaks_detected == 0 else 0.0

        # 6. Observability (10%)
        obs_score = 100.0 if observability_valid else 0.0

        # Compute weighted overall score
        overall = (
            (dep_score * 0.25)
            + (fail_score * 0.20)
            + (policy_score * 0.20)
            + (k8s_score * 0.15)
            + (sec_score * 0.10)
            + (obs_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = ReadinessTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = ReadinessTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = ReadinessTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = ReadinessTier.FAILED
            verdict = "REJECTED"
            passed = False

        return ReadinessScorecard(
            dependency_detection_score=round(dep_score, 2),
            failure_accuracy_score=round(fail_score, 2),
            policy_correctness_score=round(policy_score, 2),
            kubernetes_compatibility_score=round(k8s_score, 2),
            security_score=round(sec_score, 2),
            observability_score=round(obs_score, 2),
            overall_readiness_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            traffic_admission_safe=eval_result.traffic_allowed,
            passed=passed,
            details={
                "weights": {
                    "dependency_detection": 0.25,
                    "failure_accuracy": 0.20,
                    "policy_correctness": 0.20,
                    "kubernetes_compatibility": 0.15,
                    "security": 0.10,
                    "observability": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
