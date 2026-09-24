"""
Phase 3I.10: Observability Operations Governance Runtime Orchestrator
Coordinates all 10 verifiers, executes certification scoring, and exports evidence manifests.
"""
from typing import Dict, Any
from app.platform_verification.observability_operations_governance.verifiers import (
    GovernanceArchitectureVerifier,
    PolicyManagementVerifier,
    ReliabilityMaturityVerifier,
    SREManagementVerifier,
    RunbookAutomationVerifier,
    AutomationSafetyVerifier,
    ChangeManagementVerifier,
    IncidentGovernanceVerifier,
    ContinuousImprovementVerifier,
    OperationsDashboardVerifier,
)
from app.platform_verification.observability_operations_governance.scoring import (
    OperationsCertificationScorer,
)
from app.platform_verification.observability_operations_governance.exporter import (
    ObservabilityGovernanceEvidenceExporter,
)


class ObservabilityOperationsRuntime:
    def __init__(self, output_dir: str = "observability_governance_verification"):
        self.output_dir = output_dir
        self.governance_arch_verifier = GovernanceArchitectureVerifier()
        self.policy_verifier = PolicyManagementVerifier()
        self.maturity_verifier = ReliabilityMaturityVerifier()
        self.sre_verifier = SREManagementVerifier()
        self.runbook_verifier = RunbookAutomationVerifier()
        self.safety_verifier = AutomationSafetyVerifier()
        self.change_verifier = ChangeManagementVerifier()
        self.incident_verifier = IncidentGovernanceVerifier()
        self.improvement_verifier = ContinuousImprovementVerifier()
        self.dashboard_verifier = OperationsDashboardVerifier()
        self.scorer = OperationsCertificationScorer()
        self.exporter = ObservabilityGovernanceEvidenceExporter(output_dir=output_dir)

    def execute_all_verifications(self) -> Dict[str, Any]:
        """Runs all 10 operational verifiers."""
        results: Dict[str, Any] = {
            "governance_architecture": self.governance_arch_verifier.verify(),
            "policy_management": self.policy_verifier.verify(),
            "maturity_model": self.maturity_verifier.verify(),
            "sre_management": self.sre_verifier.verify(),
            "runbook_automation": self.runbook_verifier.verify(),
            "automation_safety": self.safety_verifier.verify(),
            "change_management": self.change_verifier.verify(),
            "incident_governance": self.incident_verifier.verify(),
            "continuous_improvement": self.improvement_verifier.verify(),
            "operations_dashboard": self.dashboard_verifier.verify(),
        }
        return results

    def run_pipeline(self) -> Dict[str, Any]:
        """Runs full end-to-end verification, scoring, and artifact export."""
        verification_results = self.execute_all_verifications()
        certification_report = self.scorer.compute_certification(verification_results)
        exported_files = self.exporter.export(verification_results, certification_report)

        return {
            "verification_results": verification_results,
            "certification_report": certification_report,
            "exported_files": exported_files,
            "success": certification_report.autonomous_operations_certified,
        }
