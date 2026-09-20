"""Data Governance Analytics & Usage Intelligence (Phase 8B)."""

from __future__ import annotations

from typing import Dict, List
from collections import Counter
from app.data_governance.access.tracking import DataAccessTracker, DataActionType


class DataUsageAnalytics:
    """Aggregates telemetry on data access patterns, AI model consumption, and sensitive data exposure."""

    def __init__(self, access_tracker: DataAccessTracker):
        self.access_tracker = access_tracker

    def get_most_accessed_assets(self, organization_id: str, top_n: int = 10) -> List[Dict[str, any]]:
        """Get assets with the highest access volume."""
        events = self.access_tracker.get_organization_access_history(organization_id)
        counts = Counter(e.asset_id for e in events if e.action in (DataActionType.READ, DataActionType.PROCESS))
        return [{"asset_id": asset_id, "access_count": count} for asset_id, count in counts.most_common(top_n)]

    def get_ai_consumption_metrics(self, organization_id: str) -> Dict[str, int]:
        """Get metrics on AI agent and workflow data consumption."""
        events = self.access_tracker.get_organization_access_history(organization_id)
        agent_accesses = sum(1 for e in events if e.agent_id is not None)
        workflow_accesses = sum(1 for e in events if e.workflow_id is not None)
        export_events = sum(1 for e in events if e.action == DataActionType.EXPORT)

        return {
            "total_access_events": len(events),
            "agent_access_events": agent_accesses,
            "workflow_access_events": workflow_accesses,
            "export_events": export_events,
        }
