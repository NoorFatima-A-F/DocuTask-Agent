"""
Replay Performance and Execution Profiler.
Measures replay throughput, state transition durations, and cache efficiency.
"""

from pydantic import BaseModel
import time


class ReplayStatistics(BaseModel):
    mission_id: str
    total_events_in_log: int = 0
    events_replayed: int = 0
    replay_duration_seconds: float = 0.0
    events_per_second: float = 0.0
    checkpoints_hit: int = 0
    checkpoints_total: int = 0
    state_transitions_count: int = 0
    average_step_latency_microseconds: float = 0.0


class ReplayStatisticsTracker:
    def __init__(self, mission_id: str):
        self.mission_id = mission_id
        self._start_time: float = time.perf_counter()
        self._events_replayed: int = 0
        self._checkpoints_hit: int = 0
        self._checkpoints_total: int = 0
        self._total_events_in_log: int = 0

    def start(self, total_events: int, total_checkpoints: int = 0) -> None:
        self._start_time = time.perf_counter()
        self._events_replayed = 0
        self._checkpoints_hit = 0
        self._total_events_in_log = total_events
        self._checkpoints_total = total_checkpoints

    def record_step(self, count: int = 1) -> None:
        self._events_replayed += count

    def record_checkpoint_hit(self) -> None:
        self._checkpoints_hit += 1

    def get_statistics(self) -> ReplayStatistics:
        elapsed = max(1e-6, time.perf_counter() - self._start_time)
        eps = self._events_replayed / elapsed
        avg_step_us = (elapsed / max(1, self._events_replayed)) * 1_000_000.0

        return ReplayStatistics(
            mission_id=self.mission_id,
            total_events_in_log=self._total_events_in_log,
            events_replayed=self._events_replayed,
            replay_duration_seconds=round(elapsed, 4),
            events_per_second=round(eps, 2),
            checkpoints_hit=self._checkpoints_hit,
            checkpoints_total=self._checkpoints_total,
            state_transitions_count=self._events_replayed,
            average_step_latency_microseconds=round(avg_step_us, 2),
        )
