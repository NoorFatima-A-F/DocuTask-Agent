"""
Backup Security Scoring Engine for Backup Security Verification Framework (Part 3G.2F).
"""

from app.platform_verification.backup_security_verification.domain.models import (
    SecurityCertificationTier,
    BackupSecurityQualityScorecard,
)
from app.platform_verification.backup_security_verification.domain.interfaces import (
    IBackupSecurityQualityScoringEngine,
)


class BackupSecurityQualityScoringEngine(IBackupSecurityQualityScoringEngine):
    """
    Computes weighted multi-criteria Backup Security Quality Scorecard
    and determines enterprise backup security certification tier.
    """

    WEIGHTS = {
        "encryption": 0.25,
        "access_control": 0.20,
        "integrity_protection": 0.20,
        "key_management": 0.15,
        "auditability": 0.10,
        "compliance": 0.10,
    }

    def compute_quality_scorecard(
        self,
        encryption_score: float,
        access_control_score: float,
        integrity_protection_score: float,
        key_management_score: float,
        auditability_score: float,
        compliance_score: float,
        execution_duration_ms: float,
    ) -> BackupSecurityQualityScorecard:
        """
        Calculates composite backup security score and evaluates certification tier.
        """
        composite = (
            encryption_score * self.WEIGHTS["encryption"]
            + access_control_score * self.WEIGHTS["access_control"]
            + integrity_protection_score * self.WEIGHTS["integrity_protection"]
            + key_management_score * self.WEIGHTS["key_management"]
            + auditability_score * self.WEIGHTS["auditability"]
            + compliance_score * self.WEIGHTS["compliance"]
        )
        composite = round(composite, 2)

        if composite >= 95.0:
            tier = SecurityCertificationTier.ENTERPRISE_BACKUP_SECURITY_CERTIFIED
        elif composite >= 90.0:
            tier = SecurityCertificationTier.SECURE_PRODUCTION_READY
        elif composite >= 80.0:
            tier = SecurityCertificationTier.SECURITY_IMPROVEMENTS_REQUIRED
        else:
            tier = SecurityCertificationTier.FAILED

        passed = (
            composite >= 90.0
            and encryption_score >= 80.0
            and access_control_score >= 80.0
            and integrity_protection_score >= 80.0
            and key_management_score >= 80.0
        )

        audit_meta = {
            "evaluation_standard": "DOCUTASK_BACKUP_SECURITY_v3G.2F",
            "weights": self.WEIGHTS,
            "passing_threshold": 90.0,
            "enterprise_gold_threshold": 95.0,
            "status": "APPROVED" if passed else "REJECTED",
        }

        return BackupSecurityQualityScorecard(
            encryption_score=encryption_score,
            access_control_score=access_control_score,
            integrity_protection_score=integrity_protection_score,
            key_management_score=key_management_score,
            auditability_score=auditability_score,
            compliance_score=compliance_score,
            composite_score=composite,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=audit_meta,
        )
