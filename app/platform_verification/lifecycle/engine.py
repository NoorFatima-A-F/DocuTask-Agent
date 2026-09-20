from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
import uuid
import time
from .planner import VerificationPlan
from .tasks import VerificationTask, TaskState

@dataclass
class ExecutionSession:
    execution_id: str
    plan_id: str
    status: str = "RUNNING"
    task_results: Dict[str, VerificationTask] = field(default_factory=dict)
    raw_artifacts: List[Dict[str, Any]] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    total_duration_ms: float = 0.0

class VerificationExecutionEngine:
    def __init__(self):
        self._sessions: Dict[str, ExecutionSession] = {}

    def start_execution(self, plan: VerificationPlan, custom_handlers: Optional[Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]]] = None) -> ExecutionSession:
        exec_id = f"exec_{uuid.uuid4().hex[:12]}"
        session = ExecutionSession(execution_id=exec_id, plan_id=plan.plan_id)
        self._sessions[exec_id] = session

        t0 = time.monotonic()
        handlers = custom_handlers or {}

        for step in plan.steps:
            task = VerificationTask(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                step_id=step.step_id,
                task_name=step.step_name,
                inputs=step.payload
            )

            handler = handlers.get(step.action_type, lambda inp: {"status": "ok", "processed_input": inp})
            task.execute(handler)
            session.task_results[step.step_id] = task

            if task.state == TaskState.FAILED:
                session.status = "FAILED"
                break

            session.raw_artifacts.append({
                "step_id": step.step_id,
                "step_name": step.step_name,
                "output": task.outputs
            })

        if session.status != "FAILED":
            session.status = "SUCCESS"

        session.total_duration_ms = (time.monotonic() - t0) * 1000.0
        session.completed_at = datetime.now(timezone.utc).isoformat()
        return session

    def get_session(self, execution_id: str) -> Optional[ExecutionSession]:
        return self._sessions.get(execution_id)
