"""
Storage Quality Scoring Engine for Enterprise Document Storage (Part 3G.2C).
"""
from typing import Dict, Any

from app.platform_verification.document_storage_verification.domain.models import (
    StorageCertificationTier,
    StorageQualityScorecard,
)
from app.platform_verification.document_storage_verification.domain.interfaces import (
    IStorageQualityScoringEngine,
)


class StorageQualityScoringEngine(IStorageQualityScoringEngine):
    """
    Computes weighted multi-dimensional storage verification scorecard
    and determines enterprise certification tiers.
    """

    WEIGHTS = {
        "recoverability": 0.20,
        "integrity": 0.20,
        "coverage": 0.15,
        "cross_system_consistency": 0.15,
        "security": 0.10,
        "performance": 0.10,
        "tenant_isolation": 0.05,
        "automation": 0.05,
    }

    def compute_quality_scorecard(
        self,
        recoverability_score: float,
        integrity_score: float,
        coverage_score: float,
        cross_system_consistency_score: float,
        security_score: float,
        performance_score: float,
        tenant_isolation_score: float,
        automation_score: float,
        execution_duration_ms: float,
    ) -> StorageQualityScorecard:
        """
        Calculates composite quality score and assigns formal enterprise certification tier.
        """
        composite = (
            recoverability_score * self.WEIGHTS["recoverability"]
            + integrity_score * self.WEIGHTS["integrity"]
            + coverage_score * self.WEIGHTS["coverage"]
            + cross_system_consistency_score * self.WEIGHTS["cross_system_consistency"]
            + security_score * self.WEIGHTS["security"]
            + performance_score * self.WEIGHTS["performance"]
            + tenant_isolation_score * self.WEIGHTS["tenant_isolation"]
            + automation_score * self.WEIGHTS["automation"]
        )
        composite = round(composite, 2)

        # Assign certification tier
        if composite >= 98.0:
            tier = StorageCertificationTier.ENTERPRISE_STORAGE_CERTIFIED
        elif composite >= 95.0:
            tier = StorageCertificationTier.ENTERPRISE_READY
        elif composite >= 90.0:
            tier = StorageCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = StorageCertificationTier.CONDITIONALLY_READY
        elif composite >= 70.0:
            tier = StorageCertificationTier.DEVELOPMENT_GRADE
        else:
            tier = StorageCertificationTier.FAILED

        # Quality gate: composite >= 90.0 and no critical dimension below 80.0
        passed = (
            composite >= 90.0
            and recoverability_score >= 80.0
            and integrity_score >= 80.0
            and coverage_score >= 80.0
            and security_score >= 80.0
        )

        audit_meta = {
            "evaluation_standard": "DOCUTASK_STORAGE_VERIFICATION_v3G.2C",
            "weights_table": self.WEIGHTS,
            "minimum_passing_threshold": 90.0,
            "enterprise_gold_threshold": 98.0,
            "status": "APPROVED" if passed else "REJECTED",
        }

        return StorageQualityScorecard(
            recoverability_score=recoverability_score,
            integrity_score=integrity_score,
            coverage_score=coverage_score,
            cross_system_consistency_score=cross_system_consistency_score,
            security_score=security_score,
            performance_score=performance_score,
            tenant_isolation_score=tenant_isolation_score,
            automation_score=automation_score,
            composite_score=composite,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=audit_meta,
        )
