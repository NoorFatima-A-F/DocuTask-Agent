"""AI Pipeline, Prompt Registry & Safety Gateway Collector."""

from pathlib import Path
from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class AIPipelineCollector(BaseCollector):
    """Inspects AI prompt registry, safety gateway, and provider abstractions."""

    @property
    def name(self) -> str:
        return "AIPipelineCollector"

    @property
    def category(self) -> str:
        return "AIEngineeringAndSafety"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        app_dir = self.repo_root / "app"

        has_prompt_registry = (app_dir / "prompts").exists()
        has_safety_gateway = (app_dir / "safety").exists()
        has_platform_delivery_strategies = (app_dir / "platform_delivery" / "strategies").exists()

        payload: Dict[str, Any] = {
            "has_prompt_registry": has_prompt_registry,
            "has_safety_gateway": has_safety_gateway,
            "has_shadow_strategy": (app_dir / "platform_delivery" / "strategies" / "shadow.py").exists(),
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if has_prompt_registry or has_platform_delivery_strategies
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"AI pipeline inspection: prompt registry ({has_prompt_registry}), safety gateway ({has_safety_gateway}), shadow rollout strategy ({payload['has_shadow_strategy']}).",
            confidence=EvidenceConfidence.MEDIUM,
            classification=classification,
        )
        records.append(record)
        return records
