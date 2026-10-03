"""
Immutable Evidence Store for Test Architecture Verification.
"""
import hashlib
from typing import Dict, Optional
from app.platform_verification.test_architecture_verification.domain.models import TestArchitectureEvidencePackage
from app.platform_verification.test_architecture_verification.domain.interfaces import ITestEvidenceStore


class TestEvidenceStore(ITestEvidenceStore):
    """Persists and seals test architecture verification evidence with SHA-256."""
    __test__ = False

    def __init__(self):
        self._store: Dict[str, TestArchitectureEvidencePackage] = {}

    def seal_and_store_evidence(self, package: TestArchitectureEvidencePackage) -> str:
        payload = f"{package.package_id}:{package.commit_sha}:{package.scorecard.composite_score}:{package.created_at}"
        package.package_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._store[package.package_id] = package
        return package.package_sha256

    def retrieve_evidence(self, package_id: str) -> Optional[TestArchitectureEvidencePackage]:
        return self._store.get(package_id)
