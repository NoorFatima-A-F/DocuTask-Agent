"""Repository Governance & Open Source Compliance Collector."""

from pathlib import Path
from typing import List, Dict, Any
from ..domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from ..base import BaseCollector


class GovernanceCollector(BaseCollector):
    """Verifies open-source governance documents, community health files, and ADRs."""

    @property
    def name(self) -> str:
        return "GovernanceCollector"

    @property
    def category(self) -> str:
        return "GovernanceAndCompliance"

    REQUIRED_DOCS = [
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        "ROADMAP.md",
    ]

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        doc_status: Dict[str, bool] = {}

        for doc in self.REQUIRED_DOCS:
            doc_path = self.repo_root / doc
            doc_status[doc] = doc_path.exists() and doc_path.stat().st_size > 100

        # Check ADR directory
        adr_dir = self.repo_root / "docs" / "adr"
        adr_count = len(list(adr_dir.glob("*.md"))) if adr_dir.exists() else 0

        # Check GitHub issue templates
        issue_template_dir = self.repo_root / ".github" / "ISSUE_TEMPLATE"
        has_issue_templates = issue_template_dir.exists() and len(list(issue_template_dir.glob("*.md"))) > 0

        # Check CODEOWNERS
        codeowners_file = self.repo_root / ".github" / "CODEOWNERS"
        has_codeowners = codeowners_file.exists()

        all_required_present = all(doc_status.values()) and has_codeowners and has_issue_templates

        payload: Dict[str, Any] = {
            "required_docs": doc_status,
            "adr_count": adr_count,
            "has_issue_templates": has_issue_templates,
            "has_codeowners": has_codeowners,
            "governance_complete": all_required_present,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_CONFIGURATION
            if all_required_present
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        missing = [k for k, v in doc_status.items() if not v]
        summary = (
            f"All {len(self.REQUIRED_DOCS)} required governance documents present. ADRs: {adr_count}. CODEOWNERS & templates active."
            if all_required_present
            else f"Missing governance items: {', '.join(missing)}."
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.CONFIGURATION_FILE,
            raw_payload=payload,
            summary=summary,
            confidence=EvidenceConfidence.LOW,
            classification=classification,
        )
        records.append(record)
        return records
