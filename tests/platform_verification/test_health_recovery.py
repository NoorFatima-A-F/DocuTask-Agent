"""
Unit and Integration Tests for Phase 3H.5.12: Automated Health Recovery Verification Framework
"""
import os
import json
import pytest

from app.platform_verification.health_recovery.domain.models import (
    HealthState,
    RecoveryCertificationTier,
)
from app.platform_verification.health_recovery.verifiers import (
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
from app.platform_verification.health_recovery.runtime import HealthRecoveryRuntime
from app.platform_verification.health_recovery.api.health_recovery_api import (
    get_health_recovery_status,
    run_health_recovery_verification,
)


class TestHealthRecoveryVerification:
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        return str(tmp_path / "health_recovery_evidence")

    def test_01_health_state_verifier(self):
        verifier = HealthStateVerifier()
        report = verifier.verify_state_transitions()

        assert report.total_transitions_evaluated >= 8
        assert report.valid_transitions_count >= 8
        assert report.invalid_transitions_rejected >= 1
        assert report.state_machine_deterministic is True

        # Check invalid transition rejection
        invalid = next(t for t in report.transitions if not t.is_valid_transition)
        assert invalid.from_state == HealthState.FAILED
        assert invalid.to_state == HealthState.READY

    def test_02_failure_detection_verifier(self):
        verifier = FailureDetectionVerifier()
        report = verifier.verify_failure_detection()

        assert report.total_scenarios_tested >= 5
        assert report.detected_scenarios_count == report.total_scenarios_tested
        assert report.mean_time_to_detect_seconds <= 2.5
        assert report.detection_pipeline_active is True

    def test_03_recovery_policy_verifier(self):
        verifier = RecoveryPolicyVerifier()
        report = verifier.verify_recovery_policies()

        assert report.total_policies_defined >= 5
        assert report.policy_engine_operational is True
        assert report.rollback_strategies_verified is True

        for policy in report.active_policies:
            assert policy.retry_limit > 0
            assert policy.timeout_seconds > 0
            assert len(policy.rollback_strategy) > 0

    def test_04_component_recovery_verifier(self):
        verifier = ComponentRecoveryVerifier()
        report = verifier.verify_component_recovery()

        assert report.total_components_verified >= 5
        assert report.successful_recoveries_count == report.total_components_verified
        assert report.all_components_recovered is True

        component_names = [c.component_name for c in report.components]
        assert "API_Gateway" in component_names
        assert "PostgreSQL_Database" in component_names
        assert "Redis_Queue" in component_names
        assert "OCR_Document_Worker" in component_names
        assert "Gemini_AI_Provider" in component_names

    def test_05_recovery_safety_verifier(self):
        verifier = RecoverySafetyVerifier()
        report = verifier.verify_recovery_safety()

        assert report.total_safety_rules_verified >= 5
        assert report.infinite_loop_protection_active is True
        assert report.blast_radius_isolated is True
        assert report.timeouts_enforced is True

    def test_06_self_healing_verifier(self):
        verifier = SelfHealingVerifier()
        report = verifier.verify_self_healing_workflow()

        assert report.total_workflows_tested >= 3
        assert report.successful_self_heals == report.total_workflows_tested
        assert report.recovery_success_rate_pct == 100.0
        assert report.mean_time_to_recovery_seconds <= 15.0
        assert report.zero_manual_intervention_verified is True

    def test_07_recovery_chaos_verifier(self):
        verifier = RecoveryChaosVerifier()
        report = verifier.execute_chaos_testing()

        assert report.total_chaos_experiments >= 4
        assert report.passed_experiments_count == report.total_chaos_experiments
        assert report.resilience_certified is True

    def test_08_recovery_validation_verifier(self):
        verifier = RecoveryValidationVerifier()
        report = verifier.verify_recovery_validation()

        assert report.total_probes_executed >= 4
        assert report.passed_probes_count == report.total_probes_executed
        assert report.post_recovery_verification_confirmed is True

        for probe in report.probes:
            assert probe.post_recovery_state == HealthState.READY
            assert probe.probe_passed is True

    def test_09_recovery_observability_verifier(self):
        verifier = RecoveryObservabilityVerifier()
        report = verifier.verify_recovery_observability()

        assert len(report.metrics) >= 6
        assert report.dashboard_configured is True
        assert report.realtime_telemetry_active is True

    def test_10_recovery_security_verifier(self):
        verifier = RecoverySecurityVerifier()
        report = verifier.verify_recovery_security()

        assert report.total_actions_audited >= 3
        assert report.authorized_actions_count >= 2
        assert report.unauthorized_actions_blocked >= 1
        assert report.zero_unauthorized_recovery_actions is True

    def test_11_health_recovery_scorer(self):
        runtime = HealthRecoveryRuntime()
        results = runtime.run_full_recovery_verification()
        scorecard = results["scorecard"]

        assert scorecard.overall_recovery_score >= 95.0
        assert scorecard.certification_tier == RecoveryCertificationTier.AUTONOMOUS_RECOVERY_READY
        assert scorecard.passed is True
        assert scorecard.mttr_seconds <= 15.0
        assert scorecard.recovery_success_rate == 100.0
        assert len(scorecard.pillar_scores) == 6

    def test_12_health_recovery_exporter(self, test_output_dir):
        runtime = HealthRecoveryRuntime(output_dir=test_output_dir)
        results = runtime.run_full_recovery_verification()

        assert os.path.exists(test_output_dir)
        assert len(results["exported_files"]) == 12

        metadata_path = os.path.join(test_output_dir, "metadata.json")
        assert os.path.exists(metadata_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["overall_score"] >= 95.0
        assert meta["certification_tier"] == "Autonomous Recovery Ready"
        assert meta["passed"] is True
        assert "file_manifest" in meta
        assert "state_transition_report.json" in meta["file_manifest"]
        assert "self_healing_report.json" in meta["file_manifest"]

    def test_13_health_recovery_api(self):
        status = get_health_recovery_status()
        assert status["status"] == "ACTIVE"
        assert status["phase"] == "3H.5.12"

        verify = run_health_recovery_verification()
        assert verify["overall_recovery_score"] >= 95.0
        assert verify["certification_tier"] == "Autonomous Recovery Ready"
        assert verify["passed"] is True
        assert verify["recovery_success_rate"] == 100.0
