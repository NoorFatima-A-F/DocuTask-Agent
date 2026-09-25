"""
Phase 3H.9: Domain Interfaces for Operational Intelligence Verification
"""
from abc import ABC, abstractmethod
from .models import (
    TelemetryCorrelationReport,
    OperationalAnalyticsReport,
    AnomalyDetectionReport,
    TrendAnalysisReport,
    CapacityForecastReport,
    RecommendationEngineReport,
    ExecutiveDashboardReport,
    DecisionSupportReport,
    ContinuousInsightReport,
    OperationalIntelligenceScorecard,
)


class ITelemetryCorrelationVerifier(ABC):
    @abstractmethod
    def verify_telemetry_correlation(self) -> TelemetryCorrelationReport:
        pass


class IOperationalAnalyticsVerifier(ABC):
    @abstractmethod
    def verify_operational_analytics(self) -> OperationalAnalyticsReport:
        pass


class IAnomalyDetectionVerifier(ABC):
    @abstractmethod
    def verify_anomaly_detection(self) -> AnomalyDetectionReport:
        pass


class ITrendAnalysisVerifier(ABC):
    @abstractmethod
    def verify_trend_analysis(self) -> TrendAnalysisReport:
        pass


class ICapacityForecastVerifier(ABC):
    @abstractmethod
    def verify_capacity_forecasting(self) -> CapacityForecastReport:
        pass


class IRecommendationEngineVerifier(ABC):
    @abstractmethod
    def verify_recommendation_engine(self) -> RecommendationEngineReport:
        pass


class IExecutiveDashboardVerifier(ABC):
    @abstractmethod
    def generate_executive_dashboard(self) -> ExecutiveDashboardReport:
        pass


class IDecisionSupportVerifier(ABC):
    @abstractmethod
    def verify_decision_support(self) -> DecisionSupportReport:
        pass


class IContinuousInsightVerifier(ABC):
    @abstractmethod
    def verify_continuous_insights(self) -> ContinuousInsightReport:
        pass


class IOperationalIntelligenceScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        corr_report: TelemetryCorrelationReport,
        analytics_report: OperationalAnalyticsReport,
        anomaly_report: AnomalyDetectionReport,
        trend_report: TrendAnalysisReport,
        forecast_report: CapacityForecastReport,
        recom_report: RecommendationEngineReport,
        dash_report: ExecutiveDashboardReport,
        decision_report: DecisionSupportReport,
        insight_report: ContinuousInsightReport,
    ) -> OperationalIntelligenceScorecard:
        pass
