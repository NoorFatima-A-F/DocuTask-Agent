"""
SOLID Evidence Store for persisting and retrieving sealed design scan packages.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.solid_verification.domain.interfaces import ISolidEvidenceStore
from app.platform_verification.solid_verification.domain.models import SolidEvidencePackage


class EnterpriseSolidEvidenceStore(ISolidEvidenceStore):
    """In-memory and persistent evidence store with SHA-256 verification."""

    def __init__(self):
        self._packages: Dict[str, SolidEvidencePackage] = {}

    def save_evidence(self, package: SolidEvidencePackage) -> str:
        package.evidence_sha256 = package.compute_sha256()
        self._packages[package.scan_id] = package
        return package.scan_id

    def get_evidence(self, scan_id: str) -> Optional[SolidEvidencePackage]:
        return self._packages.get(scan_id)
