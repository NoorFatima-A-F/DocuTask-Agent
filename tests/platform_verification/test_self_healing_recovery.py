"""
Comprehensive Unit and Integration Tests for Phase 3H.5.5: Enterprise Health Self-Healing & Automated Recovery Verification.
"""
import os
import json
import pytest
from app.platform_verification.self_healing_verification.domain.models import (
    FailureCategory,
    RecoveryStrategyType,
    SelfHealingTier,
    RecoveryValidationReport,
)
from app.platform_verification.self_healing_verification.verifiers.self_healing_architecture_verifier import (
    SelfHealingArchitectureVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.failure_classification_verifier import (
    FailureClassificationVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.recovery_policy_engine import (
    RecoveryPolicyEngine,
)
from app.platform_verification.self_healing_verification.verifiers.recovery_execution_verifier import (
    RecoveryExecutionVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.layer1_health_recovery_verifier import (
    Layer1HealthRecoveryVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.layer2_dependency_restore_verifier import (
    Layer2DependencyRestoreVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.layer3_workflow_recovery_verifier import (
    Layer3WorkflowRecoveryVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.layer4_performance_recovery_verifier import (
    Layer4PerformanceRecoveryVerifier,
)
from app.platform_verification.self_healing_verification.verifiers.layer5_stability_window_verifier import (
    Layer5StabilityWindowVerifier,
)
from app.platform_verification.self_healing_verification.scoring.self_healing_scorer import (
    SelfHealingScorer,
)
from app.platform_verification.self_healing_verification.exporter.self_healing_evidence_exporter import (
    SelfHealingEvidenceExporter,
)
from app.platform_verification.self_healing_verification.runtime.self_healing_runtime import (
    SelfHealingRuntime,
)


class TestSelfHealingRecoveryVerification:
    """Test suite for validating Enterprise Self-Healing and 5-Layer Recovery Validation."""

    def test_self_healing_architecture_verification(self):
        verifier = SelfHealingArchitectureVerifier()
        report = verifier.verify_architecture()
        assert report["status"] == "PASS"
        assert report["closed_loop_automation_active"] is True
        assert report["is_valid"] is True
        assert len(report["pipeline_components"]) >= 6

    def test_failure_classification_verification(self):
        verifier = FailureClassificationVerifier()
        report = verifier.verify_failure_classification()
        assert report.accuracy_percentage >= 95.0
        assert report.total_failures_classified >= 5
        assert len(report.classifications) == report.total_failures_classified
        assert report.is_classification_valid is True

    def test_recovery_policy_engine_evaluation(self):
        engine = RecoveryPolicyEngine()
        report = engine.evaluate_policies()
        assert report.total_policies_defined >= 5
        assert report.all_policies_valid is True
        assert len(report.policies) == report.total_policies_defined

    def test_recovery_execution_verification(self):
        verifier = RecoveryExecutionVerifier()
        report = verifier.verify_recovery_executions()
        assert report.total_executions_tested >= 4
        assert report.execution_verification_passed is True
        assert report.execution_success_rate == 100.0
        assert report.successful_executions == report.total_executions_tested

    def test_layer1_health_recovery_validation(self):
        verifier = Layer1HealthRecoveryVerifier()
        report = verifier.validate_service_health()
        assert report.liveness_passed is True
        assert report.readiness_passed is True
        assert report.all_health_passed is True
        assert report.liveness_status == "ALIVE"
        assert report.readiness_status == "READY"

    def test_layer2_dependency_restore_validation(self):
        verifier = Layer2DependencyRestoreVerifier()
        report = verifier.validate_dependency_restoration()
        assert report.total_dependencies >= 5
        assert report.all_restored is True
        assert any("PostgreSQL" in d.name for d in report.dependencies)
        assert any("Redis" in d.name for d in report.dependencies)
        assert any("Celery" in d.name for d in report.dependencies)
        assert any("MinIO" in d.name for d in report.dependencies)
        assert any("Gemini" in d.name for d in report.dependencies)

    def test_layer3_workflow_recovery_validation(self):
        verifier = Layer3WorkflowRecoveryVerifier()
        report = verifier.validate_functional_workflow()
        assert report.business_workflow_passed is True
        assert report.extraction_verified is True
        assert report.database_saved is True
        assert len(report.workflow_stages) >= 5

    def test_layer4_performance_recovery_validation(self):
        verifier = Layer4PerformanceRecoveryVerifier()
        report = verifier.validate_performance_recovery()
        assert report.performance_restored is True
        assert report.recovery_performance_ratio <= 1.20
        assert report.recovered_latency_ms <= (report.baseline_latency_ms * 1.20)

    def test_layer5_stability_window_validation(self):
        verifier = Layer5StabilityWindowVerifier()
        report = verifier.validate_stability_window()
        assert report.overall_stability_passed is True
        assert report.window_5m_stable is True
        assert report.window_30m_stable is True
        assert report.window_1h_stable is True
        assert report.repeated_crashes_detected == 0
        assert report.memory_leaks_detected is False
        assert report.error_spikes_detected is False

    def test_self_healing_scorer(self):
        classification_report = FailureClassificationVerifier().verify_failure_classification()
        execution_report = RecoveryExecutionVerifier().verify_recovery_executions()
        l1 = Layer1HealthRecoveryVerifier().validate_service_health()
        l2 = Layer2DependencyRestoreVerifier().validate_dependency_restoration()
        l3 = Layer3WorkflowRecoveryVerifier().validate_functional_workflow()
        l4 = Layer4PerformanceRecoveryVerifier().validate_performance_recovery()
        l5 = Layer5StabilityWindowVerifier().validate_stability_window()

        val_report = RecoveryValidationReport(
            validation_id="val-test",
            layer1_health=l1,
            layer2_dependency=l2,
            layer3_workflow=l3,
            layer4_performance=l4,
            layer5_stability=l5,
            all_5_layers_passed=True,
            recovery_accepted=True,
        )

        scorer = SelfHealingScorer()
        scorecard = scorer.calculate_scorecard(
            classification_report=classification_report,
            execution_report=execution_report,
            validation_report=val_report,
        )

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == SelfHealingTier.AUTONOMOUS_RECOVERY_READY
        assert scorecard.certified_enterprise_ready is True

    def test_full_self_healing_runtime_and_export(self, tmp_path):
        out_dir = str(tmp_path / "self_healing_verification")
        runtime = SelfHealingRuntime()
        results = runtime.run_full_self_healing_verification(output_dir=out_dir)

        assert results["composite_score"] >= 95.0
        assert results["certified"] is True
        assert results["tier"] == "Autonomous Recovery Ready"
        assert len(results["exported_files"]) == 8

        # Verify exported JSON structure
        for file_path in results["exported_files"]:
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
