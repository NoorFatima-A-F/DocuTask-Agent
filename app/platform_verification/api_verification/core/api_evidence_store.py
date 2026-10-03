"""
API Architecture Evidence Store.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.api_verification.domain.interfaces import IApiEvidenceStore
from app.platform_verification.api_verification.domain.models import ApiEvidencePackage


class EnterpriseApiEvidenceStore(IApiEvidenceStore):
    """In-memory and persistent evidence store for API verification packages."""

    def __init__(self):
        self._packages: Dict[str, ApiEvidencePackage] = {}

    def save_evidence(self, package: ApiEvidencePackage) -> str:
        package.evidence_sha256 = package.compute_sha256()
        self._packages[package.scan_id] = package
        return package.scan_id

    def get_evidence(self, scan_id: str) -> Optional[ApiEvidencePackage]:
        return self._packages.get(scan_id)
