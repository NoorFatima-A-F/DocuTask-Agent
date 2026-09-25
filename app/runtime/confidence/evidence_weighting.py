"""
Scientific Confidence Engine - Evidence Weighting
Calculates evidentiary weights, credibility discounting, and provenance attributions.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class EvidentiaryFactor:
    source_name: str
    raw_confidence: float
    source_reliability: float
    effective_weight: float
    likelihood_ratio: float


class EvidenceWeighter:
    """Weights and discounts multi-source verification evidence."""

    DEFAULT_SOURCE_RELIABILITY = {
        "ocr_engine": 0.92,
        "schema_validation": 0.99,
        "cross_agent_consensus": 0.94,
        "memory_grounding": 0.88,
        "human_review_history": 0.98,
    }

    @classmethod
    def evaluate_factors(
        cls,
        observations: Dict[str, float],
        custom_reliabilities: Dict[str, float] = None,
    ) -> List[EvidentiaryFactor]:
        reliabilities = dict(cls.DEFAULT_SOURCE_RELIABILITY)
        if custom_reliabilities:
            reliabilities.update(custom_reliabilities)

        factors: List[EvidentiaryFactor] = []
        for source, raw_conf in observations.items():
            rel = reliabilities.get(source, 0.85)
            # Effective weight combines raw value and reliability
            eff_weight = raw_conf * rel
            # Likelihood ratio for Bayesian update
            lr = (max(0.01, raw_conf) * rel) / (max(0.01, 1.0 - raw_conf) * (1.0 - rel + 1e-5))
            factors.append(
                EvidentiaryFactor(
                    source_name=source,
                    raw_confidence=round(raw_conf, 4),
                    source_reliability=round(rel, 4),
                    effective_weight=round(eff_weight, 4),
                    likelihood_ratio=round(lr, 4),
                )
            )
        return factors
