"""Comprehensive Unit and Integration Tests for Phase 3H.4.5 — Enterprise Alert Rule Verification Framework."""

import json

from app.platform_verification.alert_rule_verification.domain.models import (
    AlertLifecycleState,
    AlertCertificationTier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_architecture_verifier import (
    AlertArchitectureVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_taxonomy_verifier import (
    AlertTaxonomyVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.critical_alert_verifier import (
    CriticalAlertVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.warning_alert_verifier import (
    WarningAlertVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_condition_verifier import (
    AlertConditionVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_severity_verifier import (
    AlertSeverityVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_message_verifier import (
    AlertMessageVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_routing_verifier import (
    AlertRoutingVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.threshold_optimization_verifier import (
    ThresholdOptimizationVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_fatigue_verifier import (
    AlertFatigueVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.failure_injection_verifier import (
    FailureInjectionVerifier,
)
from app.platform_verification.alert_rule_verification.verifiers.alert_performance_verifier import (
    AlertPerformanceVerifier,
)
from app.platform_verification.alert_rule_verification.runtime.alert_rule_verification_runtime import (
    AlertRuleVerificationRuntime,
)


class TestAlertRuleVerification:
    """Test suite for validating Enterprise Alert Rule verification components."""

    def test_alert_architecture_verification(self):
        """3H.4.5.1: Verify alert architecture, lifecycle states, and AlertManager readiness."""
        verifier = AlertArchitectureVerifier()
        report = verifier.verify_architecture()
        assert report.status == "PASS"
        assert report.alert_system == "Prometheus AlertManager"
        assert len(report.supported_lifecycle_states) == 5
        assert "FIRING" in report.supported_lifecycle_states
        assert "RESOLVED" in report.supported_lifecycle_states

    def test_alert_taxonomy_verification(self):
        """3H.4.5.2: Verify 5-category alert classification taxonomy."""
        verifier = AlertTaxonomyVerifier()
        report = verifier.verify_taxonomy()
        assert report.status == "PASS"
        assert report.total_categories == 5
        assert "AVAILABILITY" in report.categories_covered
        assert "SECURITY" in report.categories_covered
        assert report.taxonomy_compliance_score == 100.0

    def test_critical_alert_verification(self):
        """3H.4.5.3: Verify critical failure rules (DB down, API down, worker exhaustion, queue loss)."""
        verifier = CriticalAlertVerifier()
        report = verifier.verify_critical_alerts()
        assert report.status == "PASS"
        assert report.critical_rules_count == 4
        assert report.database_failure_rule_verified is True
        assert report.api_service_down_rule_verified is True
        assert report.all_critical_rules_actionable is True

    def test_warning_alert_verification(self):
        """3H.4.5.4: Verify warning degradation rules (high latency, queue growth, resource pressure)."""
        verifier = WarningAlertVerifier()
        report = verifier.verify_warning_alerts()
        assert report.status == "PASS"
        assert report.warning_rules_count == 3
        assert report.high_latency_warning_verified is True
        assert report.ai_latency_warning_verified is True

    def test_alert_condition_transitions(self):
        """3H.4.5.5: Test false -> true -> recovered state transitions."""
        verifier = AlertConditionVerifier()
        report = verifier.verify_conditions()
        assert report.status == "PASS"
        assert report.rules_tested_count >= 8
        for res in report.transition_results:
            assert res.condition_false_state == AlertLifecycleState.NORMAL
            assert res.condition_true_state == AlertLifecycleState.FIRING
            assert res.condition_recovered_state == AlertLifecycleState.RESOLVED
            assert res.transition_success is True

    def test_alert_severity_verification(self):
        """3H.4.5.6: Verify severity distribution and zero misclassifications."""
        verifier = AlertSeverityVerifier()
        report = verifier.verify_severity()
        assert report.status == "PASS"
        assert report.zero_severity_misclassification is True
        assert report.critical_count == 4

    def test_alert_message_quality(self):
        """3H.4.5.7: Verify alert messages contain impact, recommended action, and runbooks."""
        verifier = AlertMessageVerifier()
        report = verifier.verify_messages()
        assert report.status == "PASS"
        assert report.all_have_summary is True
        assert report.all_have_impact_statement is True
        assert report.all_have_recommended_action is True
        assert report.all_have_runbook_url is True

    def test_alert_routing_and_escalation(self):
        """3H.4.5.8: Verify team routes and notification channel integrations."""
        verifier = AlertRoutingVerifier()
        report = verifier.verify_routing()
        assert report.status == "PASS"
        assert "PagerDuty" in report.routing_channels_configured
        assert "Slack" in report.routing_channels_configured
        assert "database-infra" in report.team_routes_verified
        assert report.escalation_matrix_verified is True

    def test_threshold_optimization(self):
        """3H.4.5.9: Verify evaluation duration tuning to reject transient noise."""
        verifier = ThresholdOptimizationVerifier()
        report = verifier.verify_thresholds()
        assert report["status"] == "PASS"
        assert report["evaluation_durations_optimized"] is True
        assert report["transient_spike_rejection_rate"] > 0.95

    def test_alert_fatigue_and_noise_reduction(self):
        """3H.4.5.10: Verify deduplication, cascade grouping, and maintenance suppression."""
        verifier = AlertFatigueVerifier()
        report = verifier.verify_fatigue_prevention()
        assert report.status == "PASS"
        assert report.deduplication_enabled is True
        assert report.inhibition_rules_active is True
        assert report.noise_reduction_ratio >= 0.90

    def test_failure_injection_scenarios(self):
        """3H.4.5.11: Validate real-time triggers across 5 chaos injection scenarios."""
        verifier = FailureInjectionVerifier()
        report = verifier.verify_failure_injection()
        assert report.status == "PASS"
        assert report.total_scenarios_tested == 5
        assert report.all_scenarios_passed is True
        for s in report.scenarios:
            assert s.alert_fired is True
            assert s.recovery_detected is True

    def test_alert_performance_metrics(self):
        """3H.4.5.12: Verify MTTD (<30s), MTTR, precision (>95%), and recall (100%)."""
        verifier = AlertPerformanceVerifier()
        report = verifier.verify_performance()
        assert report.status == "PASS"
        assert report.mttd_seconds < 30.0
        assert report.alert_precision_ratio >= 0.95
        assert report.alert_recall_ratio == 1.0

    def test_quality_scorecard_calculation(self):
        """3H.4.5.14: Verify 6-category weighted quality scorecard and certification tier."""
        runtime = AlertRuleVerificationRuntime()
        scorecard, _ = runtime.execute_full_verification()
        assert scorecard.overall_score >= 95.0
        assert scorecard.certification_tier == AlertCertificationTier.ENTERPRISE_ALERTING_CERTIFIED
        assert scorecard.passed is True
        assert scorecard.detection_accuracy_score == 100.0

    def test_evidence_exporter_and_manifests(self, tmp_path):
        """3H.4.5.15: Verify export of all 13 JSON evidence manifests."""
        runtime = AlertRuleVerificationRuntime(output_dir=str(tmp_path))
        scorecard, manifests = runtime.execute_full_verification()
        assert scorecard.passed is True
        assert len(manifests) == 13

        expected_files = [
            "architecture_report.json",
            "taxonomy_report.json",
            "critical_alert_report.json",
            "warning_alert_report.json",
            "condition_test_report.json",
            "severity_report.json",
            "message_quality_report.json",
            "routing_report.json",
            "fatigue_report.json",
            "failure_test_report.json",
            "performance_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        for fname in expected_files:
            fpath = tmp_path / fname
            assert fpath.exists(), f"Missing manifest: {fname}"
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
