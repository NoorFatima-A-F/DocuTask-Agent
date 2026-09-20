"""Artifact Domain Models and Supported Asset Types."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class ArtifactType(str, Enum):
    """Supported artifact asset categories (Req 13)."""
    CONTAINER_IMAGE = "CONTAINER_IMAGE"
    HELM_PACKAGE = "HELM_PACKAGE"
    WORKFLOW_PACKAGE = "WORKFLOW_PACKAGE"
    AGENT_PACKAGE = "AGENT_PACKAGE"
    PLUGIN_PACKAGE = "PLUGIN_PACKAGE"
    PROMPT_BUNDLE = "PROMPT_BUNDLE"
    MODEL_METADATA = "MODEL_METADATA"
    INFRASTRUCTURE_PACKAGE = "INFRASTRUCTURE_PACKAGE"
    FRONTEND_BUNDLE = "FRONTEND_BUNDLE"
    SDK_PACKAGE = "SDK_PACKAGE"


class ArtifactQuarantineStatus(str, Enum):
    """Artifact quarantine & safety states (Req 24)."""
    ACTIVE = "ACTIVE"
    QUARANTINED = "QUARANTINED"
    BLOCKED = "BLOCKED"
    REVOKED = "REVOKED"


@dataclass
class ArtifactIdentity:
    """Content-addressed artifact representation (Req 14)."""
    artifact_id: str
    type: ArtifactType
    name: str
    version: str
    digest: str  # e.g. sha256:4a5b6c...
    media_type: str = "application/vnd.oci.image.manifest.v1+json"
    size_bytes: int = 0
    registry: str = "ghcr.io/docutask"
    source_commit: str = ""
    build_id: str = ""
    signature_status: str = "UNSIGNED"
    sbom_reference: Optional[str] = None
    provenance_reference: Optional[str] = None
    quarantine_status: ArtifactQuarantineStatus = ArtifactQuarantineStatus.ACTIVE
    quarantine_reason: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    immutable: bool = True
    annotations: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "type": self.type.value,
            "name": self.name,
            "version": self.version,
            "digest": self.digest,
            "media_type": self.media_type,
            "size_bytes": self.size_bytes,
            "registry": self.registry,
            "source_commit": self.source_commit,
            "build_id": self.build_id,
            "signature_status": self.signature_status,
            "sbom_reference": self.sbom_reference,
            "provenance_reference": self.provenance_reference,
            "quarantine_status": self.quarantine_status.value,
            "quarantine_reason": self.quarantine_reason,
            "created_at": self.created_at.isoformat(),
            "immutable": self.immutable,
            "annotations": self.annotations,
        }
