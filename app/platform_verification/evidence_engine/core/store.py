"""
Content-Addressable Storage (CAS) Engine for Immutable Verification Artifacts.
"""
from __future__ import annotations
import hashlib
from typing import Any, Dict, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact,
    EvidenceCategory,
    EvidenceClassification,
    EvidenceLifecycleState,
    IntegrityRecord,
)
from app.platform_verification.evidence_engine.domain.interfaces import IEvidenceStore


class ContentAddressableStore(IEvidenceStore):
    """In-memory content-addressable storage engine addressed by SHA-256 digests."""

    def __init__(self) -> None:
        self._blobs: Dict[str, bytes] = {}
        self._artifacts: Dict[str, EvidenceArtifact] = {}

    def store_artifact(
        self,
        execution_id: str,
        category: EvidenceCategory,
        content: bytes,
        metadata: Optional[Dict[str, Any]] = None,
        classification: EvidenceClassification = EvidenceClassification.INTERNAL,
    ) -> EvidenceArtifact:
        digest = hashlib.sha256(content).hexdigest()
        storage_uri = f"cas://sha256/{digest}"
        self._blobs[digest] = content

        artifact = EvidenceArtifact(
            execution_id=execution_id,
            category=category,
            checksum_sha256=digest,
            storage_uri=storage_uri,
            classification=classification,
            metadata=metadata or {},
        )
        self._artifacts[artifact.artifact_id] = artifact
        return artifact

    def retrieve_artifact(self, storage_uri: str) -> bytes:
        if not storage_uri.startswith("cas://sha256/"):
            raise ValueError(f"Invalid CAS URI scheme: {storage_uri}")
        digest = storage_uri.replace("cas://sha256/", "")
        if digest not in self._blobs:
            raise KeyError(f"Blob with digest '{digest}' not found in CAS store.")
        content = self._blobs[digest]
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"Integrity check failed for {storage_uri}: Content tampered!")
        return content

    def verify_integrity(self, artifact_id: str) -> IntegrityRecord:
        if artifact_id not in self._artifacts:
            raise KeyError(f"Artifact '{artifact_id}' not found.")
        art = self._artifacts[artifact_id]
        content = self.retrieve_artifact(art.storage_uri)
        actual_hash = hashlib.sha256(content).hexdigest()
        is_valid = (actual_hash == art.checksum_sha256)
        return IntegrityRecord(
            artifact_id=artifact_id,
            hash=actual_hash,
            verified=is_valid,
        )

    def get_artifact(self, artifact_id: str) -> Optional[EvidenceArtifact]:
        return self._artifacts.get(artifact_id)

    def list_artifacts_for_execution(self, execution_id: str) -> list[EvidenceArtifact]:
        return [a for a in self._artifacts.values() if a.execution_id == execution_id]
