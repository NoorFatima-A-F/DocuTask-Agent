"""Audit Report Generator."""

from typing import Optional, List
from ..storage.repository import AuditRepository
from ..evidence.manager import EvidenceManager, EvidenceBundle
from .formats import AuditExporter


class AuditReportGenerator:
    """Generates formal compliance reports and export packages for auditors."""

    def __init__(
        self,
        repository: Optional[AuditRepository] = None,
        evidence_manager: Optional[EvidenceManager] = None,
    ):
        self.repository = repository or AuditRepository()
        self.evidence_manager = evidence_manager or EvidenceManager(self.repository)

    def generate_dossier(
        self,
        tenant_id: str,
        title: str,
        purpose: str,
        correlation_id: Optional[str] = None,
    ) -> str:
        bundle = self.evidence_manager.create_evidence_bundle(
            tenant_id=tenant_id,
            title=title,
            purpose=purpose,
            correlation_id=correlation_id,
        )
        return AuditExporter.to_markdown_dossier(bundle)
