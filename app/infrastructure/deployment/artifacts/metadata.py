"""Artifact Metadata, SBOM, and Supply Chain Security Models."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ArtifactType(str, Enum):
    """Artifact format classification."""
    CONTAINER_IMAGE = "container_image"
    PYTHON_WHEEL = "python_wheel"
    AI_MODEL_BUNDLE = "ai_model_bundle"
    CONFIG_PACKAGE = "config_package"
    WASM_MODULE = "wasm_module"


class VulnerabilitySeverity(str, Enum):
    """Vulnerability severity ratings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


@dataclass
class VulnerabilityFinding:
    """A detected software vulnerability."""
    cve_id: str
    package_name: str
    installed_version: str
    fixed_version: Optional[str] = None
    severity: VulnerabilitySeverity = VulnerabilitySeverity.LOW
    description: str = ""


@dataclass
class SBOMComponent:
    """Software Bill of Materials (SBOM) item."""
    name: str
    version: str
    purl: str
    license: str = "Apache-2.0"
    checksum_sha256: str = ""


@dataclass
class ArtifactMetadata:
    """Complete supply-chain metadata for an artifact."""
    artifact_id: str
    name: str
    version: str
    artifact_type: ArtifactType
    digest_sha256: str
    commit_sha: str
    builder: str = "docutask-builder-01"
    sbom: List[SBOMComponent] = field(default_factory=list)
    vulnerabilities: List[VulnerabilityFinding] = field(default_factory=list)
    signature: Optional[str] = None
    signed_by: Optional[str] = None
    provenance_uri: Optional[str] = None
    promotion_tier: str = "dev"  # dev, staging, prod
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def has_critical_vulnerabilities(self) -> bool:
        """Check if any critical/high CVEs are detected."""
        return any(v.severity in (VulnerabilitySeverity.CRITICAL, VulnerabilitySeverity.HIGH) for v in self.vulnerabilities)
