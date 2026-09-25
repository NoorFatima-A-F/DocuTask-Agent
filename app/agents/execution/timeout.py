"""
Execution Timeout Manager.
Enforces per-node and global workflow deadlines.
"""

from datetime import datetime, timezone
from app.agents.execution.exceptions import ExecutionTimeoutException


class TimeoutManager:
    """Monitors elapsed time and checks against configured deadlines."""

    def __init__(self, timeout_seconds: float = 3600.0):
        self.timeout_seconds = timeout_seconds
        self.started_at = datetime.now(timezone.utc).timestamp()

    def check_deadline(self) -> None:
        elapsed = datetime.now(timezone.utc).timestamp() - self.started_at
        if elapsed > self.timeout_seconds:
            raise ExecutionTimeoutException(f"Execution timed out after {elapsed:.2f}s (deadline: {self.timeout_seconds}s).")

    @property
    def remaining_seconds(self) -> float:
        elapsed = datetime.now(timezone.utc).timestamp() - self.started_at
        return max(0.0, self.timeout_seconds - elapsed)
