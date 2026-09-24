"""
Health Verification Runtime for Health Check Architecture Verification (Part 3H.1).
"""
from typing import Dict, Any
from app.platform_verification.health_architecture.state_machine.health_state_machine import (
    HealthStateMachine,
)
from app.platform_verification.health_architecture.contracts.health_contract_manager import (
    HealthContractManager,
)
from app.platform_verification.health_architecture.dependency_graph.dependency_graph_manager import (
    DependencyGraphManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_failure_policy import (
    HealthFailurePolicyManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_security_auditor import (
    HealthSecurityAuditor,
)
from app.platform_verification.health_architecture.automation.orchestration_automation_verifier import (
    OrchestrationAutomationVerifier,
)
from app.platform_verification.health_architecture.scoring.health_score_engine import (
    HealthScoreEngine,
)
from app.platform_verification.health_architecture.exporter.health_evidence_exporter import (
    HealthEvidenceExporter,
)


class HealthVerificationRuntime:
    """
    Master Runtime Coordinator that executes full-spectrum verification of the
    Health Check Architecture, computes scorecards, and exports audit evidence.
    """

    def __init__(self, output_dir: str = "health_architecture_verification"):
        self.state_machine = HealthStateMachine()
        self.contract_manager = HealthContractManager()
        self.dep_graph_manager = DependencyGraphManager()
        self.failure_policy_manager = HealthFailurePolicyManager()
        self.security_auditor = HealthSecurityAuditor()
        self.automation_verifier = OrchestrationAutomationVerifier()
        self.score_engine = HealthScoreEngine()
        self.exporter = HealthEvidenceExporter(output_dir=output_dir)

    def run_full_verification(self, export: bool = True) -> Dict[str, Any]:
        # Step 1: Health State Machine & 4-Layer Model
        model_report = self.state_machine.verify_state_model()

        # Step 2: Universal Health Contracts (/live, /ready, /health)
        contract_report = self.contract_manager.validate_contracts()

        # Step 3: Dependency Graph & Criticality Matrix
        deps_report = self.dep_graph_manager.generate_dependency_graph()

        # Step 4: Failure Classification & Automated Response Policies
        policy_report = self.failure_policy_manager.verify_failure_policies()

        # Step 5: Role-Based Health Security & Sensitive Leak Audit
        sec_report = self.security_auditor.audit_security()

        # Step 6: Orchestration (Docker / K8s / CI/CD) Integration
        auto_report = self.automation_verifier.verify_automation_integration()

        # Step 7: Scorecard Engine
        scorecard = self.score_engine.calculate_scorecard(
            model=model_report,
            contract=contract_report,
            deps=deps_report,
            policy=policy_report,
            sec=sec_report,
            auto=auto_report,
        )

        # Step 8: Evidence Export
        exported_paths = {}
        if export:
            exported_paths = self.exporter.export_all(
                model_report=model_report,
                contract_report=contract_report,
                deps_report=deps_report,
                policy_report=policy_report,
                security_report=sec_report,
                auto_report=auto_report,
                scorecard=scorecard,
            )

        return {
            "model_report": model_report,
            "contract_report": contract_report,
            "dependency_report": deps_report,
            "policy_report": policy_report,
            "security_report": sec_report,
            "automation_report": auto_report,
            "scorecard": scorecard,
            "exported_files": exported_paths,
            "success": scorecard.passed,
        }
