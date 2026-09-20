"""
Policy Comparator for Phase 13.5 (ARLP-KIP).
Compares candidate policies against baseline configurations to compute differential gains and risk tradeoffs.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class PolicyComparisonReport(BaseModel):
    baseline_policy_id: str = "pol-baseline"
    candidate_policy_id: str
    net_throughput_gain_pct: float
    risk_delta: float
    confidence_delta: float
    recommendation: str = "RECOMMENDED_FOR_APPROVAL"


class PolicyComparator:
    """
    Performs differential matrix comparison between baseline and candidate policies.
    """

    @classmethod
    def compare(cls, candidate_id: str, gain: float, risk: float, conf: float) -> PolicyComparisonReport:
        rec = "RECOMMENDED_FOR_APPROVAL" if gain > 5.0 and risk < 0.30 else "REQUIRES_MANUAL_REVIEW"
        return PolicyComparisonReport(
            baseline_policy_id="pol-baseline",
            candidate_policy_id=candidate_id,
            net_throughput_gain_pct=gain,
            risk_delta=round(risk - 0.10, 3),
            confidence_delta=round(conf - 0.90, 3),
            recommendation=rec,
        )
