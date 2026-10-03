"""Oversight Platform Exceptions."""


class OversightException(Exception):
    """Base exception for all human oversight and approval errors."""
    pass


class UnauthorizedReviewerError(OversightException):
    """Raised when a reviewer lacks required authority to approve or reject a review."""
    pass


class InvalidOverrideError(OversightException):
    """Raised when an override violates safety thresholds, policy restrictions, or missing justifications."""
    pass


class EscalationTimeoutError(OversightException):
    """Raised when an approval request exceeds SLA timeout without resolution."""
    pass


class ApprovalPolicyViolationError(OversightException):
    """Raised when an action violates mandatory human approval policies."""
    pass
