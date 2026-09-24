"""Comprehensive Test Suite for Phase 3H.3.5: Enterprise Health Monitoring Integration.

Validates all 12 core observability subsystems, domain models, Prometheus scraping,
Grafana dashboards, AlertManager rules, distributed tracing, incident correlation,
security redaction, and evidence artifact generation.
"""

from __future__ import annotations

import json
from pathlib import Path


from app.platform_verification.health_monitoring_integration.alerting.alert_quality_evaluator import (
    AlertQualityEvaluator,
)
from app.platform_verification.health_monitoring_integration.alerting.alert_rule_manager import (
    AlertRuleManager,
)
from app.platform_verification.health_monitoring_integration.architecture.observability_arch_verifier import (
    ObservabilityArchVerifier,
)
from app.platform_verification.health_monitoring_integration.domain.models import (
    AlertConfigurationReport,
    AlertQualityReport,
    FailureSimulationReport,
    GrafanaDashboardReport,
    HealthMetricsInventoryReport,
    IncidentVisibilityReport,
    MonitoringQualityScorecard,
    MonitoringSecurityReport,
    ObservabilityArchitectureReport,
    ObservabilityTier,
    PrometheusVerificationReport,
    TracingVerificationReport,
)
from app.platform_verification.health_monitoring_integration.exporter.monitoring_evidence_exporter import (
    MonitoringEvidenceExporter,
)
from app.platform_verification.health_monitoring_integration.grafana.grafana_dashboard_builder import (
    GrafanaDashboardBuilder,
)
from app.platform_verification.health_monitoring_integration.incident.incident_visibility_engine import (
    IncidentVisibilityEngine,
)
from app.platform_verification.health_monitoring_integration.inventory.health_metrics_collector import (
    HealthMetricsCollector,
)
from app.platform_verification.health_monitoring_integration.prometheus.prometheus_verifier import (
    PrometheusVerifier,
)
from app.platform_verification.health_monitoring_integration.runtime.monitoring_integration_runtime import (
    MonitoringIntegrationRuntime,
)
from app.platform_verification.health_monitoring_integration.security.monitoring_security_auditor import (
    MonitoringSecurityAuditor,
)
from app.platform_verification.health_monitoring_integration.simulation.monitoring_simulation_runner import (
    MonitoringSimulationRunner,
)
from app.platform_verification.health_monitoring_integration.tracing.distributed_trace_verifier import (
    DistributedTraceVerifier,
)


# ============================================================================
# Part 1: Observability Architecture Verifier Tests
# ============================================================================
def test_observability_architecture() -> None:
    verifier = ObservabilityArchVerifier()
    report: ObservabilityArchitectureReport = verifier.verify_architecture()

    assert report.total_expected_services == 8
    assert report.services_instrumented == 8
    assert report.metrics_pipeline_active is True
    assert report.tracing_pipeline_active is True
    assert report.logging_pipeline_active is True
    assert report.passed is True

    service_names = {s.service_name for s in report.services}
    assert "api_service" in service_names
    assert "agent_runtime" in service_names
    assert "worker_fleet" in service_names
    assert "postgres_db" in service_names
    assert "redis_queue" in service_names
    assert "storage_layer" in service_names
    assert "ocr_pipeline" in service_names
    assert "gemini_ai_provider" in service_names


# ============================================================================
# Part 2: Health Metrics Inventory Tests
# ============================================================================
def test_health_metrics_inventory() -> None:
    collector = HealthMetricsCollector()
    report: HealthMetricsInventoryReport = collector.collect_inventory()

    assert report.total_metrics_cataloged >= 25
    assert len(report.categories_covered) >= 8
    assert report.passed is True

    metric_names = {m.name for m in report.metrics}
    assert "service_up" in metric_names
    assert "http_requests_total" in metric_names
    assert "http_request_duration_seconds" in metric_names
    assert "agent_execution_total" in metric_names
    assert "worker_active_count" in metric_names
    assert "redis_queue_depth" in metric_names
    assert "postgres_connection_count" in metric_names
    assert "gemini_request_latency_seconds" in metric_names


# ============================================================================
# Part 3: Prometheus Verification Tests
# ============================================================================
def test_prometheus_verification() -> None:
    verifier = PrometheusVerifier()
    report: PrometheusVerificationReport = verifier.verify_prometheus()

    assert report.endpoint_exposed is True
    assert report.scrape_successful is True
    assert report.historical_query_supported is True
    assert report.target_down_detection_verified is True
    assert len(report.targets) >= 5
    assert report.passed is True


# ============================================================================
# Part 4: Grafana Operational Dashboards Tests
# ============================================================================
def test_grafana_dashboards() -> None:
    builder = GrafanaDashboardBuilder()
    report: GrafanaDashboardReport = builder.verify_dashboards()

    assert report.total_dashboards == 4
    assert report.outage_tested is True
    assert report.passed is True

    categories = {d.category for d in report.dashboards_validated}
    assert "Overview" in categories
    assert "Agent Operations" in categories
    assert "Infrastructure" in categories
    assert "Incident Response" in categories

    for dash in report.dashboards_validated:
        assert len(dash.panels) >= 4
        assert dash.valid is True


# ============================================================================
# Part 5: Alert Configuration Tests
# ============================================================================
def test_alert_configuration() -> None:
    manager = AlertRuleManager()
    report: AlertConfigurationReport = manager.get_alert_configuration()

    assert report.total_rules_configured >= 6
    assert report.critical_rules_count >= 2
    assert report.passed is True

    rule_names = {r.alert_name for r in report.rules}
    assert "ServiceDown" in rule_names
    assert "ApiErrorSpike" in rule_names
    assert "QueueExplosion" in rule_names
    assert "WorkerFleetHeartbeatFailure" in rule_names
    assert "PostgresConnectionSaturation" in rule_names
    assert "GeminiProviderDegradation" in rule_names

    for rule in report.rules:
        assert rule.owner
        assert rule.runbook_url.startswith("https://")
        assert rule.recovery_action


# ============================================================================
# Part 6: Alert Quality Evaluation Tests
# ============================================================================
def test_alert_quality_evaluation() -> None:
    evaluator = AlertQualityEvaluator()
    report: AlertQualityReport = evaluator.evaluate_quality()

    assert report.metrics.precision >= 0.95
    assert report.metrics.recall >= 0.95
    assert report.metrics.false_positive_rate <= 0.05
    assert report.metrics.false_negative_rate <= 0.05
    assert report.metrics.avg_detection_time_seconds <= 15.0
    assert report.metrics.noisy_alerts_detected == 0
    assert report.metrics.duplicate_alerts_detected == 0
    assert report.benchmarks_met is True
    assert report.passed is True


# ============================================================================
# Part 7: Incident Visibility Tests
# ============================================================================
def test_incident_visibility() -> None:
    engine = IncidentVisibilityEngine()
    report: IncidentVisibilityReport = engine.verify_incident_visibility("doc_99887")

    assert report.document_id == "doc_99887"
    assert report.correlation_complete is True
    assert report.passed is True
    assert len(report.correlated_events) >= 5

    event_types = {e.event_type for e in report.correlated_events}
    assert "trace_span" in event_types
    assert "metric_spike" in event_types
    assert "alert_fired" in event_types
    assert "error_log" in event_types

    assert report.diagnosis.recovery_verified is True
    assert "doc_99887" in report.diagnosis.affected_document_ids


# ============================================================================
# Part 8: Failure Simulation Tests
# ============================================================================
def test_failure_simulations() -> None:
    runner = MonitoringSimulationRunner()
    report: FailureSimulationReport = runner.run_simulations()

    assert report.total_scenarios_run == 4
    assert report.passed_scenarios == 4
    assert report.avg_detection_time_seconds <= 10.0
    assert report.avg_alert_time_seconds <= 15.0
    assert report.avg_recovery_time_seconds <= 30.0
    assert report.passed is True


# ============================================================================
# Part 9: Distributed Tracing Tests
# ============================================================================
def test_distributed_tracing() -> None:
    verifier = DistributedTraceVerifier()
    report: TracingVerificationReport = verifier.verify_tracing()

    assert report.propagation_verified is True
    assert report.correlation_ids_valid is True
    assert report.span_accuracy_pct == 100.0
    assert report.trace.total_spans == 8
    assert report.trace.missing_spans_count == 0
    assert report.passed is True


# ============================================================================
# Part 10: Monitoring Security Tests
# ============================================================================
def test_monitoring_security() -> None:
    auditor = MonitoringSecurityAuditor()
    report: MonitoringSecurityReport = auditor.audit_security()

    assert report.secrets_leaked is False
    assert report.redaction_verified is True
    assert report.auth_enforced is True
    assert report.total_security_checks >= 5
    assert report.passed is True


# ============================================================================
# Part 11: Evidence Exporter Tests
# ============================================================================
def test_monitoring_evidence_exporter(tmp_path: Path) -> None:
    exporter = MonitoringEvidenceExporter(output_dir=tmp_path)
    runtime = MonitoringIntegrationRuntime(export_dir=tmp_path)
    results = runtime.run_full_verification()

    manifests = exporter.export_all(
        arch_report=results["arch_report"],
        metrics_report=results["metrics_report"],
        prom_report=results["prom_report"],
        grafana_report=results["grafana_report"],
        alert_config_report=results["alert_config_report"],
        alert_quality_report=results["alert_quality_report"],
        incident_report=results["incident_report"],
        simulation_report=results["simulation_report"],
        tracing_report=results["tracing_report"],
        security_report=results["security_report"],
        scorecard=results["scorecard"],
    )

    assert len(manifests) == 10
    for name, path in manifests.items():
        assert path.exists()
        assert path.stat().st_size > 0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)


# ============================================================================
# Part 12: Scoring & Certification Tests
# ============================================================================
def test_monitoring_quality_scorecard() -> None:
    runtime = MonitoringIntegrationRuntime()
    results = runtime.run_full_verification()
    scorecard: MonitoringQualityScorecard = results["scorecard"]

    assert scorecard.overall_score >= 95.00
    assert scorecard.certification_tier == ObservabilityTier.ENTERPRISE_OBSERVABILITY_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True

    assert scorecard.metric_coverage_score == 100.0
    assert scorecard.alert_accuracy_score == 100.0
    assert scorecard.dashboard_quality_score == 100.0
    assert scorecard.trace_visibility_score == 100.0
    assert scorecard.incident_diagnosis_score == 100.0
    assert scorecard.security_score == 100.0
