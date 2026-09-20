"""Test Suite for Phase 3H.4 - Enterprise Health Monitoring, Alerting & Incident Signal Verification.

Validates all 12 sub-parts of Phase 3H.4:
1. Signal Architecture (12 Signals across 4 Categories)
2. Operational Metrics Collection (19 Metrics across 5 Domains)
3. Prometheus Scraping & OpenTelemetry Bridge (/metrics)
4. Grafana Dashboards (4 Enterprise Dashboards)
5. Alert Rules (Critical & Warning AlertManager rules)
6. Alert Accuracy (100% Precision, 100% Recall, Auto-Resolution)
7. Actionable Incident Signals (4 Production Scenarios)
8. Alert Fatigue Prevention (Deduplication & 90%+ Compression)
9. Chaos & Failure Injection Simulations (DB, Redis, Worker, AI)
10. Telemetry Security Audit (0 Secret/PII Leaks, Zero-Leak Verified)
11. Operational Readiness Scorecard (>= 95.00% Score, Enterprise Observability Ready)
12. Evidence Generation (10 Structured JSON Manifests)
Plus FastAPI HTTP router endpoints.
"""

import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.health_monitoring_alerting.signals.health_signal_architecture_verifier import (
    HealthSignalArchitectureVerifier,
)
from app.platform_verification.health_monitoring_alerting.metrics.operational_metrics_verifier import (
    OperationalMetricsVerifier,
)
from app.platform_verification.health_monitoring_alerting.prometheus.prometheus_scraping_verifier import (
    PrometheusScrapingVerifier,
)
from app.platform_verification.health_monitoring_alerting.grafana.grafana_dashboard_verifier import (
    GrafanaDashboardVerifier,
)
from app.platform_verification.health_monitoring_alerting.alerting.alert_rule_verifier import (
    AlertRuleVerifier,
)
from app.platform_verification.health_monitoring_alerting.accuracy.alert_accuracy_verifier import (
    AlertAccuracyVerifier,
)
from app.platform_verification.health_monitoring_alerting.incident.incident_signal_verifier import (
    IncidentSignalVerifier,
)
from app.platform_verification.health_monitoring_alerting.fatigue.alert_fatigue_prevention_verifier import (
    AlertFatiguePreventionVerifier,
)
from app.platform_verification.health_monitoring_alerting.simulation.monitoring_failure_simulator import (
    MonitoringFailureSimulator,
)
from app.platform_verification.health_monitoring_alerting.security.observability_security_auditor import (
    ObservabilitySecurityAuditor,
)
from app.platform_verification.health_monitoring_alerting.scoring.health_monitoring_scorer import (
    HealthMonitoringScorer,
)
from app.platform_verification.health_monitoring_alerting.exporter.health_monitoring_evidence_exporter import (
    HealthMonitoringEvidenceExporter,
)
from app.platform_verification.health_monitoring_alerting.runtime.health_monitoring_alerting_runtime import (
    HealthMonitoringAlertingRuntime,
)
from app.platform_verification.health_monitoring_alerting.api.health_monitoring_alerting_api import (
    router as health_monitoring_router,
)
from app.platform_verification.health_monitoring_alerting.domain.models import (
    SignalCategory,
    AlertSeverity,
    IncidentState,
    ObservabilityTier,
)


def test_part_3h_4_1_signal_architecture():
    verifier = HealthSignalArchitectureVerifier()
    report = verifier.verify_signal_architecture()
    assert report.status == "PASS"
    assert report.total_signals == 12
    assert report.availability_signals_count == 3
    assert report.performance_signals_count == 3
    assert report.resource_signals_count == 3
    assert report.dependency_signals_count == 3
    assert len(report.signals) == 12
    for sig in report.signals:
        assert sig.healthy is True
        assert sig.metric_source != ""


def test_part_3h_4_2_operational_metrics_collection():
    verifier = OperationalMetricsVerifier()
    report = verifier.verify_metrics_collection()
    assert report.status == "PASS"
    assert report.total_metrics_tracked == 19
    assert report.api_metrics_count == 4
    assert report.agent_runtime_metrics_count == 4
    assert report.queue_metrics_count == 4
    assert report.worker_metrics_count == 3
    assert report.ai_metrics_count == 4
    assert len(report.metrics) == 19
    for m in report.metrics:
        assert m.sample_value >= 0
        assert m.unit != ""
        assert m.queryable is True


def test_part_3h_4_3_prometheus_and_opentelemetry():
    verifier = PrometheusScrapingVerifier()
    report = verifier.verify_prometheus_scraping()
    assert report.status == "PASS"
    assert report.endpoint == "/metrics"
    assert report.http_status == 200
    assert report.exported_series_count >= 19
    assert report.scrape_duration_ms < 50.0
    assert report.open_telemetry_bridge_active is True
    assert report.metric_lifecycle_validated is True


def test_part_3h_4_4_grafana_dashboards():
    verifier = GrafanaDashboardVerifier()
    report = verifier.verify_dashboards()
    assert report.status == "PASS"
    assert report.total_dashboards == 4
    expected_dashboards = [
        "docutask-system-health",
        "docutask-ai-processing",
        "docutask-infrastructure",
        "docutask-agent-runtime",
    ]
    found_dashboards = [d.dashboard_id for d in report.dashboards]
    for exp in expected_dashboards:
        assert exp in found_dashboards
    for d in report.dashboards:
        assert d.verified is True
        assert d.panels_count >= 4


def test_part_3h_4_5_alert_rules():
    verifier = AlertRuleVerifier()
    report = verifier.verify_alert_rules()
    assert report.status == "PASS"
    assert report.total_rules_defined == 6
    assert report.critical_rules_count == 3
    assert report.warning_rules_count == 3
    for r in report.rules:
        assert r.active is True
        assert r.condition != ""
        assert r.message != ""
        assert r.owner != ""
        assert r.action != ""


def test_part_3h_4_6_alert_accuracy_and_resolution():
    verifier = AlertAccuracyVerifier()
    report = verifier.verify_alert_accuracy()
    assert report.status == "PASS"
    assert report.precision_pct == 100.0
    assert report.recall_pct == 100.0
    assert report.auto_resolution_verified is True
    assert report.false_positives == 0
    assert report.false_negatives == 0


def test_part_3h_4_7_incident_signals():
    verifier = IncidentSignalVerifier()
    report = verifier.verify_incident_signals()
    assert report.status == "PASS"
    assert report.incidents_generated == 4
    assert report.all_payloads_actionable is True
    assert report.dependency_chain_included is True
    assert report.logs_attached is True
    for inc in report.incidents:
        assert inc.severity in [AlertSeverity.CRITICAL, AlertSeverity.WARNING]
        assert len(inc.dependency_chain) >= 2
        assert len(inc.metrics_snapshot) >= 1
        assert inc.recommended_action != ""


def test_part_3h_4_8_fatigue_prevention_and_deduplication():
    verifier = AlertFatiguePreventionVerifier()
    report = verifier.verify_fatigue_prevention()
    assert report.status == "PASS"
    assert report.raw_alerts_received >= 40
    assert report.deduplicated_alerts_grouped <= 10
    assert report.compression_ratio_pct > 90.0
    assert report.grouping_by_root_cause_active is True
    assert report.maintenance_window_suppression_active is True


def test_part_3h_4_9_chaos_failure_simulations():
    verifier = MonitoringFailureSimulator()
    report = verifier.run_monitoring_failure_tests()
    assert report.status == "PASS"
    assert report.total_tests == 4
    assert report.passed_tests == 4
    for t in report.tests:
        assert t.metric_updated is True
        assert t.alert_fired is True
        assert t.incident_created is True
        assert t.alert_cleared_on_recovery is True
        assert t.passed is True


def test_part_3h_4_10_security_audit():
    verifier = ObservabilitySecurityAuditor()
    report = verifier.audit_security()
    assert report.status == "PASS"
    assert report.secret_leaks_found == 0
    assert report.token_leaks_found == 0
    assert report.pii_leaks_found == 0
    assert report.zero_leak_verified is True
    assert report.metrics_scanned_count >= 19


def test_part_3h_4_11_scoring_and_enterprise_tier():
    runtime = HealthMonitoringAlertingRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == ObservabilityTier.ENTERPRISE_OBSERVABILITY_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.metrics_completeness_score >= 95.0
    assert scorecard.monitoring_accuracy_score >= 95.0
    assert scorecard.alert_reliability_score >= 95.0


def test_part_3h_4_12_evidence_exporter_and_10_manifests(tmp_path):
    output_dir = str(tmp_path / "test_health_manifests")
    runtime = HealthMonitoringAlertingRuntime(export_dir=output_dir)
    res = runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "signal_architecture_report.json",
        "metrics_report.json",
        "prometheus_report.json",
        "dashboard_report.json",
        "alert_report.json",
        "incident_report.json",
        "failure_test_report.json",
        "security_report.json",
        "certification_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing manifest {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_health_monitoring_alerting_fastapi_endpoints():
    app = FastAPI()
    app.include_router(health_monitoring_router)
    client = TestClient(app)

    endpoints = [
        "/health/monitoring/signals",
        "/health/monitoring/metrics",
        "/health/monitoring/prometheus",
        "/health/monitoring/dashboards",
        "/health/monitoring/alerts",
        "/health/monitoring/accuracy",
        "/health/monitoring/incidents",
        "/health/monitoring/fatigue",
        "/health/monitoring/simulation",
        "/health/monitoring/security",
        "/health/monitoring/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    post_resp = client.post("/health/monitoring/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["scorecard"]["overall_score"] >= 95.0
