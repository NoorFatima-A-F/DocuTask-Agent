"""Enterprise Artifact Registry and Provenance Platform."""
from typing import Any, Dict, List, Optional
import uuid
from ..core.exceptions import ArtifactValidationException
from .metadata import ArtifactMetadata
from .versions import ArtifactVersion


class ArtifactRegistry:
    """Central repository for build artifacts, container images, SBOMs, and signatures."""

    def __init__(self, default_signing_key: Optional[str] = None):
        self._artifacts: Dict[str, ArtifactMetadata] = {}
        self._payloads: Dict[str, bytes] = {}
        self._default_signing_key = default_signing_key or "platform-default-signing-key-secret"

    def register_artifact(
        self,
        name: str,
        version: str,
        data: bytes,
        created_by: str = "ci-pipeline",
        license_info: str = "Apache-2.0",
        sbom_components: Optional[List[Dict[str, str]]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        auto_sign: bool = True,
    ) -> ArtifactMetadata:
        """Registers a new artifact with computed checksum, SBOM, and optional signature."""
        # Validate version format
        _ = ArtifactVersion(version)

        artifact_id = f"art-{name}-{version}-{uuid.uuid4().hex[:6]}"
        checksum = ArtifactMetadata.calculate_checksum(data)

        meta = ArtifactMetadata(
            artifact_id=artifact_id,
            name=name,
            version=version,
            checksum_sha256=checksum,
            size_bytes=len(data),
            sbom_components=sbom_components or [],
            license_info=license_info,
            created_by=created_by,
            attributes=attributes or {},
        )

        if auto_sign:
            meta.sign(self._default_signing_key, signer_identity=created_by)

        self._artifacts[artifact_id] = meta
        self._payloads[artifact_id] = data
        return meta

    def get_artifact(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        """Retrieves artifact metadata by ID."""
        return self._artifacts.get(artifact_id)

    def get_artifact_data(self, artifact_id: str) -> Optional[bytes]:
        """Retrieves raw artifact binary payload."""
        return self._payloads.get(artifact_id)

    def list_artifacts(
        self,
        name: Optional[str] = None,
        verified_only: bool = False,
    ) -> List[ArtifactMetadata]:
        """Lists artifacts with optional filtering."""
        artifacts = list(self._artifacts.values())
        if name:
            artifacts = [a for a in artifacts if a.name == name]
        if verified_only:
            artifacts = [a for a in artifacts if a.verified]
        return sorted(artifacts, key=lambda a: a.created_at, reverse=True)

    def sign_artifact(
        self,
        artifact_id: str,
        secret_key: Optional[str] = None,
        signer_identity: str = "platform-admin",
    ) -> str:
        """Signs an existing artifact."""
        meta = self.get_artifact(artifact_id)
        if not meta:
            raise ArtifactValidationException(f"Artifact '{artifact_id}' not found")
        key = secret_key or self._default_signing_key
        return meta.sign(key, signer_identity)

    def verify_artifact(self, artifact_id: str, secret_key: Optional[str] = None) -> bool:
        """Verifies artifact checksum and cryptographic signature."""
        meta = self.get_artifact(artifact_id)
        if not meta:
            raise ArtifactValidationException(f"Artifact '{artifact_id}' not found")
        data = self.get_artifact_data(artifact_id)
        if data is not None:
            actual_checksum = ArtifactMetadata.calculate_checksum(data)
            if actual_checksum != meta.checksum_sha256:
                meta.verified = False
                return False

        key = secret_key or self._default_signing_key
        return meta.verify_signature(key)

    def record_vulnerability_scan(
        self,
        artifact_id: str,
        critical: int = 0,
        high: int = 0,
        medium: int = 0,
        max_critical_allowed: int = 0,
        max_high_allowed: int = 0,
    ) -> Dict[str, Any]:
        """Records security scan results for artifact."""
        meta = self.get_artifact(artifact_id)
        if not meta:
            raise ArtifactValidationException(f"Artifact '{artifact_id}' not found")
        
        passed = (critical <= max_critical_allowed) and (high <= max_high_allowed)
        scan_record = {
            "critical": critical,
            "high": high,
            "medium": medium,
            "passed": passed,
        }
        meta.vulnerability_scan = scan_record
        return scan_record

    def enforce_provenance(self, artifact_id: str, secret_key: Optional[str] = None) -> bool:
        """Strictly validates signature, checksum, and security scan status."""
        if not self.verify_artifact(artifact_id, secret_key):
            raise ArtifactValidationException(f"Artifact '{artifact_id}' failed cryptographic signature verification")
        
        meta = self.get_artifact(artifact_id)
        if meta and not meta.vulnerability_scan.get("passed", False):
            raise ArtifactValidationException(
                f"Artifact '{artifact_id}' has failing vulnerability scan: {meta.vulnerability_scan}"
            )
        return True
