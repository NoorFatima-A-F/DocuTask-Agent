"""
Phase 3H.4.10: Enterprise Observability Security Test Suite
"""
import os
import json
import pytest
from app.platform_verification.observability_security_verification.verifiers import (
    DataClassificationVerifier,
    LogSecurityVerifier,
    LogSanitizationVerifier,
    MetricSecurityVerifier,
    TraceSecurityVerifier,
    DashboardAccessVerifier,
    AlertSecurityVerifier,
    PipelineSecurityVerifier,
    AISecurityVerifier,
    SecurityFailureSimulator,
)
from app.platform_verification.observability_security_verification.scoring.observability_security_scorer import (
    ObservabilitySecurityScorer,
)
from app.platform_verification.observability_security_verification.runtime.observability_security_runtime import (
    ObservabilitySecurityRuntime,
)
from app.platform_verification.observability_security_verification.domain.models import (
    DataClassification,
    SecurityTier,
    RBACRole,
)


class TestObservabilitySecurityVerification:
    def test_data_classification_architecture(self):
        """3H.4.10.1: Verify 4-tier data classification across telemetry fields."""
        verifier = DataClassificationVerifier()
        report = verifier.verify_data_classification()

        assert report.classification_policy_passed is True
        assert report.total_fields_audited >= 8
        assert report.restricted_fields >= 3
        assert any(i.field_name == "database_password" and i.classification == DataClassification.RESTRICTED for i in report.items)
        assert any(i.field_name == "llm_prompt_raw_text" and i.classification == DataClassification.RESTRICTED for i in report.items)

    def test_log_security_scanning(self):
        """3H.4.10.2: Scan application logs for credentials, PII, and document text."""
        verifier = LogSecurityVerifier()
        report = verifier.scan_logs_for_sensitive_data()

        assert report.log_security_passed is True
        assert report.unmasked_leaks_count == 0
        assert report.total_log_entries_scanned >= 10000
        assert len(report.scanned_findings) >= 4
        assert all(f.is_safe_after_sanitization for f in report.scanned_findings)

    def test_log_sanitization_middleware(self):
        """3H.4.10.3: Verify regex & pattern masking middleware."""
        verifier = LogSanitizationVerifier()
        report = verifier.verify_sanitization_middleware()

        assert report.sanitization_verified is True
        assert report.sample_tests_failed == 0
        assert report.sample_tests_passed >= 6
        assert len(report.active_sanitization_rules) >= 5

    def test_metric_security_and_cardinality(self):
        """3H.4.10.4: Audit Prometheus metrics for forbidden labels and cardinality explosion."""
        verifier = MetricSecurityVerifier()
        report = verifier.audit_metrics_privacy()

        assert report.metric_privacy_passed is True
        assert report.metrics_failed == 0
        assert report.total_metrics_audited >= 5
        for audit in report.audits:
            assert audit.cardinality_safe is True
            assert not audit.contains_forbidden_labels

    def test_trace_security_and_attribute_sanitization(self):
        """3H.4.10.5: Verify OpenTelemetry trace span attribute scrubbing."""
        verifier = TraceSecurityVerifier()
        report = verifier.audit_trace_security()

        assert report.trace_security_passed is True
        assert report.compliant_spans == report.total_spans_inspected
        assert report.total_spans_inspected >= 5
        for audit in report.audits:
            assert audit.no_auth_headers is True
            assert audit.no_raw_prompts is True
            assert audit.is_compliant is True

    def test_dashboard_rbac_access_control(self):
        """3H.4.10.6: Verify least privilege and 403 Forbidden enforcement on unauthorized roles."""
        verifier = DashboardAccessVerifier()
        report = verifier.verify_dashboard_rbac()

        assert report.rbac_enforcement_passed is True
        assert report.unauthorized_attempts_blocked >= 3
        assert len(report.roles_evaluated) == 4
        for check in report.permission_checks:
            if not check.allowed:
                assert check.test_result_status == 403

    def test_alert_payload_privacy_and_security(self):
        """3H.4.10.7: Audit alerts for confidential data and PII leakage."""
        verifier = AlertSecurityVerifier()
        report = verifier.audit_alert_payloads()

        assert report.alert_privacy_passed is True
        assert report.safe_templates_count == report.total_alert_templates_audited
        assert report.total_alert_templates_audited >= 5
        for audit in report.audits:
            assert audit.contains_pii is False
            assert audit.contains_credentials is False
            assert audit.contains_document_content is False
            assert audit.is_safe is True

    def test_pipeline_encryption_and_storage_retention(self):
        """3H.4.10.8 & 3H.4.10.9: Verify TLS 1.3, mTLS ingestion auth, and retention policies."""
        verifier = PipelineSecurityVerifier()
        report = verifier.verify_pipeline_and_storage_security()

        assert report.pipeline_security_passed is True
        assert report.transport_encryption_tls13 is True
        assert report.telemetry_ingestion_auth_required is True
        assert report.log_retention_days == 30
        assert report.trace_retention_days == 7
        assert report.storage_encryption_at_rest is True

    def test_ai_telemetry_abstraction_and_privacy(self):
        """3H.4.10.10: Verify AI pipeline abstracts telemetry without raw prompts or outputs."""
        verifier = AISecurityVerifier()
        report = verifier.audit_ai_telemetry_security()

        assert report.ai_observability_safe is True
        assert report.zero_prompt_leakage_verified is True
        assert report.zero_response_leakage_verified is True
        assert len(report.workflow_stages_audited) >= 5

    def test_security_failure_simulations(self):
        """3H.4.10.11: Test secret leaks, PII injection, and unauthorized RBAC escalation defense."""
        simulator = SecurityFailureSimulator()
        simulations = simulator.simulate_security_failure_injections()

        assert len(simulations) == 5
        for sim in simulations:
            assert sim.blocked_or_redacted is True
            assert sim.result_status in [
                "BLOCKED_AND_REDACTED",
                "403_FORBIDDEN",
                "CONNECTION_REFUSED_TLS_REQUIRED",
                "LABEL_DROPPED_CARDINALITY_PROTECTED",
            ]

    def test_observability_security_scorecard(self):
        """3H.4.10.12: Verify weighted scoring formula and certification tier."""
        runtime = ObservabilitySecurityRuntime()
        results = runtime.run_all_verifications(output_dir="observability_security_verification")
        scorecard = results["scorecard"]

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == SecurityTier.ENTERPRISE_OBSERVABILITY_SECURITY_CERTIFIED
        assert scorecard.certified_enterprise_ready is True
        assert scorecard.log_protection_score == 100.0
        assert scorecard.metric_security_score == 100.0
        assert scorecard.ai_telemetry_security_score == 100.0

    def test_observability_security_evidence_manifests(self, tmp_path):
        """3H.4.10.12: Verify 12 JSON evidence manifests."""
        runtime = ObservabilitySecurityRuntime()
        out_dir = str(tmp_path / "observability_security_verification")
        results = runtime.run_all_verifications(output_dir=out_dir)

        expected_files = [
            "data_classification_report.json",
            "log_security_report.json",
            "sanitization_report.json",
            "metric_security_report.json",
            "trace_security_report.json",
            "dashboard_access_report.json",
            "alert_security_report.json",
            "pipeline_security_report.json",
            "ai_security_report.json",
            "failure_test_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        assert len(results["exported_files"]) == 12
        for ef in expected_files:
            file_path = os.path.join(out_dir, ef)
            assert os.path.exists(file_path), f"Missing manifest: {ef}"
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data is not None
