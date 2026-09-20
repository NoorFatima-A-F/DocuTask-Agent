"""
Phase 3H.12: 6-Pillar Automated Recovery Quality & Self-Healing Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    RecoveryCertificationTier,
    RecoveryArchitectureReport,
    RecoveryPolicyReport,
    ServiceRestartReport,
    DatabaseRecoveryReport,
    QueueRecoveryReport,
    WorkerRecoveryReport,
    AIRecoveryReport,
    CircuitBreakerReport,
    RecoveryValidationReport,
    ReliabilityMetricsReport,
    RecoverySafetyReport,
    RecoveryAuditReport,
    RecoveryPillarScore,
    RecoveryCertificationReport,
)
from ..domain.interfaces import IAutomatedRecoveryScorer


class AutomatedRecoveryScorer(IAutomatedRecoveryScorer):
    """
    Evaluates 6 automated recovery pillars:
      - Recovery Accuracy: 25%
      - Automation Reliability: 20%
      - Safety Controls: 20%
      - Recovery Speed: 15%
      - Validation Quality: 10%
      - Audit Evidence: 10%
    """

    def calculate_certification_score(
        self,
        arch_report: RecoveryArchitectureReport,
        policy_report: RecoveryPolicyReport,
        restart_report: ServiceRestartReport,
        db_report: DatabaseRecoveryReport,
        queue_report: QueueRecoveryReport,
        worker_report: WorkerRecoveryReport,
        ai_report: AIRecoveryReport,
        circuit_report: CircuitBreakerReport,
        validation_report: RecoveryValidationReport,
        metrics_report: ReliabilityMetricsReport,
        safety_report: RecoverySafetyReport,
        audit_report: RecoveryAuditReport,
    ) -> RecoveryCertificationReport:
        # 1. Recovery Accuracy (25%)
        accuracy_checks = [
            restart_report.restart_verification_passed,
            db_report.database_recovery_passed and not db_report.corrupted_state_detected,
            queue_report.queue_recovery_passed and queue_report.duplicate_jobs_count == 0,
            worker_report.worker_self_healing_passed and worker_report.concurrency_capacity_restored,
            ai_report.ai_recovery_passed and ai_report.document_extraction_continued,
        ]
        acc_score = (sum(1 for c in accuracy_checks if c) / len(accuracy_checks)) * 100.0
        acc_weight = 25.0
        acc_weighted = (acc_score * acc_weight) / 100.0

        # 2. Automation Reliability (20%)
        automation_checks = [
            arch_report.architecture_valid,
            policy_report.policy_engine_active and len(policy_report.policies) >= 5,
            circuit_report.circuit_breaker_passed and circuit_report.cascading_failures_prevented,
            restart_report.restart_triggered_automatically,
        ]
        auto_score = (sum(1 for c in automation_checks if c) / len(automation_checks)) * 100.0
        auto_weight = 20.0
        auto_weighted = (auto_score * auto_weight) / 100.0

        # 3. Safety Controls (20%)
        safety_checks = [
            safety_report.safety_guardrails_passed,
            safety_report.runaway_restarts_prevented,
            safety_report.rollback_on_persistent_failure_enabled,
            safety_report.duplicate_processing_prevented,
            safety_report.zero_data_corruption_guarantee,
        ]
        safe_score = (sum(1 for c in safety_checks if c) / len(safety_checks)) * 100.0
        safe_weight = 20.0
        safe_weighted = (safe_score * safe_weight) / 100.0

        # 4. Recovery Speed (15%) - MTTR compliance and sub-5s component restarts
        speed_checks = [
            metrics_report.mttr_compliant_with_sla,
            metrics_report.mean_time_to_recover_seconds <= 60.0,
            restart_report.restart_duration_seconds <= 5.0,
            db_report.recovery_duration_seconds <= 5.0,
            queue_report.queue_recovery_duration_seconds <= 5.0,
        ]
        spd_score = (sum(1 for c in speed_checks if c) / len(speed_checks)) * 100.0
        spd_weight = 15.0
        spd_weighted = (spd_score * spd_weight) / 100.0

        # 5. Validation Quality (10%)
        val_checks = [
            validation_report.synthetic_test_executed,
            validation_report.overall_pipeline_passed,
            validation_report.all_dependencies_operational,
            len(validation_report.pipeline_steps) >= 5,
        ]
        val_score = (sum(1 for c in val_checks if c) / len(val_checks)) * 100.0
        val_weight = 10.0
        val_weighted = (val_score * val_weight) / 100.0

        # 6. Audit Evidence (10%)
        aud_checks = [
            audit_report.immutable_log_verified,
            len(audit_report.audit_events) >= 5,
            all(e.result == "SUCCESS" for e in audit_report.audit_events),
        ]
        aud_score = (sum(1 for c in aud_checks if c) / len(aud_checks)) * 100.0
        aud_weight = 10.0
        aud_weighted = (aud_score * aud_weight) / 100.0

        total_score = acc_weighted + auto_weighted + safe_weighted + spd_weighted + val_weighted + aud_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[RecoveryPillarScore] = [
            RecoveryPillarScore(
                pillar_name="Recovery Accuracy & State Safety",
                weight_pct=acc_weight,
                achieved_score_pct=round(acc_score, 2),
                weighted_score_pct=round(acc_weighted, 2),
                status="PASSED" if acc_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            RecoveryPillarScore(
                pillar_name="Automation Reliability & Policy Execution",
                weight_pct=auto_weight,
                achieved_score_pct=round(auto_score, 2),
                weighted_score_pct=round(auto_weighted, 2),
                status="PASSED" if auto_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            RecoveryPillarScore(
                pillar_name="Safety Controls & Non-Destructive Guards",
                weight_pct=safe_weight,
                achieved_score_pct=round(safe_score, 2),
                weighted_score_pct=round(safe_weighted, 2),
                status="PASSED" if safe_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            RecoveryPillarScore(
                pillar_name="Recovery Speed & MTTR SLA Conformance",
                weight_pct=spd_weight,
                achieved_score_pct=round(spd_score, 2),
                weighted_score_pct=round(spd_weighted, 2),
                status="PASSED" if spd_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            RecoveryPillarScore(
                pillar_name="Validation Quality & Synthetic E2E Proof",
                weight_pct=val_weight,
                achieved_score_pct=round(val_score, 2),
                weighted_score_pct=round(val_weighted, 2),
                status="PASSED" if val_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            RecoveryPillarScore(
                pillar_name="Audit Trail & Immutable Logging Integrity",
                weight_pct=aud_weight,
                achieved_score_pct=round(aud_score, 2),
                weighted_score_pct=round(aud_weighted, 2),
                status="PASSED" if aud_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = RecoveryCertificationTier.AUTONOMOUS_RECOVERY_READY
            granted = True
        elif total_score >= 90.0:
            tier = RecoveryCertificationTier.PRODUCTION_RECOVERY_READY
            granted = True
        elif total_score >= 80.0:
            tier = RecoveryCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = RecoveryCertificationTier.FAILED
            granted = False

        return RecoveryCertificationReport(
            report_title="Phase 3H.12 Enterprise Automated Recovery & Self-Healing Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Autonomous Recovery & SRE Certification Engine"
        )
