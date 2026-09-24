"""
Unit and Integration Tests for Phase 3H.5.10: Health Security, Privacy & Information Exposure Verification
"""
import os
import json
import pytest

from app.platform_verification.health_security.domain.models import (
    SecurityTier,
    HealthSecurityCertificationTier,
)
from app.platform_verification.health_security.verifiers import (
    EndpointSecurityVerifier,
    HealthAuthorizationVerifier,
    MetricsPrivacyVerifier,
    LogSecurityVerifier,
    AlertSecurityVerifier,
    TraceSecurityVerifier,
    SecretScanVerifier,
    DashboardSecurityVerifier,
    SecurityFailureInjectionVerifier,
    ComplianceSecurityVerifier,
)
from app.platform_verification.health_security.scoring import HealthSecurityScorer
from app.platform_verification.health_security.runtime import HealthSecurityRuntime


class TestHealthSecurityVerification:
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        return str(tmp_path / "health_security_evidence")

    def test_01_endpoint_security_verifier(self):
        verifier = EndpointSecurityVerifier()
        report = verifier.verify_endpoint_security()

        assert report.total_endpoints_audited >= 6
        assert report.secure_endpoints_count == report.total_endpoints_audited
        assert report.insecure_endpoints_count == 0
        assert report.information_exposure_prevented is True

        # Check /live public sanitization
        live_audit = next(e for e in report.audited_endpoints if e.endpoint_path == "/live")
        assert live_audit.access_tier == SecurityTier.PUBLIC
        assert live_audit.leaks_database_credentials is False
        assert live_audit.leaks_internal_ip is False

    def test_02_health_authorization_verifier(self):
        verifier = HealthAuthorizationVerifier()
        report = verifier.verify_health_authorization()

        assert report.total_auth_tests >= 7
        assert report.passed_auth_tests == report.total_auth_tests
        assert report.failed_auth_tests == 0
        assert report.rbac_enforcement_active is True
        assert report.anonymous_admin_blocked is True

        # Check anonymous /diagnostics access is 401
        anon_diag = next(t for t in report.auth_test_matrix if t.endpoint_path == "/diagnostics" and t.presented_credentials is None)
        assert anon_diag.actual_status == 401

        # Check viewer role to /diagnostics is 403
        viewer_diag = next(t for t in report.auth_test_matrix if t.endpoint_path == "/diagnostics" and t.presented_credentials == "Bearer viewer-user-jwt")
        assert viewer_diag.actual_status == 403

    def test_03_metrics_privacy_verifier(self):
        verifier = MetricsPrivacyVerifier()
        report = verifier.verify_metrics_privacy()

        assert report.total_metrics_audited >= 6
        assert report.compliant_metrics_count == report.total_metrics_audited
        assert report.violations_count == 0
        assert report.pii_free_telemetry_guaranteed is True
        assert report.high_cardinality_mitigation_active is True

    def test_04_log_security_verifier(self):
        verifier = LogSecurityVerifier()
        report = verifier.verify_log_security()

        assert report.total_log_streams_audited >= 4
        assert report.sanitized_streams_count == report.total_log_streams_audited
        assert report.violations_detected == 0
        assert report.zero_secret_leakage_in_logs is True

        # Test custom log string redaction directly
        raw_log = "User test@corp.com failed login with password='SuperSecretPassword123' token Bearer abc.123.xyz and CNIC 42101-1234567-1"
        sanitized = verifier.sanitize_log_text(raw_log)
        assert "SuperSecretPassword123" not in sanitized
        assert "42101-1234567-1" not in sanitized
        assert "test@corp.com" not in sanitized
        assert "Bearer [REDACTED_TOKEN]" in sanitized

    def test_05_alert_security_verifier(self):
        verifier = AlertSecurityVerifier()
        report = verifier.verify_alert_security()

        assert report.total_channels_audited >= 4
        assert report.secure_channels_count == report.total_channels_audited
        assert report.alert_payload_privacy_enforced is True
        assert report.runbook_safe_references_only is True

    def test_06_trace_security_verifier(self):
        verifier = TraceSecurityVerifier()
        report = verifier.verify_trace_security()

        assert report.total_spans_audited >= 4
        assert report.secure_spans_count == report.total_spans_audited
        assert report.trace_payload_masking_active is True

        # Check span hashing
        for span in report.span_audits:
            assert span.user_id_hashed is True
            assert span.contains_raw_prompts is False

    def test_07_secret_scan_verifier(self):
        verifier = SecretScanVerifier()
        report = verifier.scan_secrets_across_observability()

        assert report.surfaces_scanned >= 5
        assert report.total_scans_performed >= 7
        assert report.zero_secrets_exposed is True
        assert report.entropy_analysis_clean is True

    def test_08_dashboard_security_verifier(self):
        verifier = DashboardSecurityVerifier()
        report = verifier.verify_dashboard_security()

        assert report.total_components_audited >= 4
        assert report.hardened_components_count == report.total_components_audited
        assert report.dashboard_rbac_enforced is True
        assert report.storage_encryption_at_rest is True

    def test_09_security_failure_injection_verifier(self):
        verifier = SecurityFailureInjectionVerifier()
        report = verifier.execute_security_failure_injection()

        assert report.total_injection_scenarios >= 4
        assert report.neutralized_scenarios_count == report.total_injection_scenarios
        assert report.all_attacks_neutralized is True
        assert report.fail_secure_verified is True

    def test_10_compliance_security_verifier(self):
        verifier = ComplianceSecurityVerifier()
        report = verifier.verify_compliance_and_standards()

        assert report.total_controls >= 7
        assert report.passed_controls == report.total_controls
        assert report.compliance_percentage == 100.0
        assert report.owasp_asvs_compliant is True
        assert report.owasp_api_security_compliant is True
        assert report.soc2_cc6_compliant is True
        assert report.gdpr_art25_compliant is True

    def test_11_health_security_scorer(self):
        runtime = HealthSecurityRuntime()
        ep = runtime.endpoint_verifier.verify_endpoint_security()
        auth = runtime.auth_verifier.verify_health_authorization()
        metrics = runtime.metrics_verifier.verify_metrics_privacy()
        log = runtime.log_verifier.verify_log_security()
        alert = runtime.alert_verifier.verify_alert_security()
        trace = runtime.trace_verifier.verify_trace_security()
        secret = runtime.secret_verifier.scan_secrets_across_observability()
        dash = runtime.dashboard_verifier.verify_dashboard_security()
        inj = runtime.injection_verifier.execute_security_failure_injection()
        comp = runtime.compliance_verifier.verify_compliance_and_standards()

        scorer = HealthSecurityScorer()
        scorecard = scorer.calculate_scorecard(
            endpoint_report=ep,
            auth_report=auth,
            metrics_report=metrics,
            log_report=log,
            alert_report=alert,
            trace_report=trace,
            secret_report=secret,
            dashboard_report=dash,
            injection_report=inj,
            compliance_report=comp,
        )

        assert scorecard.overall_health_security_score >= 95.0
        assert scorecard.certification_tier == HealthSecurityCertificationTier.SECURE_OBSERVABILITY_READY
        assert scorecard.passed is True
        assert scorecard.zero_critical_vulnerabilities is True
        assert len(scorecard.category_scores) == 7

    def test_12_health_security_exporter(self, test_output_dir):
        runtime = HealthSecurityRuntime(output_dir=test_output_dir)
        results = runtime.run_full_verification()

        assert os.path.exists(test_output_dir)
        assert len(results["exported_files"]) >= 12

        # Check metadata.json integrity
        metadata_path = os.path.join(test_output_dir, "metadata.json")
        assert os.path.exists(metadata_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["overall_score"] >= 95.0
        assert meta["passed"] is True
        assert meta["zero_critical_vulnerabilities"] is True
        assert "file_manifest" in meta
        assert "endpoint_security_report.json" in meta["file_manifest"]

    def test_13_health_security_api(self):
        from app.platform_verification.health_security.api.health_security_api import (
            get_health_security_status,
            run_health_security_verification,
        )

        status_res = get_health_security_status()
        assert status_res["status"] == "ACTIVE"
        assert status_res["phase"] == "3H.5.10"

        verify_res = run_health_security_verification()
        assert verify_res["overall_health_security_score"] >= 95.0
        assert verify_res["passed"] is True
        assert verify_res["certification_tier"] == "Secure Observability Ready"

