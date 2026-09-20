"""
Multi-layer metrics collector for application, AI, database, and infrastructure metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Any


@dataclass
class MetricSample:
    name: str
    category: str  # app, ai, db, infra
    value: float
    unit: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MetricCollector:
    """Collects, aggregates, and exports time-series metrics across layers."""

    def __init__(self):
        self._samples: List[MetricSample] = []

    def record(self, name: str, category: str, value: float, unit: str):
        self._samples.append(MetricSample(name, category, value, unit))

    def get_by_category(self, category: str) -> List[MetricSample]:
        return [s for s in self._samples if s.category == category]

    def get_summary(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {}
        for sample in self._samples:
            if sample.category not in summary:
                summary[sample.category] = {}
            if sample.name not in summary[sample.category]:
                summary[sample.category][sample.name] = {
                    "count": 0,
                    "sum": 0.0,
                    "min": float("inf"),
                    "max": float("-inf"),
                    "unit": sample.unit,
                }
            entry = summary[sample.category][sample.name]
            entry["count"] += 1
            entry["sum"] += sample.value
            entry["min"] = min(entry["min"], sample.value)
            entry["max"] = max(entry["max"], sample.value)

        for cat in summary:
            for name in summary[cat]:
                entry = summary[cat][name]
                entry["avg"] = round(entry["sum"] / entry["count"], 2)
                entry["min"] = round(entry["min"], 2)
                entry["max"] = round(entry["max"], 2)
                entry["sum"] = round(entry["sum"], 2)

        return summary
