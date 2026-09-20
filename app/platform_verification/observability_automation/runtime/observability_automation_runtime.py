"""
Phase 3I.8: Observability Automation, Self-Healing Operations & Autonomous Reliability Runtime
Orchestrates all 12 autonomous verifiers, the 6-pillar scoring engine, and the SHA-256 evidence exporter.
"""
import logging
from typing import Dict, Any

from ..verifiers.architecture_verifier import ArchitectureVerifier
from ..verifiers.anomaly_detection_verifier import AnomalyDetectionVerifier
from ..verifiers.event_correlation_verifier import EventCorrelationVerifier
from ..verifiers.root_cause_verifier import RootCauseVerifier
from ..verifiers.remediation_verifier import RemediationVerifier
from ..verifiers.safety_control_verifier import SafetyControlVerifier
from ..verifiers.self_healing_verifier import SelfHealingVerifier
from ..verifiers.incident_automation_verifier import IncidentAutomationVerifier
from ..verifiers.reliability_learning_verifier import ReliabilityLearningVerifier
from ..verifiers.autonomous_testing_verifier import AutonomousTestingVerifier
from ..verifiers.human_control_verifier import HumanControlVerifier
from ..verifiers.autonomous_dashboard_verifier import AutonomousDashboardVerifier
from ..scoring.autonomous_reliability_scorer import AutonomousReliabilityScorer
from ..exporter.observability_automation_evidence_exporter import ObservabilityAutomationEvidenceExporter

logger = logging.getLogger(__name__)


class ObservabilityAutomationRuntime:
    def __init__(
        self,
        output_dir: str = "observability_automation_verification",
    ):
        self.output_dir = output_dir
        self.arch_verifier = ArchitectureVerifier()
        self.anomaly_verifier = AnomalyDetectionVerifier()
        self.corr_verifier = EventCorrelationVerifier()
        self.rca_verifier = RootCauseVerifier()
        self.remediation_verifier = RemediationVerifier()
        self.safety_verifier = SafetyControlVerifier()
        self.healing_verifier = SelfHealingVerifier()
        self.incident_verifier = IncidentAutomationVerifier()
        self.learning_verifier = ReliabilityLearningVerifier()
        self.testing_verifier = AutonomousTestingVerifier()
        self.human_verifier = HumanControlVerifier()
        self.dash_verifier = AutonomousDashboardVerifier()
        self.scorer = AutonomousReliabilityScorer()
        self.exporter = ObservabilityAutomationEvidenceExporter()

    def run_full_verification(self) -> Dict[str, Any]:
        logger.info("Starting Phase 3I.8 Observability Automation & Autonomous Operations Verification Suite...")

        # 1. Execute all 12 verification stages
        arch_report = self.arch_verifier.verify_architecture()
        anomaly_report = self.anomaly_verifier.verify_anomaly_detection()
        corr_report = self.corr_verifier.verify_event_correlation()
        rca_report = self.rca_verifier.verify_root_cause_analysis()
        remediation_report = self.remediation_verifier.verify_automated_remediation()
        safety_report = self.safety_verifier.verify_safety_controls()
        healing_report = self.healing_verifier.verify_self_healing_workflows()
        incident_report = self.incident_verifier.verify_incident_automation()
        learning_report = self.learning_verifier.verify_reliability_learning()
        testing_report = self.testing_verifier.verify_autonomous_testing()
        human_report = self.human_verifier.verify_human_control_policies()
        dash_report = self.dash_verifier.verify_autonomous_dashboards()

        # 2. Compute 6-pillar score and certification
        cert_report = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            anomaly_report=anomaly_report,
            corr_report=corr_report,
            rca_report=rca_report,
            remediation_report=remediation_report,
            safety_report=safety_report,
            healing_report=healing_report,
            incident_report=incident_report,
            learning_report=learning_report,
            testing_report=testing_report,
            human_report=human_report,
            dash_report=dash_report,
        )

        # 3. Export all JSON artifacts with SHA-256 signatures to output directory
        metadata = self.exporter.export_all_reports(
            output_dir=self.output_dir,
            arch_report=arch_report,
            anomaly_report=anomaly_report,
            corr_report=corr_report,
            rca_report=rca_report,
            remediation_report=remediation_report,
            safety_report=safety_report,
            healing_report=healing_report,
            incident_report=incident_report,
            learning_report=learning_report,
            testing_report=testing_report,
            human_report=human_report,
            dash_report=dash_report,
            certification_report=cert_report,
        )

        return {
            "status": "SUCCESS" if cert_report.certification_granted else "FAILED",
            "certification_tier": cert_report.certification_tier.value,
            "overall_score_pct": cert_report.overall_score_pct,
            "certification_granted": cert_report.certification_granted,
            "architecture_report": arch_report.model_dump(mode="json"),
            "anomaly_report": anomaly_report.model_dump(mode="json"),
            "correlation_report": corr_report.model_dump(mode="json"),
            "root_cause_report": rca_report.model_dump(mode="json"),
            "remediation_report": remediation_report.model_dump(mode="json"),
            "safety_report": safety_report.model_dump(mode="json"),
            "self_healing_report": healing_report.model_dump(mode="json"),
            "incident_report": incident_report.model_dump(mode="json"),
            "learning_report": learning_report.model_dump(mode="json"),
            "testing_report": testing_report.model_dump(mode="json"),
            "human_control_policy_report": human_report.model_dump(mode="json"),
            "autonomous_dashboard_report": dash_report.model_dump(mode="json"),
            "certification_report": cert_report.model_dump(mode="json"),
            "metadata": metadata,
        }
