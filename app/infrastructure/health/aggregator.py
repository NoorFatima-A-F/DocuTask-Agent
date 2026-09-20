"""
Health Aggregator Service.

Consolidates probes, heartbeat telemetry, and composite evaluations across
all registered platform entities into unified system matrices.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.health.evaluator import HealthEvaluator, HealthScore
from app.infrastructure.health.heartbeat import HeartbeatAggregator, HeartbeatStatus
from app.infrastructure.health.probes import ProbeRegistry, ProbeStatus

logger = logging.getLogger("infrastructure.health.aggregator")


class SystemHealthMatrix(BaseModel):
    """Platform-wide aggregated health status."""
    total_components: int
    healthy_count: int
    degraded_count: int
    unhealthy_count: int
    unknown_count: int
    average_health_score: float
    flapping_components: List[str]
    components: Dict[str, HealthScore]


class HealthAggregatorService:
    """
    Unified query service for multi-region and multi-cluster health state.
    """

    def __init__(
        self,
        probe_registry: Optional[ProbeRegistry] = None,
        heartbeat_aggregator: Optional[HeartbeatAggregator] = None,
        health_evaluator: Optional[HealthEvaluator] = None,
    ) -> None:
        self.probe_registry = probe_registry or ProbeRegistry()
        self.heartbeat_aggregator = heartbeat_aggregator or HeartbeatAggregator()
        self.health_evaluator = health_evaluator or HealthEvaluator(self.probe_registry)

    def get_component_health(self, component_id: str) -> HealthScore:
        return self.health_evaluator.evaluate_component(component_id)

    def get_system_health_matrix(self, component_ids: Optional[List[str]] = None) -> SystemHealthMatrix:
        """Calculate system-wide health matrix."""
        if component_ids is None:
            # Collect unique component_ids from probe registry
            component_ids = list({p.component_id for p in self.probe_registry._probes.values()})

        scores: Dict[str, HealthScore] = {}
        healthy = 0
        degraded = 0
        unhealthy = 0
        unknown = 0
        total_score = 0.0
        flapping: List[str] = []

        for cid in component_ids:
            hs = self.health_evaluator.evaluate_component(cid)
            scores[cid] = hs
            total_score += hs.score

            if hs.is_flapping:
                flapping.append(cid)

            if hs.overall_status == ProbeStatus.HEALTHY:
                healthy += 1
            elif hs.overall_status == ProbeStatus.DEGRADED:
                degraded += 1
            elif hs.overall_status == ProbeStatus.UNHEALTHY:
                unhealthy += 1
            else:
                unknown += 1

        avg_score = (total_score / len(component_ids)) if component_ids else 100.0

        return SystemHealthMatrix(
            total_components=len(component_ids),
            healthy_count=healthy,
            degraded_count=degraded,
            unhealthy_count=unhealthy,
            unknown_count=unknown,
            average_health_score=round(avg_score, 2),
            flapping_components=flapping,
            components=scores,
        )
