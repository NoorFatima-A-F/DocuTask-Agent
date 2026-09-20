"""OCI Registry Client Adapters (GHCR, GAR, ECR, ACR, Harbor, Generic OCI)."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import ArtifactIdentity


class OCIRegistryAdapter(ABC):
    """Vendor-neutral interface for OCI compliant artifact distribution."""

    @property
    @abstractmethod
    def registry_name(self) -> str:
        pass

    @abstractmethod
    def push_artifact(self, artifact: ArtifactIdentity, payload: bytes) -> str:
        """Pushes artifact payload and returns published digest."""
        pass

    @abstractmethod
    def pull_artifact(self, digest: str) -> Optional[bytes]:
        """Pulls artifact payload by digest."""
        pass

    @abstractmethod
    def list_referrers(self, digest: str, artifact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries OCI 1.1 referrers attached to a target digest (e.g. SBOMs, signatures)."""
        pass


class GenericOCIRegistryAdapter(OCIRegistryAdapter):
    """In-memory reference implementation of an OCI Registry Adapter."""

    def __init__(self, endpoint: str = "ghcr.io/docutask"):
        self.endpoint = endpoint
        self._blobs: Dict[str, bytes] = {}
        self._referrers: Dict[str, List[Dict[str, Any]]] = {}  # target_digest -> list of descriptors

    @property
    def registry_name(self) -> str:
        return f"GenericOCI({self.endpoint})"

    def push_artifact(self, artifact: ArtifactIdentity, payload: bytes) -> str:
        self._blobs[artifact.digest] = payload
        return artifact.digest

    def pull_artifact(self, digest: str) -> Optional[bytes]:
        return self._blobs.get(digest)

    def attach_referrer(self, target_digest: str, descriptor: Dict[str, Any]) -> None:
        refs = self._referrers.setdefault(target_digest, [])
        refs.append(descriptor)

    def list_referrers(self, digest: str, artifact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        refs = self._referrers.get(digest, [])
        if artifact_type:
            return [r for r in refs if r.get("artifactType") == artifact_type]
        return list(refs)
