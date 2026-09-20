"""
Phase 3H.10: 7-Pillar Autonomous Optimization & Operations Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    AutonomousCertificationTier,
    OperationalGraphReport,
    SignalCorrelationReport,
    TrendAnalysisReport,
    PredictiveReliabilityReport,
    OptimizationRecommendationsReport,
    AutonomousExecutionReport,
    ExplainabilityReport,
    LearningEffectivenessReport,
    GovernanceReport,
    PillarScore,
    CertificationReport,
)
from ..domain.interfaces import IAutonomousOptimizationScorer


class AutonomousOptimizationScorer(IAutonomousOptimizationScorer):
    """
    Evaluates 7 core pillars with calibrated enterprise weights:
      - Correlation Accuracy: 20%
      - Prediction Accuracy: 20%
      - Recommendation Quality: 20%
      - Execution Safety: 15%
      - Explainability: 10%
      - Learning Capability: 10%
      - Governance & Compliance: 5%
    """

    def calculate_certification_score(
        self,
        graph_report: OperationalGraphReport,
        correlation_report: SignalCorrelationReport,
        trend_report: TrendAnalysisReport,
        predictive_report: PredictiveReliabilityReport,
        recommendations_report: OptimizationRecommendationsReport,
        execution_report: AutonomousExecutionReport,
        explainability_report: ExplainabilityReport,
        learning_report: LearningEffectivenessReport,
        governance_report: GovernanceReport,
    ) -> CertificationReport:
        # 1. Correlation Accuracy (20%) - blend of graph topology validity and correlation accuracy
        corr_score = correlation_report.correlation_accuracy_pct if graph_report.topology_valid else 80.0
        corr_weight = 20.0
        corr_weighted = (corr_score * corr_weight) / 100.0

        # 2. Prediction Accuracy (20%) - predictive forecast accuracy and trend stability
        pred_score = (predictive_report.prediction_accuracy_pct * 0.7) + (trend_report.trend_stability_index * 0.3)
        pred_weight = 20.0
        pred_weighted = (pred_score * pred_weight) / 100.0

        # 3. Recommendation Quality (20%)
        recom_score = recommendations_report.recommendation_quality_score
        recom_weight = 20.0
        recom_weighted = (recom_score * recom_weight) / 100.0

        # 4. Execution Safety (15%)
        safety_score = execution_report.execution_safety_index
        safety_weight = 15.0
        safety_weighted = (safety_score * safety_weight) / 100.0

        # 5. Explainability (10%)
        expl_score = explainability_report.explainability_index
        expl_weight = 10.0
        expl_weighted = (expl_score * expl_weight) / 100.0

        # 6. Learning Capability (10%)
        learn_score = learning_report.learning_effectiveness_score
        learn_weight = 10.0
        learn_weighted = (learn_score * learn_weight) / 100.0

        # 7. Governance (5%)
        gov_score = governance_report.compliance_rate_pct
        gov_weight = 5.0
        gov_weighted = (gov_score * gov_weight) / 100.0

        total_score = corr_weighted + pred_weighted + recom_weighted + safety_weighted + expl_weighted + learn_weighted + gov_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[PillarScore] = [
            PillarScore(
                pillar_name="Correlation Accuracy & Topology",
                weight_pct=corr_weight,
                achieved_score_pct=round(corr_score, 2),
                weighted_score_pct=round(corr_weighted, 2),
                status="PASSED" if corr_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Prediction & Trend Reliability",
                weight_pct=pred_weight,
                achieved_score_pct=round(pred_score, 2),
                weighted_score_pct=round(pred_weighted, 2),
                status="PASSED" if pred_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Recommendation Quality & ROI",
                weight_pct=recom_weight,
                achieved_score_pct=round(recom_score, 2),
                weighted_score_pct=round(recom_weighted, 2),
                status="PASSED" if recom_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Autonomous Execution Safety",
                weight_pct=safety_weight,
                achieved_score_pct=round(safety_score, 2),
                weighted_score_pct=round(safety_weighted, 2),
                status="PASSED" if safety_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Decision Explainability & Proof",
                weight_pct=expl_weight,
                achieved_score_pct=round(expl_score, 2),
                weighted_score_pct=round(expl_weighted, 2),
                status="PASSED" if expl_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Continuous Learning & Adaptation",
                weight_pct=learn_weight,
                achieved_score_pct=round(learn_score, 2),
                weighted_score_pct=round(learn_weighted, 2),
                status="PASSED" if learn_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            PillarScore(
                pillar_name="Governance & Policy Compliance",
                weight_pct=gov_weight,
                achieved_score_pct=round(gov_score, 2),
                weighted_score_pct=round(gov_weighted, 2),
                status="PASSED" if gov_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 98.0:
            tier = AutonomousCertificationTier.AUTONOMOUS_OPERATIONS_CERTIFIED
            granted = True
        elif total_score >= 95.0:
            tier = AutonomousCertificationTier.ADVANCED_AUTONOMOUS_READY
            granted = True
        elif total_score >= 90.0:
            tier = AutonomousCertificationTier.SUPERVISED_OPERATIONS_ONLY
            granted = False
        elif total_score >= 80.0:
            tier = AutonomousCertificationTier.NEEDS_REFINEMENT
            granted = False
        else:
            tier = AutonomousCertificationTier.FAILED
            granted = False

        return CertificationReport(
            report_title="Phase 3H.10 Autonomous Operations & Self-Optimization Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=98.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Autonomous Reliability & Operations Scorer"
        )
