"""
Clean Architecture Evidence Store for saving and querying verification runs.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.clean_architecture.domain.interfaces import ICleanArchEvidenceStore
from app.platform_verification.clean_architecture.domain.models import CleanArchEvidencePackage


class EnterpriseCleanArchEvidenceStore(ICleanArchEvidenceStore):
    """Stores sealed clean architecture evidence packages with SHA-256 digests."""

    def __init__(self):
        self._packages: Dict[str, CleanArchEvidencePackage] = {}

    def save_evidence(self, package: CleanArchEvidencePackage) -> str:
        package.evidence_sha256 = package.compute_sha256()
        self._packages[package.scan_id] = package
        return package.scan_id

    def get_evidence(self, scan_id: str) -> Optional[CleanArchEvidencePackage]:
        return self._packages.get(scan_id)
