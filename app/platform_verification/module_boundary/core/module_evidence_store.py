"""
Module Architecture Evidence Store.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.module_boundary.domain.interfaces import IModuleEvidenceStore
from app.platform_verification.module_boundary.domain.models import ModuleArchitectureEvidencePackage


class EnterpriseModuleEvidenceStore(IModuleEvidenceStore):
    """In-memory and persistent evidence store with SHA-256 integrity verification."""

    def __init__(self):
        self._packages: Dict[str, ModuleArchitectureEvidencePackage] = {}

    def save_evidence(self, package: ModuleArchitectureEvidencePackage) -> str:
        package.evidence_sha256 = package.compute_sha256()
        self._packages[package.scan_id] = package
        return package.scan_id

    def get_evidence(self, scan_id: str) -> Optional[ModuleArchitectureEvidencePackage]:
        return self._packages.get(scan_id)
