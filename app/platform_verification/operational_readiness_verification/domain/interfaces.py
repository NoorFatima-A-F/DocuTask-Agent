"""
Phase 3H.4.11: Operational Readiness Scoring - Abstract Interfaces
"""
from abc import ABC, abstractmethod
from typing import List
from .models import (
    MetricsCompletenessScore,
    MonitoringAccuracyScore,
    AlertReliabilityScore,
    IncidentQualityScore,
    DashboardUsabilityScore,
    SecurityReadinessScore,
    MaturityReport,
    OperationalRiskReport,
    CertificationResult,
    RemediationReport,
    OperationalReadinessScorecard,
)


class IMetricsCompletenessEvaluator(ABC):
    @abstractmethod
    def evaluate_metrics_completeness(self) -> MetricsCompletenessScore:
        pass


class IMonitoringAccuracyEvaluator(ABC):
    @abstractmethod
    def evaluate_monitoring_accuracy(self) -> MonitoringAccuracyScore:
        pass


class IAlertReliabilityEvaluator(ABC):
    @abstractmethod
    def evaluate_alert_reliability(self) -> AlertReliabilityScore:
        pass


class IIncidentQualityEvaluator(ABC):
    @abstractmethod
    def evaluate_incident_quality(self) -> IncidentQualityScore:
        pass


class IDashboardUsabilityEvaluator(ABC):
    @abstractmethod
    def evaluate_dashboard_usability(self) -> DashboardUsabilityScore:
        pass


class ISecurityReadinessEvaluator(ABC):
    @abstractmethod
    def evaluate_security_readiness(self) -> SecurityReadinessScore:
        pass


class IMaturityClassifier(ABC):
    @abstractmethod
    def classify_maturity(self, composite_score: float, risk_report: OperationalRiskReport) -> MaturityReport:
        pass


class IOperationalRiskAnalyzer(ABC):
    @abstractmethod
    def analyze_operational_risks(
        self,
        metrics_score: MetricsCompletenessScore,
        monitoring_score: MonitoringAccuracyScore,
        alert_score: AlertReliabilityScore,
        incident_score: IncidentQualityScore,
        dashboard_score: DashboardUsabilityScore,
        security_score: SecurityReadinessScore,
    ) -> OperationalRiskReport:
        pass


class ICertificationDecisionEngine(ABC):
    @abstractmethod
    def evaluate_certification(
        self,
        composite_score: float,
        maturity_report: MaturityReport,
        risk_report: OperationalRiskReport,
    ) -> CertificationResult:
        pass


class IRemediationRecommendationGenerator(ABC):
    @abstractmethod
    def generate_recommendations(
        self,
        metrics_score: MetricsCompletenessScore,
        monitoring_score: MonitoringAccuracyScore,
        alert_score: AlertReliabilityScore,
        incident_score: IncidentQualityScore,
        dashboard_score: DashboardUsabilityScore,
        security_score: SecurityReadinessScore,
        risk_report: OperationalRiskReport,
    ) -> RemediationReport:
        pass


class IReadinessEvidenceExporter(ABC):
    @abstractmethod
    def export_evidence_manifests(
        self,
        output_dir: str,
        scorecard: OperationalReadinessScorecard,
    ) -> List[str]:
        pass
