"""
Phase 3H.5.10: Health Security Evidence Exporter
"""
import os
import json
import hashlib
from typing import Dict
from datetime import datetime, timezone

from ..domain.models import (
    EndpointSecurityReport,
    HealthAuthorizationReport,
    MetricsPrivacyReport,
    LogSecurityReport,
    AlertSecurityReport,
    TraceSecurityReport,
    SecretScanReport,
    DashboardSecurityReport,
    SecurityFailureInjectionReport,
    ComplianceSecurityReport,
    HealthSecurityScorecard,
)


class HealthSecurityExporter:
    """
    Exports all 10 verification reports, certification scorecard, and metadata.json
    with SHA-256 cryptographic hashes for enterprise compliance audits.
    """

    def __init__(self, output_dir: str = "health_security_verification"):
        self.output_dir = output_dir

    def _compute_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        endpoint_report: EndpointSecurityReport,
        auth_report: HealthAuthorizationReport,
        metrics_report: MetricsPrivacyReport,
        log_report: LogSecurityReport,
        alert_report: AlertSecurityReport,
        trace_report: TraceSecurityReport,
        secret_report: SecretScanReport,
        dashboard_report: DashboardSecurityReport,
        injection_report: SecurityFailureInjectionReport,
        compliance_report: ComplianceSecurityReport,
        scorecard: HealthSecurityScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)

        artifacts = {
            "endpoint_security_report.json": endpoint_report.model_dump(),
            "authorization_report.json": auth_report.model_dump(),
            "metrics_privacy_report.json": metrics_report.model_dump(),
            "log_security_report.json": log_report.model_dump(),
            "alert_security_report.json": alert_report.model_dump(),
            "trace_security_report.json": trace_report.model_dump(),
            "secret_scan_report.json": secret_report.model_dump(),
            "dashboard_security_report.json": dashboard_report.model_dump(),
            "failure_injection_report.json": injection_report.model_dump(),
            "compliance_report.json": compliance_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        generated_files = {}
        for filename, data in artifacts.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            generated_files[filename] = filepath

        # Calculate checksums for metadata.json
        checksums = {}
        for filename, filepath in generated_files.items():
            checksums[filename] = self._compute_sha256(filepath)

        metadata = {
            "framework_phase": "Phase 3H.5.10 — Enterprise Health Security, Privacy & Information Exposure Verification",
            "platform": "DocuTask Enterprise Agent Platform",
            "verification_id": scorecard.verification_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "overall_score": scorecard.overall_health_security_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "zero_critical_vulnerabilities": scorecard.zero_critical_vulnerabilities,
            "total_audits_performed": scorecard.total_audits_performed,
            "file_manifest": checksums,
        }

        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        generated_files["metadata.json"] = metadata_path
        return generated_files
