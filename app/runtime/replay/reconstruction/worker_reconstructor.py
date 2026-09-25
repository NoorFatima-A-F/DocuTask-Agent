"""
Worker Reconstructor for Phase 13.4.
Rebuilds worker executions, tool invocations, and individual task step lifecycles from events.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ReconstructedWorker(BaseModel):
    worker_id: str
    role: str = "general_worker"
    status: str = "IDLE"
    current_task_id: Optional[str] = None
    completed_task_count: int = 0
    failed_task_count: int = 0
    total_execution_ms: float = 0.0
    tool_invocations: List[Dict[str, Any]] = Field(default_factory=list)


class WorkerReconstructor:
    """
    Reconstructs worker state and tool execution history from events.
    """

    @classmethod
    def reconstruct_from_events(
        cls,
        events: List[Dict[str, Any]],
        target_cursor: Optional[int] = None,
    ) -> Dict[str, ReconstructedWorker]:
        workers: Dict[str, ReconstructedWorker] = {}
        sliced = events[: (target_cursor + 1)] if target_cursor is not None else events

        for ev in sliced:
            evt_type = ev.get("event_type") or ev.get("type", "")
            payload = ev.get("payload", {})
            worker_id = payload.get("worker_id")

            if not worker_id:
                continue

            if worker_id not in workers:
                workers[worker_id] = ReconstructedWorker(
                    worker_id=worker_id,
                    role=payload.get("role", "worker"),
                )

            w = workers[worker_id]

            if "worker.task_assigned" in evt_type or "worker.started" in evt_type:
                w.status = "BUSY"
                w.current_task_id = payload.get("task_id")
            elif "worker.task_completed" in evt_type or "worker.completed" in evt_type:
                w.status = "IDLE"
                w.current_task_id = None
                w.completed_task_count += 1
                w.total_execution_ms += float(payload.get("duration_ms", 0.0))
            elif "worker.task_failed" in evt_type or "worker.failed" in evt_type:
                w.status = "FAILED"
                w.failed_task_count += 1
            elif "tool.invoked" in evt_type or "tool.executed" in evt_type:
                w.tool_invocations.append(payload)

        return workers
