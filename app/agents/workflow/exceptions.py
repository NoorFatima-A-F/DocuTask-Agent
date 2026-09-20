"""
Workflow Exception Hierarchy.
Defines domain and runtime exceptions for workflow lifecycle, DAGs, sagas, and migration errors.
"""

from typing import Optional
from uuid import UUID


class WorkflowException(Exception):
    """Base exception for all workflow runtime failures."""

    def __init__(self, message: str, workflow_id: Optional[UUID] = None):
        super().__init__(message)
        self.workflow_id = workflow_id


class CyclicWorkflowGraphError(WorkflowException):
    """Raised when a workflow graph contains circular node dependencies."""
    pass


class InvalidWorkflowStateTransitionError(WorkflowException):
    """Raised when attempting an unauthorized state transition on a workflow instance."""
    pass


class OrphanedChildWorkflowError(WorkflowException):
    """Raised when a child workflow loses its parent context or leader reference."""
    pass


class InconsistentWorkflowVersionError(WorkflowException):
    """Raised when workflow definition schema version does not match instance schema."""
    pass


class InvalidWorkflowMigrationError(WorkflowException):
    """Raised when an in-flight workflow migration violates backward compatibility."""
    pass


class MissingCompensationPathError(WorkflowException):
    """Raised when a Saga step fails but has no registered compensating action."""
    pass


class UnsupportedWorkflowDefinitionError(WorkflowException):
    """Raised when an unrecognized workflow definition typology is supplied."""
    pass


class InvalidTimerConfigurationError(WorkflowException):
    """Raised when a timer delay or duration is non-positive or malformed."""
    pass


class BrokenEventSubscriptionError(WorkflowException):
    """Raised when an event gateway fails to bind to target Pub/Sub topic or webhook."""
    pass
