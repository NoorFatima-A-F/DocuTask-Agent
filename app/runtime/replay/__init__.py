"""
Phase 13.4: Autonomous Event-Sourced Mission Replay, Runtime Forensics & Enterprise Audit Intelligence Platform (AESMR-EAIP).
"""

# Phase 13.4 Modern Components
from app.runtime.replay.engine.mission_replay_engine import (
    MissionReplayEngine,
    mission_replay_engine,
)
from app.runtime.replay.engine.replay_controller import (
    ReplayController,
    replay_controller,
)
from app.runtime.replay.engine.replay_session import (
    ReplaySessionState,
    ReplayBookmark as ModernReplayBookmark,
)
from app.runtime.replay.engine.replay_executor import ReplayExecutor
from app.runtime.replay.engine.timeline_player import TimelinePlayer
from app.runtime.replay.engine.playback_controller import PlaybackRateController

from app.runtime.replay.reconstruction.mission_reconstructor import (
    MissionReconstructor,
    ReconstructedMissionState as ModernReconstructedMissionState,
)
from app.runtime.replay.reconstruction.planner_reconstructor import PlannerReconstructor
from app.runtime.replay.reconstruction.scheduler_reconstructor import SchedulerReconstructor
from app.runtime.replay.reconstruction.worker_reconstructor import WorkerReconstructor
from app.runtime.replay.reconstruction.confidence_reconstructor import ConfidenceReconstructor
from app.runtime.replay.reconstruction.telemetry_reconstructor import TelemetryReconstructor
from app.runtime.replay.reconstruction.memory_reconstructor import MemoryReconstructor
from app.runtime.replay.reconstruction.truth_reconstructor import TruthReconstructor

from app.runtime.replay.forensic.forensic_engine import (
    ForensicEngine,
    ForensicInvestigationReport,
)
from app.runtime.replay.forensic.root_cause_analyzer import (
    RootCauseAnalyzer,
    RootCauseFinding,
)
from app.runtime.replay.forensic.decision_trace import (
    DecisionTrace,
    DecisionTraceRecord,
)
from app.runtime.replay.forensic.failure_reconstruction import FailureReconstruction
from app.runtime.replay.forensic.anomaly_reconstruction import AnomalyReconstruction
from app.runtime.replay.forensic.timeline_diff import (
    TimelineDiffEngine,
    TimelineDiffReport,
)

from app.runtime.replay.verification.replay_verifier import (
    ReplayVerifier,
    ReplayVerificationResult,
)
from app.runtime.replay.verification.hash_verifier import HashVerifier
from app.runtime.replay.verification.truth_chain_verifier import TruthChainVerifier
from app.runtime.replay.verification.formula_verifier import FormulaVerifier
from app.runtime.replay.verification.projection_verifier import ProjectionVerifier

from app.runtime.replay.snapshots.snapshot_manager import (
    SnapshotManager,
    ReplayCheckpoint as ModernReplayCheckpoint,
)
from app.runtime.replay.snapshots.checkpoint_manager import CheckpointManager
from app.runtime.replay.snapshots.state_serializer import StateSerializer
from app.runtime.replay.snapshots.state_deserializer import StateDeserializer
from app.runtime.replay.snapshots.snapshot_compressor import SnapshotCompressor

from app.runtime.replay.audit.audit_report_generator import (
    AuditReportGenerator,
    EnterpriseAuditPackage,
)
from app.runtime.replay.audit.audit_bundle import AuditBundleBuilder, AuditBundle
from app.runtime.replay.audit.audit_evidence import AuditEvidenceExtractor
from app.runtime.replay.audit.audit_certificate import (
    AuditCertificateIssuer,
    ReplayCertificate,
)
from app.runtime.replay.audit.compliance_summary import ComplianceSummaryService

from app.runtime.replay.intelligence.replay_statistics import (
    ReplayStatisticsEngine,
    ReplayStatisticsSummary,
)
from app.runtime.replay.intelligence.event_density import EventDensityCalculator
from app.runtime.replay.intelligence.latency_breakdown import LatencyBreakdownEngine
from app.runtime.replay.intelligence.resource_replay import ResourceReplayTracker
from app.runtime.replay.intelligence.confidence_replay import ConfidenceReplayEngine
from app.runtime.replay.intelligence.cost_replay import CostReplayEngine

from app.runtime.replay.events.replay_events import (
    ReplayStarted,
    ReplayPaused,
    ReplayResumed,
    ReplayStopped,
    ReplayCheckpointCreated,
    ReplayCheckpointRestored,
    ReplayFrameRendered,
    ReplayVerified,
    ReplayVerificationFailed,
    ReplaySnapshotLoaded,
    ReplaySnapshotSaved,
    ReplayDiffGenerated,
    ReplayAuditGenerated,
    ReplayCertificateIssued,
    ReplayTimeTravelExecuted,
    ReplayRootCauseCompleted,
    ReplayEvidenceVerified,
)

# Legacy Backward-Compatibility Exports
from app.runtime.replay.replay_speed import ReplaySpeed, SPEED_MULTIPLIERS, SpeedProfile
from app.runtime.replay.replay_filters import ReplayFilterCriteria, ReplayFilterEngine
from app.runtime.replay.replay_bookmarks import ReplayBookmark, ReplayBookmarkManager, BookmarkType
from app.runtime.replay.replay_cursor import ReplayCursor
from app.runtime.replay.replay_checkpoint import ReplayCheckpoint, ReplayCheckpointManager
from app.runtime.replay.replay_state_machine import (
    ReplayStateMachine,
    ReconstructedMissionState,
    ReconstructedTaskState,
)
from app.runtime.replay.replay_builder import ReplayStreamBuilder
from app.runtime.replay.replay_player import ReplayPlayer, PlayerStatus
from app.runtime.replay.replay_integrity import ReplayIntegrityVerifier, IntegrityVerificationResult
from app.runtime.replay.replay_diff import ReplayStateDiffEngine, MissionStateDiff, TaskStateDiff
from app.runtime.replay.replay_statistics import ReplayStatistics, ReplayStatisticsTracker
from app.runtime.replay.replay_validator import ReplayValidator, DeterminismValidationReport
from app.runtime.replay.replay_exporter import ReplayExporter, ForensicReplayPackage
from app.runtime.replay.replay_runtime import ReplayRuntimeSession
from app.runtime.replay.replay_engine import MasterReplayEngine

__all__ = [
    # Phase 13.4
    "MissionReplayEngine",
    "mission_replay_engine",
    "ReplayController",
    "replay_controller",
    "ReplaySessionState",
    "ModernReplayBookmark",
    "ReplayExecutor",
    "TimelinePlayer",
    "PlaybackRateController",
    "MissionReconstructor",
    "ModernReconstructedMissionState",
    "PlannerReconstructor",
    "SchedulerReconstructor",
    "WorkerReconstructor",
    "ConfidenceReconstructor",
    "TelemetryReconstructor",
    "MemoryReconstructor",
    "TruthReconstructor",
    "ForensicEngine",
    "ForensicInvestigationReport",
    "RootCauseAnalyzer",
    "RootCauseFinding",
    "DecisionTrace",
    "DecisionTraceRecord",
    "FailureReconstruction",
    "AnomalyReconstruction",
    "TimelineDiffEngine",
    "TimelineDiffReport",
    "ReplayVerifier",
    "ReplayVerificationResult",
    "HashVerifier",
    "TruthChainVerifier",
    "FormulaVerifier",
    "ProjectionVerifier",
    "SnapshotManager",
    "ModernReplayCheckpoint",
    "CheckpointManager",
    "StateSerializer",
    "StateDeserializer",
    "SnapshotCompressor",
    "AuditReportGenerator",
    "EnterpriseAuditPackage",
    "AuditBundleBuilder",
    "AuditBundle",
    "AuditEvidenceExtractor",
    "AuditCertificateIssuer",
    "ReplayCertificate",
    "ComplianceSummaryService",
    "ReplayStatisticsEngine",
    "ReplayStatisticsSummary",
    "EventDensityCalculator",
    "LatencyBreakdownEngine",
    "ResourceReplayTracker",
    "ConfidenceReplayEngine",
    "CostReplayEngine",
    "ReplayStarted",
    "ReplayPaused",
    "ReplayResumed",
    "ReplayStopped",
    "ReplayCheckpointCreated",
    "ReplayCheckpointRestored",
    "ReplayFrameRendered",
    "ReplayVerified",
    "ReplayVerificationFailed",
    "ReplaySnapshotLoaded",
    "ReplaySnapshotSaved",
    "ReplayDiffGenerated",
    "ReplayAuditGenerated",
    "ReplayCertificateIssued",
    "ReplayTimeTravelExecuted",
    "ReplayRootCauseCompleted",
    "ReplayEvidenceVerified",
    # Legacy
    "ReplaySpeed",
    "SPEED_MULTIPLIERS",
    "SpeedProfile",
    "ReplayFilterCriteria",
    "ReplayFilterEngine",
    "ReplayBookmark",
    "ReplayBookmarkManager",
    "BookmarkType",
    "ReplayCursor",
    "ReplayCheckpoint",
    "ReplayCheckpointManager",
    "ReplayStateMachine",
    "ReconstructedMissionState",
    "ReconstructedTaskState",
    "ReplayStreamBuilder",
    "ReplayPlayer",
    "PlayerStatus",
    "ReplayIntegrityVerifier",
    "IntegrityVerificationResult",
    "ReplayStateDiffEngine",
    "MissionStateDiff",
    "TaskStateDiff",
    "ReplayStatistics",
    "ReplayStatisticsTracker",
    "ReplayValidator",
    "DeterminismValidationReport",
    "ReplayExporter",
    "ForensicReplayPackage",
    "ReplayRuntimeSession",
    "MasterReplayEngine",
]
