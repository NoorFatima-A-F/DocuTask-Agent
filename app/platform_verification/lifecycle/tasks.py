from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
import time

class TaskState(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"

@dataclass
class VerificationTask:
    task_id: str
    step_id: str
    task_name: str
    state: TaskState = TaskState.PENDING
    max_retries: int = 3
    current_attempt: int = 0
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    execution_duration_ms: float = 0.0
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def execute(self, action: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "VerificationTask":
        self.started_at = datetime.now(timezone.utc).isoformat()
        t0 = time.monotonic()
        self.state = TaskState.RUNNING
        self.current_attempt += 1

        try:
            res = action(self.inputs)
            self.outputs = res
            self.state = TaskState.SUCCESS
        except Exception as e:
            self.error_message = str(e)
            if self.current_attempt <= self.max_retries:
                self.state = TaskState.RETRYING
            else:
                self.state = TaskState.FAILED
        finally:
            self.execution_duration_ms = (time.monotonic() - t0) * 1000.0
            self.completed_at = datetime.now(timezone.utc).isoformat()

        return self
