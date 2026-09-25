"""Enterprise Artifact Registry managing container images, models, and packages."""

import hashlib
from typing import Dict, List, Optional
import threading
import uuid

from .metadata import (
    ArtifactMetadata,
    ArtifactType,
    SBOMComponent,
    VulnerabilityFinding,
)
from .signing import ArtifactSigner


class ArtifactRegistry:
    """Thread-safe catalog for versioned, signed, and scanned artifacts."""

    def __init__(self, signer: Optional[ArtifactSigner] = None) -> None:
        self.signer = signer or ArtifactSigner()
        self._artifacts: Dict[str, ArtifactMetadata] = {}  # artifact_id -> ArtifactMetadata
        self._name_version_index: Dict[str, str] = {}  # f"{name}:{version}" -> artifact_id
        self._lock = threading.RLock()

    def register_artifact(
        self,
        name: str,
        version: str,
        artifact_type: ArtifactType,
        commit_sha: str,
        content_bytes: Optional[bytes] = None,
        sbom: Optional[List[SBOMComponent]] = None,
        vulnerabilities: Optional[List[VulnerabilityFinding]] = None,
        auto_sign: bool = True,
    ) -> ArtifactMetadata:
        """Register and index a new artifact."""
        raw = content_bytes or f"{name}:{version}:{commit_sha}".encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        artifact_id = f"art-{uuid.uuid4().hex[:8]}"

        meta = ArtifactMetadata(
            artifact_id=artifact_id,
            name=name,
            version=version,
            artifact_type=artifact_type,
            digest_sha256=digest,
            commit_sha=commit_sha,
            sbom=sbom or [],
            vulnerabilities=vulnerabilities or [],
            promotion_tier="dev",
        )

        if auto_sign:
            self.signer.sign_artifact(meta)

        with self._lock:
            self._artifacts[artifact_id] = meta
            self._name_version_index[f"{name}:{version}"] = artifact_id

        return meta

    def get_artifact(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        """Fetch artifact by ID."""
        with self._lock:
            return self._artifacts.get(artifact_id)

    def find_by_name_and_version(self, name: str, version: str) -> Optional[ArtifactMetadata]:
        """Lookup artifact by name and version."""
        with self._lock:
            aid = self._name_version_index.get(f"{name}:{version}")
            if aid:
                return self._artifacts.get(aid)
            return None

    def promote_artifact(self, artifact_id: str, target_tier: str) -> bool:
        """Promote artifact to staging or prod after security verification."""
        with self._lock:
            art = self._artifacts.get(artifact_id)
            if not art:
                return False

            # Gating: Cannot promote if signature invalid or critical vulnerabilities exist
            if not self.signer.verify_signature(art):
                raise ValueError("Cannot promote unsigned or tampered artifact")
            if target_tier == "prod" and art.has_critical_vulnerabilities:
                raise ValueError("Cannot promote artifact with CRITICAL/HIGH vulnerabilities to production")

            art.promotion_tier = target_tier
            return True

    def list_artifacts(self, name: Optional[str] = None, promotion_tier: Optional[str] = None) -> List[ArtifactMetadata]:
        """Query artifacts."""
        with self._lock:
            res = list(self._artifacts.values())
            if name:
                res = [a for a in res if a.name == name]
            if promotion_tier:
                res = [a for a in res if a.promotion_tier == promotion_tier]
            return sorted(res, key=lambda a: a.created_at, reverse=True)
