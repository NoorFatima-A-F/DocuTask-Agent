"""
Evidence Manifest & Serialization Engine for Enterprise Document Storage (Part 3G.2C).
"""
import os
import json
from dataclasses import asdict, is_dataclass
from typing import Dict, Any, Optional

from app.platform_verification.document_storage_verification.domain.interfaces import (
    IStorageEvidenceManifestEngine,
)


def _serialize_obj(obj: Any) -> Any:
    """Helper serializer for dataclasses and enums."""
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "value"):
        return obj.value
    if isinstance(obj, dict):
        return {k: _serialize_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_obj(v) for v in obj]
    return obj


class StorageEvidenceManifestEngine(IStorageEvidenceManifestEngine):
    """
    Serializes and exports all 16 required verification artifacts to the
    evidence directory (default: evidence/document_storage_verification/).
    """

    DEFAULT_OUTPUT_DIR = "evidence/document_storage_verification"

    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Exports all 16 JSON artifacts to disk with complete machine-readable audit logs.
        """
        target_dir = os.path.abspath(output_dir or self.DEFAULT_OUTPUT_DIR)
        os.makedirs(target_dir, exist_ok=True)

        exported_paths: Dict[str, str] = {}

        # 16 Manifest mappings
        file_mappings = {
            "storage_inventory_report.json": verification_data.get("storage_inventory"),
            "storage_classification_report.json": verification_data.get("storage_classification"),
            "storage_backup_coverage_report.json": verification_data.get("backup_coverage"),
            "document_integrity_report.json": verification_data.get("document_integrity"),
            "storage_versioning_report.json": verification_data.get("storage_versioning"),
            "metadata_consistency_report.json": verification_data.get("metadata_consistency"),
            "storage_corruption_report.json": verification_data.get("storage_corruption"),
            "tenant_isolation_report.json": verification_data.get("tenant_isolation"),
            "storage_encryption_report.json": verification_data.get("storage_encryption"),
            "compression_deduplication_report.json": verification_data.get("compression_dedup"),
            "storage_performance_report.json": verification_data.get("storage_performance"),
            "large_file_benchmark_report.json": {
                "datasets": verification_data.get("storage_performance").datasets_tested
                if verification_data.get("storage_performance") and hasattr(verification_data.get("storage_performance"), "datasets_tested")
                else [],
                "throughput_summary": {
                    "avg_backup_mb_s": getattr(verification_data.get("storage_performance"), "avg_backup_throughput_mb_s", 0.0),
                    "avg_restore_mb_s": getattr(verification_data.get("storage_performance"), "avg_restore_throughput_mb_s", 0.0),
                }
            },
            "restore_simulation_report.json": verification_data.get("restore_simulation"),
            "cross_system_validation_report.json": verification_data.get("cross_system_validation"),
            "storage_quality_scorecard.json": verification_data.get("storage_quality_scorecard"),
            "enterprise_storage_verification_summary.json": {
                "verification_status": "COMPLETED_SUCCESSFULLY",
                "framework_version": "3G.2C_ENTERPRISE_DOCUMENT_STORAGE_VERIFIER",
                "composite_score": getattr(verification_data.get("storage_quality_scorecard"), "composite_score", 0.0),
                "certification_tier": getattr(verification_data.get("storage_quality_scorecard"), "certification_tier", "UNKNOWN"),
                "total_artifacts_verified": getattr(verification_data.get("storage_inventory"), "total_objects_discovered", 0),
                "rto_seconds": getattr(verification_data.get("storage_performance"), "rto_seconds", 0.0),
                "rpo_seconds": getattr(verification_data.get("storage_performance"), "rpo_seconds", 0.0),
                "tenant_isolation_passed": getattr(verification_data.get("tenant_isolation"), "passed", False),
                "corruption_detection_rate": getattr(verification_data.get("storage_corruption"), "detection_rate_percent", 0.0),
                "all_phases_passed": all(
                    getattr(v, "passed", True)
                    for k, v in verification_data.items()
                    if hasattr(v, "passed")
                ),
            },
        }

        for filename, data_content in file_mappings.items():
            serialized = _serialize_obj(data_content)
            clean_filename = os.path.basename(filename)
            file_path = os.path.abspath(os.path.join(target_dir, clean_filename))
            if not file_path.startswith(target_dir):
                raise ValueError(f"Path traversal detected: {filename}")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=2, ensure_ascii=False)
            exported_paths[filename] = file_path

        return exported_paths
