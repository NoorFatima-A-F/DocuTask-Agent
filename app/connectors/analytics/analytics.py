"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Analytics.
Provides business and technical intelligence on connector usage, costs, performance, and capability popularity.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.observability.metrics import ConnectorObservability

logger = logging.getLogger(__name__)


class FleetAnalyticsReport(BaseModel):
    """Platform-wide analytical snapshot of all connector activity."""
    total_calls: int = 0
    total_successful_calls: int = 0
    total_failed_calls: int = 0
    overall_success_rate: float = 1.0
    total_spend_usd: float = 0.0
    active_connectors_count: int = 0
    top_connectors_by_volume: List[Dict[str, Any]] = Field(default_factory=list)
    top_connectors_by_cost: List[Dict[str, Any]] = Field(default_factory=list)
    failure_hotspots: List[Dict[str, Any]] = Field(default_factory=list)


class ConnectorAnalytics:
    """
    Analyzes connector usage patterns, aggregates multi-tenant cost attribution,
    and identifies integration reliability risks.
    """

    def __init__(self, observability: Optional[ConnectorObservability] = None):
        self._observability = observability or ConnectorObservability()
        self._capability_usage: Dict[str, int] = {}

    def track_capability_usage(self, capability_name: str) -> None:
        """Records an invocation against an abstract capability name."""
        self._capability_usage[capability_name] = self._capability_usage.get(capability_name, 0) + 1

    def generate_fleet_report(self) -> FleetAnalyticsReport:
        """Computes platform-wide analytics report from observed telemetry."""
        summaries = self._observability.get_all_summaries()

        total_calls = sum(s.total_calls for s in summaries.values())
        success_calls = sum(s.successful_calls for s in summaries.values())
        failed_calls = sum(s.failed_calls for s in summaries.values())
        total_spend = sum(s.total_cost_usd for s in summaries.values())

        success_rate = (success_calls / total_calls) if total_calls > 0 else 1.0

        # Sort by volume
        by_volume = sorted(
            [{"connector_id": s.connector_id, "calls": s.total_calls} for s in summaries.values()],
            key=lambda x: x["calls"],
            reverse=True,
        )

        # Sort by cost
        by_cost = sorted(
            [{"connector_id": s.connector_id, "cost_usd": s.total_cost_usd} for s in summaries.values()],
            key=lambda x: x["cost_usd"],
            reverse=True,
        )

        # Hotspots (connectors with failed calls)
        hotspots = sorted(
            [{"connector_id": s.connector_id, "failed_calls": s.failed_calls, "errors": s.error_counts} for s in summaries.values() if s.failed_calls > 0],
            key=lambda x: x["failed_calls"],
            reverse=True,
        )

        return FleetAnalyticsReport(
            total_calls=total_calls,
            total_successful_calls=success_calls,
            total_failed_calls=failed_calls,
            overall_success_rate=success_rate,
            total_spend_usd=total_spend,
            active_connectors_count=len(summaries),
            top_connectors_by_volume=by_volume[:10],
            top_connectors_by_cost=by_cost[:10],
            failure_hotspots=hotspots[:5],
        )

    def get_popular_capabilities(self) -> List[Dict[str, Any]]:
        """Returns top capabilities sorted by invocation frequency."""
        return sorted(
            [{"capability": cap, "invocations": count} for cap, count in self._capability_usage.items()],
            key=lambda x: x["invocations"],
            reverse=True,
        )
