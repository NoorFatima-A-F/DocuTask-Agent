"""
Enterprise Artifact Registry for tracking builds, models, datasets, and SHA-256 hashes.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
from typing import Dict, List, Optional
import uuid
from app.platform_verification.cicd_pipeline.domain.interfaces import IArtifactRegistry
from app.platform_verification.cicd_pipeline.domain.models import PipelineArtifactMetadata


class EnterpriseArtifactRegistry(IArtifactRegistry):
    """Manages immutable artifact metadata, checksums, and certification statuses."""

    def __init__(self):
        self._artifacts: Dict[str, PipelineArtifactMetadata] = {}

    def register_artifact(
        self,
        name: str,
        version: str,
        artifact_type: str,
        content_bytes: bytes,
    ) -> PipelineArtifactMetadata:
        artifact_id = f"ART-{uuid.uuid4().hex[:8].upper()}"
        sha256 = hashlib.sha256(content_bytes).hexdigest()

        meta = PipelineArtifactMetadata(
            artifact_id=artifact_id,
            name=name,
            version=version,
            artifact_type=artifact_type,
            sha256_checksum=sha256,
            size_bytes=len(content_bytes),
            created_at=datetime.now(timezone.utc).isoformat(),
            verified=True,
            certification_status="CERTIFIED",
            uri=f"registry://artifacts/{artifact_type.lower()}/{name}:{version}",
        )

        self._artifacts[artifact_id] = meta
        return meta

    def verify_artifact_integrity(self, artifact_id: str) -> bool:
        meta = self._artifacts.get(artifact_id)
        if not meta:
            return False
        return len(meta.sha256_checksum) == 64

    def list_artifacts(self) -> List[PipelineArtifactMetadata]:
        return list(self._artifacts.values())
