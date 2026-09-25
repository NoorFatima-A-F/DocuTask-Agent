"""Domain interfaces for reliability engineering intelligence."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.platform_verification.reliability_intelligence.domain.models import (
    CapacityIntelligenceReport,
    ChangeImpactReport,
    ChaosLearningReport,
    ContinuousImprovementReport,
    ErrorBudgetReport,
    FailurePatternReport,
    ReliabilityMaturityScorecard,
    ReliabilityModelReport,
    ReliabilityRecommendationReport,
    ReliabilityRiskReport,
    ReliabilitySecurityReport,
    RootCauseReport,
    SLOVerificationReport,
)


class IReliabilityModelVerifier(ABC):
    @abstractmethod
    def verify_reliability_model(self) -> ReliabilityModelReport:
        pass


class ISLOVerifier(ABC):
    @abstractmethod
    def verify_slos(self) -> SLOVerificationReport:
        pass


class IErrorBudgetManager(ABC):
    @abstractmethod
    def manage_error_budgets(self) -> ErrorBudgetReport:
        pass


class IFailurePatternAnalyzer(ABC):
    @abstractmethod
    def analyze_failure_patterns(self) -> FailurePatternReport:
        pass


class IRootCauseEngine(ABC):
    @abstractmethod
    def analyze_root_causes(self) -> RootCauseReport:
        pass


class IReliabilityRiskScorer(ABC):
    @abstractmethod
    def score_reliability_risks(self) -> ReliabilityRiskReport:
        pass


class ICapacityIntelligenceEngine(ABC):
    @abstractmethod
    def evaluate_capacity(self) -> CapacityIntelligenceReport:
        pass


class IChangeImpactAnalyzer(ABC):
    @abstractmethod
    def analyze_change_impact(self) -> ChangeImpactReport:
        pass


class IChaosLearningTracker(ABC):
    @abstractmethod
    def track_chaos_learning(self) -> ChaosLearningReport:
        pass


class IReliabilityRecommender(ABC):
    @abstractmethod
    def generate_recommendations(self) -> ReliabilityRecommendationReport:
        pass


class IContinuousImprovementLoop(ABC):
    @abstractmethod
    def verify_improvement_pipeline(self) -> ContinuousImprovementReport:
        pass


class IReliabilitySecurityAuditor(ABC):
    @abstractmethod
    def audit_security(self) -> ReliabilitySecurityReport:
        pass


class IReliabilityMaturityScorer(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        model_report: ReliabilityModelReport,
        slo_report: SLOVerificationReport,
        budget_report: ErrorBudgetReport,
        pattern_report: FailurePatternReport,
        root_cause_report: RootCauseReport,
        risk_report: ReliabilityRiskReport,
        capacity_report: CapacityIntelligenceReport,
        change_report: ChangeImpactReport,
        chaos_report: ChaosLearningReport,
        rec_report: ReliabilityRecommendationReport,
        improvement_report: ContinuousImprovementReport,
        security_report: ReliabilitySecurityReport,
    ) -> ReliabilityMaturityScorecard:
        pass
