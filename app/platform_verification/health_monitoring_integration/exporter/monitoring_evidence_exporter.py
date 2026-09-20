"""Monitoring Evidence Exporter (Part 3H.3.5.11).

Exports all 10 required health monitoring verification audit manifests to health_monitoring_verification/ directory.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

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


class MonitoringEvidenceExporter:
    """Exports structured audit manifests for Phase 3H.3.5."""

    def __init__(self, output_dir: Optional[Path | str] = None) -> None:
        self.output_dir = Path(output_dir or "health_monitoring_verification")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_all(
        self,
        arch_report: ObservabilityArchitectureReport,
        metrics_report: HealthMetricsInventoryReport,
        prom_report: PrometheusVerificationReport,
        grafana_report: GrafanaDashboardReport,
        alert_config_report: AlertConfigurationReport,
        alert_quality_report: AlertQualityReport,
        incident_report: IncidentVisibilityReport,
        simulation_report: FailureSimulationReport,
        tracing_report: TracingVerificationReport,
        security_report: MonitoringSecurityReport,
        scorecard: MonitoringQualityScorecard,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Path]:
        """Persists all 10 manifests to disk."""
        exported: Dict[str, Path] = {}

        # 1. observability_architecture_report.json
        arch_path = self.output_dir / "observability_architecture_report.json"
        with open(arch_path, "w", encoding="utf-8") as f:
            json.dump(asdict(arch_report), f, indent=2, default=str)
        exported["observability_architecture_report"] = arch_path

        # 2. metrics_inventory.json
        metrics_path = self.output_dir / "metrics_inventory.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics_report), f, indent=2, default=str)
        exported["metrics_inventory"] = metrics_path

        # 3. prometheus_report.json
        prom_path = self.output_dir / "prometheus_report.json"
        with open(prom_path, "w", encoding="utf-8") as f:
            json.dump(asdict(prom_report), f, indent=2, default=str)
        exported["prometheus_report"] = prom_path

        # 4. grafana_report.json
        grafana_path = self.output_dir / "grafana_report.json"
        with open(grafana_path, "w", encoding="utf-8") as f:
            json.dump(asdict(grafana_report), f, indent=2, default=str)
        exported["grafana_report"] = grafana_path

        # 5. alert_report.json (Combines configuration and quality metrics)
        alert_path = self.output_dir / "alert_report.json"
        alert_payload = {
            "configuration": asdict(alert_config_report),
            "quality_evaluation": asdict(alert_quality_report),
            "passed": alert_config_report.passed and alert_quality_report.passed,
        }
        with open(alert_path, "w", encoding="utf-8") as f:
            json.dump(alert_payload, f, indent=2, default=str)
        exported["alert_report"] = alert_path

        # 6. tracing_report.json
        tracing_path = self.output_dir / "tracing_report.json"
        with open(tracing_path, "w", encoding="utf-8") as f:
            json.dump(asdict(tracing_report), f, indent=2, default=str)
        exported["tracing_report"] = tracing_path

        # 7. security_report.json
        sec_path = self.output_dir / "security_report.json"
        with open(sec_path, "w", encoding="utf-8") as f:
            json.dump(asdict(security_report), f, indent=2, default=str)
        exported["security_report"] = sec_path

        # 8. incident_visibility_report.json
        inc_path = self.output_dir / "incident_visibility_report.json"
        with open(inc_path, "w", encoding="utf-8") as f:
            json.dump(asdict(incident_report), f, indent=2, default=str)
        exported["incident_visibility_report"] = inc_path

        # 9. failure_simulation_report.json
        sim_path = self.output_dir / "failure_simulation_report.json"
        with open(sim_path, "w", encoding="utf-8") as f:
            json.dump(asdict(simulation_report), f, indent=2, default=str)
        exported["failure_simulation_report"] = sim_path

        # 10. metadata.json
        meta_path = self.output_dir / "metadata.json"
        meta_payload = {
            "system": "DocuTask Agent",
            "phase": "3H.3.5",
            "component": "Enterprise Health Monitoring Integration",
            "status": scorecard.certification_verdict,
            "overall_score": scorecard.overall_score,
            "tier": scorecard.certification_tier.value if isinstance(scorecard.certification_tier, ObservabilityTier) else str(scorecard.certification_tier),
            "passed": scorecard.passed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": "production-simulation",
            "dimension_scores": {
                "metric_coverage": scorecard.metric_coverage_score,
                "alert_accuracy": scorecard.alert_accuracy_score,
                "dashboard_quality": scorecard.dashboard_quality_score,
                "trace_visibility": scorecard.trace_visibility_score,
                "incident_diagnosis": scorecard.incident_diagnosis_score,
                "security": scorecard.security_score,
            },
            "manifest_files": [
                "observability_architecture_report.json",
                "metrics_inventory.json",
                "prometheus_report.json",
                "grafana_report.json",
                "alert_report.json",
                "tracing_report.json",
                "security_report.json",
                "incident_visibility_report.json",
                "failure_simulation_report.json",
                "metadata.json",
            ],
            "custom_metadata": additional_metadata or {},
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_payload, f, indent=2, default=str)
        exported["metadata"] = meta_path

        return exported
