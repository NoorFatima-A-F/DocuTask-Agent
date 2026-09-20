"""
Replay Forensic Exporter.
Serializes replay history into compliant forensic evidence archives.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json
import hashlib
from datetime import datetime, timezone
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_state_machine import ReconstructedMissionState
from app.runtime.replay.replay_integrity import ReplayIntegrityVerifier


class ForensicReplayPackage(BaseModel):
    package_id: str
    mission_id: str
    exported_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_events: int
    hash_chain_verified: bool
    hash_chain_head: Optional[str]
    final_state: Dict[str, Any]
    events: List[Dict[str, Any]]
    package_signature: str


class ReplayExporter:
    @staticmethod
    def export_mission_package(
        mission_id: str,
        events: List[RuntimeEvent],
        final_state: ReconstructedMissionState,
    ) -> ForensicReplayPackage:
        integrity = ReplayIntegrityVerifier.verify_event_stream(events)
        event_dicts = [e.model_dump() for e in events]
        state_dict = final_state.model_dump()

        raw_content = json.dumps(
            {"mission_id": mission_id, "events": event_dicts, "state": state_dict},
            sort_keys=True,
            default=str,
        )
        sig = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()

        return ForensicReplayPackage(
            package_id=f"pkg_{mission_id}_{len(events)}",
            mission_id=mission_id,
            total_events=len(events),
            hash_chain_verified=integrity.is_valid,
            hash_chain_head=integrity.hash_chain_head,
            final_state=state_dict,
            events=event_dicts,
            package_signature=sig,
        )
