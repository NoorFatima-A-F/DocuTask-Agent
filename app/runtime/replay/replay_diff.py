"""
Replay State Diff Subsystem.
Computes structural and data differences between two reconstructed mission states.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from app.runtime.replay.replay_state_machine import ReconstructedMissionState


class TaskStateDiff(BaseModel):
    task_id: str
    status_before: str
    status_after: str
    duration_delta_ms: float = 0.0
    cost_delta_usd: float = 0.0


class MissionStateDiff(BaseModel):
    mission_id: str
    generation_before: int
    generation_after: int
    events_applied_before: int
    events_applied_after: int
    status_changed: bool
    status_before: str
    status_after: str
    cost_delta_usd: float
    new_completed_tasks: List[str] = Field(default_factory=list)
    new_failed_tasks: List[str] = Field(default_factory=list)
    mutations_delta: int = 0
    task_diffs: Dict[str, TaskStateDiff] = Field(default_factory=dict)


class ReplayStateDiffEngine:
    @staticmethod
    def compare_states(before: ReconstructedMissionState, after: ReconstructedMissionState) -> MissionStateDiff:
        new_completed = [t for t in after.completed_tasks if t not in before.completed_tasks]
        new_failed = [t for t in after.failed_tasks if t not in before.failed_tasks]

        task_diffs: Dict[str, TaskStateDiff] = {}
        all_task_ids = set(before.tasks.keys()).union(set(after.tasks.keys()))

        for tid in all_task_ids:
            t_before = before.tasks.get(tid)
            t_after = after.tasks.get(tid)

            status_before = t_before.status if t_before else "UNINITIALIZED"
            status_after = t_after.status if t_after else "UNINITIALIZED"

            dur_before = t_before.duration_ms or 0.0 if t_before else 0.0
            dur_after = t_after.duration_ms or 0.0 if t_after else 0.0

            cost_before = t_before.cost_usd if t_before else 0.0
            cost_after = t_after.cost_usd if t_after else 0.0

            if status_before != status_after or dur_before != dur_after or cost_before != cost_after:
                task_diffs[tid] = TaskStateDiff(
                    task_id=tid,
                    status_before=status_before,
                    status_after=status_after,
                    duration_delta_ms=dur_after - dur_before,
                    cost_delta_usd=cost_after - cost_before,
                )

        return MissionStateDiff(
            mission_id=after.mission_id,
            generation_before=before.generation,
            generation_after=after.generation,
            events_applied_before=before.total_events_applied,
            events_applied_after=after.total_events_applied,
            status_changed=(before.status != after.status),
            status_before=before.status,
            status_after=after.status,
            cost_delta_usd=after.cumulative_cost_usd - before.cumulative_cost_usd,
            new_completed_tasks=new_completed,
            new_failed_tasks=new_failed,
            mutations_delta=after.mutations_applied - before.mutations_applied,
            task_diffs=task_diffs,
        )
