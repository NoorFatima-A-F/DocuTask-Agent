"""
Asynchronous Worker & Queue Domain Exceptions.
"""

from app.core.exceptions import BaseAppException, ResourceNotFoundException


class JobException(BaseAppException):
    """Base exception for background job processing failures."""

    def __init__(self, message: str = "Background job processing error", status_code: int = 500, errors=None):
        super().__init__(message=message, status_code=status_code, errors=errors)


class JobNotFoundException(ResourceNotFoundException):
    """Raised when background job is not found."""

    def __init__(self, message: str = "Job not found", errors=None):
        super().__init__(message=message, errors=errors)


class JobExecutionException(JobException):
    """Raised when worker fails to execute background job task."""

    def __init__(self, message: str = "Job execution failed", errors=None):
        super().__init__(message=message, status_code=500, errors=errors)


class DuplicateJobException(BaseAppException):
    """Raised when attempting to queue a duplicate job for a document already in progress."""

    def __init__(self, message: str = "An active processing job is already running for this document", errors=None):
        super().__init__(message=message, status_code=409, errors=errors)
