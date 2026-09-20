"""Test Suite for Phase 3H.3.9 - AI Health Monitoring Integration Verification Framework.

Tests all 12 modules, API routes, telemetry pipelines, dashboards, alerts, SLOs, and manifest exports.
"""

import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.ai_health_monitoring.architecture.ai_observability_architecture_verifier import AIObservabilityArchitectureVerifier
from app.platform_verification.ai_health_monitoring.metrics.ai_metrics_collector_verifier import AIMetricsCollectorVerifier
from app.platform_verification.ai_health_monitoring.dashboards.ai_dashboard_verifier import AIDashboardVerifier
from app.platform_verification.ai_health_monitoring.logging.ai_logging_verifier import AILoggingVerifier
from app.platform_verification.ai_health_monitoring.tracing.ai_tracing_verifier import AITracingVerifier
from app.platform_verification.ai_health_monitoring.alerting.ai_alerting_verifier import AIAlertingVerifier
from app.platform_verification.ai_health_monitoring.slo.ai_slo_monitoring_verifier import AISLOMonitoringVerifier
from app.platform_verification.ai_health_monitoring.incidents.ai_incident_detector_verifier import AIIncidentDetectorVerifier
from app.platform_verification.ai_health_monitoring.automation.ai_automated_response_verifier import AIAutomatedResponseVerifier
from app.platform_verification.ai_health_monitoring.security.ai_monitoring_security_verifier import AIMonitoringSecurityVerifier
from app.platform_verification.ai_health_monitoring.scoring.ai_monitoring_quality_scorer import AIMonitoringQualityScorer
from app.platform_verification.ai_health_monitoring.exporter.ai_monitoring_evidence_exporter import AIMonitoringEvidenceExporter
from app.platform_verification.ai_health_monitoring.runtime.ai_health_monitoring_runtime import AIHealthMonitoringRuntime
from app.platform_verification.ai_health_monitoring.api.ai_health_monitoring_api import router as ai_monitoring_router
from app.platform_verification.ai_health_monitoring.domain.models import (
    AIMetricCategory,
    AIObservabilityTier,
)


def test_part_3h_3_9_1_observability_architecture():
    verifier = AIObservabilityArchitectureVerifier()
    report = verifier.verify_architecture()
    assert report.passed is True
    assert report.metrics_pipeline == "connected"
    assert report.logs_pipeline == "connected"
    assert report.tracing_pipeline == "connected"
    assert len(report.pipelines) >= 3
    for p in report.pipelines:
        assert p.connected is True
        assert p.data_delivery_latency_ms < 100.0


def test_part_3h_3_9_2_metrics_collection():
    verifier = AIMetricsCollectorVerifier()
    report = verifier.verify_metrics_collection()
    assert report.passed is True
    assert report.total_metrics_collected >= 15
    assert len(report.metrics_by_category) == 5
    for cat in AIMetricCategory:
        assert cat.value in report.metrics_by_category
    for m in report.metrics:
        assert m.collected_successfully is True
        assert len(m.labels) >= 4


def test_part_3h_3_9_3_dashboards():
    verifier = AIDashboardVerifier()
    report = verifier.verify_dashboards()
    assert report.passed is True
    assert report.total_dashboards_verified >= 4
    for d in report.dashboards:
        assert d.verified is True
        assert d.panel_count >= 4
        for p in d.panels:
            assert p.promql_or_query != ""
            assert p.operational_question_answered != ""


def test_part_3h_3_9_4_logging():
    verifier = AILoggingVerifier()
    report = verifier.verify_logging()
    assert report.passed is True
    assert report.total_event_types_verified >= 3
    assert report.all_json_structured is True
    assert report.all_sanitized is True
    for ev in report.events:
        assert len(ev.required_fields) >= 5
        assert ev.sample_entry is not None


def test_part_3h_3_9_5_tracing_and_bottlenecks():
    verifier = AITracingVerifier()
    report = verifier.verify_tracing()
    assert report.passed is True
    assert report.total_spans_in_workflow >= 6
    assert report.total_workflow_duration_ms > 0
    assert report.ai_inference_duration_ms > 0
    assert report.ai_latency_percentage > 50.0
    assert "gemini" in report.bottleneck_identified or "inference" in report.bottleneck_identified


def test_part_3h_3_9_6_alerting_rules():
    verifier = AIAlertingVerifier()
    report = verifier.verify_alerting()
    assert report.passed is True
    assert report.total_alert_rules >= 4
    for rule in report.rules:
        assert rule.rule_active is True
        assert len(rule.notification_channels) >= 2
        assert rule.prescribed_action != ""


def test_part_3h_3_9_7_slos():
    verifier = AISLOMonitoringVerifier()
    report = verifier.verify_slos()
    assert report.passed is True
    assert report.total_slos_tracked >= 4
    assert report.all_slos_met is True
    for slo in report.slos:
        assert slo.compliant is True
        assert slo.current_attainment_pct >= slo.target_pct


def test_part_3h_3_9_8_incident_detection():
    verifier = AIIncidentDetectorVerifier()
    report = verifier.verify_incident_detection()
    assert report.passed is True
    assert report.total_incident_tests >= 3
    assert report.all_incidents_detected_and_handled is True
    for t in report.tests:
        assert t.alert_triggered is True
        assert t.dashboard_updated is True
        assert t.automated_response_executed is True
        assert t.recovery_validated is True


def test_part_3h_3_9_9_automated_response():
    verifier = AIAutomatedResponseVerifier()
    report = verifier.verify_automated_response()
    assert report.passed is True
    assert report.total_automation_rules >= 3
    assert report.all_rules_verified is True
    for r in report.rules:
        assert r.audit_logged is True
        assert r.latency_to_action_ms <= 250.0


def test_part_3h_3_9_10_monitoring_security():
    verifier = AIMonitoringSecurityVerifier()
    report = verifier.verify_security()
    assert report.passed is True
    assert report.sensitive_data_exposed is False
    assert report.total_checks >= 3
    for c in report.checks:
        assert c.rbac_enforced is True
        assert c.encryption_at_rest_in_transit is True


def test_part_3h_3_9_11_evidence_exporter_and_9_manifests(tmp_path):
    output_dir = str(tmp_path / "ai_monitoring_out")
    runtime = AIHealthMonitoringRuntime(export_dir=output_dir)
    res = runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "telemetry_report.json",
        "metrics_report.json",
        "dashboard_report.json",
        "logging_report.json",
        "tracing_report.json",
        "alerting_report.json",
        "slo_report.json",
        "incident_test_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing expected file {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_part_3h_3_9_12_quality_scorer_and_tier():
    runtime = AIHealthMonitoringRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == AIObservabilityTier.ENTERPRISE_AI_OBSERVABILITY_READY
    assert scorecard.certification_verdict == "CERTIFIED"


def test_ai_health_monitoring_fastapi_endpoints():
    app = FastAPI()
    app.include_router(ai_monitoring_router)
    client = TestClient(app)

    endpoints = [
        "/health/ai-monitoring/architecture",
        "/health/ai-monitoring/metrics",
        "/health/ai-monitoring/dashboards",
        "/health/ai-monitoring/logging",
        "/health/ai-monitoring/tracing",
        "/health/ai-monitoring/alerting",
        "/health/ai-monitoring/slos",
        "/health/ai-monitoring/incidents",
        "/health/ai-monitoring/automation",
        "/health/ai-monitoring/security",
        "/health/ai-monitoring/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    post_resp = client.post("/health/ai-monitoring/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["passed"] is True
    assert data["scorecard"]["overall_score"] >= 95.0
