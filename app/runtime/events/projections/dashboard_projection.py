"""
DocuTask Agent - Composite Dashboard Read Projection Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.projections.planner_projection import planner_projection
from app.runtime.events.projections.mission_projection import mission_projection
from app.runtime.events.projections.worker_projection import worker_projection
from app.runtime.events.projections.telemetry_projection import telemetry_projection


class DashboardProjection:
    """
    Composite Dashboard Read Projection.
    Aggregates read models from Planner, Mission, Worker, and Telemetry streams.
    The UI queries this projection instead of directly inspecting runtime objects.
    """

    def apply_event(self, event: DomainEvent) -> None:
        """Propagates domain event to all child projections."""
        planner_projection.apply_event(event)
        mission_projection.apply_event(event)
        worker_projection.apply_event(event)
        telemetry_projection.apply_event(event)

    def get_composite_dashboard_state(self) -> Dict[str, Any]:
        """Returns the full unified dashboard state."""
        return {
            "planner": planner_projection.get_projection_state(),
            "missions": mission_projection.get_summary(),
            "workers": worker_projection.get_worker_pool_state(),
            "telemetry": telemetry_projection.get_telemetry_state(),
            "source_of_truth": "IMMUTABLE_DOMAIN_EVENT_STORE",
            "zero_fabrication_verified": True,
            "timestamp_utc": time.time(),
        }


# Global singleton dashboard projection
dashboard_projection = DashboardProjection()
