"""
Weighted Deployment Quality Scoring and Certification Engine.
"""
from app.platform_verification.deployment_verification.domain.models import (
    BuildReproducibilityReport,
    DependencyLockReport,
    EnvironmentDriftReport,
    DeploymentAutomationReport,
    SecretDeploymentReport,
    ReleaseStrategyReport,
    RollbackVerificationReport,
    ZeroDowntimeReport,
    DeploymentCertificationReport,
    DeploymentCertificationTier,
)
from app.platform_verification.deployment_verification.domain.interfaces import IDeploymentScoringEngine


class DeploymentScoringEngine(IDeploymentScoringEngine):
    """Calculates weighted composite score across 6 deployment verification pillars."""

    # Weights: Reproducibility (20%), Automation (20%), Security (20%), Reliability (15%), Rollback (15%), Environment Consistency (10%)
    WEIGHT_REPRO = 0.20
    WEIGHT_AUTO = 0.20
    WEIGHT_SEC = 0.20
    WEIGHT_RELIABILITY = 0.15
    WEIGHT_ROLLBACK = 0.15
    WEIGHT_ENV_PARITY = 0.10

    def calculate_scorecard(
        self,
        build_rep: BuildReproducibilityReport,
        lock_rep: DependencyLockReport,
        drift_rep: EnvironmentDriftReport,
        auto_rep: DeploymentAutomationReport,
        sec_rep: SecretDeploymentReport,
        release_rep: ReleaseStrategyReport,
        rollback_rep: RollbackVerificationReport,
        zero_rep: ZeroDowntimeReport,
    ) -> DeploymentCertificationReport:
        repro_s = (100.0 if build_rep.is_reproducible else 50.0) * 0.5 + (100.0 if lock_rep.is_strictly_pinned else 60.0) * 0.5
        auto_s = auto_rep.automation_percentage
        sec_s = 100.0 if sec_rep.status == "PASS" else 40.0
        rel_s = 100.0 if release_rep.status == "PASS" and zero_rep.status == "PASS" else 70.0
        roll_s = 100.0 if rollback_rep.rollback_successful else 40.0
        env_s = drift_rep.parity_score

        composite = (
            (repro_s * self.WEIGHT_REPRO)
            + (auto_s * self.WEIGHT_AUTO)
            + (sec_s * self.WEIGHT_SEC)
            + (rel_s * self.WEIGHT_RELIABILITY)
            + (roll_s * self.WEIGHT_ROLLBACK)
            + (env_s * self.WEIGHT_ENV_PARITY)
        )
        composite = round(composite, 2)

        if composite >= 95.0 and rollback_rep.rollback_successful and sec_rep.status == "PASS":
            tier = DeploymentCertificationTier.ENTERPRISE_DEPLOYMENT_READY
        elif composite >= 90.0:
            tier = DeploymentCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = DeploymentCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = DeploymentCertificationTier.FAILED

        return DeploymentCertificationReport(
            reproducibility_score=round(repro_s, 2),
            automation_score=round(auto_s, 2),
            security_score=round(sec_s, 2),
            reliability_score=round(rel_s, 2),
            rollback_capability_score=round(roll_s, 2),
            environment_consistency_score=round(env_s, 2),
            composite_score=composite,
            tier=tier,
        )
