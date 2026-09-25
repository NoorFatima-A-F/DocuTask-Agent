"""
Phase 3H.10: Autonomous Operational Intelligence & Self-Optimization — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
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


class IOperationalGraphVerifier(ABC):
    @abstractmethod
    def verify_operational_graph(self) -> OperationalGraphReport:
        pass


class ISignalCorrelationVerifier(ABC):
    @abstractmethod
    def verify_signal_correlation(self) -> SignalCorrelationReport:
        pass


class ITrendAnalysisVerifier(ABC):
    @abstractmethod
    def verify_trend_analysis(self) -> TrendAnalysisReport:
        pass


class IPredictiveReliabilityVerifier(ABC):
    @abstractmethod
    def verify_predictive_reliability(self) -> PredictiveReliabilityReport:
        pass


class IOptimizationRecommendationVerifier(ABC):
    @abstractmethod
    def verify_optimization_recommendations(self) -> OptimizationRecommendationsReport:
        pass


class IAutonomousExecutionVerifier(ABC):
    @abstractmethod
    def verify_autonomous_execution(self) -> AutonomousExecutionReport:
        pass


class IExplainabilityVerifier(ABC):
    @abstractmethod
    def verify_explainability(self) -> ExplainabilityReport:
        pass


class ILearningEffectivenessVerifier(ABC):
    @abstractmethod
    def verify_learning_effectiveness(self) -> LearningEffectivenessReport:
        pass


class IGovernanceVerifier(ABC):
    @abstractmethod
    def verify_governance(self) -> GovernanceReport:
        pass


class IAutonomousOptimizationScorer(ABC):
    @abstractmethod
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
        pass


class IAutonomousOptimizationExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        graph_report: OperationalGraphReport,
        correlation_report: SignalCorrelationReport,
        trend_report: TrendAnalysisReport,
        predictive_report: PredictiveReliabilityReport,
        recommendations_report: OptimizationRecommendationsReport,
        execution_report: AutonomousExecutionReport,
        explainability_report: ExplainabilityReport,
        learning_report: LearningEffectivenessReport,
        governance_report: GovernanceReport,
        certification_report: CertificationReport,
    ) -> Dict[str, Any]:
        pass
