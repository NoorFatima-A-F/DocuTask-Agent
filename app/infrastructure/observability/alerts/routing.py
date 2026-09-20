"""
Multi-Dimensional Alert Routing Engine.

Routes alerts based on team ownership, environment, severity, region,
tenant boundaries, and component tags.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.infrastructure.observability.alerts.models import AlertInstance, AlertSeverity

logger = logging.getLogger("infrastructure.observability.alerts.routing")


class AlertRouteRule(BaseModel):
    """Specification mapping alert criteria to notification channels."""
    route_id: str
    team: Optional[str] = None
    min_severity: Optional[AlertSeverity] = None
    regions: List[str] = Field(default_factory=list)
    tenants: List[str] = Field(default_factory=list)
    channels: List[str] = Field(default_factory=list)  # e.g. ["pagerduty", "slack-sre", "webhook"]


class AlertRouter:
    """
    Evaluates alert attributes and returns destination notification targets.
    """

    def __init__(self) -> None:
        self._routes: List[AlertRouteRule] = []

    def add_route(self, route: AlertRouteRule) -> None:
        self._routes.append(route)

    def route_alert(self, alert: AlertInstance) -> List[str]:
        """Determine all destination channels for an incoming alert instance."""
        destination_channels: Set[str] = set()

        severity_order = [
            AlertSeverity.INFO,
            AlertSeverity.MINOR,
            AlertSeverity.MAJOR,
            AlertSeverity.CRITICAL,
            AlertSeverity.EMERGENCY,
        ]
        alert_sev_idx = severity_order.index(alert.severity)

        for route in self._routes:
            if route.team and route.team != alert.team:
                continue

            if route.min_severity:
                min_idx = severity_order.index(route.min_severity)
                if alert_sev_idx < min_idx:
                    continue

            if route.regions and alert.region not in route.regions:
                continue

            if route.tenants and alert.tenant_id not in route.tenants:
                continue

            destination_channels.update(route.channels)

        if not destination_channels:
            # Default fallback channel
            destination_channels.add("default-ops-webhook")

        return sorted(list(destination_channels))
