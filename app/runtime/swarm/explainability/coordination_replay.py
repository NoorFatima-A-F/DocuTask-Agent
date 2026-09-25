"""
AMCN-SIP Phase 13.8 - Coordination Replay & Swarm Explainability
Deterministic step-by-step replay of multi-agent interactions, cryptographic frame proofs, and timeline reconstruction.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional


@dataclass
class CoordinationFrame:
    frame_index: int
    timestamp: str
    event_type: str
    initiator_agent_id: str
    target_agent_id: Optional[str]
    action_payload: Dict[str, Any]
    active_coalition_ids: List[str]
    system_state_hash: str
    rationale: str = ""


class CoordinationReplayEngine:
    """
    Records and deterministically reconstructs multi-agent coordination traces.
    """

    def __init__(self):
        self._frames: List[CoordinationFrame] = []
        self._seed_default_frames()

    def record_frame(
        self,
        event_type: str,
        initiator_agent_id: str,
        target_agent_id: Optional[str],
        action_payload: Dict[str, Any],
        active_coalition_ids: List[str],
        rationale: str = "",
    ) -> CoordinationFrame:
        idx = len(self._frames)
        ts = datetime.now(timezone.utc).isoformat()
        state_repr = json.dumps(
            {
                "idx": idx,
                "ts": ts,
                "event": event_type,
                "initiator": initiator_agent_id,
                "target": target_agent_id,
                "payload": action_payload,
            },
            sort_keys=True,
        )
        state_hash = hashlib.sha256(state_repr.encode()).hexdigest()

        frame = CoordinationFrame(
            frame_index=idx,
            timestamp=ts,
            event_type=event_type,
            initiator_agent_id=initiator_agent_id,
            target_agent_id=target_agent_id,
            action_payload=action_payload,
            active_coalition_ids=active_coalition_ids,
            system_state_hash=state_hash,
            rationale=rationale,
        )
        self._frames.append(frame)
        return frame

    def get_timeline(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [f.__dict__ for f in self._frames[-limit:]]

    def get_frame(self, frame_index: int) -> Optional[CoordinationFrame]:
        if 0 <= frame_index < len(self._frames):
            return self._frames[frame_index]
        return None

    def reconstruct_trace(self, start_idx: int = 0, end_idx: Optional[int] = None) -> Dict[str, Any]:
        end = end_idx if end_idx is not None else len(self._frames)
        selected_frames = self._frames[start_idx:end]
        combined_hash = hashlib.sha256("".join(f.system_state_hash for f in selected_frames).encode()).hexdigest()
        return {
            "total_frames": len(selected_frames),
            "start_index": start_idx,
            "end_index": end,
            "integrity_merkle_root": combined_hash,
            "frames": [f.__dict__ for f in selected_frames],
        }

    def _seed_default_frames(self):
        events = [
            ("AGENT_DISCOVERY", "agent-exec-01", "agent-plan-01", {"query": "expert_in_dag_scheduling"}, ["coalition-alpha"], "Executive discovered Lead Planner for Mission 9482."),
            ("TASK_AUCTION_PUBLISHED", "agent-plan-01", None, {"task_id": "task_ocr_batch_01", "budget": 120.0}, ["coalition-alpha"], "Published batch OCR task to auction marketplace."),
            ("BID_SUBMITTED", "agent-spec-ocr", "agent-plan-01", {"bid_cost": 85.0, "latency_ms": 140.0}, ["coalition-alpha"], "OCR Specialist submitted competitive bid."),
            ("BID_ACCEPTED", "agent-plan-01", "agent-spec-ocr", {"auction_id": "auc_001", "status": "AWARDED"}, ["coalition-alpha"], "Planner awarded task to OCR Specialist."),
            ("CONSENSUS_INITIATED", "agent-coord-01", None, {"proposal": "VERIFY_SCHEMA_INVARIANT"}, ["coalition-alpha"], "Consensus initiated for document schema verification."),
            ("VOTE_CAST", "agent-val-sec", "agent-coord-01", {"vote": "APPROVE", "weight": 1.0}, ["coalition-alpha"], "Security Validator cast affirmative vote."),
            ("CONSENSUS_DECIDED", "agent-coord-01", None, {"verdict": "APPROVED", "tally": 1.0}, ["coalition-alpha"], "Consensus reached with 100% affirmative quorum."),
        ]
        for ev, init, tgt, payload, coals, rat in events:
            self.record_frame(ev, init, tgt, payload, coals, rat)
