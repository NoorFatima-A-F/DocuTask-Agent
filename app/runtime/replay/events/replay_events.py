"""
Phase 13.4 Replay Domain Events (AESMR-EAIP).
Typed immutable events capturing replay session lifecycles, checkpoints, diffs, and verification results.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


def _gen_id(prefix: str = "rpl_evt") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseReplayEvent(BaseModel):
    event_id: str = Field(default_factory=_gen_id)
    replay_session_id: str
    mission_id: str
    event_type: str
    timestamp: str = Field(default_factory=_now_iso)
    payload: Dict[str, Any] = Field(default_factory=dict)
    provenance_hash: Optional[str] = None


class ReplayStarted(BaseReplayEvent):
    event_type: str = "replay.session.started"
    initial_cursor: int = 0
    total_events: int = 0
    playback_speed: float = 1.0


class ReplayPaused(BaseReplayEvent):
    event_type: str = "replay.session.paused"
    paused_at_cursor: int = 0
    reconstructed_time: Optional[str] = None


class ReplayResumed(BaseReplayEvent):
    event_type: str = "replay.session.resumed"
    resumed_at_cursor: int = 0


class ReplayStopped(BaseReplayEvent):
    event_type: str = "replay.session.stopped"
    final_cursor: int = 0


class ReplayCheckpointCreated(BaseReplayEvent):
    event_type: str = "replay.checkpoint.created"
    checkpoint_id: str
    cursor: int
    state_hash: str
    snapshot_size_bytes: int


class ReplayCheckpointRestored(BaseReplayEvent):
    event_type: str = "replay.checkpoint.restored"
    checkpoint_id: str
    restored_cursor: int


class ReplayFrameRendered(BaseReplayEvent):
    event_type: str = "replay.frame.rendered"
    frame_index: int
    source_event_id: str
    subsystem: str
    resulting_confidence: float = 0.0


class ReplayVerified(BaseReplayEvent):
    event_type: str = "replay.integrity.verified"
    root_merkle_hash: str
    event_count_verified: int
    is_authentic: bool = True


class ReplayVerificationFailed(BaseReplayEvent):
    event_type: str = "replay.integrity.failed"
    corrupted_event_id: str
    expected_hash: str
    observed_hash: str
    failure_reason: str


class ReplaySnapshotLoaded(BaseReplayEvent):
    event_type: str = "replay.snapshot.loaded"
    snapshot_id: str
    event_cursor: int


class ReplaySnapshotSaved(BaseReplayEvent):
    event_type: str = "replay.snapshot.saved"
    snapshot_id: str
    state_hash: str


class ReplayDiffGenerated(BaseReplayEvent):
    event_type: str = "replay.diff.generated"
    reference_mission_id: str
    comparison_mission_id: str
    similarity_score: float
    total_differences: int


class ReplayAuditGenerated(BaseReplayEvent):
    event_type: str = "replay.audit.generated"
    audit_bundle_id: str
    signer_id: str
    compliance_framework: str = "ISO/IEC 42001"


class ReplayCertificateIssued(BaseReplayEvent):
    event_type: str = "replay.certificate.issued"
    certificate_id: str
    digital_signature: str
    truth_ledger_root: str


class ReplayTimeTravelExecuted(BaseReplayEvent):
    event_type: str = "replay.timetravel.executed"
    source_cursor: int
    target_cursor: int
    target_event_id: str


class ReplayRootCauseCompleted(BaseReplayEvent):
    event_type: str = "replay.rootcause.completed"
    incident_event_id: str
    root_cause_category: str
    confidence: float
    causal_event_chain: List[str] = Field(default_factory=list)


class ReplayEvidenceVerified(BaseReplayEvent):
    event_type: str = "replay.evidence.verified"
    evidence_id: str
    truth_hash: str
    is_valid: bool = True
