"""
Metric Versioning and Compatibility Engine for DocuTask Agent.
Manages semantic versions of metric definitions and backward compatibility transformations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MetricVersionChange:
    from_version: str
    to_version: str
    change_type: str  # BREAKING, ENHANCEMENT, BUGFIX
    description: str
    formula_delta: Optional[str] = None


class MetricVersionManager:
    """
    Manages metric definition lifecycle and semantic versioning.
    """

    CURRENT_METRIC_SCHEMA_VERSION: str = "2.0"

    VERSION_HISTORY: Dict[str, List[MetricVersionChange]] = {
        "worker_utilization": [
            MetricVersionChange(
                from_version="1.0",
                to_version="2.0",
                change_type="BREAKING",
                description="Upgraded from static active ratio to continuous integral active worker duration over allocated window.",
                formula_delta="Replaced count ratio with exact timestamp integral sum(active_ms)/sum(allocated_ms).",
            )
        ],
        "bayesian_confidence": [
            MetricVersionChange(
                from_version="1.0",
                to_version="2.0",
                change_type="BREAKING",
                description="Replaced naive arithmetic weighted sum with Calibrated Bayesian Log-Odds Evidence Fusion with sample-size attenuation.",
                formula_delta="logit(P(theta|E)) = logit(P(theta)) + sum_i [ w_i * logit(s_i) ].",
            )
        ],
    }

    @classmethod
    def get_version_history(cls, metric_id: str) -> List[MetricVersionChange]:
        return cls.VERSION_HISTORY.get(metric_id, [])

    @classmethod
    def is_version_supported(cls, version: str) -> bool:
        return version in ("1.0", "2.0", "2.1")
