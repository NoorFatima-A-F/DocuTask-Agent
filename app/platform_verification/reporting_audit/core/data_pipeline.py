"""
Reporting Data Pipeline extracting, normalizing, and aggregating metrics and evidence.
"""
from __future__ import annotations
from typing import Dict, List
from app.platform_verification.reporting_audit.domain.interfaces import IReportingDataPipeline
from app.platform_verification.reporting_audit.domain.models import (
    QualityTrend,
    VerificationSummary,
)


class EnterpriseReportingDataPipeline(IReportingDataPipeline):
    """Stores and normalizes verification run history for trend and regression analysis."""

    def __init__(self):
        self._summaries: List[VerificationSummary] = []
        self._trends: Dict[str, List[QualityTrend]] = {}

    def ingest_verification_run(self, summary: VerificationSummary) -> None:
        self._summaries.insert(0, summary)

        # Ingest standard metrics into trend series
        self._record_trend_point(
            metric_name="extraction_accuracy",
            timestamp=summary.timestamp,
            value=summary.overall_score / 100.0,
            baseline=0.92,
        )
        self._record_trend_point(
            metric_name="hallucination_rate",
            timestamp=summary.timestamp,
            value=summary.hallucination_rate,
            baseline=0.02,
        )
        self._record_trend_point(
            metric_name="p95_latency_ms",
            timestamp=summary.timestamp,
            value=summary.p95_latency_ms,
            baseline=400.0,
        )

    def _record_trend_point(self, metric_name: str, timestamp: str, value: float, baseline: float) -> None:
        if metric_name not in self._trends:
            self._trends[metric_name] = []

        dev = round(((value - baseline) / baseline) * 100.0, 2)
        # For latency/hallucination, higher value is regression; for accuracy, lower is regression
        is_regression = (value > baseline * 1.1) if "latency" in metric_name or "hallucination" in metric_name else (value < baseline * 0.9)

        self._trends[metric_name].append(
            QualityTrend(
                metric_name=metric_name,
                timestamp=timestamp,
                value=value,
                baseline=baseline,
                deviation_pct=dev,
                is_regression=is_regression,
            )
        )

    def get_quality_trends(self, metric_name: str, limit: int = 20) -> List[QualityTrend]:
        return self._trends.get(metric_name, [])[-limit:]

    def list_recent_summaries(self, limit: int = 10) -> List[VerificationSummary]:
        return self._summaries[:limit]
