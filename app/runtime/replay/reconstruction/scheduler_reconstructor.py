"""
Scheduler Reconstructor for Phase 13.4.
Rebuilds DAG wavefront schedules, 7-state runtime queues, and worker assignment proofs from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedSchedulerState(BaseModel):
    current_wavefront: int = 0
    queues: Dict[str, List[str]] = Field(default_factory=lambda: {
        "pending": [],
        "ready": [],
        "scheduled": [],
        "running": [],
        "blocked": [],
        "completed": [],
        "failed": [],
    })
    worker_allocations: Dict[str, str] = Field(default_factory=dict)
    active_concurrency: int = 0
    max_concurrency: int = 8
    queue_latency_ms: float = 0.0


class SchedulerReconstructor:
    """
    Reconstructs DAG wavefront scheduling states from immutable event logs.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> ReconstructedSchedulerState:
        state = ReconstructedSchedulerState()
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})

            if "schedule.wavefront" in evt_type:
                state.current_wavefront = payload.get("wavefront_index", state.current_wavefront)
            elif "worker.assigned" in evt_type or "schedule.assigned" in evt_type:
                task_id = payload.get("task_id", "")
                worker_id = payload.get("worker_id", "")
                if task_id and worker_id:
                    state.worker_allocations[task_id] = worker_id
            elif "queue.transition" in evt_type:
                task_id = payload.get("task_id", "")
                from_q = payload.get("from_queue")
                to_q = payload.get("to_queue")
                if from_q in state.queues and task_id in state.queues[from_q]:
                    state.queues[from_q].remove(task_id)
                if to_q in state.queues and task_id:
                    state.queues[to_q].append(task_id)
            elif "task.scheduled" in evt_type:
                task_id = payload.get("task_id", "")
                if task_id and task_id not in state.queues["scheduled"]:
                    state.queues["scheduled"].append(task_id)
            elif "task.completed" in evt_type:
                task_id = payload.get("task_id", "")
                if task_id:
                    for q in state.queues.values():
                        if task_id in q:
                            q.remove(task_id)
                    state.queues["completed"].append(task_id)

        state.active_concurrency = len(state.queues["running"])
        return state
