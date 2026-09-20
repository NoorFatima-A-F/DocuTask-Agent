"""
Immutable Evidence Store for Database Architecture Verification.
"""
import hashlib
import json
from typing import Dict, Optional
from app.platform_verification.database_verification.domain.models import DatabaseVerificationEvidencePackage
from app.platform_verification.database_verification.domain.interfaces import IDatabaseEvidenceStore


class DatabaseEvidenceStore(IDatabaseEvidenceStore):
    """Stores and seals database verification evidence packages with SHA-256."""

    def __init__(self):
        self._store: Dict[str, DatabaseVerificationEvidencePackage] = {}

    def seal_and_store_evidence(self, package: DatabaseVerificationEvidencePackage) -> str:
        # Compute SHA-256 seal
        payload = f"{package.package_id}:{package.commit_sha}:{package.scorecard.composite_score}:{package.created_at}"
        package.package_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self._store[package.package_id] = package
        return package.package_sha256

    def retrieve_evidence(self, package_id: str) -> Optional[DatabaseVerificationEvidencePackage]:
        return self._store.get(package_id)
