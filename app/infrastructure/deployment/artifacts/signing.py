"""Cryptographic Artifact Signing, Provenance Attestation, and Verification."""

import hashlib
import hmac

from .metadata import ArtifactMetadata


class ArtifactSigner:
    """Signs artifacts and verifies cryptographic provenance and integrity."""

    def __init__(self, signing_secret: str = "secret-docutask-cosign-key") -> None:
        self.signing_secret = signing_secret.encode("utf-8")

    def sign_artifact(self, artifact: ArtifactMetadata, signer_identity: str = "docutask-release-signer") -> str:
        """Generate HMAC-SHA256 signature for the artifact digest and provenance."""
        payload = f"{artifact.artifact_id}:{artifact.digest_sha256}:{artifact.commit_sha}:{artifact.version}"
        sig = hmac.new(self.signing_secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        artifact.signature = sig
        artifact.signed_by = signer_identity
        return sig

    def verify_signature(self, artifact: ArtifactMetadata) -> bool:
        """Verify artifact cryptographic signature."""
        if not artifact.signature:
            return False

        payload = f"{artifact.artifact_id}:{artifact.digest_sha256}:{artifact.commit_sha}:{artifact.version}"
        expected = hmac.new(self.signing_secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(artifact.signature, expected)
