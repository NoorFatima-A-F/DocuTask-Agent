"""AI Failure Mode Classification Taxonomy (Part 3H.3.8.8).

Classifies AI error signatures into actionable operational categories with deterministic remediation policies.
"""

from __future__ import annotations

from typing import List

from app.platform_verification.ai_provider_health.domain.interfaces import (
    IAIFailureClassifier,
)
from app.platform_verification.ai_provider_health.domain.models import (
    AIFailureCategory,
    AIFailureClassificationItem,
    AIFailureClassificationReport,
)


class AIFailureClassifier(IAIFailureClassifier):
    """Classifies AI errors into structured categories and maps them to automated action workflows."""

    CLASSIFICATIONS: List[AIFailureClassificationItem] = [
        AIFailureClassificationItem(
            error_signature="HTTP_500_INTERNAL_SERVER_ERROR",
            http_status_code=500,
            category=AIFailureCategory.PROVIDER_UNAVAILABLE,
            prescribed_action="Transient failure: Execute exponential retry with max 3 attempts",
            queue_impact="Re-enqueue task with jitter delay",
            operator_alert_required=False,
        ),
        AIFailureClassificationItem(
            error_signature="HTTP_503_SERVICE_UNAVAILABLE",
            http_status_code=503,
            category=AIFailureCategory.PROVIDER_UNAVAILABLE,
            prescribed_action="Provider outage: Trigger automated multi-provider failover switch",
            queue_impact="Route inflight tasks to secondary provider",
            operator_alert_required=True,
        ),
        AIFailureClassificationItem(
            error_signature="HTTP_401_UNAUTHORIZED",
            http_status_code=401,
            category=AIFailureCategory.AUTHENTICATION_FAILURE,
            prescribed_action="Fatal auth error: Halt retries immediately, generate P1 SRE alert, rotate key",
            queue_impact="Pause document pipeline safely to prevent burn rate",
            operator_alert_required=True,
        ),
        AIFailureClassificationItem(
            error_signature="HTTP_429_RATE_LIMIT_EXCEEDED",
            http_status_code=429,
            category=AIFailureCategory.QUOTA_EXHAUSTION,
            prescribed_action="Capacity limit: Apply adaptive token-bucket backoff (14.4x burn dampener)",
            queue_impact="Hold pending tasks in durable Redis backpressure queue",
            operator_alert_required=False,
        ),
        AIFailureClassificationItem(
            error_signature="SCHEMA_VALIDATION_ERROR_UNPARSEABLE_JSON",
            http_status_code=200,
            category=AIFailureCategory.INVALID_RESPONSE,
            prescribed_action="Malformed payload: Attempt schema repair prompt, then fallback to secondary model",
            queue_impact="Re-drive task through LLM validation pipeline",
            operator_alert_required=False,
        ),
    ]

    def classify_error(self, status_code: int, error_msg: str) -> AIFailureClassificationItem:
        """Dynamically classifies an arbitrary runtime error into the taxonomy."""
        if status_code in (500, 502, 503, 504):
            return AIFailureClassificationItem(
                error_signature=f"HTTP_{status_code}_PROVIDER_ERROR",
                http_status_code=status_code,
                category=AIFailureCategory.PROVIDER_UNAVAILABLE,
                prescribed_action="Retry or Failover",
                queue_impact="Re-enqueue with backoff",
                operator_alert_required=status_code == 503,
            )
        elif status_code in (401, 403):
            return AIFailureClassificationItem(
                error_signature=f"HTTP_{status_code}_AUTH_ERROR",
                http_status_code=status_code,
                category=AIFailureCategory.AUTHENTICATION_FAILURE,
                prescribed_action="Halt retries and alert SRE",
                queue_impact="Pause queue safely",
                operator_alert_required=True,
            )
        elif status_code == 429:
            return AIFailureClassificationItem(
                error_signature="HTTP_429_RATE_LIMIT",
                http_status_code=429,
                category=AIFailureCategory.QUOTA_EXHAUSTION,
                prescribed_action="Exponential Backoff",
                queue_impact="Preserve in durable queue",
                operator_alert_required=False,
            )
        else:
            return AIFailureClassificationItem(
                error_signature="SCHEMA_QUALITY_ERROR",
                http_status_code=status_code,
                category=AIFailureCategory.INVALID_RESPONSE,
                prescribed_action="Validation retry / repair",
                queue_impact="Re-drive with stricter guardrails",
                operator_alert_required=False,
            )

    def classify_failures(self) -> AIFailureClassificationReport:
        items = list(self.CLASSIFICATIONS)
        covered_cats = {item.category for item in items}
        all_covered = len(covered_cats) == 4
        passed = len(items) >= 4 and all_covered

        return AIFailureClassificationReport(
            total_failure_patterns_classified=len(items),
            all_categories_covered=all_covered,
            classifications=items,
            passed=passed,
            details={
                "taxonomy_standard": "DocuTask LLMOps Failure Matrix v2.0",
                "categories": [c.value for c in AIFailureCategory],
            },
        )
