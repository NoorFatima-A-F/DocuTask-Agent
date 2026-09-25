"""
Phase 3H.4.9.11: Recovery Quality Scorer
"""
from typing import Dict, Any
from ..domain.interfaces import IRecoveryScorer
from ..domain.models import (
    RecoveryScorecard,
    RecoveryTier,
    RecoveryMetricsReport,
    DataIntegrityReport,
    RecoverySafetyReport,
    HealthValidationReport,
    PostIncidentImprovementReport,
)


class RecoveryScorer(IRecoveryScorer):
    def calculate_scorecard(
        self,
        automation_result: Dict[str, Any],
        metrics_report: RecoveryMetricsReport,
        integrity_report: DataIntegrityReport,
        safety_report: RecoverySafetyReport,
        validation_report: HealthValidationReport,
        improvement_report: PostIncidentImprovementReport,
    ) -> RecoveryScorecard:
        # 1. Recovery success rate (20%)
        success_rate = metrics_report.recovery_success_rate
        success_score = min(100.0, max(0.0, success_rate))

        # 2. Recovery speed (20%)
        # Target MTTR < 60s -> 100%, 60-120s -> 80%, >120s -> 50%
        if metrics_report.mttr_seconds <= 30.0:
            speed_score = 100.0
        elif metrics_report.mttr_seconds <= 60.0:
            speed_score = 95.0
        elif metrics_report.mttr_seconds <= 120.0:
            speed_score = 80.0
        else:
            speed_score = 50.0

        # 3. Data integrity (20%)
        if integrity_report.checksum_match and integrity_report.database_transactions_consistent and integrity_report.queue_jobs_lost == 0:
            integrity_score = 100.0
        else:
            integrity_score = 0.0

        # 4. Automation safety (15%)
        if safety_report.overall_safety_passed and safety_report.max_retries_enforced:
            safety_score = 100.0
        else:
            safety_score = 50.0

        # 5. Validation quality (15%)
        if validation_report.overall_health_validated and validation_report.functional_test.all_passed:
            val_score = 100.0
        else:
            val_score = 50.0

        # 6. Improvement process (10%)
        if len(improvement_report.preventive_actions) >= 2 and len(improvement_report.lessons_learned) >= 1:
            imp_score = 100.0
        else:
            imp_score = 70.0

        # Composite score calculation
        composite = (
            (success_score * 0.20)
            + (speed_score * 0.20)
            + (integrity_score * 0.20)
            + (safety_score * 0.15)
            + (val_score * 0.15)
            + (imp_score * 0.10)
        )

        if composite >= 95.0:
            tier = RecoveryTier.ENTERPRISE_RECOVERY_READY
            certified = True
        elif composite >= 90.0:
            tier = RecoveryTier.PRODUCTION_RECOVERY_READY
            certified = True
        elif composite >= 80.0:
            tier = RecoveryTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = RecoveryTier.FAILED
            certified = False

        return RecoveryScorecard(
            recovery_success_rate_score=round(success_score, 2),
            recovery_speed_score=round(speed_score, 2),
            data_integrity_score=round(integrity_score, 2),
            automation_safety_score=round(safety_score, 2),
            validation_quality_score=round(val_score, 2),
            improvement_process_score=round(imp_score, 2),
            composite_score=round(composite, 2),
            tier=tier,
            certified_enterprise_ready=certified,
        )
