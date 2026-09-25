"""
Job State Machine & Transition Rules Engine.
Enforces strict state transitions across DocumentJob lifecycle states.
"""

from typing import Dict, Set
from app.core.logging import logger


class InvalidJobStateTransitionException(Exception):
    """Raised when an invalid job state transition is attempted."""
    pass


class JobState:
    """DocumentJob state constants."""
    CREATED = "CREATED"
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    OCR_COMPLETED = "OCR_COMPLETED"
    AI_PROCESSING = "AI_PROCESSING"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"


class JobStateMachine:
    """State machine governing valid DocumentJob state transitions."""

    VALID_TRANSITIONS: Dict[str, Set[str]] = {
        JobState.CREATED: {JobState.UPLOADED, JobState.CANCELLED, JobState.FAILED},
        JobState.UPLOADED: {JobState.QUEUED, JobState.CANCELLED, JobState.FAILED},
        JobState.QUEUED: {JobState.PROCESSING, JobState.CANCELLED, JobState.FAILED},
        JobState.PROCESSING: {JobState.OCR_COMPLETED, JobState.RETRYING, JobState.FAILED, JobState.CANCELLED},
        JobState.OCR_COMPLETED: {JobState.AI_PROCESSING, JobState.RETRYING, JobState.FAILED, JobState.CANCELLED},
        JobState.AI_PROCESSING: {JobState.VALIDATING, JobState.RETRYING, JobState.FAILED, JobState.CANCELLED},
        JobState.VALIDATING: {JobState.COMPLETED, JobState.RETRYING, JobState.FAILED, JobState.CANCELLED},
        JobState.RETRYING: {JobState.QUEUED, JobState.PROCESSING, JobState.FAILED, JobState.CANCELLED},
        JobState.COMPLETED: set(),  # Terminal state
        JobState.FAILED: {JobState.QUEUED},  # Allowed via DLQ manual replay
        JobState.CANCELLED: set()   # Terminal state
    }

    @classmethod
    def validate_transition(cls, current_state: str, new_state: str) -> bool:
        """
        Validates if transition from current_state to new_state is allowed.
        Raises InvalidJobStateTransitionException if invalid.
        """
        if current_state not in cls.VALID_TRANSITIONS:
            raise InvalidJobStateTransitionException(f"Unknown current state: '{current_state}'")

        allowed_next_states = cls.VALID_TRANSITIONS[current_state]
        if new_state not in allowed_next_states:
            msg = f"Invalid state transition from '{current_state}' to '{new_state}'. Allowed: {list(allowed_next_states)}"
            logger.error(msg)
            raise InvalidJobStateTransitionException(msg)

        logger.info(f"Job state transitioned successfully: '{current_state}' -> '{new_state}'")
        return True
