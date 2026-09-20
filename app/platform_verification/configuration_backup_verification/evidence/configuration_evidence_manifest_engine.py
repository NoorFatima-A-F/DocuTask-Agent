"""
Evidence Manifest Engine for Enterprise Configuration Backup Verification (Part 3G.2D).
"""
import os
import json
from dataclasses import asdict, is_dataclass
from typing import Dict, Any, Optional

from app.platform_verification.configuration_backup_verification.domain.interfaces import (
    IConfigurationEvidenceManifestEngine,
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


class ConfigurationEvidenceManifestEngine(IConfigurationEvidenceManifestEngine):
    """
    Serializes and exports all 14 required verification artifacts to the
    evidence directory (default: evidence/configuration_backup_verification/).
    """

    DEFAULT_OUTPUT_DIR = "evidence/configuration_backup_verification"

    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Exports all 14 JSON artifacts to disk with complete machine-readable audit logs.
        """
        target_dir = output_dir or self.DEFAULT_OUTPUT_DIR
        os.makedirs(target_dir, exist_ok=True)

        exported_paths: Dict[str, str] = {}

        file_mappings = {
            "configuration_inventory.json": verification_data.get("configuration_inventory"),
            "configuration_catalog.json": verification_data.get("configuration_catalog"),
            "configuration_validation_report.json": verification_data.get("configuration_validation"),
            "secret_inventory.json": verification_data.get("secret_inventory"),
            "secret_backup_report.json": verification_data.get("secret_backup"),
            "encryption_key_recovery.json": verification_data.get("encryption_key_recovery"),
            "certificate_recovery.json": verification_data.get("certificate_recovery"),
            "feature_flag_restore_report.json": verification_data.get("feature_flag_restore"),
            "infrastructure_configuration_report.json": verification_data.get("infrastructure_configuration"),
            "configuration_drift_report.json": verification_data.get("configuration_drift"),
            "restore_simulation_report.json": verification_data.get("restore_simulation"),
            "compliance_report.json": verification_data.get("compliance_report"),
            "security_report.json": verification_data.get("security_report"),
            "metadata.json": {
                "framework": "PART_3G.2D_CONFIGURATION_SECRET_CRYPTOGRAPHIC_BACKUP_VERIFICATION",
                "version": "1.0.0",
                "composite_score": getattr(verification_data.get("scorecard"), "composite_score", 0.0),
                "certification_tier": getattr(verification_data.get("scorecard"), "certification_tier", "UNKNOWN"),
                "total_configuration_sources": getattr(verification_data.get("configuration_inventory"), "configuration_sources", 0),
                "total_secrets_audited": getattr(verification_data.get("secret_inventory"), "total_secrets_discovered", 0),
                "cryptographic_outputs_identical": getattr(verification_data.get("encryption_key_recovery"), "all_cryptographic_outputs_identical", False),
                "compliance_score_percent": getattr(verification_data.get("compliance_report"), "compliance_score_percent", 0.0),
                "gate_passed": getattr(verification_data.get("scorecard"), "passed", False),
            },
        }

        for filename, data_content in file_mappings.items():
            serialized = _serialize_obj(data_content)
            file_path = os.path.join(target_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=2, ensure_ascii=False)
            exported_paths[filename] = os.path.abspath(file_path)

        return exported_paths
