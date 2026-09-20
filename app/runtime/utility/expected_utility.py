"""
Scientific Utility Engine - Expected Utility Formulation
Calculates multi-attribute expected utility under Von Neumann-Morgenstern decision theory.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from app.runtime.utility.utility_functions import UtilityFunctions, RiskProfile


@dataclass
class UtilityWeights:
    accuracy: float = 0.35
    latency: float = 0.20
    cost: float = 0.15
    safety_compliance: float = 0.15
    reliability: float = 0.15

    def normalize(self) -> "UtilityWeights":
        total = self.accuracy + self.latency + self.cost + self.safety_compliance + self.reliability
        if total <= 0:
            return UtilityWeights(0.2, 0.2, 0.2, 0.2, 0.2)
        return UtilityWeights(
            accuracy=self.accuracy / total,
            latency=self.latency / total,
            cost=self.cost / total,
            safety_compliance=self.safety_compliance / total,
            reliability=self.reliability / total,
        )


@dataclass
class UtilityBreakdown:
    expected_utility: float
    accuracy_utility: float
    latency_utility: float
    cost_utility: float
    safety_utility: float
    reliability_utility: float
    risk_penalty: float
    weights_applied: Dict[str, float]


class ExpectedUtilityEngine:
    """Computes expected utility for a candidate execution plan or model routing choice."""

    @classmethod
    def compute(
        cls,
        normalized_features: Dict[str, float],
        weights: Optional[UtilityWeights] = None,
        risk_profile: RiskProfile = RiskProfile.RISK_AVERSE,
    ) -> UtilityBreakdown:
        w = (weights or UtilityWeights()).normalize()

        # Extract normalized attributes (all assumed in [0, 1])
        acc_raw = normalized_features.get("ocr_confidence", 0.85) * 0.5 + normalized_features.get("schema_validation_score", 1.0) * 0.5
        lat_norm = normalized_features.get("latency_p95_ms", 0.2)  # cost metric
        cost_norm = normalized_features.get("api_cost_usd", 0.1)   # cost metric
        comp_norm = 1.0 - (normalized_features.get("compliance_flags", 0.0))
        rel_norm = normalized_features.get("historical_success_rate", 0.95) * 0.5 + normalized_features.get("worker_reliability", 0.98) * 0.5
        risk_norm = normalized_features.get("anomaly_score", 0.05) * 0.5 + normalized_features.get("epistemic_uncertainty", 0.1) * 0.5

        # Transform using chosen risk profile
        lambda_param = 3.0 if risk_profile in (RiskProfile.RISK_AVERSE, RiskProfile.STRICT_ENTERPRISE) else 0.0

        u_acc = UtilityFunctions.exponential_utility(acc_raw, risk_aversion_lambda=lambda_param, is_cost=False)
        u_lat = UtilityFunctions.exponential_utility(lat_norm, risk_aversion_lambda=lambda_param, is_cost=True)
        u_cost = UtilityFunctions.exponential_utility(cost_norm, risk_aversion_lambda=lambda_param, is_cost=True)
        u_safe = UtilityFunctions.exponential_utility(comp_norm, risk_aversion_lambda=lambda_param, is_cost=False)
        u_rel = UtilityFunctions.exponential_utility(rel_norm, risk_aversion_lambda=lambda_param, is_cost=False)

        # Multi-attribute expected utility
        eu_base = (
            w.accuracy * u_acc +
            w.latency * u_lat +
            w.cost * u_cost +
            w.safety_compliance * u_safe +
            w.reliability * u_rel
        )

        risk_penalty = 0.2 * risk_norm if risk_profile == RiskProfile.STRICT_ENTERPRISE else 0.1 * risk_norm
        final_eu = max(0.0, min(1.0, eu_base - risk_penalty))

        return UtilityBreakdown(
            expected_utility=round(final_eu, 4),
            accuracy_utility=round(u_acc, 4),
            latency_utility=round(u_lat, 4),
            cost_utility=round(u_cost, 4),
            safety_utility=round(u_safe, 4),
            reliability_utility=round(u_rel, 4),
            risk_penalty=round(risk_penalty, 4),
            weights_applied={
                "accuracy": round(w.accuracy, 4),
                "latency": round(w.latency, 4),
                "cost": round(w.cost, 4),
                "safety_compliance": round(w.safety_compliance, 4),
                "reliability": round(w.reliability, 4),
            },
        )
