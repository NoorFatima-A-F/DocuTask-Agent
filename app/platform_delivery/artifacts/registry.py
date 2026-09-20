"""Authoritative Enterprise Artifact Registry (Req 13, 14, 15, 24)."""
from typing import Any, Dict, List, Optional
import uuid

from .digests import DigestCalculator
from .models import ArtifactIdentity, ArtifactQuarantineStatus, ArtifactType
from .oci import GenericOCIRegistryAdapter, OCIRegistryAdapter


class ArtifactRegistry:
    """Central registry abstraction managing all content-addressed platform artifacts and OCI referrers."""

    def __init__(self, oci_adapter: Optional[OCIRegistryAdapter] = None):
        self.oci_adapter = oci_adapter or GenericOCIRegistryAdapter()
        self._artifacts_by_digest: Dict[str, ArtifactIdentity] = {}
        self._artifacts_by_id: Dict[str, ArtifactIdentity] = {}

    def register_artifact(
        self,
        name: str,
        version: str,
        artifact_type: ArtifactType,
        payload: bytes,
        source_commit: str = "",
        build_id: str = "",
        registry: str = "ghcr.io/docutask",
        annotations: Optional[Dict[str, str]] = None,
    ) -> ArtifactIdentity:
        digest = DigestCalculator.calculate_sha256(payload)
        art_id = f"art-{name}-{version}-{uuid.uuid4().hex[:6]}"

        # Prevent duplicate mutation of same digest with different content
        if digest in self._artifacts_by_digest:
            return self._artifacts_by_digest[digest]

        art = ArtifactIdentity(
            artifact_id=art_id,
            type=artifact_type,
            name=name,
            version=version,
            digest=digest,
            size_bytes=len(payload),
            registry=registry,
            source_commit=source_commit,
            build_id=build_id,
            annotations=annotations or {},
        )

        # Push to OCI layer
        self.oci_adapter.push_artifact(art, payload)

        self._artifacts_by_digest[digest] = art
        self._artifacts_by_id[art_id] = art
        return art

    def get_by_digest(self, digest: str) -> Optional[ArtifactIdentity]:
        return self._artifacts_by_digest.get(digest)

    def get_by_id(self, artifact_id: str) -> Optional[ArtifactIdentity]:
        return self._artifacts_by_id.get(artifact_id)

    def list_artifacts(
        self,
        artifact_type: Optional[ArtifactType] = None,
        quarantine_status: Optional[ArtifactQuarantineStatus] = None,
    ) -> List[ArtifactIdentity]:
        results = list(self._artifacts_by_digest.values())
        if artifact_type:
            results = [a for a in results if a.type == artifact_type]
        if quarantine_status:
            results = [a for a in results if a.quarantine_status == quarantine_status]
        return sorted(results, key=lambda a: a.created_at, reverse=True)

    def quarantine_artifact(self, digest: str, reason: str) -> ArtifactIdentity:
        art = self.get_by_digest(digest)
        if not art:
            raise KeyError(f"Artifact with digest '{digest}' not found")
        art.quarantine_status = ArtifactQuarantineStatus.QUARANTINED
        art.quarantine_reason = reason
        return art

    def unquarantine_artifact(self, digest: str) -> ArtifactIdentity:
        art = self.get_by_digest(digest)
        if not art:
            raise KeyError(f"Artifact with digest '{digest}' not found")
        art.quarantine_status = ArtifactQuarantineStatus.ACTIVE
        art.quarantine_reason = None
        return art
