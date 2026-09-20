"""
Cross-Layer Health Analysis.

Correlates telemetry across infrastructure nodes, workflow execution queues,
database state, and AI runtime providers.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.observability.diagnostics.health_analysis")


class LayerHealthStatus(BaseModel):
    """Health score and anomaly status for a single operational layer."""
    layer_name: str  # INFRASTRUCTURE, WORKFLOWS, AI_RUNTIME, DATABASE, NETWORK
    score: float = Field(default=100.0, ge=0.0, le=100.0)
    is_healthy: bool = True
    active_anomalies: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)


class PlatformHealthReport(BaseModel):
    """Holistic cross-layer operational health assessment."""
    overall_health_score: float
    layers: Dict[str, LayerHealthStatus]
    summary_message: str


class CrossLayerHealthAnalyzer:
    """
    Evaluates multi-layer platform telemetry to produce cross-correlated health assessments.
    """

    def analyze(
        self,
        cpu_usage_pct: float = 20.0,
        memory_usage_pct: float = 35.0,
        queue_depth: int = 0,
        ai_error_rate_pct: float = 0.0,
        db_latency_ms: float = 5.0,
    ) -> PlatformHealthReport:
        """Evaluate platform layers and compute composite operational health."""
        layers: Dict[str, LayerHealthStatus] = {}

        # 1. Infrastructure Layer
        infra_anomalies = []
        infra_score = 100.0
        if cpu_usage_pct > 85.0:
            infra_score -= 30.0
            infra_anomalies.append(f"High CPU utilization: {cpu_usage_pct}%")
        if memory_usage_pct > 90.0:
            infra_score -= 40.0
            infra_anomalies.append(f"Critical memory utilization: {memory_usage_pct}%")

        layers["INFRASTRUCTURE"] = LayerHealthStatus(
            layer_name="INFRASTRUCTURE",
            score=max(0.0, infra_score),
            is_healthy=(len(infra_anomalies) == 0),
            active_anomalies=infra_anomalies,
            metrics={"cpu_pct": cpu_usage_pct, "memory_pct": memory_usage_pct},
        )

        # 2. Workflow & Queue Layer
        wf_anomalies = []
        wf_score = 100.0
        if queue_depth > 1000:
            wf_score -= 35.0
            wf_anomalies.append(f"Elevated queue backlog: {queue_depth} messages")

        layers["WORKFLOWS"] = LayerHealthStatus(
            layer_name="WORKFLOWS",
            score=max(0.0, wf_score),
            is_healthy=(len(wf_anomalies) == 0),
            active_anomalies=wf_anomalies,
            metrics={"queue_depth": queue_depth},
        )

        # 3. AI Runtime Layer
        ai_anomalies = []
        ai_score = 100.0
        if ai_error_rate_pct > 5.0:
            ai_score -= 50.0
            ai_anomalies.append(f"AI Provider error rate: {ai_error_rate_pct}%")

        layers["AI_RUNTIME"] = LayerHealthStatus(
            layer_name="AI_RUNTIME",
            score=max(0.0, ai_score),
            is_healthy=(len(ai_anomalies) == 0),
            active_anomalies=ai_anomalies,
            metrics={"error_rate_pct": ai_error_rate_pct},
        )

        # 4. Database Layer
        db_anomalies = []
        db_score = 100.0
        if db_latency_ms > 100.0:
            db_score -= 40.0
            db_anomalies.append(f"High DB query latency: {db_latency_ms}ms")

        layers["DATABASE"] = LayerHealthStatus(
            layer_name="DATABASE",
            score=max(0.0, db_score),
            is_healthy=(len(db_anomalies) == 0),
            active_anomalies=db_anomalies,
            metrics={"db_latency_ms": db_latency_ms},
        )

        avg_score = sum(l.score for l in layers.values()) / len(layers)
        all_anomalies = [a for l in layers.values() for a in l.active_anomalies]

        summary = "All platform layers operating optimally." if not all_anomalies else f"{len(all_anomalies)} operational anomalies detected."

        return PlatformHealthReport(
            overall_health_score=round(avg_score, 2),
            layers=layers,
            summary_message=summary,
        )
