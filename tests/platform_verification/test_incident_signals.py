"""Comprehensive Unit and Integration Tests for Phase 3H.4.7 — Enterprise Incident Signal Verification Framework."""

import json

from app.platform_verification.incident_signal_verification.domain.models import (
    IncidentPriority,
    IncidentCertificationTier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_architecture_verifier import (
    IncidentArchitectureVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.alert_incident_mapping_verifier import (
    AlertIncidentMappingVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_payload_verifier import (
    IncidentPayloadVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.dependency_blast_radius_verifier import (
    DependencyBlastRadiusVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.impact_assessment_verifier import (
    ImpactAssessmentVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.priority_calculator_verifier import (
    PriorityCalculatorVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_correlation_verifier import (
    IncidentCorrelationVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_timeline_verifier import (
    IncidentTimelineVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.runbook_integration_verifier import (
    RunbookIntegrationVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_security_verifier import (
    IncidentSecurityVerifier,
)
from app.platform_verification.incident_signal_verification.verifiers.incident_automation_verifier import (
    IncidentAutomationVerifier,
)
from app.platform_verification.incident_signal_verification.runtime.incident_signal_verification_runtime import (
    IncidentSignalVerificationRuntime,
)


class TestIncidentSignalVerification:
    """Test suite for validating Enterprise Incident Signal Verification components."""

    def test_incident_architecture_verification(self):
        """3H.4.7.1: Verify incident lifecycle architecture, states, and transition tracking."""
        verifier = IncidentArchitectureVerifier()
        report = verifier.verify_architecture()
        assert report.status == "PASS"
        assert len(report.lifecycle_states_supported) == 7
        assert "DETECTED" in report.lifecycle_states_supported
        assert "RESOLVED" in report.lifecycle_states_supported
        assert report.state_transitions_verified is True

    def test_alert_incident_mapping(self):
        """3H.4.7.2: Verify alert-to-incident transformation (DB, API, Worker, Latency, Gemini)."""
        verifier = AlertIncidentMappingVerifier()
        report = verifier.verify_alert_mapping()
        assert report.status == "PASS"
        assert report.total_alert_mappings == 5
        assert report.mapping_accuracy_score == 100.0
        for m in report.mappings:
            assert m.verified is True
            assert m.mapped_priority in [IncidentPriority.P1_CRITICAL, IncidentPriority.P2_HIGH]

    def test_incident_payload_quality(self):
        """3H.4.7.3: Verify diagnostic payload completeness and extended context (trace ID, metrics snapshot)."""
        verifier = IncidentPayloadVerifier()
        report = verifier.verify_payload_quality()
        assert report.status == "PASS"
        assert report.schema_compliance_ratio == 1.00
        assert report.context_enrichment_verified is True

    def test_dependency_blast_radius(self):
        """3H.4.7.4: Verify dependency graph traversal and downstream blast radius calculation."""
        verifier = DependencyBlastRadiusVerifier()
        report = verifier.verify_dependency_analysis()
        assert report.status == "PASS"
        assert report.dependency_nodes_mapped == 8
        assert report.dependency_graph_complete is True
        for a in report.blast_radius_analyses:
            assert a.verified is True
            assert len(a.downstream_affected) > 0

    def test_impact_assessment_verification(self):
        """3H.4.7.5: Verify multi-tier operational impact assessment (users, business documents, technical queues)."""
        verifier = ImpactAssessmentVerifier()
        report = verifier.verify_impact_assessment()
        assert report.status == "PASS"
        assert report.affected_users > 0
        assert report.failed_requests > 0
        assert report.impact_calculation_verified is True

    def test_priority_calculation(self):
        """3H.4.7.6: Verify priority calculation formula (P1 to P4)."""
        verifier = PriorityCalculatorVerifier()
        report = verifier.verify_priority_calculation()
        assert report.status == "PASS"
        assert report.p1_scenarios_verified >= 2
        assert report.priority_calculation_accuracy == 100.0

    def test_incident_correlation(self):
        """3H.4.7.7: Verify cascade symptom alert consolidation into single root cause incident."""
        verifier = IncidentCorrelationVerifier()
        report = verifier.verify_correlation()
        assert report.status == "PASS"
        assert report.cascade_events_tested == 3
        assert report.duplicate_incidents_prevented > 0
        assert report.correlation_accuracy == 100.0

    def test_incident_timeline_and_mttd_mtta_mttr(self):
        """3H.4.7.8: Verify event timeline tracking, MTTD (< 30s), MTTA, and MTTR metrics."""
        verifier = IncidentTimelineVerifier()
        report = verifier.verify_timeline()
        assert report.status == "PASS"
        assert report.mttd_seconds < 30.0
        assert report.timeline_event_logging_verified is True

    def test_runbook_integration(self):
        """3H.4.7.9: Verify actionable runbook attachments for all incident types."""
        verifier = RunbookIntegrationVerifier()
        report = verifier.verify_runbooks()
        assert report.status == "PASS"
        assert report.runbook_coverage_percentage == 100.0
        assert report.all_runbooks_actionable is True

    def test_incident_security_and_pii(self):
        """3H.4.7.10: Verify zero secret/PII leak across incident payloads and logs."""
        verifier = IncidentSecurityVerifier()
        report = verifier.verify_security()
        assert report.status == "PASS"
        assert report.api_key_leaks_found == 0
        assert report.password_leaks_found == 0
        assert report.customer_pii_leaks_found == 0
        assert report.zero_leak_verified is True

    def test_incident_response_automation(self):
        """3H.4.7.11: Verify automated self-healing triggers (restart, autoscale, fallback)."""
        verifier = IncidentAutomationVerifier()
        report = verifier.verify_automation()
        assert report.status == "PASS"
        assert report.database_restart_recovery_verified is True
        assert report.worker_autoscale_recovery_verified is True
        assert report.ai_provider_fallback_verified is True

    def test_quality_scorecard_calculation(self):
        """3H.4.7.12: Verify 7-category weighted quality scorecard and certification tier."""
        runtime = IncidentSignalVerificationRuntime()
        scorecard, _ = runtime.execute_full_verification()
        assert scorecard.overall_score >= 95.0
        assert scorecard.certification_tier == IncidentCertificationTier.ENTERPRISE_INCIDENT_READY
        assert scorecard.passed is True
        assert scorecard.alert_to_incident_accuracy_score == 100.0
        assert scorecard.context_completeness_score == 100.0

    def test_evidence_exporter_and_manifests(self, tmp_path):
        """3H.4.7.13: Verify export of all 13 JSON evidence manifests."""
        runtime = IncidentSignalVerificationRuntime(output_dir=str(tmp_path))
        scorecard, manifests = runtime.execute_full_verification()
        assert scorecard.passed is True
        assert len(manifests) == 13

        expected_files = [
            "incident_architecture_report.json",
            "alert_mapping_report.json",
            "payload_quality_report.json",
            "dependency_analysis_report.json",
            "impact_report.json",
            "priority_report.json",
            "correlation_report.json",
            "timeline_report.json",
            "runbook_report.json",
            "security_report.json",
            "automation_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        for fname in expected_files:
            fpath = tmp_path / fname
            assert fpath.exists(), f"Missing manifest: {fname}"
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
