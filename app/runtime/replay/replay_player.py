"""
Async Replay Player Subsystem.
Controls mission playback, step forward/backward, seek, reverse play, and pause/resume states.
"""

from typing import List, Optional, Callable
from enum import Enum
import asyncio
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_cursor import ReplayCursor
from app.runtime.replay.replay_speed import ReplaySpeed, SPEED_MULTIPLIERS, SpeedProfile
from app.runtime.replay.replay_checkpoint import ReplayCheckpointManager, ReplayCheckpoint
from app.runtime.replay.replay_state_machine import ReplayStateMachine, ReconstructedMissionState


class PlayerStatus(str, Enum):
    IDLE = "IDLE"
    PLAYING = "PLAYING"
    PLAYING_REVERSE = "PLAYING_REVERSE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class ReplayPlayer:
    """Async controller for mission replay sessions."""

    def __init__(
        self,
        mission_id: str,
        events: List[RuntimeEvent],
        checkpoint_interval: int = 50,
    ):
        self.mission_id = mission_id
        self.events: List[RuntimeEvent] = list(events)
        self.cursor: ReplayCursor = ReplayCursor()
        self.status: PlayerStatus = PlayerStatus.IDLE
        self.speed: ReplaySpeed = ReplaySpeed.NORMAL
        self.checkpoint_manager: ReplayCheckpointManager = ReplayCheckpointManager(interval=checkpoint_interval)

        self._state: ReconstructedMissionState = ReplayStateMachine.create_initial_state(mission_id)
        self._current_index: int = 0
        self._play_task: Optional[asyncio.Task] = None
        self._on_state_change_callbacks: List[Callable[[ReconstructedMissionState, ReplayCursor], None]] = []

        # Build initial checkpoints
        self._build_checkpoints()
        self._update_cursor()

    def _build_checkpoints(self) -> None:
        state = ReplayStateMachine.create_initial_state(self.mission_id)
        for idx, event in enumerate(self.events):
            state = ReplayStateMachine.apply_event(state, event)
            if (idx + 1) % self.checkpoint_manager.interval == 0 or idx == len(self.events) - 1:
                cp = ReplayCheckpoint(
                    checkpoint_id=f"cp_{self.mission_id}_{idx}",
                    mission_id=self.mission_id,
                    event_index=idx,
                    event_id=event.event_id,
                    state_payload=state.model_dump(),
                )
                self.checkpoint_manager.add_checkpoint(cp)

    def _update_cursor(self) -> None:
        event_id = self.events[self._current_index].event_id if self.events and 0 <= self._current_index < len(self.events) else None
        ts = self.events[self._current_index].timestamp if self.events and 0 <= self._current_index < len(self.events) else None
        self.cursor.update_position(self._current_index, len(self.events), event_id, ts)

    @property
    def current_state(self) -> ReconstructedMissionState:
        return self._state

    def register_callback(self, cb: Callable[[ReconstructedMissionState, ReplayCursor], None]) -> None:
        self._on_state_change_callbacks.append(cb)

    def _notify(self) -> None:
        for cb in self._on_state_change_callbacks:
            try:
                cb(self._state, self.cursor)
            except Exception:
                pass

    def seek_to_index(self, target_index: int) -> ReconstructedMissionState:
        """Seeks to target event index leveraging preceding checkpoints."""
        if not self.events:
            self._state = ReplayStateMachine.create_initial_state(self.mission_id)
            self._current_index = 0
            self._update_cursor()
            return self._state

        clamped = max(0, min(target_index, len(self.events) - 1))

        # Check for fast checkpoint
        nearest_cp = self.checkpoint_manager.get_nearest_preceding_checkpoint(clamped)
        if nearest_cp and nearest_cp.event_index <= clamped:
            state = ReconstructedMissionState.model_validate(nearest_cp.state_payload)
            start_idx = nearest_cp.event_index + 1
        else:
            state = ReplayStateMachine.create_initial_state(self.mission_id)
            start_idx = 0

        for i in range(start_idx, clamped + 1):
            state = ReplayStateMachine.apply_event(state, self.events[i])

        self._state = state
        self._current_index = clamped
        self._update_cursor()
        self._notify()
        return self._state

    def step_forward(self) -> ReconstructedMissionState:
        """Steps forward by one event."""
        if self._current_index < len(self.events) - 1:
            return self.seek_to_index(self._current_index + 1)
        return self._state

    def step_backward(self) -> ReconstructedMissionState:
        """Steps backward by one event."""
        if self._current_index > 0:
            return self.seek_to_index(self._current_index - 1)
        return self._state

    def pause(self) -> None:
        self.status = PlayerStatus.PAUSED
        if self._play_task and not self._play_task.done():
            self._play_task.cancel()
            self._play_task = None

    def set_speed(self, speed: ReplaySpeed) -> None:
        self.speed = speed

    async def play(self, reverse: bool = False) -> None:
        """Starts continuous playback."""
        self.pause()
        self.status = PlayerStatus.PLAYING_REVERSE if reverse else PlayerStatus.PLAYING

        profile = SpeedProfile(speed=self.speed, multiplier=SPEED_MULTIPLIERS[self.speed])

        while (not reverse and self._current_index < len(self.events) - 1) or (reverse and self._current_index > 0):
            if self.status not in {PlayerStatus.PLAYING, PlayerStatus.PLAYING_REVERSE}:
                break

            if reverse:
                self.step_backward()
            else:
                self.step_forward()

            delay = profile.compute_step_delay_seconds()
            if delay > 0:
                await asyncio.sleep(delay)

        self.status = PlayerStatus.COMPLETED
