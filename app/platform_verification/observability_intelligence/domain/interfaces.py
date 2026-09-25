"""
Phase 3I.9: Observability Intelligence, Predictive Reliability & AIOps Maturity — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    AIOpsArchitectureReport,
    OperationalDataQualityReport,
    FailurePredictionReport,
    CapacityForecastingReport,
    BehaviorBaselineReport,
    PredictiveAnomalyReport,
    ReliabilityIntelligenceReport,
    IncidentPreventionReport,
    DeploymentIntelligenceReport,
    AIReliabilityMonitoringReport,
    ContinuousOptimizationReport,
    AIOpsExplainabilityReport,
    AIOpsValidationReport,
    PredictiveCertificationReport,
)


class IAIOpsArchitectureVerifier(ABC):
    @abstractmethod
    def verify_aiops_architecture(self) -> AIOpsArchitectureReport:
        pass


class IOperationalDataQualityVerifier(ABC):
    @abstractmethod
    def verify_data_quality(self) -> OperationalDataQualityReport:
        pass


class IFailurePredictionVerifier(ABC):
    @abstractmethod
    def verify_failure_prediction(self) -> FailurePredictionReport:
        pass


class ICapacityForecastingVerifier(ABC):
    @abstractmethod
    def verify_capacity_forecasting(self) -> CapacityForecastingReport:
        pass


class IBehaviorBaselineVerifier(ABC):
    @abstractmethod
    def verify_behavior_baselines(self) -> BehaviorBaselineReport:
        pass


class IPredictiveAnomalyVerifier(ABC):
    @abstractmethod
    def verify_predictive_anomalies(self) -> PredictiveAnomalyReport:
        pass


class IReliabilityScoreVerifier(ABC):
    @abstractmethod
    def verify_reliability_score(self) -> ReliabilityIntelligenceReport:
        pass


class IIncidentPreventionVerifier(ABC):
    @abstractmethod
    def verify_incident_prevention(self) -> IncidentPreventionReport:
        pass


class IDeploymentIntelligenceVerifier(ABC):
    @abstractmethod
    def verify_deployment_intelligence(self) -> DeploymentIntelligenceReport:
        pass


class IAIReliabilityVerifier(ABC):
    @abstractmethod
    def verify_ai_reliability(self) -> AIReliabilityMonitoringReport:
        pass


class IContinuousOptimizationVerifier(ABC):
    @abstractmethod
    def verify_continuous_optimization(self) -> ContinuousOptimizationReport:
        pass


class IAIOpsExplainabilityVerifier(ABC):
    @abstractmethod
    def verify_aiops_explainability(self) -> AIOpsExplainabilityReport:
        pass


class IAIOpsValidationVerifier(ABC):
    @abstractmethod
    def verify_aiops_validation(self) -> AIOpsValidationReport:
        pass


class IPredictiveReliabilityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: AIOpsArchitectureReport,
        data_report: OperationalDataQualityReport,
        pred_report: FailurePredictionReport,
        capacity_report: CapacityForecastingReport,
        baseline_report: BehaviorBaselineReport,
        anomaly_report: PredictiveAnomalyReport,
        score_report: ReliabilityIntelligenceReport,
        prevention_report: IncidentPreventionReport,
        deploy_report: DeploymentIntelligenceReport,
        ai_report: AIReliabilityMonitoringReport,
        opt_report: ContinuousOptimizationReport,
        explain_report: AIOpsExplainabilityReport,
        val_report: AIOpsValidationReport,
    ) -> PredictiveCertificationReport:
        pass


class IObservabilityIntelligenceEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AIOpsArchitectureReport,
        data_report: OperationalDataQualityReport,
        pred_report: FailurePredictionReport,
        capacity_report: CapacityForecastingReport,
        baseline_report: BehaviorBaselineReport,
        anomaly_report: PredictiveAnomalyReport,
        score_report: ReliabilityIntelligenceReport,
        prevention_report: IncidentPreventionReport,
        deploy_report: DeploymentIntelligenceReport,
        ai_report: AIReliabilityMonitoringReport,
        opt_report: ContinuousOptimizationReport,
        explain_report: AIOpsExplainabilityReport,
        val_report: AIOpsValidationReport,
        certification_report: PredictiveCertificationReport,
    ) -> Dict[str, Any]:
        pass
