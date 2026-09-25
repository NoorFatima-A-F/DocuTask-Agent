"""
Business Priority Model for Phase 13.6 (ARIA-EOP).
Manages organizational priority tiers (CRITICAL_SLA, HIGH_VALUE, BALANCED_STANDARD, BACKGROUND_BATCH).
"""

from pydantic import BaseModel


class PriorityWeights(BaseModel):
    tier_name: str
    weight_latency: float
    weight_cost: float
    weight_confidence: float
    max_budget_multiplier: float


class BusinessPriority:
    """
    Translates business priority tiers into scalarization weights and resource multipliers.
    """

    TIERS = {
        "CRITICAL_SLA": PriorityWeights(
            tier_name="CRITICAL_SLA",
            weight_latency=0.60,
            weight_cost=0.05,
            weight_confidence=0.35,
            max_budget_multiplier=2.5,
        ),
        "HIGH_VALUE": PriorityWeights(
            tier_name="HIGH_VALUE",
            weight_latency=0.20,
            weight_cost=0.10,
            weight_confidence=0.70,
            max_budget_multiplier=1.8,
        ),
        "BALANCED_STANDARD": PriorityWeights(
            tier_name="BALANCED_STANDARD",
            weight_latency=0.35,
            weight_cost=0.25,
            weight_confidence=0.40,
            max_budget_multiplier=1.0,
        ),
        "BACKGROUND_BATCH": PriorityWeights(
            tier_name="BACKGROUND_BATCH",
            weight_latency=0.05,
            weight_cost=0.75,
            weight_confidence=0.20,
            max_budget_multiplier=0.4,
        ),
    }

    @classmethod
    def get_tier_weights(cls, tier: str = "BALANCED_STANDARD") -> PriorityWeights:
        return cls.TIERS.get(tier, cls.TIERS["BALANCED_STANDARD"])
