"""
Phase 3H.4.9: Incident Recovery Verification Runtime
"""
from typing import Dict, Any, List
from ..verifiers import (
    RecoveryArchitectureVerifier,
    ActionMappingVerifier,
    AutomatedRecoveryVerifier,
    HealthValidationVerifier,
    RecoveryMetricsVerifier,
    FailureRecoverySimulator,
    DataIntegrityVerifier,
    RecoveryRollbackVerifier,
    RecoverySafetyVerifier,
    PostIncidentImprovementVerifier,
)
from ..scoring.recovery_scorer import RecoveryScorer
from ..exporter.recovery_evidence_exporter import RecoveryEvidenceExporter
from ..domain.models import RecoveryScorecard


class RecoveryVerificationRuntime:
    def __init__(self):
        self.arch_verifier = RecoveryArchitectureVerifier()
        self.mapping_verifier = ActionMappingVerifier()
        self.auto_verifier = AutomatedRecoveryVerifier()
        self.health_verifier = HealthValidationVerifier()
        self.metrics_verifier = RecoveryMetricsVerifier()
        self.simulator = FailureRecoverySimulator()
        self.integrity_verifier = DataIntegrityVerifier()
        self.rollback_verifier = RecoveryRollbackVerifier()
        self.safety_verifier = RecoverySafetyVerifier()
        self.improvement_verifier = PostIncidentImprovementVerifier()
        self.scorer = RecoveryScorer()
        self.exporter = RecoveryEvidenceExporter()

    def run_all_verifications(self, output_dir: str = "incident_recovery_verification") -> Dict[str, Any]:
        arch_data = self.arch_verifier.verify_recovery_architecture()
        action_mapping_data = self.mapping_verifier.verify_action_mappings()
        automation_data = self.auto_verifier.verify_automation_workflow()
        validation_report = self.health_verifier.validate_post_recovery_health()
        metrics_report = self.metrics_verifier.compute_recovery_metrics()
        simulations = self.simulator.simulate_failure_recovery_scenarios()
        integrity_report = self.integrity_verifier.verify_data_integrity()
        rollback_report = self.rollback_verifier.verify_rollback_mechanisms()
        safety_report = self.safety_verifier.verify_safety_guardrails()
        improvement_report = self.improvement_verifier.generate_post_incident_review("inc-db-failover-001")

        scorecard = self.scorer.calculate_scorecard(
            automation_result=automation_data,
            metrics_report=metrics_report,
            integrity_report=integrity_report,
            safety_report=safety_report,
            validation_report=validation_report,
            improvement_report=improvement_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            architecture_data=arch_data,
            action_mapping_data=action_mapping_data,
            automation_data=automation_data,
            validation_report=validation_report,
            metrics_report=metrics_report,
            simulations=simulations,
            integrity_report=integrity_report,
            rollback_report=rollback_report,
            safety_report=safety_report,
            improvement_report=improvement_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "exported_files": exported_files,
            "architecture": arch_data,
            "action_mapping": action_mapping_data,
            "automation": automation_data,
            "validation": validation_report,
            "metrics": metrics_report,
            "simulations": simulations,
            "integrity": integrity_report,
            "rollback": rollback_report,
            "safety": safety_report,
            "improvement": improvement_report,
        }
