"""
Exporter for Part 3I: Enterprise Observability Infrastructure (Logging + Metrics)
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    LoggingCertificationReport,
    MetricsCertificationReport,
    UnifiedObservabilityCertification,
)
from ..domain.interfaces import IObservabilityExporter


class ObservabilityExporter(IObservabilityExporter):
    """
    Exports dual-track reports to `observability_verification/logging/` and `observability_verification/metrics/` with SHA-256 manifests.
    """

    def export_all_observability_reports(
        self,
        base_dir: str,
        logging_reports: Dict[str, Any],
        logging_cert: LoggingCertificationReport,
        metrics_reports: Dict[str, Any],
        metrics_cert: MetricsCertificationReport,
        unified_cert: UnifiedObservabilityCertification,
    ) -> Dict[str, Any]:
        logging_dir = os.path.join(base_dir, "logging")
        metrics_dir = os.path.join(base_dir, "metrics")
        os.makedirs(logging_dir, exist_ok=True)
        os.makedirs(metrics_dir, exist_ok=True)

        # 1. Export Logging Reports
        log_payloads = {**logging_reports, "certification_report.json": logging_cert.model_dump(mode="json")}
        log_manifest: Dict[str, str] = {}
        for filename, data in log_payloads.items():
            filepath = os.path.join(logging_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            log_manifest[filename] = hashlib.sha256(content_str.encode("utf-8")).hexdigest()

        log_meta = {
            "track": "Part 3I.1 — Enterprise Logging Infrastructure Verification",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "score_pct": logging_cert.overall_score_pct,
            "certification_tier": logging_cert.certification_tier,
            "certification_granted": logging_cert.certification_granted,
            "artifacts_count": len(log_manifest),
            "manifest_sha256": log_manifest,
        }
        with open(os.path.join(logging_dir, "metadata.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(log_meta, indent=2))

        # 2. Export Metrics Reports
        met_payloads = {**metrics_reports, "certification_report.json": metrics_cert.model_dump(mode="json")}
        met_manifest: Dict[str, str] = {}
        for filename, data in met_payloads.items():
            filepath = os.path.join(metrics_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            met_manifest[filename] = hashlib.sha256(content_str.encode("utf-8")).hexdigest()

        met_meta = {
            "track": "Part 3I.2 — Enterprise Metrics Infrastructure Verification",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "score_pct": metrics_cert.overall_score_pct,
            "certification_tier": metrics_cert.certification_tier,
            "certification_granted": metrics_cert.certification_granted,
            "artifacts_count": len(met_manifest),
            "manifest_sha256": met_manifest,
        }
        with open(os.path.join(metrics_dir, "metadata.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(met_meta, indent=2))

        # 3. Export Root Unified Certification & Metadata
        root_cert_path = os.path.join(base_dir, "unified_certification.json")
        with open(root_cert_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(unified_cert.model_dump(mode="json"), indent=2))

        unified_meta = {
            "project": "DocuTask-Agent",
            "program_phase": "Part 3I — Enterprise Observability Infrastructure Verification",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "logging_score_pct": unified_cert.logging_score_pct,
            "metrics_score_pct": unified_cert.metrics_score_pct,
            "overall_score_pct": unified_cert.overall_score_pct,
            "certification_tier": unified_cert.certification_tier.value,
            "certification_granted": unified_cert.certification_granted,
            "logging_artifacts": len(log_manifest),
            "metrics_artifacts": len(met_manifest),
            "auditor": unified_cert.auditor,
        }
        with open(os.path.join(base_dir, "metadata.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(unified_meta, indent=2))

        return unified_meta
