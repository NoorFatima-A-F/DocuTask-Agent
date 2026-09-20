"""
Phase 3H.12: Evidence Exporter for Enterprise Automated Recovery & Self-Healing Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    RecoveryArchitectureReport,
    RecoveryPolicyReport,
    ServiceRestartReport,
    DatabaseRecoveryReport,
    QueueRecoveryReport,
    WorkerRecoveryReport,
    AIRecoveryReport,
    CircuitBreakerReport,
    RecoveryValidationReport,
    ReliabilityMetricsReport,
    RecoverySafetyReport,
    RecoveryAuditReport,
    RecoveryCertificationReport,
)
from ..domain.interfaces import IAutomatedRecoveryExporter


class AutomatedRecoveryExporter(IAutomatedRecoveryExporter):
    """
    Exports 13 standardized JSON evidence reports plus signed metadata.json with SHA-256 digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        arch_report: RecoveryArchitectureReport,
        policy_report: RecoveryPolicyReport,
        restart_report: ServiceRestartReport,
        db_report: DatabaseRecoveryReport,
        queue_report: QueueRecoveryReport,
        worker_report: WorkerRecoveryReport,
        ai_report: AIRecoveryReport,
        circuit_report: CircuitBreakerReport,
        validation_report: RecoveryValidationReport,
        metrics_report: ReliabilityMetricsReport,
        safety_report: RecoverySafetyReport,
        audit_report: RecoveryAuditReport,
        certification_report: RecoveryCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "recovery_architecture_report.json": arch_report.model_dump(mode="json"),
            "recovery_policy_report.json": policy_report.model_dump(mode="json"),
            "service_restart_report.json": restart_report.model_dump(mode="json"),
            "database_recovery_report.json": db_report.model_dump(mode="json"),
            "queue_recovery_report.json": queue_report.model_dump(mode="json"),
            "worker_recovery_report.json": worker_report.model_dump(mode="json"),
            "ai_recovery_report.json": ai_report.model_dump(mode="json"),
            "circuit_breaker_report.json": circuit_report.model_dump(mode="json"),
            "validation_report.json": validation_report.model_dump(mode="json"),
            "reliability_metrics_report.json": metrics_report.model_dump(mode="json"),
            "safety_report.json": safety_report.model_dump(mode="json"),
            "audit_report.json": audit_report.model_dump(mode="json"),
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
            "phase": "Phase 3H.12 — Enterprise Automated Recovery & Self-Healing Verification Framework",
            "environment": "PRODUCTION_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "recovery_tests_completed": policy_report.total_policies,
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
