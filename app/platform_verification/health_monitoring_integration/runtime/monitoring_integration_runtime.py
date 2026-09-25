"""Monitoring Integration Runtime Coordinator.

Unites all 12 parts of the Enterprise Health Monitoring Integration Verification Framework.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

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
from app.platform_verification.health_monitoring_integration.scoring.monitoring_quality_scorer import (
    MonitoringQualityScorer,
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


class MonitoringIntegrationRuntime:
    """Master coordinator executing end-to-end health monitoring integration verification."""

    def __init__(self, export_dir: Optional[Path | str] = None) -> None:
        self.export_dir = Path(export_dir or "health_monitoring_verification")
        self.arch_verifier = ObservabilityArchVerifier()
        self.metrics_collector = HealthMetricsCollector()
        self.prometheus_verifier = PrometheusVerifier()
        self.dashboard_builder = GrafanaDashboardBuilder()
        self.alert_manager = AlertRuleManager()
        self.alert_evaluator = AlertQualityEvaluator()
        self.incident_engine = IncidentVisibilityEngine()
        self.simulation_runner = MonitoringSimulationRunner()
        self.trace_verifier = DistributedTraceVerifier()
        self.security_auditor = MonitoringSecurityAuditor()
        self.scorer = MonitoringQualityScorer()
        self.evidence_exporter = MonitoringEvidenceExporter(output_dir=self.export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Runs the complete verification lifecycle across all 12 parts."""
        # 1. Architecture Verification
        arch_report: ObservabilityArchitectureReport = self.arch_verifier.verify_architecture()

        # 2. Metrics Inventory Collection
        metrics_report: HealthMetricsInventoryReport = self.metrics_collector.collect_inventory()

        # 3. Prometheus Verification
        prom_report: PrometheusVerificationReport = self.prometheus_verifier.verify_prometheus()

        # 4. Grafana Dashboard Verification
        grafana_report: GrafanaDashboardReport = self.dashboard_builder.verify_dashboards()

        # 5. Alert Configuration
        alert_config_report: AlertConfigurationReport = self.alert_manager.get_alert_configuration()

        # 6. Alert Quality Evaluation
        alert_quality_report: AlertQualityReport = self.alert_evaluator.evaluate_quality()

        # 7. Incident Visibility Verification
        incident_report: IncidentVisibilityReport = self.incident_engine.verify_incident_visibility()

        # 8. Failure Simulations
        simulation_report: FailureSimulationReport = self.simulation_runner.run_simulations()

        # 9. Distributed Tracing Verification
        tracing_report: TracingVerificationReport = self.trace_verifier.verify_tracing()

        # 10. Security Audit
        security_report: MonitoringSecurityReport = self.security_auditor.audit_security()

        # 11. Scorecard Calculation
        scorecard: MonitoringQualityScorecard = self.scorer.compute_scorecard(
            arch_report=arch_report,
            metrics_report=metrics_report,
            prom_report=prom_report,
            grafana_report=grafana_report,
            alert_config_report=alert_config_report,
            alert_quality_report=alert_quality_report,
            incident_report=incident_report,
            simulation_report=simulation_report,
            tracing_report=tracing_report,
            security_report=security_report,
        )

        # 12. Export 10 Evidence Manifests
        manifest_files = self.evidence_exporter.export_all(
            arch_report=arch_report,
            metrics_report=metrics_report,
            prom_report=prom_report,
            grafana_report=grafana_report,
            alert_config_report=alert_config_report,
            alert_quality_report=alert_quality_report,
            incident_report=incident_report,
            simulation_report=simulation_report,
            tracing_report=tracing_report,
            security_report=security_report,
            scorecard=scorecard,
            additional_metadata={
                "services_count": arch_report.services_instrumented,
                "metrics_cataloged": metrics_report.total_metrics_cataloged,
                "dashboards_count": grafana_report.total_dashboards,
                "alert_rules_count": alert_config_report.total_rules_configured,
                "spans_in_trace": tracing_report.trace.total_spans,
                "simulation_scenarios_passed": simulation_report.passed_scenarios,
            },
        )

        return {
            "scorecard": scorecard,
            "manifest_files": manifest_files,
            "arch_report": arch_report,
            "metrics_report": metrics_report,
            "prom_report": prom_report,
            "grafana_report": grafana_report,
            "alert_config_report": alert_config_report,
            "alert_quality_report": alert_quality_report,
            "incident_report": incident_report,
            "simulation_report": simulation_report,
            "tracing_report": tracing_report,
            "security_report": security_report,
        }
