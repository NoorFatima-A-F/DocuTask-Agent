"""
Failure Analyzer.
Evaluates failure patterns across recent execution sessions and identifies repeating failure clusters.
"""

from typing import List
from app.agents.recovery.failure import Failure, FailureCategory


class FailureAnalyzer:
    """Analyzes failure frequency and detects recurring error patterns."""

    def is_transient(self, failure: Failure) -> bool:
        """Determines if the failure is likely transient (e.g. timeout, network jitter)."""
        transient_categories = {
            FailureCategory.TIMEOUT_FAILURE,
            FailureCategory.TOOL_FAILURE,
            FailureCategory.PROVIDER_FAILURE
        }
        return failure.category in transient_categories and failure.recoverability_score >= 0.7
