"""
Persistent Metric Store for definitions, execution results, and time-series trends.
"""
from __future__ import annotations
import uuid
from typing import Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricResult,
    MetricStoreRecord,
    TrendPoint,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IMetricStore


class MetricStore(IMetricStore):
    """In-memory and repository store for metrics history and trend tracking."""

    def __init__(self) -> None:
        self._records: List[MetricStoreRecord] = []
        self._by_metric: Dict[str, List[MetricStoreRecord]] = {}

    def save_result(self, execution_id: str, result: MetricResult) -> MetricStoreRecord:
        record = MetricStoreRecord(
            record_id=f"rec_{uuid.uuid4().hex[:10]}",
            metric_id=result.metric_id,
            execution_id=execution_id,
            value=result.raw_value,
            normalized_score=result.normalized_score,
            unit=result.unit,
            metadata=result.metadata,
        )
        self._records.append(record)
        self._by_metric.setdefault(result.metric_id, []).append(record)
        return record

    def get_history(self, metric_id: str) -> List[MetricStoreRecord]:
        return list(self._by_metric.get(metric_id, []))

    def get_trend_points(self, metric_id: str) -> List[TrendPoint]:
        records = self.get_history(metric_id)
        return [
            TrendPoint(
                timestamp=r.timestamp,
                version=r.metadata.get("version", "v1.0.0"),
                value=r.value,
            )
            for r in records
        ]
