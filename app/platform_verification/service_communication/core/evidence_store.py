"""
Immutable Evidence Store for Service Communication Verification.
"""
import hashlib
from typing import Dict, Optional
from app.platform_verification.service_communication.domain.models import ServiceCommunicationEvidencePackage
from app.platform_verification.service_communication.domain.interfaces import IServiceCommunicationEvidenceStore


class ServiceCommunicationEvidenceStore(IServiceCommunicationEvidenceStore):
    """Persists and seals service communication verification evidence packages with SHA-256."""

    def __init__(self):
        self._store: Dict[str, ServiceCommunicationEvidencePackage] = {}

    def seal_and_store_evidence(self, package: ServiceCommunicationEvidencePackage) -> str:
        payload = f"{package.package_id}:{package.commit_sha}:{package.scorecard.composite_score}:{package.created_at}"
        package.package_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._store[package.package_id] = package
        return package.package_sha256

    def retrieve_evidence(self, package_id: str) -> Optional[ServiceCommunicationEvidencePackage]:
        return self._store.get(package_id)
