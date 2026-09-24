"""
Backup Readiness Scoring Engine for Backup Certification Framework (Part 3G.2G).
Calculates weighted scores across 7 dimensions and certifies enterprise readiness tiers.
"""
from app.platform_verification.backup_certification.domain.models import (
    BackupCertificationTier,
    BackupReadinessScorecard,
)
from app.platform_verification.backup_certification.domain.interfaces import (
    IBackupReadinessScoringEngine,
)


class BackupReadinessScoringEngine(IBackupReadinessScoringEngine):
    """
    Computes weighted Certification Score:
    Score = (Completeness * 0.20) + (Restore * 0.25) + (Integrity * 0.15) + (Security * 0.15)
          + (Automation * 0.10) + (Monitoring * 0.10) + (Documentation * 0.05)
    """

    WEIGHTS = {
        "backup_completeness": 0.20,
        "restore_success": 0.25,
        "integrity": 0.15,
        "security": 0.15,
        "automation": 0.10,
        "monitoring": 0.10,
        "documentation": 0.05,
    }

    def compute_certification_score(
        self,
        completeness_score: float,
        restore_score: float,
        integrity_score: float,
        security_score: float,
        automation_score: float,
        monitoring_score: float,
        documentation_score: float,
    ) -> BackupReadinessScorecard:
        overall_score = (
            (completeness_score * self.WEIGHTS["backup_completeness"])
            + (restore_score * self.WEIGHTS["restore_success"])
            + (integrity_score * self.WEIGHTS["integrity"])
            + (security_score * self.WEIGHTS["security"])
            + (automation_score * self.WEIGHTS["automation"])
            + (monitoring_score * self.WEIGHTS["monitoring"])
            + (documentation_score * self.WEIGHTS["documentation"])
        )
        overall_score = round(overall_score, 2)

        if overall_score >= 95.0:
            tier = BackupCertificationTier.LEVEL_4_MISSION_CRITICAL_READY
        elif overall_score >= 90.0:
            tier = BackupCertificationTier.LEVEL_3_ENTERPRISE_READY
        elif overall_score >= 80.0:
            tier = BackupCertificationTier.LEVEL_2_PRODUCTION_READY
        elif overall_score >= 70.0:
            tier = BackupCertificationTier.LEVEL_1_BASIC_READY
        else:
            tier = BackupCertificationTier.UNCERTIFIED_FAILED

        passed = overall_score >= 80.0
        ci_cd_deployment_approved = overall_score >= 90.0

        meta = {
            "evaluation_standard": "DOCUTASK_BACKUP_CERTIFICATION_v3G.2G",
            "weights": self.WEIGHTS,
            "ci_cd_gate_minimum_score": 90.0,
            "mission_critical_threshold": 95.0,
            "status": "CERTIFIED" if passed else "REJECTED",
        }

        return BackupReadinessScorecard(
            backup_completeness=completeness_score,
            restore_success=restore_score,
            integrity=integrity_score,
            security=security_score,
            automation=automation_score,
            monitoring=monitoring_score,
            documentation=documentation_score,
            overall_score=overall_score,
            certification_level=tier,
            passed=passed,
            ci_cd_deployment_approved=ci_cd_deployment_approved,
            evaluation_metadata=meta,
        )
