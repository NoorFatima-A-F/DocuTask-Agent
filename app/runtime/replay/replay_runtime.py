"""
Enterprise Replay Runtime Subsystem.
Orchestrates mission replay sessions, state progression, and fast seeking.
"""

from typing import Dict, List, Optional
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_player import ReplayPlayer, PlayerStatus
from app.runtime.replay.replay_speed import ReplaySpeed
from app.runtime.replay.replay_bookmarks import ReplayBookmarkManager, ReplayBookmark, BookmarkType
from app.runtime.replay.replay_integrity import ReplayIntegrityVerifier, IntegrityVerificationResult
from app.runtime.replay.replay_state_machine import ReconstructedMissionState
from app.runtime.replay.replay_cursor import ReplayCursor
from app.runtime.replay.replay_statistics import ReplayStatisticsTracker, ReplayStatistics
from app.runtime.replay.replay_validator import ReplayValidator, DeterminismValidationReport


class ReplayRuntimeSession:
    """Manages an active replay session for a specific mission."""

    def __init__(self, mission_id: str, events: List[RuntimeEvent]):
        self.mission_id = mission_id
        self.events = list(events)
        self.player = ReplayPlayer(mission_id=mission_id, events=self.events)
        self.bookmark_manager = ReplayBookmarkManager(mission_id=mission_id)
        self.stats_tracker = ReplayStatisticsTracker(mission_id=mission_id)

        # Auto-detect milestone bookmarks
        self._auto_populate_bookmarks()

    def _auto_populate_bookmarks(self) -> None:
        for idx, event in enumerate(self.events):
            cat = str(event.category).lower()
            etype = str(event.event_type).lower()

            if "started" in etype and idx == 0:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.MISSION_START,
                    label="Mission Ingestion Started",
                )
            elif "mutation" in etype or "mutated" in etype:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.PLANNER_MUTATION,
                    label=f"Planner DAG Mutation (Gen {event.payload.get('generation', 2)})",
                )
            elif "failed" in etype:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.TASK_FAILURE,
                    label=f"Failure Point: {event.payload.get('task_id', 'Task')}",
                )
            elif "recovery" in cat or "recovery" in etype:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.RECOVERY_INJECTION,
                    label="Recovery Pipeline Injected",
                )
            elif "human" in cat or "human" in etype:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.HUMAN_INTERVENTION,
                    label="Human Operator Review",
                )
            elif "verification" in etype or "governance" in cat:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.SMT_VERIFICATION,
                    label="SMT Invariant Proof Passed",
                )
            elif idx == len(self.events) - 1:
                self.bookmark_manager.add_bookmark(
                    event_index=idx,
                    event_id=event.event_id,
                    bookmark_type=BookmarkType.MISSION_COMPLETE,
                    label="Mission Completed",
                )

    def seek(self, index: int) -> ReconstructedMissionState:
        self.stats_tracker.record_step(1)
        return self.player.seek_to_index(index)

    def seek_to_event_id(self, event_id: str) -> Optional[ReconstructedMissionState]:
        for idx, e in enumerate(self.events):
            if e.event_id == event_id:
                return self.seek(idx)
        return None

    def seek_to_bookmark(self, bookmark_id: str) -> Optional[ReconstructedMissionState]:
        bm = self.bookmark_manager.get_bookmark(bookmark_id)
        if bm:
            return self.seek(bm.event_index)
        return None

    def step_forward(self) -> ReconstructedMissionState:
        self.stats_tracker.record_step(1)
        return self.player.step_forward()

    def step_backward(self) -> ReconstructedMissionState:
        self.stats_tracker.record_step(1)
        return self.player.step_backward()

    def pause(self) -> None:
        self.player.pause()

    async def play(self, reverse: bool = False) -> None:
        await self.player.play(reverse=reverse)

    def set_speed(self, speed: ReplaySpeed) -> None:
        self.player.set_speed(speed)

    def verify_integrity(self) -> IntegrityVerificationResult:
        return ReplayIntegrityVerifier.verify_event_stream(self.events)

    def validate_determinism(self, repetitions: int = 3) -> DeterminismValidationReport:
        return ReplayValidator.validate_determinism(self.mission_id, self.events, repetitions)

    def get_statistics(self) -> ReplayStatistics:
        return self.stats_tracker.get_statistics()
