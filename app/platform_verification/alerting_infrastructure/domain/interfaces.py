"""
Phase 3I.5: Enterprise Alerting & Incident Detection Verification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    AlertingArchitectureReport,
    AlertSignalCoverageReport,
    AlertRulesReport,
    AIAgentAlertReport,
    IncidentSeverityReport,
    RemediationReport,
    AlertSecurityReport,
    AlertTestingReport,
    AlertingCertificationReport,
)


class IAlertingArchitectureVerifier(ABC):
    @abstractmethod
    def verify_alerting_architecture(self) -> AlertingArchitectureReport:
        pass


class IAlertSignalCoverageVerifier(ABC):
    @abstractmethod
    def verify_signal_coverage(self) -> AlertSignalCoverageReport:
        pass


class IAlertRuleEngineeringVerifier(ABC):
    @abstractmethod
    def verify_alert_rules(self) -> AlertRulesReport:
        pass


class IAIAgentAlertVerifier(ABC):
    @abstractmethod
    def verify_ai_agent_alerts(self) -> AIAgentAlertReport:
        pass


class ISeverityRoutingVerifier(ABC):
    @abstractmethod
    def verify_severity_routing(self) -> IncidentSeverityReport:
        pass


class IAutomatedRemediationVerifier(ABC):
    @abstractmethod
    def verify_remediation_workflows(self) -> RemediationReport:
        pass


class IAlertSecurityVerifier(ABC):
    @abstractmethod
    def verify_alert_security(self) -> AlertSecurityReport:
        pass


class IAlertTestingSimulationVerifier(ABC):
    @abstractmethod
    def verify_alert_testing_scenarios(self) -> AlertTestingReport:
        pass


class IAlertingQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: AlertingArchitectureReport,
        signal_report: AlertSignalCoverageReport,
        rule_report: AlertRulesReport,
        ai_report: AIAgentAlertReport,
        routing_report: IncidentSeverityReport,
        remediation_report: RemediationReport,
        sec_report: AlertSecurityReport,
        testing_report: AlertTestingReport,
    ) -> AlertingCertificationReport:
        pass


class IAlertingEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AlertingArchitectureReport,
        signal_report: AlertSignalCoverageReport,
        rule_report: AlertRulesReport,
        ai_report: AIAgentAlertReport,
        routing_report: IncidentSeverityReport,
        remediation_report: RemediationReport,
        sec_report: AlertSecurityReport,
        testing_report: AlertTestingReport,
        certification_report: AlertingCertificationReport,
    ) -> Dict[str, Any]:
        pass
