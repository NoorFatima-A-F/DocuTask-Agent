"""Incident Automation Runtime Coordinator.

Unites all 13 subsystems of the Enterprise Incident Response Automation & Self-Healing Verification Framework.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from app.platform_verification.incident_response_automation.architecture.incident_arch_verifier import (
    IncidentArchVerifier,
)
from app.platform_verification.incident_response_automation.cicd.cicd_incident_verifier import (
    CICDIncidentVerifier,
)
from app.platform_verification.incident_response_automation.classifier.incident_classifier import (
    IncidentClassifier,
)
from app.platform_verification.incident_response_automation.correlation.incident_correlation_engine import (
    IncidentCorrelationEngine,
)
from app.platform_verification.incident_response_automation.detector.incident_detector import (
    IncidentDetector,
)
from app.platform_verification.incident_response_automation.domain.models import (
    CICDPipelineReport,
    IncidentArchitectureReport,
    IncidentClassificationReport,
    IncidentCorrelationReport,
    IncidentDetectionReport,
    IncidentKnowledgeReport,
    IncidentQualityScorecard,
    IncidentSecurityReport,
    PostmortemReport,
    RecoveryPolicyReport,
    RunbookExecutionReport,
    SelfHealingReport,
)
from app.platform_verification.incident_response_automation.exporter.incident_evidence_exporter import (
    IncidentEvidenceExporter,
)
from app.platform_verification.incident_response_automation.healing.self_healing_engine import (
    SelfHealingEngine,
)
from app.platform_verification.incident_response_automation.knowledge.incident_knowledge_base import (
    IncidentKnowledgeBase,
)
from app.platform_verification.incident_response_automation.postmortem.postmortem_generator import (
    PostmortemGenerator,
)
from app.platform_verification.incident_response_automation.runbooks.runbook_engine import (
    RunbookEngine,
)
from app.platform_verification.incident_response_automation.safety.recovery_policy_engine import (
    RecoveryPolicyEngine,
)
from app.platform_verification.incident_response_automation.scoring.incident_quality_scorer import (
    IncidentQualityScorer,
)
from app.platform_verification.incident_response_automation.security.incident_security_auditor import (
    IncidentSecurityAuditor,
)


class IncidentAutomationRuntime:
    """Master runtime orchestrator for incident response automation verification."""

    def __init__(
        self,
        runbooks_dir: Optional[Path | str] = None,
        export_dir: Optional[Path | str] = None,
    ) -> None:
        self.runbooks_dir = Path(runbooks_dir or "runbooks")
        self.export_dir = Path(export_dir or "incident_response_verification")
        self.arch_verifier = IncidentArchVerifier()
        self.detector = IncidentDetector()
        self.classifier = IncidentClassifier()
        self.runbook_engine = RunbookEngine(runbooks_dir=self.runbooks_dir)
        self.healing_engine = SelfHealingEngine()
        self.policy_engine = RecoveryPolicyEngine()
        self.correlation_engine = IncidentCorrelationEngine()
        self.knowledge_base = IncidentKnowledgeBase()
        self.postmortem_gen = PostmortemGenerator()
        self.security_auditor = IncidentSecurityAuditor()
        self.cicd_verifier = CICDIncidentVerifier()
        self.scorer = IncidentQualityScorer()
        self.evidence_exporter = IncidentEvidenceExporter(output_dir=self.export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Runs the complete verification lifecycle across all 13 subsystems."""
        # 1. Architecture Verification
        arch_report: IncidentArchitectureReport = self.arch_verifier.verify_architecture()

        # 2. Automated Incident Detection
        detect_report: IncidentDetectionReport = self.detector.detect_incidents()

        # 3. Incident Classification
        class_report: IncidentClassificationReport = self.classifier.classify_incidents()

        # 4. Runbook Execution & Validation
        runbook_report: RunbookExecutionReport = self.runbook_engine.execute_runbook("restart_worker.yaml")

        # 5. Self-Healing Verification
        healing_report: SelfHealingReport = self.healing_engine.execute_self_healing_tests()

        # 6. Recovery Safety Policy Evaluation
        policy_report: RecoveryPolicyReport = self.policy_engine.evaluate_recovery_policies()

        # 7. Incident Cross-Signal Correlation
        correlation_report: IncidentCorrelationReport = self.correlation_engine.correlate_incident()

        # 8. Operational Knowledge Base
        knowledge_report: IncidentKnowledgeReport = self.knowledge_base.get_knowledge_report()

        # 9. Postmortem Generation
        postmortem_report: PostmortemReport = self.postmortem_gen.generate_postmortem()

        # 10. Security Audit
        security_report: IncidentSecurityReport = self.security_auditor.audit_security()

        # 11. CI/CD Integration
        cicd_report: CICDPipelineReport = self.cicd_verifier.verify_pipeline()

        # 12. Scorecard Calculation
        scorecard: IncidentQualityScorecard = self.scorer.compute_scorecard(
            arch_report=arch_report,
            detect_report=detect_report,
            class_report=class_report,
            runbook_report=runbook_report,
            healing_report=healing_report,
            policy_report=policy_report,
            correlation_report=correlation_report,
            knowledge_report=knowledge_report,
            postmortem_report=postmortem_report,
            security_report=security_report,
        )

        # 13. Export Evidence Manifests (10 JSON files)
        manifest_files = self.evidence_exporter.export_all(
            arch_report=arch_report,
            detect_report=detect_report,
            class_report=class_report,
            runbook_report=runbook_report,
            healing_report=healing_report,
            policy_report=policy_report,
            correlation_report=correlation_report,
            knowledge_report=knowledge_report,
            postmortem_report=postmortem_report,
            security_report=security_report,
            cicd_report=cicd_report,
            scorecard=scorecard,
            additional_metadata={
                "subsystems_count": len(arch_report.subsystems),
                "signals_detected_count": detect_report.total_signals_detected,
                "classified_incidents_count": class_report.total_classified_incidents,
                "self_healing_avg_mttr": healing_report.avg_mttr_seconds,
                "knowledge_entries_count": knowledge_report.total_knowledge_entries,
                "cicd_pipeline_stages": len(cicd_report.stages_executed),
            },
        )

        return {
            "scorecard": scorecard,
            "manifest_files": manifest_files,
            "arch_report": arch_report,
            "detect_report": detect_report,
            "class_report": class_report,
            "runbook_report": runbook_report,
            "healing_report": healing_report,
            "policy_report": policy_report,
            "correlation_report": correlation_report,
            "knowledge_report": knowledge_report,
            "postmortem_report": postmortem_report,
            "security_report": security_report,
            "cicd_report": cicd_report,
        }
