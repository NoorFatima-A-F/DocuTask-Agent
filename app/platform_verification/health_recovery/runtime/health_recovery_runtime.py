"""
Phase 3H.5.12: Automated Health Recovery Runtime Orchestrator
"""
from typing import Dict, Any, Optional

from ..verifiers import (
    HealthStateVerifier,
    FailureDetectionVerifier,
    RecoveryPolicyVerifier,
    ComponentRecoveryVerifier,
    RecoverySafetyVerifier,
    SelfHealingVerifier,
    RecoveryChaosVerifier,
    RecoveryValidationVerifier,
    RecoveryObservabilityVerifier,
    RecoverySecurityVerifier,
)
from ..scoring import HealthRecoveryScorer
from ..exporter import HealthRecoveryExporter
from ..domain.models import HealthRecoveryScorecard


class HealthRecoveryRuntime:
    """
    Main runtime orchestrator for executing Phase 3H.5.12:
    - Runs all 10 recovery verifications
    - Computes 6-pillar operational readiness scorecard
    - Exports 12 standardized evidence files and cryptographic metadata manifest
    """

    def __init__(
        self,
        output_dir: str = "health_recovery_verification",
        state_verifier: Optional[HealthStateVerifier] = None,
        detection_verifier: Optional[FailureDetectionVerifier] = None,
        policy_verifier: Optional[RecoveryPolicyVerifier] = None,
        component_verifier: Optional[ComponentRecoveryVerifier] = None,
        safety_verifier: Optional[RecoverySafetyVerifier] = None,
        self_healing_verifier: Optional[SelfHealingVerifier] = None,
        chaos_verifier: Optional[RecoveryChaosVerifier] = None,
        validation_verifier: Optional[RecoveryValidationVerifier] = None,
        observability_verifier: Optional[RecoveryObservabilityVerifier] = None,
        security_verifier: Optional[RecoverySecurityVerifier] = None,
        scorer: Optional[HealthRecoveryScorer] = None,
        exporter: Optional[HealthRecoveryExporter] = None,
    ):
        self.output_dir = output_dir
        self.state_verifier = state_verifier or HealthStateVerifier()
        self.detection_verifier = detection_verifier or FailureDetectionVerifier()
        self.policy_verifier = policy_verifier or RecoveryPolicyVerifier()
        self.component_verifier = component_verifier or ComponentRecoveryVerifier()
        self.safety_verifier = safety_verifier or RecoverySafetyVerifier()
        self.self_healing_verifier = self_healing_verifier or SelfHealingVerifier()
        self.chaos_verifier = chaos_verifier or RecoveryChaosVerifier()
        self.validation_verifier = validation_verifier or RecoveryValidationVerifier()
        self.observability_verifier = observability_verifier or RecoveryObservabilityVerifier()
        self.security_verifier = security_verifier or RecoverySecurityVerifier()
        self.scorer = scorer or HealthRecoveryScorer()
        self.exporter = exporter or HealthRecoveryExporter(output_dir=self.output_dir)

    def run_full_recovery_verification(self) -> Dict[str, Any]:
        # Step 1: Execute all 10 recovery verification modules
        transition_report = self.state_verifier.verify_state_transitions()
        detection_report = self.detection_verifier.verify_failure_detection()
        policy_report = self.policy_verifier.verify_recovery_policies()
        component_report = self.component_verifier.verify_component_recovery()
        safety_report = self.safety_verifier.verify_recovery_safety()
        self_healing_report = self.self_healing_verifier.verify_self_healing_workflow()
        chaos_report = self.chaos_verifier.execute_chaos_testing()
        validation_report = self.validation_verifier.verify_recovery_validation()
        observability_report = self.observability_verifier.verify_recovery_observability()
        security_report = self.security_verifier.verify_recovery_security()

        # Step 2: Compute master scorecard
        scorecard: HealthRecoveryScorecard = self.scorer.calculate_scorecard(
            transition_report=transition_report,
            detection_report=detection_report,
            policy_report=policy_report,
            component_report=component_report,
            safety_report=safety_report,
            self_healing_report=self_healing_report,
            chaos_report=chaos_report,
            validation_report=validation_report,
            observability_report=observability_report,
            security_report=security_report,
        )

        # Step 3: Export evidence manifests with SHA-256 signatures
        exported_files = self.exporter.export_all(
            transition_report=transition_report,
            detection_report=detection_report,
            policy_report=policy_report,
            component_report=component_report,
            safety_report=safety_report,
            self_healing_report=self_healing_report,
            chaos_report=chaos_report,
            validation_report=validation_report,
            observability_report=observability_report,
            security_report=security_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "transition_report": transition_report,
            "detection_report": detection_report,
            "policy_report": policy_report,
            "component_report": component_report,
            "safety_report": safety_report,
            "self_healing_report": self_healing_report,
            "chaos_report": chaos_report,
            "validation_report": validation_report,
            "observability_report": observability_report,
            "security_report": security_report,
            "exported_files": exported_files,
        }
