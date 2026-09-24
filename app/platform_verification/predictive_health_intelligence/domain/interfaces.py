"""
Abstract interfaces and protocols for Part 3H.3.4.
"""
from typing import Protocol
from app.platform_verification.predictive_health_intelligence.domain.models import (
    TelemetryReport,
    BaselineReport,
    AnomalyReport,
    RiskPredictionReport,
    EarlyWarningReport,
    RecommendationReport,
    AccuracyReport,
    PredictiveHealthScorecard,
)


class IHealthTelemetryCollector(Protocol):
    def collect_telemetry(self) -> TelemetryReport: ...


class IHealthBaselineManager(Protocol):
    def get_baseline_report(self) -> BaselineReport: ...


class IHealthAnomalyDetector(Protocol):
    def detect_anomalies(self) -> AnomalyReport: ...


class IHealthRiskEngine(Protocol):
    def compute_risk_predictions(self) -> RiskPredictionReport: ...


class IEarlyWarningSystem(Protocol):
    def generate_early_warnings(self) -> EarlyWarningReport: ...


class IPreventiveActionRecommender(Protocol):
    def generate_recommendations(self) -> RecommendationReport: ...


class IFalsePositiveValidator(Protocol):
    def evaluate_accuracy(self) -> AccuracyReport: ...


class IPredictiveHealthScorer(Protocol):
    def compute_scorecard(
        self,
        telemetry_rep: TelemetryReport,
        baseline_rep: BaselineReport,
        anomaly_rep: AnomalyReport,
        risk_rep: RiskPredictionReport,
        warning_rep: EarlyWarningReport,
        rec_rep: RecommendationReport,
        accuracy_rep: AccuracyReport,
        observability_valid: bool,
    ) -> PredictiveHealthScorecard: ...
