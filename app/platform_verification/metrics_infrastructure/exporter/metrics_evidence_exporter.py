"""
Phase 3I.3: Evidence Exporter for Enterprise Metrics Infrastructure Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    MetricsArchitectureReport,
    MetricsStandardReport,
    ApplicationMetricsReport,
    AIMetricsReport,
    InfrastructureMetricsReport,
    BusinessSLAMetricsReport,
    DashboardReport,
    AlertValidationReport,
    MetricsAccuracyReport,
    MetricsSecurityReport,
    MetricsPerformanceReport,
    ChaosMetricReport,
    MetricsCertificationReport,
)
from ..domain.interfaces import IMetricsEvidenceExporter


class MetricsEvidenceExporter(IMetricsEvidenceExporter):
    """
    Exports standardized JSON evidence reports plus signed metadata.json with SHA-256 cryptographic digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        arch_report: MetricsArchitectureReport,
        std_report: MetricsStandardReport,
        app_report: ApplicationMetricsReport,
        ai_report: AIMetricsReport,
        infra_report: InfrastructureMetricsReport,
        biz_report: BusinessSLAMetricsReport,
        dash_report: DashboardReport,
        alert_report: AlertValidationReport,
        acc_report: MetricsAccuracyReport,
        sec_report: MetricsSecurityReport,
        perf_report: MetricsPerformanceReport,
        chaos_report: ChaosMetricReport,
        certification_report: MetricsCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "architecture_report.json": arch_report.model_dump(mode="json"),
            "standard_validation.json": std_report.model_dump(mode="json"),
            "application_metrics_report.json": app_report.model_dump(mode="json"),
            "ai_metrics_report.json": ai_report.model_dump(mode="json"),
            "infrastructure_metrics_report.json": infra_report.model_dump(mode="json"),
            "dashboard_report.json": dash_report.model_dump(mode="json"),
            "alert_validation_report.json": alert_report.model_dump(mode="json"),
            "security_report.json": sec_report.model_dump(mode="json"),
            "performance_report.json": perf_report.model_dump(mode="json"),
            "certification_report.json": certification_report.model_dump(mode="json"),
        }

        manifest: Dict[str, str] = {}
        for filename, data in report_payloads.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            sha256_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            manifest[filename] = sha256_hash

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "Phase 3I.3 — Enterprise Metrics Infrastructure Verification Framework",
            "environment": "PRODUCTION_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "services_monitored": arch_report.services_monitored,
            "overall_score_pct": certification_report.overall_score_pct,
            "certification_tier": certification_report.certification_tier.value,
            "certification_granted": certification_report.certification_granted,
            "total_artifacts": len(manifest),
            "manifest_sha256": manifest,
            "auditor": certification_report.auditor,
        }

        meta_path = os.path.join(output_dir, "metadata.json")
        meta_str = json.dumps(metadata, indent=2)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(meta_str)

        return metadata
