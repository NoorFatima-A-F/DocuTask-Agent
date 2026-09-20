"""
Asynchronous AI Agent Workflow State Transition Validator.
"""
from __future__ import annotations
from typing import Set, Tuple
from app.platform_verification.api_verification.domain.interfaces import IAsyncAgentWorkflowValidator
from app.platform_verification.api_verification.domain.models import AgentTaskState


class EnterpriseAsyncAgentWorkflowValidator(IAsyncAgentWorkflowValidator):
    """Validates that long-running AI operations follow valid state transitions without blocking HTTP."""

    ALLOWED_TRANSITIONS = {
        AgentTaskState.CREATED: {AgentTaskState.RUNNING, AgentTaskState.CANCELLED},
        AgentTaskState.RUNNING: {AgentTaskState.WAITING_FOR_HUMAN, AgentTaskState.COMPLETED, AgentTaskState.FAILED, AgentTaskState.CANCELLED},
        AgentTaskState.WAITING_FOR_HUMAN: {AgentTaskState.RUNNING, AgentTaskState.CANCELLED},
        AgentTaskState.COMPLETED: set(),  # Terminal state
        AgentTaskState.FAILED: {AgentTaskState.CREATED},  # Can retry
        AgentTaskState.CANCELLED: set(),  # Terminal state
    }

    def validate_task_transitions(self, current_state: str, next_state: str) -> Tuple[bool, str]:
        try:
            curr_enum = AgentTaskState(current_state)
            next_enum = AgentTaskState(next_state)
        except ValueError:
            return False, f"Invalid state enum: {current_state} -> {next_state}"

        allowed = self.ALLOWED_TRANSITIONS.get(curr_enum, set())
        if next_enum in allowed:
            return True, f"Valid state transition: {current_state} -> {next_state}"
        else:
            return False, f"Illegal state transition: Cannot transition from terminal/invalid state '{current_state}' to '{next_state}'."
