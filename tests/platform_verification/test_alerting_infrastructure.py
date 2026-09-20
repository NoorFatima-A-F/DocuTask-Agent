"""
Phase 3I.5: Enterprise Alerting & Incident Detection Verification - Unit and Integration Tests
"""
import os
import json
import pytest
import hashlib
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.alerting_infrastructure.domain.models import (
    IncidentSeverity,
    AlertTriggerState,
    AlertCertificationTier,
    NotificationChannelSpec,
    AlertingArchitectureReport,
    SignalSourceCoverageSpec,
    AlertSignalCoverageReport,
    AlertRuleSpec,
    AlertRulesReport,
    AIAgentAlertRuleSpec,
    AIAgentAlertReport,
    RoutingDestinationSpec,
    IncidentSeverityReport,
    RemediationActionSpec,
    RemediationReport,
    AlertSecurityAuditSpec,
    AlertSecurityReport,
    ChaosAlertScenarioSpec,
    AlertTestingReport,
    AlertingPillarScore,
    AlertingCertificationReport,
)
from app.platform_verification.alerting_infrastructure.verifiers.alerting_architecture_verifier import AlertingArchitectureVerifier
from app.platform_verification.alerting_infrastructure.verifiers.alert_signal_coverage_verifier import AlertSignalCoverageVerifier
from app.platform_verification.alerting_infrastructure.verifiers.alert_rule_engineering_verifier import AlertRuleEngineeringVerifier
from app.platform_verification.alerting_infrastructure.verifiers.ai_agent_alert_verifier import AIAgentAlertVerifier
from app.platform_verification.alerting_infrastructure.verifiers.severity_routing_verifier import SeverityRoutingVerifier
from app.platform_verification.alerting_infrastructure.verifiers.automated_remediation_verifier import AutomatedRemediationVerifier
from app.platform_verification.alerting_infrastructure.verifiers.alert_security_verifier import AlertSecurityVerifier
from app.platform_verification.alerting_infrastructure.verifiers.alert_testing_simulation_verifier import AlertTestingSimulationVerifier
from app.platform_verification.alerting_infrastructure.scoring.alerting_quality_scorer import AlertingQualityScorer
from app.platform_verification.alerting_infrastructure.exporter.alerting_evidence_exporter import AlertingEvidenceExporter
from app.platform_verification.alerting_infrastructure.runtime.alerting_verification_runtime import AlertingVerificationRuntime
from app.platform_verification.alerting_infrastructure.api.alerting_verification_api import router as alerting_api_router


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    arch = AlertingArchitectureReport(
        rules_configured_count=124,
        notification_channels=[
            NotificationChannelSpec(channel_name="PagerDuty", channel_type="PagerDuty", target_destination="https://events.pagerduty.com")
        ]
    )
    assert arch.rules_configured_count == 124
    assert arch.monitored_services == 8
    assert len(arch.notification_channels) == 1

    rule = AlertRuleSpec(
        rule_id="R-01",
        name="TestRule",
        signal_type="Latency",
        condition_expression="p95 > 2.0",
        duration_window="for: 5m",
        severity=IncidentSeverity.SEV_2,
        description="High latency rule"
    )
    assert rule.severity == IncidentSeverity.SEV_2
    assert rule.false_positive_protection is True

    cert_rep = AlertingCertificationReport(
        certification_tier=AlertCertificationTier.ENTERPRISE_INCIDENT_READY,
        overall_score_pct=98.5
    )
    assert cert_rep.certification_granted is True
    assert cert_rep.certification_tier == AlertCertificationTier.ENTERPRISE_INCIDENT_READY


# ─── 2. Architecture Verifier Tests ───────────────────────────────────────────

def test_alerting_architecture_verifier():
    verifier = AlertingArchitectureVerifier()
    report = verifier.verify_alerting_architecture()

    assert report.status == "PASS"
    assert report.monitored_services == 8
    assert report.rules_configured_count >= 100
    assert len(report.notification_channels) == 4

    channel_types = [c.channel_type for c in report.notification_channels]
    assert "PagerDuty" in channel_types
    assert "Slack" in channel_types
    assert "Email" in channel_types
    assert "Webhook" in channel_types


# ─── 3. Signal Coverage Verifier Tests ────────────────────────────────────────

def test_alert_signal_coverage_verifier():
    verifier = AlertSignalCoverageVerifier()
    report = verifier.verify_signal_coverage()

    assert report.overall_signal_coverage_pct == 100.0
    assert report.multi_signal_correlation_active is True
    assert len(report.signal_sources) == 4

    categories = [s.source_category for s in report.signal_sources]
    assert "Metrics" in categories
    assert "Logs" in categories
    assert "Traces" in categories
    assert "Business Signals" in categories


# ─── 4. Alert Rule Engineering Verifier Tests ─────────────────────────────────

def test_alert_rule_engineering_verifier():
    verifier = AlertRuleEngineeringVerifier()
    report = verifier.verify_alert_rules()

    assert report.alert_rules_compliant is True
    assert report.duration_window_enforced is True
    assert len(report.rules) >= 7

    # Verify Golden Signals coverage
    signal_types = {r.signal_type for r in report.rules}
    assert "Latency" in signal_types
    assert "Traffic" in signal_types
    assert "Errors" in signal_types
    assert "Saturation" in signal_types

    # Verify duration windows exist on all rules
    for r in report.rules:
        assert r.duration_window.startswith("for:")
        assert r.false_positive_protection is True


# ─── 5. AI Agent Alert Verifier Tests ─────────────────────────────────────────

def test_ai_agent_alert_verifier():
    verifier = AIAgentAlertVerifier()
    report = verifier.verify_ai_agent_alerts()

    assert report.ai_alerting_coverage_score == 100.0
    assert report.agent_retry_explosion_detection is True
    assert report.planning_failure_detection is True
    assert report.extraction_accuracy_drop_detection is True
    assert len(report.ai_alert_rules) >= 6

    rule_names = [r.alert_name for r in report.ai_alert_rules]
    assert "AIAgentTaskFailureRateHigh" in rule_names
    assert "AIAgentRetryExplosionDetected" in rule_names
    assert "AIPlannerDecompositionFailure" in rule_names
    assert "OCRToolUnavailableFailure" in rule_names
    assert "DocumentExtractionConfidenceDegradation" in rule_names


# ─── 6. Severity & Routing Verifier Tests ─────────────────────────────────────

def test_severity_routing_verifier():
    verifier = SeverityRoutingVerifier()
    report = verifier.verify_severity_routing()

    assert report.routing_accuracy_pct == 100.0
    assert len(report.severity_tiers) == 4
    assert len(report.routing_table) == 4

    severities = [r.severity for r in report.routing_table]
    assert IncidentSeverity.SEV_1 in severities
    assert IncidentSeverity.SEV_2 in severities
    assert IncidentSeverity.SEV_3 in severities
    assert IncidentSeverity.SEV_4 in severities

    sev1_rule = next(r for r in report.routing_table if r.severity == IncidentSeverity.SEV_1)
    assert "PagerDuty" in sev1_rule.dispatch_channel
    assert sev1_rule.escalation_timeout_mins == 5


# ─── 7. Automated Remediation Verifier Tests ──────────────────────────────────

def test_automated_remediation_verifier():
    verifier = AutomatedRemediationVerifier()
    report = verifier.verify_remediation_workflows()

    assert report.self_healing_success_rate_pct == 100.0
    assert report.postmortem_auto_generation_enabled is True
    assert len(report.remediation_actions) >= 4

    for act in report.remediation_actions:
        assert act.health_verification_passed is True
        assert act.execution_latency_ms < 2000.0
        assert act.incident_ticket_id.startswith("INC-")


# ─── 8. Security Verifier Tests ───────────────────────────────────────────────

def test_alert_security_verifier():
    verifier = AlertSecurityVerifier()
    report = verifier.verify_alert_security()

    assert report.security_score_pct == 100.0
    assert report.sanitization_verified is True
    assert len(report.audits) == 4

    for a in report.audits:
        assert a.pii_exposed is False
        assert a.credentials_exposed is False
        assert a.document_content_exposed is False
        assert a.status == "SECURE"


# ─── 9. Alert Testing / Chaos Simulation Tests ────────────────────────────────

def test_alert_testing_simulation_verifier():
    verifier = AlertTestingSimulationVerifier()
    report = verifier.verify_alert_testing_scenarios()

    assert report.all_tests_passed is True
    assert len(report.scenarios) == 4

    test_ids = [s.test_id for s in report.scenarios]
    assert "CHAOS-ALERT-001" in test_ids
    assert "CHAOS-ALERT-002" in test_ids
    assert "CHAOS-ALERT-003" in test_ids
    assert "CHAOS-ALERT-004" in test_ids

    for sc in report.scenarios:
        assert sc.actual_alert_fired == sc.expected_alert
        assert sc.actual_severity == sc.expected_severity
        assert sc.remediation_triggered is True
        assert sc.passed is True


# ─── 10. Quality Scorer Tests ─────────────────────────────────────────────────

def test_alerting_quality_scorer():
    runtime = AlertingVerificationRuntime()
    arch = runtime.arch_verifier.verify_alerting_architecture()
    signal = runtime.signal_verifier.verify_signal_coverage()
    rule = runtime.rule_verifier.verify_alert_rules()
    ai = runtime.ai_verifier.verify_ai_agent_alerts()
    routing = runtime.routing_verifier.verify_severity_routing()
    remediation = runtime.remediation_verifier.verify_remediation_workflows()
    sec = runtime.sec_verifier.verify_alert_security()
    testing = runtime.testing_verifier.verify_alert_testing_scenarios()

    scorer = AlertingQualityScorer()
    certification = scorer.calculate_certification_score(
        arch_report=arch,
        signal_report=signal,
        rule_report=rule,
        ai_report=ai,
        routing_report=routing,
        remediation_report=remediation,
        sec_report=sec,
        testing_report=testing,
    )

    assert certification.overall_score_pct >= 95.0
    assert certification.certification_tier == AlertCertificationTier.ENTERPRISE_INCIDENT_READY
    assert certification.certification_granted is True
    assert len(certification.pillar_scores) == 6

    total_weight = sum(p.weight_pct for p in certification.pillar_scores)
    assert abs(total_weight - 100.0) < 0.001


# ─── 11. Exporter & Runtime Tests ─────────────────────────────────────────────

def test_alerting_evidence_exporter(tmp_path):
    out_dir = str(tmp_path / "observability_verification" / "alerting")
    runtime = AlertingVerificationRuntime()
    result = runtime.run_full_verification(export_dir=out_dir)

    metadata = result["metadata"]
    assert metadata["rules_configured"] >= 100
    assert metadata["total_artifacts"] == 10

    metadata_path = os.path.join(out_dir, "metadata.json")
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        meta_loaded = json.load(f)

    assert "manifest_sha256" in meta_loaded
    for filename, recorded_hash in meta_loaded["manifest_sha256"].items():
        file_path = os.path.join(out_dir, filename)
        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as rf:
            content_str = rf.read()
        computed_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        assert computed_hash == recorded_hash


# ─── 12. FastAPI Router Tests ─────────────────────────────────────────────────

def test_alerting_verification_api_endpoints():
    app = FastAPI()
    app.include_router(alerting_api_router)
    client = TestClient(app)

    # Health endpoint
    resp = client.get("/api/v1/alerting-verification/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # Architecture endpoint
    resp = client.get("/api/v1/alerting-verification/architecture")
    assert resp.status_code == 200
    assert resp.json()["monitored_services"] == 8

    # Signals endpoint
    resp = client.get("/api/v1/alerting-verification/signals")
    assert resp.status_code == 200
    assert resp.json()["overall_signal_coverage_pct"] == 100.0

    # Rules endpoint
    resp = client.get("/api/v1/alerting-verification/rules")
    assert resp.status_code == 200
    assert resp.json()["alert_rules_compliant"] is True

    # AI Agent endpoint
    resp = client.get("/api/v1/alerting-verification/ai-agent")
    assert resp.status_code == 200
    assert resp.json()["ai_alerting_coverage_score"] == 100.0

    # Routing endpoint
    resp = client.get("/api/v1/alerting-verification/routing")
    assert resp.status_code == 200
    assert resp.json()["routing_accuracy_pct"] == 100.0

    # Remediation endpoint
    resp = client.get("/api/v1/alerting-verification/remediation")
    assert resp.status_code == 200
    assert resp.json()["self_healing_success_rate_pct"] == 100.0

    # Security endpoint
    resp = client.get("/api/v1/alerting-verification/security")
    assert resp.status_code == 200
    assert resp.json()["security_score_pct"] == 100.0

    # Testing endpoint
    resp = client.get("/api/v1/alerting-verification/testing")
    assert resp.status_code == 200
    assert resp.json()["all_tests_passed"] is True

    # Scorecard endpoint
    resp = client.get("/api/v1/alerting-verification/scorecard")
    assert resp.status_code == 200
    assert resp.json()["overall_score_pct"] >= 95.0

    # Verification run POST endpoint
    resp = client.post("/api/v1/alerting-verification/verify")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["certification_tier"] == "Enterprise Incident Ready"
