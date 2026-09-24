"""
Enterprise Readiness Contract Runtime Coordinator
Executes full verification workflow across all 13 subsystems.
"""
from typing import Dict, Any

from app.platform_verification.readiness_contract.state_machine.readiness_state_machine import ReadinessStateMachine
from app.platform_verification.readiness_contract.contract.readiness_contract_manager import ReadinessContractManager
from app.platform_verification.readiness_contract.decision.readiness_decision_engine import ReadinessDecisionEngine
from app.platform_verification.readiness_contract.policy.readiness_policy_engine import ReadinessPolicyEngine
from app.platform_verification.readiness_contract.startup.startup_readiness_validator import StartupReadinessValidator
from app.platform_verification.readiness_contract.transitions.failure_transition_tester import FailureTransitionTester
from app.platform_verification.readiness_contract.orchestration.readiness_orchestration_verifier import ReadinessOrchestrationVerifier
from app.platform_verification.readiness_contract.security.readiness_security_verifier import ReadinessSecurityVerifier
from app.platform_verification.readiness_contract.observability.readiness_metrics_exporter import ReadinessMetricsExporter
from app.platform_verification.readiness_contract.scoring.readiness_score_engine import ReadinessScoreEngine
from app.platform_verification.readiness_contract.exporter.readiness_evidence_exporter import ReadinessEvidenceExporter


class ReadinessRuntime:
    """
    Master coordinator for Enterprise Readiness Contract Architecture Verification.
    Orchestrates all verification components, generates reports, computes scores,
    and exports evidence artifacts.
    """

    def __init__(self, policy_path: str = "readiness_policy.yaml", evidence_dir: str = "readiness_verification"):
        self.state_machine = ReadinessStateMachine()
        self.contract_manager = ReadinessContractManager()
        self.decision_engine = ReadinessDecisionEngine()
        self.policy_engine = ReadinessPolicyEngine(policy_path=policy_path)
        self.startup_validator = StartupReadinessValidator()
        self.transition_tester = FailureTransitionTester()
        self.orchestration_verifier = ReadinessOrchestrationVerifier()
        self.security_verifier = ReadinessSecurityVerifier()
        self.metrics_exporter = ReadinessMetricsExporter()
        self.score_engine = ReadinessScoreEngine()
        self.evidence_exporter = ReadinessEvidenceExporter(output_dir=evidence_dir)

    def execute_full_verification(self) -> Dict[str, Any]:
        """
        Executes end-to-end readiness verification across all categories.
        Returns comprehensive dictionary of reports, scorecard, and exported paths.
        """
        # 1. State Machine Verification
        sm_report = self.state_machine.verify_state_machine()

        # 2. Contract Schema Verification
        contract_report = self.contract_manager.validate_readiness_contract()

        # 3. Policy & Dependency Modeling Verification
        policy_report = self.policy_engine.evaluate_policy()

        # 4. Startup Sequence Verification
        startup_report = self.startup_validator.validate_startup_sequence()

        # 5. Failure & Transition Testing
        transition_report = self.transition_tester.test_failure_transitions()

        # 6. Orchestration & Probe Compatibility
        orch_report = self.orchestration_verifier.verify_orchestration()

        # 7. Security Verification
        sec_report = self.security_verifier.verify_security()
        sec_passed = sec_report.get("passed", False)

        # 8. Observability & Metrics Export
        metrics_summary = self.metrics_exporter.get_metrics_summary()
        prometheus_text = self.metrics_exporter.generate_prometheus_payload()
        obs_passed = metrics_summary.get("prometheus_compatible", False)

        # 9. Compute Scorecard
        scorecard = self.score_engine.compute_scorecard(
            contract_report=contract_report,
            state_report=sm_report,
            policy_report=policy_report,
            startup_report=startup_report,
            failure_report=transition_report,
            orchestration_report=orch_report,
            security_passed=sec_passed,
            observability_passed=obs_passed,
        )

        # 10. Export Evidence
        exported_files = self.evidence_exporter.export_all(
            contract_report=contract_report,
            state_report=sm_report,
            policy_report=policy_report,
            startup_report=startup_report,
            failure_report=transition_report,
            orch_report=orch_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "contract_report": contract_report,
            "sm_report": sm_report,
            "policy_report": policy_report,
            "startup_report": startup_report,
            "transition_report": transition_report,
            "orch_report": orch_report,
            "security_report": sec_report,
            "metrics_summary": metrics_summary,
            "prometheus_text": prometheus_text,
            "exported_files": exported_files,
        }
