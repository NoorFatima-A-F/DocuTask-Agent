"""
Phase 3I.5: Runtime Orchestrator for Enterprise Alerting & Incident Detection Verification
"""
from typing import Dict, Any
from ..domain.models import (
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
from ..verifiers.alerting_architecture_verifier import AlertingArchitectureVerifier
from ..verifiers.alert_signal_coverage_verifier import AlertSignalCoverageVerifier
from ..verifiers.alert_rule_engineering_verifier import AlertRuleEngineeringVerifier
from ..verifiers.ai_agent_alert_verifier import AIAgentAlertVerifier
from ..verifiers.severity_routing_verifier import SeverityRoutingVerifier
from ..verifiers.automated_remediation_verifier import AutomatedRemediationVerifier
from ..verifiers.alert_security_verifier import AlertSecurityVerifier
from ..verifiers.alert_testing_simulation_verifier import AlertTestingSimulationVerifier
from ..scoring.alerting_quality_scorer import AlertingQualityScorer
from ..exporter.alerting_evidence_exporter import AlertingEvidenceExporter


class AlertingVerificationRuntime:
    """
    Orchestrates all Phase 3I.5 alerting and incident detection verification engines, executes 6-pillar quality scoring, and exports signed evidence manifests.
    """

    def __init__(self):
        self.arch_verifier = AlertingArchitectureVerifier()
        self.signal_verifier = AlertSignalCoverageVerifier()
        self.rule_verifier = AlertRuleEngineeringVerifier()
        self.ai_verifier = AIAgentAlertVerifier()
        self.routing_verifier = SeverityRoutingVerifier()
        self.remediation_verifier = AutomatedRemediationVerifier()
        self.sec_verifier = AlertSecurityVerifier()
        self.testing_verifier = AlertTestingSimulationVerifier()
        self.scorer = AlertingQualityScorer()
        self.exporter = AlertingEvidenceExporter()

    def run_full_verification(self, export_dir: str = "observability_verification/alerting") -> Dict[str, Any]:
        arch_report: AlertingArchitectureReport = self.arch_verifier.verify_alerting_architecture()
        signal_report: AlertSignalCoverageReport = self.signal_verifier.verify_signal_coverage()
        rule_report: AlertRulesReport = self.rule_verifier.verify_alert_rules()
        ai_report: AIAgentAlertReport = self.ai_verifier.verify_ai_agent_alerts()
        routing_report: IncidentSeverityReport = self.routing_verifier.verify_severity_routing()
        remediation_report: RemediationReport = self.remediation_verifier.verify_remediation_workflows()
        sec_report: AlertSecurityReport = self.sec_verifier.verify_alert_security()
        testing_report: AlertTestingReport = self.testing_verifier.verify_alert_testing_scenarios()

        certification_report: AlertingCertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            signal_report=signal_report,
            rule_report=rule_report,
            ai_report=ai_report,
            routing_report=routing_report,
            remediation_report=remediation_report,
            sec_report=sec_report,
            testing_report=testing_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            signal_report=signal_report,
            rule_report=rule_report,
            ai_report=ai_report,
            routing_report=routing_report,
            remediation_report=remediation_report,
            sec_report=sec_report,
            testing_report=testing_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "signal_report": signal_report,
            "rule_report": rule_report,
            "ai_report": ai_report,
            "routing_report": routing_report,
            "remediation_report": remediation_report,
            "sec_report": sec_report,
            "testing_report": testing_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
