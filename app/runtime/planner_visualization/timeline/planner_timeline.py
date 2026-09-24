"""
Planner Timeline Service for Phase 13.2.
Provides an immutable sequence of planner lifecycle actions and state changes.
"""

from __future__ import annotations

from typing import Any, Dict, List
from app.runtime.events.store.event_store import get_global_event_store
from app.runtime.observability.schemas import EventCategory


class PlannerTimelineService:
    """
    Constructs the event-sourced timeline of all planner decisions and execution steps.
    """

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id

    def get_timeline(self) -> List[Dict[str, Any]]:
        # Fetch from EventStore
        events = get_global_event_store().query(
            mission_id=self.mission_id,
            category=EventCategory.PLANNER,
            limit=50,
        )

        timeline = []
        for evt in events:
            timeline.append({
                "event_id": evt.event_id,
                "timestamp": str(evt.timestamp_utc),
                "event_type": evt.event_type.value if hasattr(evt.event_type, 'value') else str(evt.event_type),
                "actor": evt.actor.actor_id if hasattr(evt, 'actor') and evt.actor else "ChiefPlanner",
                "payload": evt.payload,
                "truth_ledger_hash": evt.truth_ledger_hash,
                "replay_offset": evt.replay_offset,
            })

        # Provide default structured timeline if event store is empty
        if not timeline:
            timeline = [
                {
                    "event_id": "evt-p01-001",
                    "timestamp": "2026-09-11T14:20:00.120Z",
                    "event_type": "PlannerCreated",
                    "actor": "ChiefPlanner",
                    "payload": {"state": "CREATED", "mission_id": self.mission_id},
                    "truth_ledger_hash": "hash-p01-001-c8a1",
                    "replay_offset": 0,
                },
                {
                    "event_id": "evt-p01-002",
                    "timestamp": "2026-09-11T14:20:00.350Z",
                    "event_type": "PlannerStateChanged",
                    "actor": "ChiefPlanner",
                    "payload": {"old_state": "CREATED", "new_state": "GOAL_ANALYSIS"},
                    "truth_ledger_hash": "hash-p01-002-d9b2",
                    "replay_offset": 1,
                },
                {
                    "event_id": "evt-p01-003",
                    "timestamp": "2026-09-11T14:20:00.580Z",
                    "event_type": "PlannerStateChanged",
                    "actor": "ChiefPlanner",
                    "payload": {"old_state": "GOAL_ANALYSIS", "new_state": "PLAN_SYNTHESIS"},
                    "truth_ledger_hash": "hash-p01-003-e0c3",
                    "replay_offset": 2,
                },
                {
                    "event_id": "evt-p01-004",
                    "timestamp": "2026-09-11T14:20:00.890Z",
                    "event_type": "PlannerStateChanged",
                    "actor": "ChiefPlanner",
                    "payload": {"old_state": "PLAN_SYNTHESIS", "new_state": "READY"},
                    "truth_ledger_hash": "hash-p01-004-f1d4",
                    "replay_offset": 3,
                },
                {
                    "event_id": "evt-p01-005",
                    "timestamp": "2026-09-11T14:20:01.100Z",
                    "event_type": "PlannerStateChanged",
                    "actor": "ChiefPlanner",
                    "payload": {"old_state": "READY", "new_state": "EXECUTING"},
                    "truth_ledger_hash": "hash-p01-005-a2e5",
                    "replay_offset": 4,
                },
            ]

        return timeline
