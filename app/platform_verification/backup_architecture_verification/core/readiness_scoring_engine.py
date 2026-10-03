"""
Part 14: Backup Readiness Scoring Engine.
Computes the weighted Backup Architecture Readiness Score across all 9 evaluation
categories and awards official enterprise certification tiers.
"""
from typing import Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    CertificationTier,
    BackupReadinessScorecard,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IReadinessScoringEngine,
)


class ReadinessScoringEngine(IReadinessScoringEngine):
    """
    Evaluates category scores with exact enterprise weights:
    - Asset Discovery: 10%
    - Classification: 10%
    - Strategy Quality: 20%
    - Coverage: 20%
    - Retention: 10%
    - Lifecycle: 10%
    - Metadata: 10%
    - Observability: 5%
    - Policy Validation: 5%
    """

    def calculate_readiness_score(
        self,
        discovery_score: float,
        classification_score: float,
        strategy_score: float,
        coverage_score: float,
        retention_score: float,
        lifecycle_score: float,
        metadata_score: float,
        observability_score: float,
        policy_score: float,
        execution_duration_ms: float,
    ) -> BackupReadinessScorecard:
        # Category weights
        w_discovery = 0.10
        w_classification = 0.10
        w_strategy = 0.20
        w_coverage = 0.20
        w_retention = 0.10
        w_lifecycle = 0.10
        w_metadata = 0.10
        w_observability = 0.05
        w_policy = 0.05

        composite = (
            (discovery_score * w_discovery)
            + (classification_score * w_classification)
            + (strategy_score * w_strategy)
            + (coverage_score * w_coverage)
            + (retention_score * w_retention)
            + (lifecycle_score * w_lifecycle)
            + (metadata_score * w_metadata)
            + (observability_score * w_observability)
            + (policy_score * w_policy)
        )

        composite_rounded = round(composite, 2)

        if composite_rounded >= 95.0:
            tier = CertificationTier.ENTERPRISE_CERTIFIED
            passed = True
        elif composite_rounded >= 90.0:
            tier = CertificationTier.PRODUCTION_READY
            passed = True
        elif composite_rounded >= 80.0:
            tier = CertificationTier.CONDITIONALLY_READY
            passed = False
        elif composite_rounded >= 70.0:
            tier = CertificationTier.DEVELOPMENT_QUALITY
            passed = False
        else:
            tier = CertificationTier.NOT_READY
            passed = False

        metadata = {
            "standards_compliance": [
                "Google SRE Backup Principles",
                "AWS Well-Architected Reliability Pillar",
                "Azure Reliability Framework",
                "NIST SP 800-34 Rev. 1",
                "ISO 22301 (Business Continuity)",
                "ISO/IEC 27001:2022 (A.8.13 Information Backup)",
                "CIS Controls v8 Safeguard 11",
                "Kubernetes Disaster Recovery Best Practices",
            ],
            "weights_table": {
                "Asset Discovery": "10%",
                "Classification": "10%",
                "Strategy Quality": "20%",
                "Coverage": "20%",
                "Retention": "10%",
                "Lifecycle": "10%",
                "Metadata": "10%",
                "Observability": "5%",
                "Policy Validation": "5%",
            },
        }

        return BackupReadinessScorecard(
            asset_discovery_score=discovery_score,
            classification_score=classification_score,
            strategy_quality_score=strategy_score,
            coverage_score=coverage_score,
            retention_score=retention_score,
            lifecycle_score=lifecycle_score,
            metadata_score=metadata_score,
            observability_score=observability_score,
            policy_validation_score=policy_score,
            readiness_composite_score=composite_rounded,
            certification_tier=tier,
            passed=passed,
            execution_duration_ms=execution_duration_ms,
            verification_metadata=metadata,
        )

    def export_scorecard_json(self, scorecard: BackupReadinessScorecard) -> Dict[str, Any]:
        """Formats the scorecard to JSON dictionary."""
        return {
            "readiness_composite_score": scorecard.readiness_composite_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "execution_duration_ms": scorecard.execution_duration_ms,
            "category_scores": {
                "asset_discovery_score": scorecard.asset_discovery_score,
                "classification_score": scorecard.classification_score,
                "strategy_quality_score": scorecard.strategy_quality_score,
                "coverage_score": scorecard.coverage_score,
                "retention_score": scorecard.retention_score,
                "lifecycle_score": scorecard.lifecycle_score,
                "metadata_score": scorecard.metadata_score,
                "observability_score": scorecard.observability_score,
                "policy_validation_score": scorecard.policy_validation_score,
            },
            "verification_metadata": scorecard.verification_metadata,
        }
