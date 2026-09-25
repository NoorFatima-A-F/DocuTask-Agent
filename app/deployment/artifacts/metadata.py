"""Artifact Metadata & Provenance Data Model."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib
import hmac


@dataclass
class ArtifactMetadata:
    """Provenance, cryptographic signature, and SBOM metadata for build artifacts."""
    artifact_id: str
    name: str
    version: str
    checksum_sha256: str
    size_bytes: int
    signature: Optional[str] = None
    signed_by: Optional[str] = None
    sbom_components: List[Dict[str, str]] = field(default_factory=list)
    vulnerability_scan: Dict[str, Any] = field(default_factory=lambda: {"critical": 0, "high": 0, "medium": 0, "passed": True})
    license_info: str = "Apache-2.0"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = "ci-pipeline"
    verified: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def calculate_checksum(cls, data: bytes) -> str:
        """Computes SHA-256 checksum for byte content."""
        return hashlib.sha256(data).hexdigest()

    def sign(self, secret_key: str, signer_identity: str) -> str:
        """Generates HMAC-SHA256 signature for the artifact checksum."""
        sig = hmac.new(
            secret_key.encode("utf-8"),
            self.checksum_sha256.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        self.signature = sig
        self.signed_by = signer_identity
        self.verified = True
        return sig

    def verify_signature(self, secret_key: str) -> bool:
        """Verifies signature against secret key and checksum."""
        if not self.signature:
            return False
        expected_sig = hmac.new(
            secret_key.encode("utf-8"),
            self.checksum_sha256.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        is_valid = hmac.compare_digest(self.signature, expected_sig)
        self.verified = is_valid
        return is_valid

    def to_dict(self) -> Dict[str, Any]:
        """Serializes metadata to dictionary."""
        return {
            "artifact_id": self.artifact_id,
            "name": self.name,
            "version": self.version,
            "checksum_sha256": self.checksum_sha256,
            "size_bytes": self.size_bytes,
            "signature": self.signature,
            "signed_by": self.signed_by,
            "sbom_components_count": len(self.sbom_components),
            "vulnerability_scan": self.vulnerability_scan,
            "license_info": self.license_info,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "verified": self.verified,
            "attributes": self.attributes,
        }
