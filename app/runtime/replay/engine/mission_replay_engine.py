"""
Master Mission Replay Engine for Phase 13.4 (AESMR-EAIP).
Coordinates deterministic event reconstruction, playback controls, forensic analysis, and audit certification.
"""

from typing import Dict, Any, List, Optional
from app.runtime.replay.reconstruction.mission_reconstructor import MissionReconstructor, ReconstructedMissionState
from app.runtime.replay.reconstruction.planner_reconstructor import PlannerReconstructor
from app.runtime.replay.reconstruction.scheduler_reconstructor import SchedulerReconstructor
from app.runtime.replay.reconstruction.worker_reconstructor import WorkerReconstructor
from app.runtime.replay.reconstruction.confidence_reconstructor import ConfidenceReconstructor
from app.runtime.replay.reconstruction.telemetry_reconstructor import TelemetryReconstructor
from app.runtime.replay.reconstruction.memory_reconstructor import MemoryReconstructor
from app.runtime.replay.reconstruction.truth_reconstructor import TruthReconstructor
from app.runtime.replay.forensic.forensic_engine import ForensicEngine, ForensicInvestigationReport
from app.runtime.replay.forensic.root_cause_analyzer import RootCauseAnalyzer
from app.runtime.replay.forensic.decision_trace import DecisionTrace
from app.runtime.replay.forensic.timeline_diff import TimelineDiffEngine
from app.runtime.replay.verification.replay_verifier import ReplayVerifier, ReplayVerificationResult
from app.runtime.replay.snapshots.snapshot_manager import SnapshotManager
from app.runtime.replay.audit.audit_report_generator import AuditReportGenerator, EnterpriseAuditPackage
from app.runtime.replay.audit.audit_certificate import AuditCertificateIssuer
from app.runtime.replay.intelligence.replay_statistics import ReplayStatisticsEngine


class MissionReplayEngine:
    """
    Central deterministic replay engine for DocuTask Agent.
    """

    def __init__(self, snapshot_interval: int = 20):
        self.snapshot_manager = SnapshotManager(checkpoint_interval=snapshot_interval)

    def reconstruct_mission(
        self,
        mission_id: str,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> ReconstructedMissionState:
        return MissionReconstructor.reconstruct_up_to_cursor(mission_id, events, cursor)

    def reconstruct_planner(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return PlannerReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def reconstruct_scheduler(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return SchedulerReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def reconstruct_workers(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        workers = WorkerReconstructor.reconstruct_from_events(events, cursor)
        return {k: v.model_dump() for k, v in workers.items()}

    def reconstruct_confidence(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return ConfidenceReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def reconstruct_telemetry(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return TelemetryReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def reconstruct_memory(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return MemoryReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def reconstruct_truth(
        self,
        events: List[Dict[str, Any]],
        cursor: Optional[int] = None,
    ) -> Dict[str, Any]:
        return TruthReconstructor.reconstruct_from_events(events, cursor).model_dump()

    def verify_replay_integrity(
        self,
        mission_id: str,
        events: List[Dict[str, Any]],
        expected_root_hash: Optional[str] = None,
    ) -> ReplayVerificationResult:
        return ReplayVerifier.verify_replay(mission_id, events, expected_root_hash)

    def run_forensic_investigation(
        self,
        mission_id: str,
        events: List[Dict[str, Any]],
        fault_event_id: Optional[str] = None,
    ) -> ForensicInvestigationReport:
        return ForensicEngine.investigate_mission(mission_id, events, fault_event_id)

    def generate_audit_package(
        self,
        mission_id: str,
        events: List[Dict[str, Any]],
        truth_root: Optional[str] = None,
    ) -> EnterpriseAuditPackage:
        return AuditReportGenerator.generate_audit_package(mission_id, events, truth_root)

    def get_statistics(
        self,
        mission_id: str,
        events: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return ReplayStatisticsEngine.compute_statistics(mission_id, events).model_dump()


# Singleton
mission_replay_engine = MissionReplayEngine()
