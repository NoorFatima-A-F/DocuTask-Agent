"""
Evidence Manifest Engine for Backup Security Verification Framework (Part 3G.2F).
"""
import os
import json
from pathlib import Path
from app.core.security import resolve_safe_path, validate_safe_filename_segment
from dataclasses import asdict, is_dataclass
from typing import Dict, Any, Optional

from app.platform_verification.backup_security_verification.domain.interfaces import (
    IBackupSecurityEvidenceEngine,
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


class BackupSecurityEvidenceEngine(IBackupSecurityEvidenceEngine):
    """
    Serializes and exports all 14 required security verification artifacts
    to the evidence directory (default: evidence/backup_security_verification/).
    """

    DEFAULT_OUTPUT_DIR = "evidence/backup_security_verification"

    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Exports all 14 JSON artifacts to disk with complete machine-readable audit logs.
        """
        target_dir = resolve_safe_path(Path.cwd(), output_dir or self.DEFAULT_OUTPUT_DIR)
        target_dir.mkdir(parents=True, exist_ok=True)

        exported_paths: Dict[str, str] = {}

        file_mappings = {
            "backup_security_inventory.json": verification_data.get("backup_security_inventory"),
            "data_classification_report.json": verification_data.get("data_classification_report"),
            "encryption_report.json": verification_data.get("encryption_report"),
            "key_management_report.json": verification_data.get("key_management_report"),
            "key_rotation_report.json": verification_data.get("key_rotation_report"),
            "access_control_report.json": verification_data.get("access_control_report"),
            "iam_test_report.json": verification_data.get("iam_test_report"),
            "tamper_detection_report.json": verification_data.get("tamper_detection_report"),
            "poisoning_protection_report.json": verification_data.get("poisoning_protection_report"),
            "immutability_report.json": verification_data.get("immutability_report"),
            "audit_report.json": verification_data.get("audit_report"),
            "retention_security_report.json": verification_data.get("retention_security_report"),
            "compliance_report.json": verification_data.get("compliance_report"),
            "metadata.json": {
                "framework": "PART_3G.2F_BACKUP_SECURITY_VERIFICATION",
                "version": "1.0.0",
                "composite_score": getattr(verification_data.get("scorecard"), "composite_score", 0.0),
                "certification_tier": getattr(verification_data.get("scorecard"), "certification_tier", "UNKNOWN"),
                "total_backup_assets": getattr(verification_data.get("backup_security_inventory"), "backup_assets", 0),
                "encrypted_backup_assets": getattr(verification_data.get("backup_security_inventory"), "encrypted_assets", 0),
                "unencrypted_backup_assets": getattr(verification_data.get("backup_security_inventory"), "unencrypted_assets", 0),
                "tamper_detection_active": getattr(verification_data.get("tamper_detection_report"), "one_byte_modification_detected", False),
                "poisoning_protection_active": getattr(verification_data.get("poisoning_protection_report"), "untrusted_sources_rejected", False),
                "immutability_active": getattr(verification_data.get("immutability_report"), "object_lock_compliance_mode_active", False),
                "gate_passed": getattr(verification_data.get("scorecard"), "passed", False),
            },
        }

        for filename, data_content in file_mappings.items():
            serialized = _serialize_obj(data_content)
            safe_filename = validate_safe_filename_segment(filename)
            file_path = resolve_safe_path(target_dir, safe_filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=2, ensure_ascii=False)
            exported_paths[filename] = str(file_path)

        return exported_paths
