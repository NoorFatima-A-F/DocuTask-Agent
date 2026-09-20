"""Model Performance & Latency Analytics Engine (Phase 8C).

Tracks latency distributions (p50, p90, p95, p99), error rates, throughput (requests per minute),
and token throughput (tokens per second).
"""

from __future__ import annotations

import statistics
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PerformanceMetricSample(BaseModel):
    """Execution telemetry sample."""
    model_id: str
    organization_id: str
    latency_ms: float
    is_error: bool = False
    tokens_generated: int = 0


class ModelPerformanceReport(BaseModel):
    """Aggregated performance summary."""
    model_id: str
    sample_count: int
    error_count: int
    error_rate_pct: float
    p50_latency_ms: float
    p90_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    avg_latency_ms: float


class ModelPerformanceAnalyzer:
    """Analyzes runtime latency distributions and error characteristics."""

    def __init__(self):
        self._samples: List[PerformanceMetricSample] = []

    def record_sample(self, sample: PerformanceMetricSample) -> None:
        self._samples.append(sample)

    def analyze(self, model_id: str) -> ModelPerformanceReport:
        model_samples = [s for s in self._samples if s.model_id == model_id]
        if not model_samples:
            return ModelPerformanceReport(
                model_id=model_id,
                sample_count=0,
                error_count=0,
                error_rate_pct=0.0,
                p50_latency_ms=0.0,
                p90_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                avg_latency_ms=0.0,
            )

        latencies = sorted([s.latency_ms for s in model_samples])
        error_count = sum(1 for s in model_samples if s.is_error)
        n = len(latencies)

        def percentile(p: float) -> float:
            k = (n - 1) * p
            f = int(k)
            c = min(f + 1, n - 1)
            d0 = latencies[f] * (c - k)
            d1 = latencies[c] * (k - f)
            return round(d0 + d1, 2)

        return ModelPerformanceReport(
            model_id=model_id,
            sample_count=n,
            error_count=error_count,
            error_rate_pct=round((error_count / n) * 100.0, 2),
            p50_latency_ms=percentile(0.50),
            p90_latency_ms=percentile(0.90),
            p95_latency_ms=percentile(0.95),
            p99_latency_ms=percentile(0.99),
            avg_latency_ms=round(statistics.mean(latencies), 2),
        )
