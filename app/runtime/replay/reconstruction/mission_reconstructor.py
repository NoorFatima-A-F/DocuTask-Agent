"""
Mission Reconstructor for Phase 13.4 (AESMR-EAIP).
Deterministically rebuilds the full mission lifecycle exclusively from ordered domain events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import hashlib
import json


class ReconstructedMissionState(BaseModel):
    mission_id: str
    status: str = "INITIALIZED"
    current_cursor: int = 0
    total_events_processed: int = 0
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_ms: float = 0.0
    planner_state: Dict[str, Any] = Field(default_factory=dict)
    scheduler_state: Dict[str, Any] = Field(default_factory=dict)
    worker_state: Dict[str, Any] = Field(default_factory=dict)
    confidence_state: Dict[str, Any] = Field(default_factory=dict)
    memory_state: Dict[str, Any] = Field(default_factory=dict)
    telemetry_state: Dict[str, Any] = Field(default_factory=dict)
    truth_state: Dict[str, Any] = Field(default_factory=dict)
    evidence_count: int = 0
    state_merkle_hash: str = ""


class MissionReconstructor:
    """
    Reconstructs complete, deterministic runtime state up to any given event index.
    Never uses UI cache or mock data.
    """

    @classmethod
    def reconstruct_up_to_cursor(
        cls,
        mission_id: str,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedMissionState:
        if target_cursor is None or target_cursor >= len(events):
            target_cursor = len(events) - 1

        state = ReconstructedMissionState(
            mission_id=mission_id,
            current_cursor=max(0, target_cursor),
            total_events_processed=min(len(events), target_cursor + 1),
        )

        if not events:
            return state

        hasher = hashlib.sha256()

        for idx, ev in enumerate(events[: target_cursor + 1]):
            payload = ev.get("payload", {})
            evt_type = ev.get("event_type") or ev.get("type", "")
            ts = ev.get("timestamp", "")

            if idx == 0:
                state.start_time = ts
            state.end_time = ts

            # Feed event hash
            ev_str = f"{idx}:{ev.get('event_id', '')}:{evt_type}:{json.dumps(payload, sort_keys=True)}"
            hasher.update(ev_str.encode("utf-8"))

            # Update mission level status
            if "mission.started" in evt_type or "mission.created" in evt_type:
                state.status = "RUNNING"
            elif "mission.completed" in evt_type:
                state.status = "COMPLETED"
            elif "mission.failed" in evt_type:
                state.status = "FAILED"
            elif "mission.paused" in evt_type:
                state.status = "PAUSED"

            # Route to subsystem updates
            if "planner" in evt_type or "dag" in evt_type:
                state.planner_state.update(payload)
                state.planner_state["last_event_type"] = evt_type
            elif "worker" in evt_type:
                worker_id = payload.get("worker_id", "default_worker")
                workers = state.worker_state.setdefault("workers", {})
                workers[worker_id] = payload
            elif "schedule" in evt_type or "queue" in evt_type:
                state.scheduler_state.update(payload)
            elif "confidence" in evt_type or "score" in evt_type:
                state.confidence_state.update(payload)
            elif "evidence" in evt_type:
                state.evidence_count += 1
            elif "memory" in evt_type:
                state.memory_state.update(payload)
            elif "telemetry" in evt_type or "cost" in evt_type:
                state.telemetry_state.update(payload)
            elif "truth" in evt_type or "invariant" in evt_type:
                state.truth_state.update(payload)

        state.state_merkle_hash = f"sha256:{hasher.hexdigest()}"
        return state
