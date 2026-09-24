"""
Phase 3I.5: Evidence Exporter for Enterprise Alerting & Incident Detection Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.models import (
    AlertingArchitectureReport,
    AlertSignalCoverageReport,
    AlertRulesReport,
    AIAgentAlertReport,
    IncidentSeverityReport,
    RemediationReport,
    AlertSecurityReport,
    AlertTestingReport,
    AlertingCertificationReport,
)
from ..domain.interfaces import IAlertingEvidenceExporter


class AlertingEvidenceExporter(IAlertingEvidenceExporter):
    """
    Exports standardized JSON evidence reports plus signed metadata.json with SHA-256 cryptographic digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AlertingArchitectureReport,
        signal_report: AlertSignalCoverageReport,
        rule_report: AlertRulesReport,
        ai_report: AIAgentAlertReport,
        routing_report: IncidentSeverityReport,
        remediation_report: RemediationReport,
        sec_report: AlertSecurityReport,
        testing_report: AlertTestingReport,
        certification_report: AlertingCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "architecture_report.json": arch_report.model_dump(mode="json"),
            "signal_coverage_report.json": signal_report.model_dump(mode="json"),
            "alert_rules_report.json": rule_report.model_dump(mode="json"),
            "ai_alert_report.json": ai_report.model_dump(mode="json"),
            "routing_report.json": routing_report.model_dump(mode="json"),
            "severity_report.json": routing_report.model_dump(mode="json"),
            "remediation_report.json": remediation_report.model_dump(mode="json"),
            "security_report.json": sec_report.model_dump(mode="json"),
            "testing_report.json": testing_report.model_dump(mode="json"),
            "certification_report.json": certification_report.model_dump(mode="json"),
        }

        manifest: Dict[str, str] = {}
        for raw_filename, data in report_payloads.items():
            filename = validate_safe_filename_segment(raw_filename)
            filepath = resolve_safe_path(output_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            sha256_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            manifest[filename] = sha256_hash

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "Phase 3I.5 — Enterprise Alerting & Incident Detection Verification Framework",
            "environment": "PRODUCTION_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "rules_configured": arch_report.rules_configured_count,
            "overall_score_pct": certification_report.overall_score_pct,
            "certification_tier": certification_report.certification_tier.value,
            "certification_granted": certification_report.certification_granted,
            "total_artifacts": len(manifest),
            "manifest_sha256": manifest,
            "auditor": certification_report.auditor,
        }

        meta_path = resolve_safe_path(output_dir, "metadata.json")
        meta_str = json.dumps(metadata, indent=2)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(meta_str)

        return metadata
