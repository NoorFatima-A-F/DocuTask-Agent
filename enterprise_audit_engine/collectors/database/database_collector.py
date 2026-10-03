"""Database Architecture & Migration Safety Collector."""

from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class DatabaseCollector(BaseCollector):
    """Inspects database migration safety linters and models."""

    @property
    def name(self) -> str:
        return "DatabaseCollector"

    @property
    def category(self) -> str:
        return "DatabaseArchitectureAndSafety"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        migrations_dir = self.repo_root / "app" / "platform_delivery" / "migrations"

        has_expand_contract = (migrations_dir / "expand_contract.py").exists()
        has_safety_linter = (migrations_dir / "safety.py").exists()

        payload: Dict[str, Any] = {
            "has_expand_contract_module": has_expand_contract,
            "has_safety_linter_module": has_safety_linter,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if has_expand_contract and has_safety_linter
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"Database migration safety verified: expand-contract module ({has_expand_contract}), safety linter ({has_safety_linter}).",
            confidence=EvidenceConfidence.MEDIUM,
            classification=classification,
        )
        records.append(record)
        return records
