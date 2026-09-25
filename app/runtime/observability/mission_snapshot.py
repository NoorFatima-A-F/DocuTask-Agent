"""
Mission Snapshot Generator.

Replays immutable event logs to deterministically reconstruct the complete state,
timeline, node lifecycle, token economics, and error counts of any mission.
"""

from __future__ import annotations

import time
from typing import Dict, List
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    EventCategory,
    MissionSnapshotPayload,
    MissionTimelineItem,
)


class MissionSnapshotGenerator:
    """Deterministic state snapshot builder from event logs."""

    @classmethod
    def generate_snapshot(
        cls, mission_id: str, events: List[BaseRuntimeEvent]
    ) -> MissionSnapshotPayload:
        """Processes event log sequentially to construct point-in-time mission snapshot."""
        if not events:
            now = time.time()
            return MissionSnapshotPayload(
                mission_id=mission_id,
                status="UNKNOWN",
                created_at=now,
                updated_at=now,
                total_events=0,
                total_duration_ms=0.0,
                total_tokens_used=0,
                total_cost_usd=0.0,
                active_nodes_count=0,
                completed_nodes_count=0,
                failed_nodes_count=0,
                retries_count=0,
                timeline=[],
                current_metrics={},
            )

        events_sorted = sorted(events, key=lambda e: e.timestamp)
        status = "PENDING"
        created_at = events_sorted[0].timestamp
        updated_at = events_sorted[-1].timestamp
        total_tokens = 0
        total_cost = 0.0
        retries = 0
        nodes_state: Dict[str, str] = {}
        timeline_items: List[MissionTimelineItem] = []

        for evt in events_sorted:
            # 1. Timeline item
            summary = evt.payload.get("summary") or f"{evt.category.value}: {evt.event_type}"
            timeline_items.append(
                MissionTimelineItem(
                    event_id=evt.event_id,
                    timestamp=evt.timestamp,
                    stage=evt.stage,
                    category=evt.category.value,
                    event_type=evt.event_type,
                    status=evt.status,
                    duration_ms=evt.duration_ms,
                    summary=summary,
                    evidence=evt.evidence or {},
                    event_hash=evt.event_hash,
                )
            )

            # 2. Mission status
            if evt.category == EventCategory.MISSION:
                if evt.event_type in ("MISSION_STARTED", "MISSION_CREATED"):
                    status = "RUNNING"
                elif evt.event_type == "MISSION_COMPLETED":
                    status = "COMPLETED"
                elif evt.event_type == "MISSION_FAILED":
                    status = "FAILED"

            # 3. Node state tracking
            if evt.node_id:
                if evt.event_type in ("NODE_SCHEDULED", "NODE_ASSIGNED", "NODE_STARTED"):
                    nodes_state[evt.node_id] = "RUNNING"
                elif evt.event_type == "NODE_COMPLETED" or (evt.category == EventCategory.EXECUTION and evt.status == "SUCCESS"):
                    nodes_state[evt.node_id] = "COMPLETED"
                elif evt.event_type == "NODE_FAILED" or (evt.category == EventCategory.EXECUTION and evt.status == "FAILED"):
                    nodes_state[evt.node_id] = "FAILED"

            # 4. Economics & Failures
            if evt.category == EventCategory.COST:
                total_cost += float(evt.payload.get("cost_usd", 0.0))
                total_tokens += int(evt.payload.get("total_tokens", 0))
            if evt.category == EventCategory.FAILURE or "RETRY" in evt.event_type:
                retries += 1

        active_count = sum(1 for s in nodes_state.values() if s == "RUNNING")
        completed_count = sum(1 for s in nodes_state.values() if s == "COMPLETED")
        failed_count = sum(1 for s in nodes_state.values() if s == "FAILED")
        total_duration = max(0.0, (updated_at - created_at) * 1000.0)

        return MissionSnapshotPayload(
            mission_id=mission_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            total_events=len(events_sorted),
            total_duration_ms=round(total_duration, 2),
            total_tokens_used=total_tokens,
            total_cost_usd=round(total_cost, 5),
            active_nodes_count=active_count,
            completed_nodes_count=completed_count,
            failed_nodes_count=failed_count,
            retries_count=retries,
            timeline=timeline_items,
            current_metrics={
                "duration_ms": total_duration,
                "tokens": float(total_tokens),
                "cost_usd": total_cost,
                "nodes_total": float(len(nodes_state)),
            },
        )
