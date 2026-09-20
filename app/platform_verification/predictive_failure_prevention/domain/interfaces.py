"""
Phase 3H.5.9: Domain Interfaces for Predictive Health Intelligence & Proactive Failure Prevention
"""
from abc import ABC, abstractmethod
from .models import (
    PredictiveArchitectureReport,
    FeatureEngineeringReport,
    AnomalyDetectionReport,
    FailurePredictionReport,
    CapacityPredictionReport,
    ProactiveRemediationReport,
    PredictionAccuracyReport,
    PredictiveIncidentReport,
    ReliabilityTwinReport,
    ChaosPredictionReport,
    PredictiveDashboardReport,
    PredictiveHealthScorecard,
)


class IPredictiveArchitectureVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> PredictiveArchitectureReport:
        pass


class IFeatureEngineeringVerifier(ABC):
    @abstractmethod
    def verify_feature_engineering(self) -> FeatureEngineeringReport:
        pass


class IAnomalyDetectionVerifier(ABC):
    @abstractmethod
    def verify_anomaly_detection(self) -> AnomalyDetectionReport:
        pass


class IFailurePredictionVerifier(ABC):
    @abstractmethod
    def verify_failure_predictions(self) -> FailurePredictionReport:
        pass


class ICapacityPredictionVerifier(ABC):
    @abstractmethod
    def verify_capacity_predictions(self) -> CapacityPredictionReport:
        pass


class IProactiveRemediationVerifier(ABC):
    @abstractmethod
    def verify_proactive_remediation(self) -> ProactiveRemediationReport:
        pass


class IPredictionAccuracyVerifier(ABC):
    @abstractmethod
    def verify_prediction_accuracy(self) -> PredictionAccuracyReport:
        pass


class IPredictiveIncidentVerifier(ABC):
    @abstractmethod
    def verify_predictive_incidents(self) -> PredictiveIncidentReport:
        pass


class IReliabilityTwinVerifier(ABC):
    @abstractmethod
    def verify_reliability_twin(self) -> ReliabilityTwinReport:
        pass


class IChaosPredictionVerifier(ABC):
    @abstractmethod
    def verify_chaos_predictions(self) -> ChaosPredictionReport:
        pass


class IPredictiveDashboardVerifier(ABC):
    @abstractmethod
    def verify_predictive_dashboards(self) -> PredictiveDashboardReport:
        pass


class IPredictiveHealthScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        arch_report: PredictiveArchitectureReport,
        feature_report: FeatureEngineeringReport,
        anomaly_report: AnomalyDetectionReport,
        prediction_report: FailurePredictionReport,
        capacity_report: CapacityPredictionReport,
        remediation_report: ProactiveRemediationReport,
        accuracy_report: PredictionAccuracyReport,
        incident_report: PredictiveIncidentReport,
        twin_report: ReliabilityTwinReport,
        chaos_report: ChaosPredictionReport,
        dashboard_report: PredictiveDashboardReport,
    ) -> PredictiveHealthScorecard:
        pass
