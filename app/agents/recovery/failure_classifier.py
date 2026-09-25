"""
Failure Classifier.
Classifies raw execution errors into canonical categories, severities, and recoverability scores.
"""

from app.agents.recovery.failure import (
    Failure,
    FailureCategory,
    FailureEvidence,
    FailureIdentity,
    FailureSeverity,
)


class FailureClassifier:
    """Classifies execution faults using deterministic pattern matching and telemetry."""

    def classify(self, identity: FailureIdentity, evidence: FailureEvidence) -> Failure:
        msg = evidence.error_message.lower()
        err_type = evidence.error_type.lower()

        # Categorize
        if "timeout" in msg or "timeout" in err_type or "deadline" in msg:
            category = FailureCategory.TIMEOUT_FAILURE
            severity = FailureSeverity.MEDIUM
            score = 0.8
            cause = "Task exceeded allotted execution deadline"
        elif "tool" in msg or "tool" in err_type or identity.tool_name is not None:
            category = FailureCategory.TOOL_FAILURE
            severity = FailureSeverity.MEDIUM
            score = 0.9
            cause = f"Tool failure encountered for tool '{identity.tool_name or 'unknown'}'"
        elif "worker" in msg or "exhaust" in msg:
            category = FailureCategory.WORKER_FAILURE
            severity = FailureSeverity.HIGH
            score = 0.75
            cause = "Worker pool exhaustion or worker failure"
        elif "token" in msg or "budget" in msg:
            category = FailureCategory.TOKEN_BUDGET_FAILURE
            severity = FailureSeverity.HIGH
            score = 0.5
            cause = "Execution exceeded configured token budget ceiling"
        elif "memory" in msg or "oom" in msg:
            category = FailureCategory.MEMORY_FAILURE
            severity = FailureSeverity.HIGH
            score = 0.6
            cause = "Task exceeded memory quota"
        elif "checkpoint" in msg:
            category = FailureCategory.CHECKPOINT_FAILURE
            severity = FailureSeverity.HIGH
            score = 0.4
            cause = "Checkpoint capture or verification failed"
        elif "dependency" in msg or "deadlock" in msg:
            category = FailureCategory.DEPENDENCY_FAILURE
            severity = FailureSeverity.CRITICAL
            score = 0.3
            cause = "Dependency graph cycle or deadlock detected"
        else:
            category = FailureCategory.EXECUTION_FAILURE
            severity = FailureSeverity.MEDIUM
            score = 0.7
            cause = f"Execution runtime error: {evidence.error_message}"

        return Failure(
            identity=identity,
            category=category,
            severity=severity,
            confidence=0.95,
            recoverability_score=score,
            probable_cause=cause,
            evidence=evidence
        )
