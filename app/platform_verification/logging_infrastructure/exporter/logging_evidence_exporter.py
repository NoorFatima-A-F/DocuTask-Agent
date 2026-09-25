"""
Phase 3I.2: Evidence Exporter for Enterprise Logging Infrastructure Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    ArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AgentLoggingReport,
    SecurityReport,
    PerformanceReport,
    FailureTestReport,
    CertificationReport,
)
from ..domain.interfaces import ILoggingEvidenceExporter


class LoggingEvidenceExporter(ILoggingEvidenceExporter):
    """
    Exports 8 standardized JSON evidence reports plus signed metadata.json with SHA-256 digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        arch_report: ArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        agent_report: AgentLoggingReport,
        sec_report: SecurityReport,
        perf_report: PerformanceReport,
        failure_report: FailureTestReport,
        certification_report: CertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "architecture_report.json": arch_report.model_dump(mode="json"),
            "structured_logging_report.json": struct_report.model_dump(mode="json"),
            "correlation_report.json": corr_report.model_dump(mode="json"),
            "agent_logging_report.json": agent_report.model_dump(mode="json"),
            "security_report.json": sec_report.model_dump(mode="json"),
            "performance_report.json": perf_report.model_dump(mode="json"),
            "failure_test_report.json": failure_report.model_dump(mode="json"),
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
            "phase": "Phase 3I.2 — Enterprise Logging Infrastructure Verification Framework",
            "environment": "PRODUCTION_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "services_detected": arch_report.services_detected,
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
