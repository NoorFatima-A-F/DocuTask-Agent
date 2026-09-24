"""
In-process REST API Router for Metrics Engine Operations.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricDefinition,
)
from app.platform_verification.evaluation_engine.core.metric_registry import MetricRegistry
from app.platform_verification.evaluation_engine.core.ab_testing import ABTestingEngine
from app.platform_verification.evaluation_engine.core.scoring_engine import ScoringEngine


class MetricsAPI:
    """In-process API endpoints for metric registration, calculation, and comparison."""

    def __init__(
        self,
        registry: MetricRegistry,
        ab_engine: ABTestingEngine,
        scoring_engine: ScoringEngine,
    ) -> None:
        self.registry = registry
        self.ab_engine = ab_engine
        self.scoring_engine = scoring_engine

    def post_metric(self, definition: MetricDefinition) -> Dict[str, Any]:
        """POST /metrics"""
        self.registry.register(definition)
        return {"status": "CREATED", "metric_id": definition.id}

    def get_metric(self, metric_id: str) -> Optional[Dict[str, Any]]:
        """GET /metrics/{id}"""
        try:
            m = self.registry.get(metric_id)
            return {
                "id": m.id,
                "name": m.name,
                "category": m.category.value,
                "formula": m.formula,
                "threshold": m.threshold,
                "weight": m.weight,
            }
        except KeyError:
            return None

    def post_compare(
        self, variant_a: str, values_a: List[float], variant_b: str, values_b: List[float], metric: str
    ) -> Dict[str, Any]:
        """POST /metrics/compare"""
        res = self.ab_engine.compare_variants(variant_a, values_a, variant_b, values_b, metric)
        return {
            "variant_a": res.variant_a,
            "variant_b": res.variant_b,
            "metric": res.metric_name,
            "delta_abs": res.delta_absolute,
            "delta_pct": res.delta_percentage,
            "p_value": res.p_value,
            "winner": res.winner,
            "analysis": res.analysis,
        }
