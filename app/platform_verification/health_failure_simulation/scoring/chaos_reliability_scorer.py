"""
Phase 3H.11: 5-Pillar Chaos Reliability & Failure Simulation Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    ChaosCertificationTier,
    ChaosArchitectureReport,
    ScenarioRegistryReport,
    DatabaseFailureReport,
    QueueFailureReport,
    WorkerFailureReport,
    AIProviderFailureReport,
    ResourceFailureReport,
    FailureDetectionMetricsReport,
    RollbackValidationReport,
    ChaosSafetyReport,
    ChaosPillarScore,
    ChaosCertificationReport,
)
from ..domain.interfaces import IChaosReliabilityScorer


class ChaosReliabilityScorer(IChaosReliabilityScorer):
    """
    Evaluates 5 chaos reliability pillars:
      - Failure Detection Accuracy: 25%
      - Recovery Success: 25%
      - System Stability: 20%
      - Safety Controls: 15%
      - Evidence Quality: 15%
    """

    def calculate_certification_score(
        self,
        arch_report: ChaosArchitectureReport,
        registry_report: ScenarioRegistryReport,
        db_report: DatabaseFailureReport,
        queue_report: QueueFailureReport,
        worker_report: WorkerFailureReport,
        ai_report: AIProviderFailureReport,
        resource_report: ResourceFailureReport,
        detection_report: FailureDetectionMetricsReport,
        rollback_report: RollbackValidationReport,
        safety_report: ChaosSafetyReport,
    ) -> ChaosCertificationReport:
        # 1. Failure Detection Accuracy (25%)
        det_score = detection_report.detection_accuracy_pct
        det_weight = 25.0
        det_weighted = (det_score * det_weight) / 100.0

        # 2. Recovery Success (25%)
        rec_score = rollback_report.rollback_success_rate_pct
        rec_weight = 25.0
        rec_weighted = (rec_score * rec_weight) / 100.0

        # 3. System Stability (20%) - derived from absence of crashes and zero data corruption
        stability_checks = [
            db_report.api_gateway_alive and not db_report.data_corruption_detected,
            not queue_report.system_crashed and queue_report.graceful_degradation_active,
            worker_report.worker_pool_health == "HEALTHY",
            not ai_report.overall_platform_crashed and ai_report.ai_processing_degraded_gracefully,
            resource_report.host_oom_prevented and resource_report.disk_full_protection_active,
        ]
        stab_score = (sum(1 for c in stability_checks if c) / len(stability_checks)) * 100.0
        stab_weight = 20.0
        stab_weighted = (stab_score * stab_weight) / 100.0

        # 4. Safety Controls (15%)
        safety_checks = [
            safety_report.blast_radius_contained,
            safety_report.experiment_timeout_enforced,
            safety_report.auto_abort_triggers_verified,
            not safety_report.critical_data_loss_risk_detected,
            safety_report.environment_isolation_verified,
        ]
        safe_score = (sum(1 for c in safety_checks if c) / len(safety_checks)) * 100.0
        safe_weight = 15.0
        safe_weighted = (safe_score * safe_weight) / 100.0

        # 5. Evidence Quality (15%)
        ev_checks = [
            arch_report.architecture_valid,
            registry_report.registry_validated and len(registry_report.scenarios) >= 10,
            detection_report.metrics_compliant,
            rollback_report.final_health_status == "ALL_GREEN",
            safety_report.safety_audit_passed,
        ]
        ev_score = (sum(1 for c in ev_checks if c) / len(ev_checks)) * 100.0
        ev_weight = 15.0
        ev_weighted = (ev_score * ev_weight) / 100.0

        total_score = det_weighted + rec_weighted + stab_weighted + safe_weighted + ev_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[ChaosPillarScore] = [
            ChaosPillarScore(
                pillar_name="Failure Detection Accuracy",
                weight_pct=det_weight,
                achieved_score_pct=round(det_score, 2),
                weighted_score_pct=round(det_weighted, 2),
                status="PASSED" if det_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            ChaosPillarScore(
                pillar_name="Recovery Success & Self-Healing",
                weight_pct=rec_weight,
                achieved_score_pct=round(rec_score, 2),
                weighted_score_pct=round(rec_weighted, 2),
                status="PASSED" if rec_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            ChaosPillarScore(
                pillar_name="System Stability & Non-Crash Resilience",
                weight_pct=stab_weight,
                achieved_score_pct=round(stab_score, 2),
                weighted_score_pct=round(stab_weighted, 2),
                status="PASSED" if stab_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            ChaosPillarScore(
                pillar_name="Chaos Safety & Blast-Radius Controls",
                weight_pct=safe_weight,
                achieved_score_pct=round(safe_score, 2),
                weighted_score_pct=round(safe_weighted, 2),
                status="PASSED" if safe_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            ChaosPillarScore(
                pillar_name="Evidence Completeness & Audit Integrity",
                weight_pct=ev_weight,
                achieved_score_pct=round(ev_score, 2),
                weighted_score_pct=round(ev_weighted, 2),
                status="PASSED" if ev_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = ChaosCertificationTier.CHAOS_VERIFIED_RELIABLE
            granted = True
        elif total_score >= 90.0:
            tier = ChaosCertificationTier.PRODUCTION_RELIABILITY_READY
            granted = True
        elif total_score >= 80.0:
            tier = ChaosCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = ChaosCertificationTier.FAILED
            granted = False

        return ChaosCertificationReport(
            report_title="Phase 3H.11 Enterprise Health Failure Simulation & Chaos Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Chaos Engineering & Reliability Certification Engine"
        )
