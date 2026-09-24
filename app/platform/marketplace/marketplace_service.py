"""Agent Marketplace Service.

Catalog for discovering, downloading, and 1-click installing verified autonomous agent plugins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.platform.plugins.plugin_loader import (
    PluginLoader,
    PluginManifest,
    global_plugin_loader,
)


@dataclass
class MarketplacePackage:
    package_id: str
    name: str
    version: str
    author: str
    category: str
    description: str
    security_audit_score: float  # 0.0 - 100.0
    download_count: int
    rating: float
    verified: bool
    manifest: Dict[str, Any]
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "package_id": self.package_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "category": self.category,
            "description": self.description,
            "security_audit_score": self.security_audit_score,
            "download_count": self.download_count,
            "rating": self.rating,
            "verified": self.verified,
            "tags": self.tags,
            "manifest": self.manifest,
        }


class MarketplaceService:
    def __init__(self, loader: Optional[PluginLoader] = None):
        self.loader = loader or global_plugin_loader
        self._packages: Dict[str, MarketplacePackage] = {}
        self._seed_marketplace_catalog()

    def _seed_marketplace_catalog(self) -> None:
        catalog = [
            MarketplacePackage(
                package_id="pkg.fintech.invoice_pro",
                name="InvoicePro Elite Agent",
                version="1.4.0",
                author="DocuTask Labs",
                category="FINANCE",
                description="State-of-the-art multi-lingual invoice extraction with Mod11 VAT checksum verification.",
                security_audit_score=99.4,
                download_count=14200,
                rating=4.95,
                verified=True,
                tags=["invoices", "ocr", "reconciliation", "sap"],
                manifest={
                    "plugin_id": "plugin.invoice.processing",
                    "name": "InvoicePro Elite Agent",
                    "version": "1.4.0",
                    "capabilities_provided": ["perception.ocr", "extraction.invoice", "validation.reconciliation"],
                },
            ),
            MarketplacePackage(
                package_id="pkg.hr.talent_matcher",
                name="TalentMatcher ATS Screener",
                version="1.2.0",
                author="TalentAI Labs",
                category="HUMAN_RESOURCES",
                description="Parses complex multi-column resumes and scores talent against job requisitions.",
                security_audit_score=98.1,
                download_count=8900,
                rating=4.88,
                verified=True,
                tags=["resumes", "ats", "hiring", "skills"],
                manifest={
                    "plugin_id": "plugin.resume.screener",
                    "name": "TalentMatcher ATS Screener",
                    "version": "1.2.0",
                    "capabilities_provided": ["extraction.resume", "scoring.ats_match"],
                },
            ),
            MarketplacePackage(
                package_id="pkg.health.hipaa_shield",
                name="HIPAA Clinical Shield",
                version="2.0.1",
                author="MedSecure Systems",
                category="HEALTHCARE",
                description="Zero-leakage PHI redactor and ICD-10 diagnostic coding extractor.",
                security_audit_score=100.0,
                download_count=6400,
                rating=4.98,
                verified=True,
                tags=["healthcare", "hipaa", "phi", "icd10"],
                manifest={
                    "plugin_id": "plugin.medical.records",
                    "name": "HIPAA Clinical Shield",
                    "version": "2.0.1",
                    "capabilities_provided": ["privacy.deidentify", "extraction.clinical"],
                },
            ),
            MarketplacePackage(
                package_id="pkg.legal.lexis_covenant",
                name="LexisCovenant Contract Reviewer",
                version="1.1.5",
                author="LexisCorp AI",
                category="LEGAL",
                description="Identifies risky indemnities, non-competes, and liabilities in MSAs and NDAs.",
                security_audit_score=97.8,
                download_count=11200,
                rating=4.91,
                verified=True,
                tags=["contracts", "legal", "indemnity", "risk"],
                manifest={
                    "plugin_id": "plugin.legal.contracts",
                    "name": "LexisCovenant Contract Reviewer",
                    "version": "1.1.5",
                    "capabilities_provided": ["extraction.contract", "analysis.risk"],
                },
            ),
        ]
        for p in catalog:
            self._packages[p.package_id] = p

    def list_packages(self) -> List[MarketplacePackage]:
        return list(self._packages.values())

    def get_package(self, package_id: str) -> Optional[MarketplacePackage]:
        return self._packages.get(package_id)

    def install_package(self, package_id: str) -> Dict[str, Any]:
        pkg = self.get_package(package_id)
        if not pkg:
            raise KeyError(f"Package '{package_id}' not found in marketplace")

        manifest = PluginManifest.from_dict(pkg.manifest)
        self.loader.load_plugin(manifest)
        pkg.download_count += 1

        return {
            "status": "INSTALLED",
            "package_id": package_id,
            "plugin_id": manifest.plugin_id,
            "version": manifest.version,
            "capabilities": manifest.capabilities_provided,
        }


global_marketplace_service = MarketplaceService()
