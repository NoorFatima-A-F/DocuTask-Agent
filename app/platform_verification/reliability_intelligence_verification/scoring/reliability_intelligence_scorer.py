"""
Phase 3H.5.7: Reliability Intelligence Scorer
"""
from ..domain.interfaces import IReliabilityIntelligenceScorer
from ..domain.models import (
    ReliabilityDataCollectionReport,
    ComponentReliabilityScoreReport,
    SystemReliabilityHealthReport,
    SLOComplianceReport,
    ErrorBudgetReport,
    ReliabilityRiskReport,
    ResilienceRecommendationReport,
    ChaosValidationReport,
    ReliabilityTrendReport,
    ReliabilityGovernanceReport,
    ReliabilityScorecard,
)


class ReliabilityIntelligenceScorer(IReliabilityIntelligenceScorer):
    def calculate_scorecard(
        self,
        data_report: ReliabilityDataCollectionReport,
        comp_report: ComponentReliabilityScoreReport,
        health_report: SystemReliabilityHealthReport,
        slo_report: SLOComplianceReport,
        budget_report: ErrorBudgetReport,
        risk_report: ReliabilityRiskReport,
        rec_report: ResilienceRecommendationReport,
        chaos_report: ChaosValidationReport,
        trend_report: ReliabilityTrendReport,
        gov_report: ReliabilityGovernanceReport,
    ) -> ReliabilityScorecard:
        # 1. Reliability measurement accuracy (20%)
        meas_acc = 100.0 if (data_report.collection_pipeline_healthy and data_report.total_components_monitored >= 10) else 80.0

        # 2. Health scoring quality (20%)
        health_qual = 100.0 if (comp_report.total_components_scored >= 10 and health_report.production_ready) else 80.0

        # 3. SLO management (15%)
        slo_score = 100.0 if (slo_report.all_slos_met and slo_report.overall_slo_compliance_pct >= 95.0) else 80.0

        # 4. Error budget implementation (15%)
        budget_score = 100.0 if (budget_report.overall_budget_healthy and not budget_report.budget_exhaustion_detected) else 80.0

        # 5. Risk prediction (15%)
        risk_score = 100.0 if (risk_report.risk_analysis_valid and chaos_report.all_chaos_tests_passed) else 80.0

        # 6. Resilience recommendations (10%)
        rec_score = 100.0 if (rec_report.total_recommendations >= 4 and trend_report.long_term_resilience_improving) else 80.0

        # 7. Governance controls (5%)
        gov_score = 100.0 if gov_report.deployment_gate_approved else 80.0

        composite = (
            meas_acc * 0.20
            + health_qual * 0.20
            + slo_score * 0.15
            + budget_score * 0.15
            + risk_score * 0.15
            + rec_score * 0.10
            + gov_score * 0.05
        )

        composite = round(composite, 2)

        if composite >= 95.0:
            tier = "Reliability Intelligence Certified"
            certified = True
        elif composite >= 90.0:
            tier = "Production Reliability Ready"
            certified = True
        elif composite >= 80.0:
            tier = "Improvement Required"
            certified = False
        else:
            tier = "Failed"
            certified = False

        return ReliabilityScorecard(
            reliability_measurement_accuracy=round(meas_acc, 2),
            health_scoring_quality=round(health_qual, 2),
            slo_management_score=round(slo_score, 2),
            error_budget_score=round(budget_score, 2),
            risk_prediction_score=round(risk_score, 2),
            recommendations_score=round(rec_score, 2),
            governance_score=round(gov_score, 2),
            composite_score=composite,
            tier=tier,
            certified_enterprise_ready=certified,
        )
