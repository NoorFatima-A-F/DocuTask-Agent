"""
Phase 3I.8: Observability Automation, Self-Healing Operations & Autonomous Reliability — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    AutonomousArchitectureReport,
    AnomalyDetectionReport,
    EventCorrelationReport,
    RootCauseAnalysisReport,
    RemediationExecutionReport,
    AutomationSafetyReport,
    SelfHealingValidationReport,
    IncidentAutomationReport,
    ReliabilityLearningReport,
    AutonomousTestingReport,
    HumanControlPolicyReport,
    AutonomousDashboardReport,
    AutonomousCertificationReport,
)


class IArchitectureVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> AutonomousArchitectureReport:
        pass


class IAnomalyDetectionVerifier(ABC):
    @abstractmethod
    def verify_anomaly_detection(self) -> AnomalyDetectionReport:
        pass


class IEventCorrelationVerifier(ABC):
    @abstractmethod
    def verify_event_correlation(self) -> EventCorrelationReport:
        pass


class IRootCauseVerifier(ABC):
    @abstractmethod
    def verify_root_cause_analysis(self) -> RootCauseAnalysisReport:
        pass


class IRemediationVerifier(ABC):
    @abstractmethod
    def verify_automated_remediation(self) -> RemediationExecutionReport:
        pass


class ISafetyControlVerifier(ABC):
    @abstractmethod
    def verify_safety_controls(self) -> AutomationSafetyReport:
        pass


class ISelfHealingVerifier(ABC):
    @abstractmethod
    def verify_self_healing_workflows(self) -> SelfHealingValidationReport:
        pass


class IIncidentAutomationVerifier(ABC):
    @abstractmethod
    def verify_incident_automation(self) -> IncidentAutomationReport:
        pass


class IReliabilityLearningVerifier(ABC):
    @abstractmethod
    def verify_reliability_learning(self) -> ReliabilityLearningReport:
        pass


class IAutonomousTestingVerifier(ABC):
    @abstractmethod
    def verify_autonomous_testing(self) -> AutonomousTestingReport:
        pass


class IHumanControlVerifier(ABC):
    @abstractmethod
    def verify_human_control_policies(self) -> HumanControlPolicyReport:
        pass


class IAutonomousDashboardVerifier(ABC):
    @abstractmethod
    def verify_autonomous_dashboards(self) -> AutonomousDashboardReport:
        pass


class IAutonomousReliabilityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: AutonomousArchitectureReport,
        anomaly_report: AnomalyDetectionReport,
        corr_report: EventCorrelationReport,
        rca_report: RootCauseAnalysisReport,
        remediation_report: RemediationExecutionReport,
        safety_report: AutomationSafetyReport,
        healing_report: SelfHealingValidationReport,
        incident_report: IncidentAutomationReport,
        learning_report: ReliabilityLearningReport,
        testing_report: AutonomousTestingReport,
        human_report: HumanControlPolicyReport,
        dash_report: AutonomousDashboardReport,
    ) -> AutonomousCertificationReport:
        pass


class IObservabilityAutomationEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AutonomousArchitectureReport,
        anomaly_report: AnomalyDetectionReport,
        corr_report: EventCorrelationReport,
        rca_report: RootCauseAnalysisReport,
        remediation_report: RemediationExecutionReport,
        safety_report: AutomationSafetyReport,
        healing_report: SelfHealingValidationReport,
        incident_report: IncidentAutomationReport,
        learning_report: ReliabilityLearningReport,
        testing_report: AutonomousTestingReport,
        human_report: HumanControlPolicyReport,
        dash_report: AutonomousDashboardReport,
        certification_report: AutonomousCertificationReport,
    ) -> Dict[str, Any]:
        pass
