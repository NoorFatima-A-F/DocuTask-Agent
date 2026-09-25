"""
Configuration Quality Scoring Engine for Enterprise Configuration Backup Verification (Part 3G.2D).
"""

from app.platform_verification.configuration_backup_verification.domain.models import (
    ConfigCertificationTier,
    ConfigurationQualityScorecard,
)
from app.platform_verification.configuration_backup_verification.domain.interfaces import (
    IConfigurationQualityScoringEngine,
)


class ConfigurationQualityScoringEngine(IConfigurationQualityScoringEngine):
    """
    Computes weighted multi-criteria Configuration Recovery Quality Scorecard
    and determines enterprise operational certification tier.
    """

    WEIGHTS = {
        "configuration_coverage": 0.15,
        "secret_coverage_encryption": 0.15,
        "cryptographic_continuity": 0.15,
        "certificate_health": 0.10,
        "iac_and_feature_flags": 0.10,
        "restore_simulation": 0.15,
        "drift_and_version": 0.10,
        "security_and_compliance": 0.10,
    }

    def compute_quality_scorecard(
        self,
        configuration_coverage_score: float,
        secret_coverage_encryption_score: float,
        cryptographic_continuity_score: float,
        certificate_health_score: float,
        iac_and_feature_flags_score: float,
        restore_simulation_score: float,
        drift_and_version_score: float,
        security_and_compliance_score: float,
        execution_duration_ms: float,
    ) -> ConfigurationQualityScorecard:
        """
        Calculates composite score and assigns formal certification tier.
        """
        composite = (
            configuration_coverage_score * self.WEIGHTS["configuration_coverage"]
            + secret_coverage_encryption_score * self.WEIGHTS["secret_coverage_encryption"]
            + cryptographic_continuity_score * self.WEIGHTS["cryptographic_continuity"]
            + certificate_health_score * self.WEIGHTS["certificate_health"]
            + iac_and_feature_flags_score * self.WEIGHTS["iac_and_feature_flags"]
            + restore_simulation_score * self.WEIGHTS["restore_simulation"]
            + drift_and_version_score * self.WEIGHTS["drift_and_version"]
            + security_and_compliance_score * self.WEIGHTS["security_and_compliance"]
        )
        composite = round(composite, 2)

        if composite >= 98.0:
            tier = ConfigCertificationTier.ENTERPRISE_CERTIFIED
        elif composite >= 95.0:
            tier = ConfigCertificationTier.PRODUCTION_READY
        elif composite >= 90.0:
            tier = ConfigCertificationTier.ACCEPTABLE
        elif composite >= 80.0:
            tier = ConfigCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = ConfigCertificationTier.FAILED

        passed = (
            composite >= 90.0
            and configuration_coverage_score >= 80.0
            and secret_coverage_encryption_score >= 80.0
            and cryptographic_continuity_score >= 80.0
            and restore_simulation_score >= 80.0
            and security_and_compliance_score >= 80.0
        )

        audit_meta = {
            "standard": "DOCUTASK_CONFIG_RECOVERY_VERIFICATION_v3G.2D",
            "weights": self.WEIGHTS,
            "passing_threshold": 90.0,
            "enterprise_gold_threshold": 98.0,
            "gate_status": "APPROVED" if passed else "REJECTED",
        }

        return ConfigurationQualityScorecard(
            configuration_coverage_score=configuration_coverage_score,
            secret_coverage_encryption_score=secret_coverage_encryption_score,
            cryptographic_continuity_score=cryptographic_continuity_score,
            certificate_health_score=certificate_health_score,
            iac_and_feature_flags_score=iac_and_feature_flags_score,
            restore_simulation_score=restore_simulation_score,
            drift_and_version_score=drift_and_version_score,
            security_and_compliance_score=security_and_compliance_score,
            composite_score=composite,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            audit_metadata=audit_meta,
        )
