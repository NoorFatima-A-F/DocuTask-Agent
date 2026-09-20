"""
Immutable Evidence Store for Deployment Verification.
"""
import hashlib
from typing import Dict, Optional
from app.platform_verification.deployment_verification.domain.models import DeploymentVerificationEvidencePackage
from app.platform_verification.deployment_verification.domain.interfaces import IDeploymentEvidenceStore


class DeploymentEvidenceStore(IDeploymentEvidenceStore):
    """Persists and seals deployment verification evidence packages with SHA-256."""

    def __init__(self):
        self._store: Dict[str, DeploymentVerificationEvidencePackage] = {}

    def seal_and_store_evidence(self, package: DeploymentVerificationEvidencePackage) -> str:
        payload = f"{package.package_id}:{package.commit_sha}:{package.scorecard.composite_score}:{package.created_at}"
        package.package_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._store[package.package_id] = package
        return package.package_sha256

    def retrieve_evidence(self, package_id: str) -> Optional[DeploymentVerificationEvidencePackage]:
        return self._store.get(package_id)
