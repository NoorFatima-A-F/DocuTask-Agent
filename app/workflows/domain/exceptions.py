"""
Workflow Engine Exception Hierarchy.
"""

from typing import Any, Dict, Optional
import uuid


class WorkflowException(Exception):
    """Base exception for all workflow domain, compilation, and execution errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "WORKFLOW_ERROR",
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        task_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.workflow_id = workflow_id
        self.execution_id = execution_id
        self.task_id = task_id
        self.details = details or {}
        self.error_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_id": self.error_id,
            "error_code": self.error_code,
            "message": self.message,
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "details": self.details,
        }


class WorkflowValidationException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="WORKFLOW_VALIDATION_ERROR", **kwargs)


class WorkflowCompilationException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="WORKFLOW_COMPILATION_ERROR", **kwargs)


class WorkflowExecutionException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="WORKFLOW_EXECUTION_ERROR", **kwargs)


class TaskExecutionException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="TASK_EXECUTION_ERROR", **kwargs)


class CompensationException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="COMPENSATION_ERROR", **kwargs)


class WorkflowTimeoutException(WorkflowException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="WORKFLOW_TIMEOUT_ERROR", **kwargs)
