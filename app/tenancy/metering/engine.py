"""Usage Metering Platform & Cost Aggregation Engine (ESP-MOOS).

Tracks granular operational telemetry across:
- AI Tokens (Prompt, Completion, Embeddings)
- Model Invocations
- Workflow Executions
- Agent Tasks
- Connector Calls
- Document / Knowledge Storage (MB/GB)
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional
from app.tenancy.core.models import MeteringEvent


class UsageMeteringPlatform:
    """Collects and aggregates usage metering events for billing and analytics."""

    # Cost per unit rates (USD)
    RATES: Dict[str, float] = {
        "ai.tokens.prompt_1k": 0.00015,
        "ai.tokens.completion_1k": 0.00060,
        "ai.embeddings_1k": 0.00005,
        "workflow.execution": 0.00100,
        "agent.task": 0.00200,
        "connector.call": 0.00050,
        "storage.gb_month": 0.02000,
    }

    def __init__(self):
        self._events: List[MeteringEvent] = []

    def record_usage(
        self,
        organization_id: str,
        workspace_id: str,
        resource_type: str,
        quantity: float,
        unit: str,
        metadata: Optional[Dict[str, any]] = None,
    ) -> MeteringEvent:
        """Record a single granular usage event."""
        unit_rate = self.RATES.get(resource_type, 0.0)
        cost = quantity * unit_rate

        event = MeteringEvent(
            event_id=f"meter_{uuid.uuid4().hex[:12]}",
            organization_id=organization_id,
            workspace_id=workspace_id,
            resource_type=resource_type,
            quantity=quantity,
            unit=unit,
            cost_usd=cost,
            metadata=metadata or {},
        )
        self._events.append(event)
        return event

    def get_total_spend(self, organization_id: str) -> float:
        """Calculate total USD spend recorded for an organization."""
        return sum(e.cost_usd for e in self._events if e.organization_id == organization_id)

    def get_usage_summary(self, organization_id: str) -> Dict[str, Dict[str, float]]:
        """Aggregate total usage quantities and costs grouped by resource type."""
        summary: Dict[str, Dict[str, float]] = {}
        for e in self._events:
            if e.organization_id == organization_id:
                if e.resource_type not in summary:
                    summary[e.resource_type] = {"total_quantity": 0.0, "total_cost_usd": 0.0}
                summary[e.resource_type]["total_quantity"] += e.quantity
                summary[e.resource_type]["total_cost_usd"] += e.cost_usd
        return summary
