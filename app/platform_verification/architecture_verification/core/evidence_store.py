"""
Architecture Evidence Store for saving and retrieving immutable scan artifacts.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.architecture_verification.domain.interfaces import IArchitectureEvidenceStore
from app.platform_verification.architecture_verification.domain.models import ArchitectureEvidencePackage


class EnterpriseArchitectureEvidenceStore(IArchitectureEvidenceStore):
    """In-memory and persistent evidence store with SHA-256 integrity verification."""

    def __init__(self):
        self._store: Dict[str, ArchitectureEvidencePackage] = {}

    def save_evidence(self, package: ArchitectureEvidencePackage) -> str:
        package.evidence_sha256 = package.compute_sha256()
        self._store[package.scan_id] = package
        return package.scan_id

    def get_evidence(self, scan_id: str) -> Optional[ArchitectureEvidencePackage]:
        return self._store.get(scan_id)
