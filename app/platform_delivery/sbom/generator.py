"""Software Bill of Materials (SBOM) Generator & Formatter (SPDX & CycloneDX)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class SBOMFormat(str, Enum):
    """Supported standard SBOM formats (Req 20)."""
    CYCLONEDX_1_5 = "CycloneDX-1.5"
    SPDX_2_3 = "SPDX-2.3"


@dataclass
class SBOMComponent:
    """Individual software dependency record."""
    name: str
    version: str
    purl: str
    license_concluded: str = "Apache-2.0"
    checksum_sha256: Optional[str] = None
    supplier: str = "open-source-upstream"


@dataclass
class SBOMDocument:
    """Standardized SBOM document."""
    sbom_id: str
    artifact_digest: str
    format: SBOMFormat
    components: List[SBOMComponent] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_cyclonedx_dict(self) -> Dict[str, Any]:
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "serialNumber": f"urn:uuid:{self.sbom_id}",
            "version": 1,
            "metadata": {
                "timestamp": self.created_at.isoformat(),
                "component": {
                    "name": "docutask-agent",
                    "type": "application",
                },
            },
            "components": [
                {
                    "name": c.name,
                    "version": c.version,
                    "purl": c.purl,
                    "licenses": [{"license": {"id": c.license_concluded}}],
                    "hashes": [{"alg": "SHA-256", "content": c.checksum_sha256}] if c.checksum_sha256 else [],
                }
                for c in self.components
            ],
        }


class SBOMManager:
    """Generates, stores, and evaluates SBOM documents."""

    def __init__(self):
        self._sboms: Dict[str, SBOMDocument] = {}  # artifact_digest -> SBOMDocument

    def generate_sbom(
        self,
        artifact_digest: str,
        components: Optional[List[SBOMComponent]] = None,
        sbom_format: SBOMFormat = SBOMFormat.CYCLONEDX_1_5,
    ) -> SBOMDocument:
        default_comps = components or [
            SBOMComponent(name="fastapi", version="0.110.0", purl="pkg:pypi/fastapi@0.110.0", license_concluded="MIT"),
            SBOMComponent(name="pydantic", version="2.6.4", purl="pkg:pypi/pydantic@2.6.4", license_concluded="MIT"),
            SBOMComponent(name="sqlalchemy", version="2.0.28", purl="pkg:pypi/sqlalchemy@2.0.28", license_concluded="MIT"),
            SBOMComponent(name="google-genai", version="0.1.1", purl="pkg:pypi/google-genai@0.1.1", license_concluded="Apache-2.0"),
        ]

        doc = SBOMDocument(
            sbom_id=str(uuid.uuid4()),
            artifact_digest=artifact_digest,
            format=sbom_format,
            components=default_comps,
        )
        self._sboms[artifact_digest] = doc
        return doc

    def get_sbom(self, artifact_digest: str) -> Optional[SBOMDocument]:
        return self._sboms.get(artifact_digest)
