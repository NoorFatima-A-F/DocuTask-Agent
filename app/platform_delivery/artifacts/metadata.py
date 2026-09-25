"""OCI Referrers and Associated Metadata Descriptors (Req 15)."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OCIReferrerDescriptor:
    """OCI 1.1 Referrer descriptor representing metadata attached to an image."""
    media_type: str
    digest: str
    size: int
    artifact_type: str  # e.g. "application/vnd.dev.cosign.simplesigning.v1+json" or "application/spdx+json"
    annotations: Dict[str, str] = field(default_factory=dict)


@dataclass
class OCIManifest:
    """Standard OCI v1.1 Manifest Representation."""
    schema_version: int = 2
    media_type: str = "application/vnd.oci.image.manifest.v1+json"
    config_digest: str = ""
    layers: List[Dict[str, Any]] = field(default_factory=list)
    subject_digest: Optional[str] = None  # Reference to parent artifact for attached metadata
    annotations: Dict[str, str] = field(default_factory=dict)
