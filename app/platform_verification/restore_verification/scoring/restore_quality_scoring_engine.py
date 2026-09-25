"""
Restore Quality Scoring Engine for Automated Restore Verification System (Part 3G.2E).
"""

from app.platform_verification.restore_verification.domain.models import (
    RestoreCertificationTier,
    RestoreQualityScorecard,
)
from app.platform_verification.restore_verification.domain.interfaces import (
    IRestoreQualityScoringEngine,
)


class RestoreQualityScoringEngine(IRestoreQualityScoringEngine):
    """
    Computes weighted multi-criteria Disaster Recovery Quality Scorecard
    and determines enterprise disaster recovery certification tier.
    """

    WEIGHTS = {
        "backup_recovery_success": 0.25,
        "data_integrity": 0.20,
        "service_recovery": 0.20,
        "functional_validation": 0.15,
        "security_validation": 0.10,
        "recovery_speed": 0.10,
    }

    def compute_quality_scorecard(
        self,
        backup_recovery_success_score: float,
        data_integrity_score: float,
        service_recovery_score: float,
        functional_validation_score: float,
        security_validation_score: float,
        recovery_speed_score: float,
        execution_duration_ms: float,
    ) -> RestoreQualityScorecard:
        """
        Calculates composite disaster recovery readiness score.
        """
        composite = (
            backup_recovery_success_score * self.WEIGHTS["backup_recovery_success"]
            + data_integrity_score * self.WEIGHTS["data_integrity"]
            + service_recovery_score * self.WEIGHTS["service_recovery"]
            + functional_validation_score * self.WEIGHTS["functional_validation"]
            + security_validation_score * self.WEIGHTS["security_validation"]
            + recovery_speed_score * self.WEIGHTS["recovery_speed"]
        )
        composite = round(composite, 2)

        if composite >= 95.0:
            tier = RestoreCertificationTier.DISASTER_RECOVERY_CERTIFIED
        elif composite >= 90.0:
            tier = RestoreCertificationTier.RECOVERY_READY
        elif composite >= 80.0:
            tier = RestoreCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = RestoreCertificationTier.FAILED

        passed = (
            composite >= 90.0
            and backup_recovery_success_score >= 80.0
            and data_integrity_score >= 80.0
            and service_recovery_score >= 80.0
            and functional_validation_score >= 80.0
        )

        audit_meta = {
            "evaluation_framework": "DOCUTASK_RESTORE_VERIFICATION_v3G.2E",
            "weights": self.WEIGHTS,
            "passing_threshold": 90.0,
            "certified_threshold": 95.0,
            "status": "APPROVED" if passed else "REJECTED",
        }

        return RestoreQualityScorecard(
            backup_recovery_success_score=backup_recovery_success_score,
            data_integrity_score=data_integrity_score,
            service_recovery_score=service_recovery_score,
            functional_validation_score=functional_validation_score,
            security_validation_score=security_validation_score,
            recovery_speed_score=recovery_speed_score,
            composite_score=composite,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=audit_meta,
        )
