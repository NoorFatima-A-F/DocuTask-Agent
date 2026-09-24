"""Cost Optimization Recommendations and Efficiency Engine."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List


class RecommendationType(str, Enum):
    SEMANTIC_CACHE = "SEMANTIC_CACHE"
    RIGHTSIZE_WORKERS = "RIGHTSIZE_WORKERS"
    COLD_STORAGE_TIER = "COLD_STORAGE_TIER"
    MODEL_QUANTIZATION = "MODEL_QUANTIZATION"


@dataclass
class CostRecommendation:
    recommendation_id: str
    title: str
    recommendation_type: RecommendationType
    estimated_monthly_savings_usd: float
    description: str
    impact: str = "HIGH"  # HIGH, MEDIUM, LOW


class CostOptimizationEngine:
    """Generates automated recommendations to optimize cloud and AI token expenditure."""

    def evaluate_optimizations(
        self,
        cache_hit_rate_pct: float,
        idle_worker_hours: float,
        stale_documents_gb: float,
    ) -> List[CostRecommendation]:
        recs: List[CostRecommendation] = []

        # 1. Semantic Embedding Cache Recommendation
        if cache_hit_rate_pct < 40.0:
            savings = 450.0 * (1.0 - (cache_hit_rate_pct / 100.0))
            recs.append(
                CostRecommendation(
                    recommendation_id=f"rec-cache-{uuid.uuid4().hex[:6]}",
                    title="Enable Semantic Embedding Cache for Repeated Queries",
                    recommendation_type=RecommendationType.SEMANTIC_CACHE,
                    estimated_monthly_savings_usd=round(savings, 2),
                    description="Current embedding cache hit rate is low. Enabling exact/semantic caching reduces duplicate model calls.",
                    impact="HIGH",
                )
            )

        # 2. Worker Auto-scaling / Rightsizing
        if idle_worker_hours > 50.0:
            savings = idle_worker_hours * 0.04 * 30.0
            recs.append(
                CostRecommendation(
                    recommendation_id=f"rec-scale-{uuid.uuid4().hex[:6]}",
                    title="Scale Down Idle Workers During Off-Peak Hours",
                    recommendation_type=RecommendationType.RIGHTSIZE_WORKERS,
                    estimated_monthly_savings_usd=round(savings, 2),
                    description="High idle worker capacity observed outside business hours. Adjust HPA min replicas.",
                    impact="MEDIUM",
                )
            )

        # 3. Storage Lifecycle Tiering
        if stale_documents_gb > 100.0:
            savings = stale_documents_gb * 0.015
            recs.append(
                CostRecommendation(
                    recommendation_id=f"rec-tier-{uuid.uuid4().hex[:6]}",
                    title="Move Archived Documents to Coldline Storage",
                    recommendation_type=RecommendationType.COLD_STORAGE_TIER,
                    estimated_monthly_savings_usd=round(savings, 2),
                    description="Historical document payloads older than 90 days can be moved to cold storage.",
                    impact="LOW",
                )
            )

        return recs
