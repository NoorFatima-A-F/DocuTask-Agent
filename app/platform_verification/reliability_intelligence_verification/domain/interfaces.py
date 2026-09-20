"""
Phase 3H.5.7: Domain Interfaces for Reliability Intelligence
"""
from abc import ABC, abstractmethod
from .models import (
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


class IReliabilityDataCollector(ABC):
    @abstractmethod
    def collect_reliability_data(self) -> ReliabilityDataCollectionReport:
        pass


class IComponentScoreEngine(ABC):
    @abstractmethod
    def calculate_component_scores(
        self, data_report: ReliabilityDataCollectionReport
    ) -> ComponentReliabilityScoreReport:
        pass


class ISystemHealthScoreEngine(ABC):
    @abstractmethod
    def calculate_system_health(
        self, comp_report: ComponentReliabilityScoreReport
    ) -> SystemReliabilityHealthReport:
        pass


class ISLOVerifier(ABC):
    @abstractmethod
    def verify_slos(self) -> SLOComplianceReport:
        pass


class IErrorBudgetManager(ABC):
    @abstractmethod
    def evaluate_error_budgets(self) -> ErrorBudgetReport:
        pass


class IReliabilityRiskAnalyzer(ABC):
    @abstractmethod
    def analyze_reliability_risks(self) -> ReliabilityRiskReport:
        pass


class IResilienceRecommendationEngine(ABC):
    @abstractmethod
    def generate_recommendations(
        self, risk_report: ReliabilityRiskReport
    ) -> ResilienceRecommendationReport:
        pass


class IChaosReliabilityValidator(ABC):
    @abstractmethod
    def run_chaos_validation(self) -> ChaosValidationReport:
        pass


class IReliabilityTrendAnalyzer(ABC):
    @abstractmethod
    def analyze_reliability_trends(self) -> ReliabilityTrendReport:
        pass


class IReliabilityGovernanceVerifier(ABC):
    @abstractmethod
    def evaluate_governance(
        self,
        health_report: SystemReliabilityHealthReport,
        budget_report: ErrorBudgetReport,
        risk_report: ReliabilityRiskReport,
    ) -> ReliabilityGovernanceReport:
        pass


class IReliabilityIntelligenceScorer(ABC):
    @abstractmethod
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
        pass
