"""
Phase 3H.11: Evidence Exporter for Enterprise Health Failure Simulation & Chaos Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
from ..domain.models import (
    ChaosArchitectureReport,
    ScenarioRegistryReport,
    DatabaseFailureReport,
    QueueFailureReport,
    WorkerFailureReport,
    AIProviderFailureReport,
    ResourceFailureReport,
    FailureDetectionMetricsReport,
    RollbackValidationReport,
    ChaosSafetyReport,
    ChaosCertificationReport,
)
from ..domain.interfaces import IChaosEvidenceExporter


class ChaosEvidenceExporter(IChaosEvidenceExporter):
    """
    Exports 11 standardized JSON evidence reports plus signed metadata.json with SHA-256 digests.
    """

    def export_all_reports(
        self,
        output_dir: str,
        arch_report: ChaosArchitectureReport,
        registry_report: ScenarioRegistryReport,
        db_report: DatabaseFailureReport,
        queue_report: QueueFailureReport,
        worker_report: WorkerFailureReport,
        ai_report: AIProviderFailureReport,
        resource_report: ResourceFailureReport,
        detection_report: FailureDetectionMetricsReport,
        rollback_report: RollbackValidationReport,
        safety_report: ChaosSafetyReport,
        certification_report: ChaosCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "chaos_architecture_report.json": arch_report.model_dump(mode="json"),
            "scenario_registry.json": registry_report.model_dump(mode="json"),
            "database_failure_report.json": db_report.model_dump(mode="json"),
            "queue_failure_report.json": queue_report.model_dump(mode="json"),
            "worker_failure_report.json": worker_report.model_dump(mode="json"),
            "ai_failure_report.json": ai_report.model_dump(mode="json"),
            "resource_failure_report.json": resource_report.model_dump(mode="json"),
            "detection_metrics.json": detection_report.model_dump(mode="json"),
            "rollback_report.json": rollback_report.model_dump(mode="json"),
            "safety_report.json": safety_report.model_dump(mode="json"),
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
            "phase": "Phase 3H.11 — Enterprise Health Failure Simulation & Chaos Verification Framework",
            "environment": "STAGING_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "experiments_completed": registry_report.total_scenarios,
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
