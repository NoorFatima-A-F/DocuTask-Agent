"""
Digital Twin Runtime - Fidelity Monitor
Quantifies how closely the digital twin shadow environment mirrors production reality.
"""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class FidelityMetrics:
    shadow_id: str
    output_agreement_score: float  # [0.0 - 1.0]
    latency_divergence_pct: float  # e.g. 3.2%
    token_consumption_delta: int
    decision_alignment_rate: float
    fidelity_status: str  # HIGH_FIDELITY | ACCEPTABLE | DIVERGENT | CRITICAL_DESYNC

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FidelityMonitor:
    """Monitors digital twin fidelity against real-world production runs."""

    @staticmethod
    def compute_fidelity(
        shadow_id: str,
        prod_output: str,
        shadow_output: str,
        prod_latency_ms: float,
        shadow_latency_ms: float,
        prod_tokens: int,
        shadow_tokens: int,
        prod_decision: str,
        shadow_decision: str,
    ) -> FidelityMetrics:
        # 1. Output string overlap / agreement
        p_set = set(prod_output.lower().split())
        s_set = set(shadow_output.lower().split())
        intersection = p_set.intersection(s_set)
        union = p_set.union(s_set)
        jaccard = len(intersection) / max(1, len(union))

        # 2. Latency divergence percentage
        denom_lat = max(1.0, prod_latency_ms)
        lat_div = abs(shadow_latency_ms - prod_latency_ms) / denom_lat * 100.0

        # 3. Token consumption delta
        token_delta = shadow_tokens - prod_tokens

        # 4. Decision alignment
        decision_match = 1.0 if prod_decision == shadow_decision else 0.0

        # Status determination
        if jaccard >= 0.90 and lat_div <= 15.0 and decision_match == 1.0:
            status = "HIGH_FIDELITY"
        elif jaccard >= 0.75 and lat_div <= 30.0:
            status = "ACCEPTABLE"
        elif jaccard >= 0.50:
            status = "DIVERGENT"
        else:
            status = "CRITICAL_DESYNC"

        return FidelityMetrics(
            shadow_id=shadow_id,
            output_agreement_score=round(jaccard, 4),
            latency_divergence_pct=round(lat_div, 2),
            token_consumption_delta=token_delta,
            decision_alignment_rate=round(decision_match, 2),
            fidelity_status=status,
        )
