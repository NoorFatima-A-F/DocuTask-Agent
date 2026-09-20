"""
Phase 3H.10: Runtime Orchestrator for Autonomous Operational Intelligence & Self-Optimization
"""
from typing import Dict, Any
from ..domain.models import (
    OperationalGraphReport,
    SignalCorrelationReport,
    TrendAnalysisReport,
    PredictiveReliabilityReport,
    OptimizationRecommendationsReport,
    AutonomousExecutionReport,
    ExplainabilityReport,
    LearningEffectivenessReport,
    GovernanceReport,
    CertificationReport,
)
from ..verifiers.operational_graph_verifier import OperationalGraphVerifier
from ..verifiers.signal_correlation_verifier import SignalCorrelationVerifier
from ..verifiers.trend_analysis_verifier import TrendAnalysisVerifier
from ..verifiers.predictive_reliability_verifier import PredictiveReliabilityVerifier
from ..verifiers.optimization_recommendation_verifier import OptimizationRecommendationVerifier
from ..verifiers.autonomous_execution_verifier import AutonomousExecutionVerifier
from ..verifiers.explainability_verifier import ExplainabilityVerifier
from ..verifiers.learning_effectiveness_verifier import LearningEffectivenessVerifier
from ..verifiers.governance_verifier import GovernanceVerifier
from ..scoring.autonomous_optimization_scorer import AutonomousOptimizationScorer
from ..exporter.autonomous_optimization_exporter import AutonomousOptimizationExporter


class AutonomousOptimizationRuntime:
    """
    Executes all Phase 3H.10 verifiers, triggers 7-pillar scoring, and handles artifact exports.
    """

    def __init__(self):
        self.graph_verifier = OperationalGraphVerifier()
        self.correlation_verifier = SignalCorrelationVerifier()
        self.trend_verifier = TrendAnalysisVerifier()
        self.predictive_verifier = PredictiveReliabilityVerifier()
        self.recommendations_verifier = OptimizationRecommendationVerifier()
        self.execution_verifier = AutonomousExecutionVerifier()
        self.explainability_verifier = ExplainabilityVerifier()
        self.learning_verifier = LearningEffectivenessVerifier()
        self.governance_verifier = GovernanceVerifier()
        self.scorer = AutonomousOptimizationScorer()
        self.exporter = AutonomousOptimizationExporter()

    def run_full_verification(self, export_dir: str = "autonomous_intelligence_verification") -> Dict[str, Any]:
        graph_report: OperationalGraphReport = self.graph_verifier.verify_operational_graph()
        correlation_report: SignalCorrelationReport = self.correlation_verifier.verify_signal_correlation()
        trend_report: TrendAnalysisReport = self.trend_verifier.verify_trend_analysis()
        predictive_report: PredictiveReliabilityReport = self.predictive_verifier.verify_predictive_reliability()
        recommendations_report: OptimizationRecommendationsReport = self.recommendations_verifier.verify_optimization_recommendations()
        execution_report: AutonomousExecutionReport = self.execution_verifier.verify_autonomous_execution()
        explainability_report: ExplainabilityReport = self.explainability_verifier.verify_explainability()
        learning_report: LearningEffectivenessReport = self.learning_verifier.verify_learning_effectiveness()
        governance_report: GovernanceReport = self.governance_verifier.verify_governance()

        certification_report: CertificationReport = self.scorer.calculate_certification_score(
            graph_report=graph_report,
            correlation_report=correlation_report,
            trend_report=trend_report,
            predictive_report=predictive_report,
            recommendations_report=recommendations_report,
            execution_report=execution_report,
            explainability_report=explainability_report,
            learning_report=learning_report,
            governance_report=governance_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            graph_report=graph_report,
            correlation_report=correlation_report,
            trend_report=trend_report,
            predictive_report=predictive_report,
            recommendations_report=recommendations_report,
            execution_report=execution_report,
            explainability_report=explainability_report,
            learning_report=learning_report,
            governance_report=governance_report,
            certification_report=certification_report,
        )

        return {
            "graph_report": graph_report,
            "correlation_report": correlation_report,
            "trend_report": trend_report,
            "predictive_report": predictive_report,
            "recommendations_report": recommendations_report,
            "execution_report": execution_report,
            "explainability_report": explainability_report,
            "learning_report": learning_report,
            "governance_report": governance_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
