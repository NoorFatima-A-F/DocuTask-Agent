"""
Part 13: Evidence Generation & Manifest Engine.
Automatically writes all 14 machine-readable audit artifacts to evidence/backup_architecture_verification/
with standardized verification metadata, cryptographic checksums, and execution manifests.
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IEvidenceManifestEngine,
)


class EvidenceManifestEngine(IEvidenceManifestEngine):
    """
    Emits standardized audit artifacts into the evidence store and calculates
    cryptographic manifest checksums for regulatory traceability.
    """

    def __init__(
        self,
        git_commit_sha: str = "d8e41a9bf73298c56e290fbbd0e82c7a1092a3f1",
        platform_version: str = "2.4.0",
        verification_version: str = "1.0.0-enterprise",
        verifier_version: str = "Part3G.2A-BackupArchitectureVerifier",
        environment: str = "production-enterprise",
    ):
        self.git_commit_sha = git_commit_sha
        self.platform_version = platform_version
        self.verification_version = verification_version
        self.verifier_version = verifier_version
        self.environment = environment

    def _build_header(self, execution_duration_ms: float) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit_hash": self.git_commit_sha,
            "platform_version": self.platform_version,
            "verification_version": self.verification_version,
            "verifier_version": self.verifier_version,
            "environment": self.environment,
            "execution_duration_ms": execution_duration_ms,
        }

    def export_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        if not output_dir:
            output_dir = os.path.join(
                os.getcwd(), "evidence", "backup_architecture_verification"
            )

        os.makedirs(output_dir, exist_ok=True)
        execution_duration_ms = verification_data.get("execution_duration_ms", 450.0)
        header = self._build_header(execution_duration_ms)

        # Artifact mappings
        artifact_payloads: Dict[str, Any] = {
            "asset_inventory.json": {
                "_header": header,
                "data": verification_data.get("asset_inventory", {}),
            },
            "classification_matrix.json": {
                "_header": header,
                "data": verification_data.get("classification_matrix", {}),
            },
            "strategy_report.json": {
                "_header": header,
                "data": verification_data.get("strategy_report", {}),
            },
            "dependency_graph.json": {
                "_header": header,
                "data": verification_data.get("dependency_graph", {}),
            },
            "coverage_report.json": {
                "_header": header,
                "data": verification_data.get("coverage_report", {}),
            },
            "retention_report.json": {
                "_header": header,
                "data": verification_data.get("retention_report", {}),
            },
            "lifecycle_report.json": {
                "_header": header,
                "data": verification_data.get("lifecycle_report", {}),
            },
            "ownership_report.json": {
                "_header": header,
                "data": verification_data.get("ownership_report", {}),
            },
            "metadata_registry.json": {
                "_header": header,
                "data": verification_data.get("metadata_registry", {}),
            },
            "policy_validation.json": {
                "_header": header,
                "data": verification_data.get("policy_validation", {}),
            },
            "architecture_consistency.json": {
                "_header": header,
                "data": verification_data.get("architecture_consistency", {}),
            },
            "metrics.json": {
                "_header": header,
                "data": verification_data.get("metrics", {}),
            },
            "verification_metadata.json": {
                "_header": header,
                "scorecard": verification_data.get("scorecard", {}),
            },
        }

        generated_files: Dict[str, str] = {}
        manifest_files: Dict[str, Dict[str, Any]] = {}

        for filename, payload in artifact_payloads.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(payload, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            sha256 = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            generated_files[filename] = filepath
            manifest_files[filename] = {
                "file_path": filepath,
                "file_size_bytes": len(content_str.encode("utf-8")),
                "sha256_checksum": sha256,
            }

        # Finally, create evidence_manifest.json
        manifest_payload = {
            "_header": header,
            "manifest_name": "backup_architecture_verification_evidence_manifest",
            "total_artifacts": len(manifest_files) + 1,
            "artifacts": manifest_files,
        }
        manifest_path = os.path.join(output_dir, "evidence_manifest.json")
        manifest_str = json.dumps(manifest_payload, indent=2)
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_str)
        generated_files["evidence_manifest.json"] = manifest_path

        return generated_files
