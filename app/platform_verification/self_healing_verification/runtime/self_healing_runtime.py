"""
Phase 3H.5.5: Self-Healing & Automated Recovery Runtime
"""
import uuid
from typing import Dict, Any, List
from ..verifiers import (
    SelfHealingArchitectureVerifier,
    FailureClassificationVerifier,
    RecoveryPolicyEngine,
    RecoveryExecutionVerifier,
    Layer1HealthRecoveryVerifier,
    Layer2DependencyRestoreVerifier,
    Layer3WorkflowRecoveryVerifier,
    Layer4PerformanceRecoveryVerifier,
    Layer5StabilityWindowVerifier,
)
from ..scoring.self_healing_scorer import SelfHealingScorer
from ..exporter.self_healing_evidence_exporter import SelfHealingEvidenceExporter
from ..domain.models import RecoveryValidationReport, SelfHealingScorecard


class SelfHealingRuntime:
    def __init__(self):
        self.arch_verifier = SelfHealingArchitectureVerifier()
        self.classification_verifier = FailureClassificationVerifier()
        self.policy_engine = RecoveryPolicyEngine()
        self.execution_verifier = RecoveryExecutionVerifier()
        self.layer1_health_verifier = Layer1HealthRecoveryVerifier()
        self.layer2_dep_verifier = Layer2DependencyRestoreVerifier()
        self.layer3_wf_verifier = Layer3WorkflowRecoveryVerifier()
        self.layer4_perf_verifier = Layer4PerformanceRecoveryVerifier()
        self.layer5_stab_verifier = Layer5StabilityWindowVerifier()
        self.scorer = SelfHealingScorer()
        self.exporter = SelfHealingEvidenceExporter()

    def run_full_self_healing_verification(self, output_dir: str = "self_healing_verification") -> Dict[str, Any]:
        arch_report = self.arch_verifier.verify_architecture()
        classification_report = self.classification_verifier.verify_failure_classification()
        policy_report = self.policy_engine.evaluate_policies()
        execution_report = self.execution_verifier.verify_recovery_executions()

        l1 = self.layer1_health_verifier.validate_service_health()
        l2 = self.layer2_dep_verifier.validate_dependency_restoration()
        l3 = self.layer3_wf_verifier.validate_functional_workflow()
        l4 = self.layer4_perf_verifier.validate_performance_recovery()
        l5 = self.layer5_stab_verifier.validate_stability_window()

        all_5 = (
            l1.all_health_passed
            and l2.all_restored
            and l3.business_workflow_passed
            and l4.performance_restored
            and l5.overall_stability_passed
        )

        validation_report = RecoveryValidationReport(
            validation_id=f"val-sh-{uuid.uuid4().hex[:8]}",
            layer1_health=l1,
            layer2_dependency=l2,
            layer3_workflow=l3,
            layer4_performance=l4,
            layer5_stability=l5,
            all_5_layers_passed=all_5,
            recovery_accepted=all_5,
        )

        scorecard = self.scorer.calculate_scorecard(
            classification_report=classification_report,
            execution_report=execution_report,
            validation_report=validation_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            validation_report=validation_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "validation_report": validation_report,
            "classification_report": classification_report,
            "policy_report": policy_report,
            "execution_report": execution_report,
            "exported_files": exported_files,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified": scorecard.certified_enterprise_ready,
        }
