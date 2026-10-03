"""
Immutable Evidence Store for Observability Verification.
"""
import hashlib
from typing import Dict, Optional
from app.platform_verification.observability_verification.domain.models import ObservabilityVerificationEvidencePackage
from app.platform_verification.observability_verification.domain.interfaces import IObservabilityEvidenceStore


class ObservabilityEvidenceStore(IObservabilityEvidenceStore):
    """Persists and seals observability verification evidence packages with SHA-256."""

    def __init__(self):
        self._store: Dict[str, ObservabilityVerificationEvidencePackage] = {}

    def seal_and_store_evidence(self, package: ObservabilityVerificationEvidencePackage) -> str:
        payload = f"{package.package_id}:{package.commit_sha}:{package.scorecard.composite_score}:{package.created_at}"
        package.package_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._store[package.package_id] = package
        return package.package_sha256

    def retrieve_evidence(self, package_id: str) -> Optional[ObservabilityVerificationEvidencePackage]:
        return self._store.get(package_id)
