"""Reliability Maturity Scorer & Certification Engine.

Part 3H.3.7N: Multi-Dimensional SRE Maturity Scoring & Certification.
Weights:
- SLO Management: 20%
- Reliability Analytics: 20%
- Failure Intelligence: 20%
- Capacity Prediction: 15%
- Improvement Automation: 15%
- Security: 10%
"""

from app.platform_verification.reliability_intelligence.domain.models import (
    ReliabilityMaturityScorecard,
    ReliabilityMaturityTier,
    ReliabilityModelReport,
    SLOVerificationReport,
    ErrorBudgetReport,
    FailurePatternReport,
    RootCauseReport,
    ReliabilityRiskReport,
    CapacityIntelligenceReport,
    ChangeImpactReport,
    ChaosLearningReport,
    ReliabilityRecommendationReport,
    ContinuousImprovementReport,
    ReliabilitySecurityReport,
)


class ReliabilityMaturityScorer:
    """Computes weighted multi-dimensional maturity scores and certifies platform reliability."""

    WEIGHT_SLO_MANAGEMENT = 0.20
    WEIGHT_RELIABILITY_ANALYTICS = 0.20
    WEIGHT_FAILURE_INTELLIGENCE = 0.20
    WEIGHT_CAPACITY_PREDICTION = 0.15
    WEIGHT_IMPROVEMENT_AUTOMATION = 0.15
    WEIGHT_SECURITY = 0.10

    TARGET_THRESHOLD = 95.0

    def compute_scorecard(
        self,
        model_report: ReliabilityModelReport,
        slo_report: SLOVerificationReport,
        error_budget_report: ErrorBudgetReport,
        failure_pattern_report: FailurePatternReport,
        root_cause_report: RootCauseReport,
        risk_score_report: ReliabilityRiskReport,
        capacity_report: CapacityIntelligenceReport,
        change_impact_report: ChangeImpactReport,
        chaos_report: ChaosLearningReport,
        recommendation_report: ReliabilityRecommendationReport,
        improvement_report: ContinuousImprovementReport,
        security_report: ReliabilitySecurityReport,
    ) -> ReliabilityMaturityScorecard:
        """Calculates 6-dimensional weighted score and returns certification scorecard."""

        # 1. SLO Management (20%)
        # Sub-factors: Model pass (100%), SLO compliance % (scaled), Error budget pass
        slo_comp_pct = slo_report.slo_compliance_pct
        model_score = 100.0 if model_report.passed else 50.0
        budget_score = 100.0 if error_budget_report.passed else 60.0
        slo_mgmt_score = round(0.35 * model_score + 0.35 * slo_comp_pct + 0.30 * budget_score, 2)

        # 2. Reliability Analytics (20%)
        # Sub-factors: Failure pattern pass & trend, Risk score composite
        failure_score = 100.0 if failure_pattern_report.passed else 50.0
        risk_score = 100.0 if risk_score_report.passed else 60.0
        analytics_score = round(0.50 * failure_score + 0.50 * risk_score, 2)

        # 3. Failure Intelligence (20%)
        # Sub-factors: Root cause resolution confidence & MTTR reduction
        rc_score = 100.0 if root_cause_report.passed else 50.0
        chaos_score = min(100.0, 80.0 + (chaos_report.avg_mttr_improvement_pct * 0.4)) if chaos_report.passed else 50.0
        failure_intel_score = round(0.50 * rc_score + 0.50 * chaos_score, 2)

        # 4. Capacity Prediction (15%)
        # Sub-factors: Capacity intelligence pass & forecast coverage
        capacity_score = 100.0 if capacity_report.passed else 60.0

        # 5. Improvement Automation (15%)
        # Sub-factors: Change impact pass, Recommendation pass, Continuous improvement loop
        change_score = 100.0 if change_impact_report.passed else 60.0
        rec_score = 100.0 if recommendation_report.passed else 60.0
        loop_score = 100.0 if improvement_report.passed else 60.0
        improvement_auto_score = round(0.34 * change_score + 0.33 * rec_score + 0.33 * loop_score, 2)

        # 6. Security (10%)
        security_score = 100.0 if (security_report.passed and not security_report.pii_or_secrets_exposed) else 40.0

        # Overall Weighted Score
        overall_score = round(
            (slo_mgmt_score * self.WEIGHT_SLO_MANAGEMENT)
            + (analytics_score * self.WEIGHT_RELIABILITY_ANALYTICS)
            + (failure_intel_score * self.WEIGHT_FAILURE_INTELLIGENCE)
            + (capacity_score * self.WEIGHT_CAPACITY_PREDICTION)
            + (improvement_auto_score * self.WEIGHT_IMPROVEMENT_AUTOMATION)
            + (security_score * self.WEIGHT_SECURITY),
            2,
        )

        # Determine Tier
        if overall_score >= 95.0:
            tier = ReliabilityMaturityTier.RELIABILITY_ENGINEERING_MATURE
            verdict = "CERTIFIED"
            passed = True
        elif overall_score >= 90.0:
            tier = ReliabilityMaturityTier.ENTERPRISE_RELIABILITY_READY
            verdict = "CONDITIONAL_APPROVAL"
            passed = True
        elif overall_score >= 80.0:
            tier = ReliabilityMaturityTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED_REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = ReliabilityMaturityTier.FAILED
            verdict = "REJECTED"
            passed = False

        return ReliabilityMaturityScorecard(
            slo_management_score=slo_mgmt_score,
            reliability_analytics_score=analytics_score,
            failure_intelligence_score=failure_intel_score,
            capacity_prediction_score=capacity_score,
            improvement_automation_score=improvement_auto_score,
            security_score=security_score,
            overall_score=overall_score,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "target_threshold_pct": self.TARGET_THRESHOLD,
                "dimension_weights": {
                    "slo_management": self.WEIGHT_SLO_MANAGEMENT,
                    "reliability_analytics": self.WEIGHT_RELIABILITY_ANALYTICS,
                    "failure_intelligence": self.WEIGHT_FAILURE_INTELLIGENCE,
                    "capacity_prediction": self.WEIGHT_CAPACITY_PREDICTION,
                    "improvement_automation": self.WEIGHT_IMPROVEMENT_AUTOMATION,
                    "security": self.WEIGHT_SECURITY,
                },
            },
        )
