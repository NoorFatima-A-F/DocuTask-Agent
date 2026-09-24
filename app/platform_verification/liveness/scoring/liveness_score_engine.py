"""
Liveness Quality Score Engine (Part 16).
Computes weighted composite quality scorecards across the 6 core liveness categories:
1. Runtime detection accuracy: 25%
2. Event loop monitoring: 20%
3. Deadlock detection: 15%
4. Resource monitoring: 15%
5. Recovery integration: 15%
6. Security: 10%
Certification Tiers:
- 95-100: Enterprise Liveness Ready
- 90-94: Production Ready
- 80-89: Needs Improvement
- <80: Failed
"""
from app.platform_verification.liveness.domain.models import (
    LivenessContractReport,
    ProcessStateReport,
    EventLoopHealthReport,
    DeadlockReport,
    WorkerLivenessReport,
    SchedulerLivenessReport,
    ResourceHealthReport,
    FailureSimulationReport,
    RecoveryReport,
    SecurityReport,
    LivenessScorecard,
    LivenessTier,
)


class LivenessScoreEngine:
    """
    Evaluates enterprise liveness subsystems against the 6-category weighted scoring formula.
    """

    def compute_scorecard(
        self,
        contract_report: LivenessContractReport,
        process_report: ProcessStateReport,
        loop_report: EventLoopHealthReport,
        deadlock_report: DeadlockReport,
        worker_report: WorkerLivenessReport,
        scheduler_report: SchedulerLivenessReport,
        resource_report: ResourceHealthReport,
        failure_report: FailureSimulationReport,
        recovery_report: RecoveryReport,
        security_report: SecurityReport,
    ) -> LivenessScorecard:
        # 1. Runtime detection accuracy (25%)
        # Contract validity (50pts) + Process existence & state monitoring (50pts)
        runtime_score = 0.0
        if contract_report.passed and contract_report.isolated_from_dependencies:
            runtime_score += 50.0
        if process_report.all_processes_alive:
            runtime_score += 50.0

        # 2. Event loop monitoring (20%)
        # Loop healthy (50pts) + Latency < threshold (50pts)
        loop_score = 0.0
        if loop_report.loop_healthy:
            loop_score += 50.0
        if loop_report.maximum_latency_ms < loop_report.failure_threshold_ms:
            loop_score += 50.0

        # 3. Deadlock detection (15%)
        # Watchdog active (50pts) + Zero deadlocks detected / restart signal on freeze (50pts)
        deadlock_score = 0.0
        if deadlock_report.watchdog_active:
            deadlock_score += 50.0
        if deadlock_report.passed:
            deadlock_score += 50.0

        # 4. Resource monitoring (15%)
        # Memory state normal/warning (50pts) + CPU not throttled (50pts)
        resource_score = 0.0
        if resource_report.memory_state in ["NORMAL", "WARNING"]:
            resource_score += 50.0
        if not resource_report.cpu_throttled:
            resource_score += 50.0

        # 5. Recovery integration (15%)
        # MTTR < 30s (50pts) + All failure simulations passed (50pts)
        recovery_score = 0.0
        if recovery_report.passed and recovery_report.mttr_seconds < 30.0:
            recovery_score += 50.0
        if failure_report.passed:
            recovery_score += 50.0

        # 6. Security (10%)
        # Zero info leaks (50pts) + Auth & rate limiting (50pts)
        security_score = 0.0
        if security_report.public_endpoint_leak_free and security_report.credentials_leaked_count == 0:
            security_score += 50.0
        if security_report.auth_policy_enforced and security_report.rate_limiting_active:
            security_score += 50.0

        # Weighted composite score
        overall = (
            (runtime_score * 0.25)
            + (loop_score * 0.20)
            + (deadlock_score * 0.15)
            + (resource_score * 0.15)
            + (recovery_score * 0.15)
            + (security_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = LivenessTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = LivenessTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = LivenessTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = LivenessTier.FAILED
            verdict = "REJECTED"
            passed = False

        return LivenessScorecard(
            runtime_detection_accuracy_score=round(runtime_score, 2),
            event_loop_monitoring_score=round(loop_score, 2),
            deadlock_detection_score=round(deadlock_score, 2),
            resource_monitoring_score=round(resource_score, 2),
            recovery_integration_score=round(recovery_score, 2),
            security_score=round(security_score, 2),
            overall_liveness_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            auto_recovery_validated=recovery_report.passed,
            passed=passed,
            details={
                "weights": {
                    "runtime_detection_accuracy": 0.25,
                    "event_loop_monitoring": 0.20,
                    "deadlock_detection": 0.15,
                    "resource_monitoring": 0.15,
                    "recovery_integration": 0.15,
                    "security": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
