"""
Execution Progress Tracker.
Tracks completed, in-flight, and pending task percentages.
"""

from typing import Dict
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState


class ExecutionProgress(BaseModel):
    """Calculated progress indicators for an active execution."""
    total_nodes: int = Field(default=0, ge=0)
    completed_nodes: int = Field(default=0, ge=0)
    failed_nodes: int = Field(default=0, ge=0)
    in_progress_nodes: int = Field(default=0, ge=0)
    percentage_complete: float = Field(default=0.0, ge=0.0, le=100.0)
    model_config = {"frozen": True}


class ProgressTracker:
    """Computes completion percentage and execution pace."""

    @staticmethod
    def calculate_progress(node_states: Dict[str, ExecutionLifecycleState]) -> ExecutionProgress:
        total = len(node_states)
        if total == 0:
            return ExecutionProgress()

        completed = sum(1 for s in node_states.values() if s == ExecutionLifecycleState.COMPLETED)
        failed = sum(1 for s in node_states.values() if s == ExecutionLifecycleState.FAILED)
        running = sum(1 for s in node_states.values() if s in (ExecutionLifecycleState.RUNNING, ExecutionLifecycleState.SCHEDULED))

        pct = round((completed / total) * 100.0, 1)
        return ExecutionProgress(
            total_nodes=total,
            completed_nodes=completed,
            failed_nodes=failed,
            in_progress_nodes=running,
            percentage_complete=pct
        )
