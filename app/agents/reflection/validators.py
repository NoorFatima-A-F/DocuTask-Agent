"""
Reflection Fail-Fast Validators.
Validates execution traces, evaluation graphs, critique consistency, learning artifacts, and recommendations.
"""

from app.agents.reflection.exceptions import (
    DuplicateLearningArtifactError,
    IncompleteExecutionTraceError,
    InconsistentEvidenceError,
    InvalidConfidenceScoreError,
    MalformedRecommendationError,
)
from app.agents.reflection.learning_artifact import LearningArtifact
from app.agents.reflection.recommendation_engine import Recommendation
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.self_critique import SelfCritique


class ReflectionValidator:
    """Fail-fast validation rules protecting reflection pipeline integrity."""

    @staticmethod
    def validate_execution_trace(trace: ExecutionTraceEnvelope) -> None:
        """Validates that execution trace contains necessary metadata and task history."""
        if not trace.execution_id:
            raise IncompleteExecutionTraceError("Execution trace must possess a valid execution_id.")
        if not trace.final_state:
            raise IncompleteExecutionTraceError("Execution trace must declare a non-empty final_state.")

    @staticmethod
    def validate_confidence_score(score: float, context_label: str = "Score") -> None:
        """Ensures confidence score is strictly within [0.0, 1.0]."""
        if score < 0.0 or score > 1.0:
            raise InvalidConfidenceScoreError(
                f"{context_label} must be normalized within [0.0, 1.0]. Provided: {score}"
            )

    @staticmethod
    def validate_recommendation(recommendation: Recommendation) -> None:
        """Validates that a recommendation has rationale, non-empty impact, and evidence."""
        if not recommendation.title.strip():
            raise MalformedRecommendationError("Recommendation must have a non-empty title.")
        if not recommendation.rationale.strip():
            raise MalformedRecommendationError("Recommendation must specify a rationale.")
        if not recommendation.expected_impact.strip():
            raise MalformedRecommendationError("Recommendation must declare an expected impact.")
        ReflectionValidator.validate_confidence_score(recommendation.confidence, "Recommendation confidence")

    @staticmethod
    def validate_critique(critique: SelfCritique) -> None:
        """Validates self critique consistency and ensures absence of circular references."""
        for finding in critique.findings:
            ReflectionValidator.validate_confidence_score(finding.confidence, f"Finding {finding.finding_id}")
            if finding.category == "CIRCULAR_REASONING" and not finding.evidence:
                raise InconsistentEvidenceError("Circular reasoning finding must provide evidence.")

    @staticmethod
    def validate_artifacts(artifacts: list[LearningArtifact]) -> None:
        """Rejects duplicate learning artifact IDs or titles."""
        seen_ids = set()
        for art in artifacts:
            if art.artifact_id in seen_ids:
                raise DuplicateLearningArtifactError(f"Duplicate artifact ID detected: {art.artifact_id}")
            seen_ids.add(art.artifact_id)
            ReflectionValidator.validate_confidence_score(art.confidence_score, f"Artifact {art.artifact_id}")
