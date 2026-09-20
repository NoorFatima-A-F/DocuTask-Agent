"""
Exception Hierarchy for the Reflection Subsystem.
Defines strongly typed domain and runtime exceptions for the reflection engine.
"""

from typing import Optional
from uuid import UUID


class ReflectionException(Exception):
    """Base exception for all reflection-related failures."""

    def __init__(self, message: str, reflection_id: Optional[UUID] = None):
        super().__init__(message)
        self.reflection_id = reflection_id


class IncompleteExecutionTraceError(ReflectionException):
    """Raised when an execution trace lacks essential execution state, nodes, or outcome."""
    pass


class InvalidEvaluationGraphError(ReflectionException):
    """Raised when an evaluation graph contains circular dependencies or invalid nodes."""
    pass


class InconsistentEvidenceError(ReflectionException):
    """Raised when critique assertions contradict observed telemetry or tool outputs."""
    pass


class CircularCritiqueReferenceError(ReflectionException):
    """Raised when critique reasoning contains circular causal loops."""
    pass


class DuplicateLearningArtifactError(ReflectionException):
    """Raised when attempting to register an identical or duplicate learning artifact."""
    pass


class MalformedRecommendationError(ReflectionException):
    """Raised when a recommendation lacks mandatory rationale, confidence, or evidence."""
    pass


class InvalidConfidenceScoreError(ReflectionException):
    """Raised when a confidence score falls outside the normalized [0.0, 1.0] interval."""
    pass


class AdaptationApprovalRequiredError(ReflectionException):
    """Raised when an adaptation proposal is accessed without authorized sign-off."""
    pass
