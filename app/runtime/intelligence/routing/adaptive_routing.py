"""
Adaptive Resource Optimization & Routing for Phase 10 (AISLCOP).

Learns optimal runtime configurations and tool/model routing preferences from
measured empirical performance per document domain.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from app.runtime.intelligence.experience.experience_record import ExperienceRecord


@dataclass
class DomainResourceProfile:
    document_domain: str
    preferred_ocr_engine: str = "tesseract_v2"
    preferred_llm_model: str = "gemini-1.5-flash"
    fallback_model: str = "gemini-1.5-pro"
    optimal_batch_size: int = 4
    concurrency_limit: int = 3
    estimated_latency_ms: float = 1100.0
    estimated_cost_usd: float = 0.010
    sample_count: int = 1
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AdaptiveResourceOptimizer:
    """
    Learns and updates domain-to-resource routing preferences based on experience logs.
    """

    def __init__(self):
        self._profiles: Dict[str, DomainResourceProfile] = {
            "invoice": DomainResourceProfile(
                document_domain="invoice",
                preferred_ocr_engine="tesseract_v2_optimized",
                preferred_llm_model="gemini-1.5-flash",
                fallback_model="gemini-1.5-pro",
                estimated_latency_ms=950.0,
                estimated_cost_usd=0.008,
            ),
            "contract": DomainResourceProfile(
                document_domain="contract",
                preferred_ocr_engine="pdfplumber_advanced",
                preferred_llm_model="gemini-1.5-pro",
                fallback_model="gemini-1.5-pro",
                estimated_latency_ms=2200.0,
                estimated_cost_usd=0.035,
            ),
            "medical": DomainResourceProfile(
                document_domain="medical",
                preferred_ocr_engine="vision_multimodal_ocr",
                preferred_llm_model="gemini-1.5-pro",
                fallback_model="gemini-1.5-pro",
                estimated_latency_ms=1800.0,
                estimated_cost_usd=0.028,
            ),
        }

    def get_profile(self, domain: str) -> DomainResourceProfile:
        norm = domain.lower()
        if norm in self._profiles:
            return self._profiles[norm]
        # Return generic default
        return DomainResourceProfile(document_domain=domain)

    def update_from_experiences(self, experiences: List[ExperienceRecord]) -> Dict[str, DomainResourceProfile]:
        """Recalibrates domain profiles based on latest empirical experiences."""
        domain_groups: Dict[str, List[ExperienceRecord]] = {}
        for exp in experiences:
            norm = exp.document_type.lower()
            if norm not in domain_groups:
                domain_groups[norm] = []
            domain_groups[norm].append(exp)

        for domain, exps in domain_groups.items():
            if not exps:
                continue
            avg_lat = sum(e.total_latency_ms for e in exps) / len(exps)
            avg_cost = sum(e.total_cost_usd for e in exps) / len(exps)
            avg_conf = sum(e.final_confidence for e in exps) / len(exps)

            current = self.get_profile(domain)
            current.estimated_latency_ms = round(avg_lat, 2)
            current.estimated_cost_usd = round(avg_cost, 6)
            current.sample_count = len(exps)
            current.updated_at = time.time()

            # Dynamic model tier adjustment: if Flash achieves high confidence, prefer Flash
            if avg_conf >= 0.95 and avg_cost < 0.015:
                current.preferred_llm_model = "gemini-1.5-flash"
            else:
                current.preferred_llm_model = "gemini-1.5-pro"

            self._profiles[domain] = current

        return self._profiles

    def list_profiles(self) -> List[DomainResourceProfile]:
        return list(self._profiles.values())
