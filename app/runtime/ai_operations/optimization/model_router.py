"""
Phase 13.17: Multi-Objective Pareto Model Router
Dynamic model selection optimizing trade-offs between Cost, Latency, and Quality under SLA constraints.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple
from app.runtime.ai_operations.models.schemas import (
    ModelTier,
    ModelRouteDecision,
)


class ModelCatalog:
    """Enterprise model catalog with cost, latency, and capability profiles."""

    PROFILES: Dict[str, Dict[str, Any]] = {
        ModelTier.FLASH_LITE.value: {
            "tier": ModelTier.FLASH_LITE,
            "cost_per_1k_prompt": 0.000075,
            "cost_per_1k_completion": 0.0003,
            "typical_latency_ms": 120.0,
            "quality_rating": 0.82,
            "max_context": 1000000,
        },
        ModelTier.FLASH.value: {
            "tier": ModelTier.FLASH,
            "cost_per_1k_prompt": 0.00015,
            "cost_per_1k_completion": 0.0006,
            "typical_latency_ms": 250.0,
            "quality_rating": 0.91,
            "max_context": 1000000,
        },
        ModelTier.PRO.value: {
            "tier": ModelTier.PRO,
            "cost_per_1k_prompt": 0.00125,
            "cost_per_1k_completion": 0.005,
            "typical_latency_ms": 850.0,
            "quality_rating": 0.98,
            "max_context": 2000000,
        },
        ModelTier.OMNI.value: {
            "tier": ModelTier.OMNI,
            "cost_per_1k_prompt": 0.00025,
            "cost_per_1k_completion": 0.0010,
            "typical_latency_ms": 320.0,
            "quality_rating": 0.93,
            "max_context": 1000000,
        },
    }


class ModelRouter:
    """Evaluates multi-objective Pareto frontier and selects optimal model."""

    @staticmethod
    def route_task(
        task_id: str,
        estimated_prompt_tokens: int = 1500,
        estimated_completion_tokens: int = 500,
        weight_quality: float = 0.50,
        weight_latency: float = 0.30,
        weight_cost: float = 0.20,
        max_latency_sla_ms: Optional[float] = None,
        max_cost_budget_usd: Optional[float] = None,
    ) -> ModelRouteDecision:
        # Normalize weights
        total_w = weight_quality + weight_latency + weight_cost
        wq = weight_quality / total_w
        wl = weight_latency / total_w
        wc = weight_cost / total_w

        max_latency_ref = 1500.0
        max_cost_ref = 0.010

        candidates: List[Tuple[str, float, float, float, float]] = []

        for model_id, prof in ModelCatalog.PROFILES.items():
            est_cost = (
                (estimated_prompt_tokens / 1000.0) * prof["cost_per_1k_prompt"]
                + (estimated_completion_tokens / 1000.0) * prof["cost_per_1k_completion"]
            )
            est_lat = prof["typical_latency_ms"]
            quality = prof["quality_rating"]

            # SLA & Budget filters
            if max_latency_sla_ms and est_lat > max_latency_sla_ms:
                continue
            if max_cost_budget_usd and est_cost > max_cost_budget_usd:
                continue

            # Pareto score formula: wq * Quality - wl * (Latency / LatMax) - wc * (Cost / CostMax)
            pareto_score = (
                (wq * quality)
                - (wl * min(1.0, est_lat / max_latency_ref))
                - (wc * min(1.0, est_cost / max_cost_ref))
            )
            candidates.append((model_id, pareto_score, est_cost, est_lat, quality))

        if not candidates:
            # Fallback to Flash
            default_model = ModelTier.FLASH.value
            prof = ModelCatalog.PROFILES[default_model]
            return ModelRouteDecision(
                task_id=task_id,
                selected_model=default_model,
                selected_tier=prof["tier"],
                estimated_cost_usd=0.0005,
                estimated_latency_ms=250.0,
                estimated_quality_score=0.91,
                pareto_score=0.75,
                weights={"quality": wq, "latency": wl, "cost": wc},
                fallback_models=[ModelTier.FLASH_LITE.value, ModelTier.PRO.value],
            )

        # Sort by pareto score descending
        candidates.sort(key=lambda c: c[1], reverse=True)
        best_model, best_score, best_cost, best_lat, best_qual = candidates[0]
        fallbacks = [c[0] for c in candidates[1:]]

        return ModelRouteDecision(
            task_id=task_id,
            selected_model=best_model,
            selected_tier=ModelCatalog.PROFILES[best_model]["tier"],
            estimated_cost_usd=round(best_cost, 6),
            estimated_latency_ms=round(best_lat, 2),
            estimated_quality_score=round(best_qual, 3),
            pareto_score=round(best_score, 4),
            weights={"quality": round(wq, 2), "latency": round(wl, 2), "cost": round(wc, 2)},
            fallback_models=fallbacks,
        )
