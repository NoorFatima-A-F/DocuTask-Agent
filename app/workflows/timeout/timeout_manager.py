"""
Enterprise Workflow Timeout Engine.
Tracks and enforces deadlines for workflows, individual tasks, AI calls, connector calls, and human approvals.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from ..domain.exceptions import WorkflowTimeoutException


class TimeoutManager:
    """Manages execution timeouts, deadlines, and heartbeats."""

    @staticmethod
    def is_timed_out(start_time: datetime, timeout_seconds: int) -> bool:
        """Check if elapsed duration exceeds timeout seconds."""
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        return elapsed > timeout_seconds

    @staticmethod
    def assert_not_timed_out(start_time: datetime, timeout_seconds: int, task_id: Optional[str] = None) -> None:
        """Raise WorkflowTimeoutException if duration exceeded."""
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        if elapsed > timeout_seconds:
            raise WorkflowTimeoutException(
                f"Task '{task_id or 'unknown'}' timed out after {elapsed:.1f}s (limit: {timeout_seconds}s)",
                task_id=task_id,
            )
