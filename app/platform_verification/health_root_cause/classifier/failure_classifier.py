"""Failure & Severity Classifier (3H.4.2.3 & 3H.4.2.6).

Classifies diagnosed failures into 5 standard failure categories:
- Infrastructure Failure
- Dependency Failure
- Application Failure
- External Service Failure
- Performance Degradation

And assigns 4 incident severity levels:
- SEV-1 Critical (Total outage / DB down / data persistence blocked)
- SEV-2 Major (Worker pool degraded / queue backlog growing)
- SEV-3 Minor (Single worker crash / isolated task failure)
- SEV-4 Warning (Transient latency spike / warning threshold)
"""

from typing import Dict, Any
from ..domain.models import FailureCategory, IncidentSeverity


class FailureClassifier:
    """Classifies failure events and assigns severity."""

    def __init__(self):
        self._category_map: Dict[str, FailureCategory] = {
            "postgresql": FailureCategory.DEPENDENCY,
            "redis_queue": FailureCategory.DEPENDENCY,
            "worker_fleet": FailureCategory.APPLICATION,
            "gemini_ai": FailureCategory.EXTERNAL_SERVICE,
            "ocr_provider": FailureCategory.EXTERNAL_SERVICE,
            "api_gateway": FailureCategory.INFRASTRUCTURE,
            "document_storage": FailureCategory.INFRASTRUCTURE,
        }

    def classify_category(self, component: str, reason: str) -> FailureCategory:
        """Determines failure category based on component and reason."""
        if "latency" in reason.lower() or "backlog" in reason.lower():
            return FailureCategory.PERFORMANCE_DEGRADATION
        return self._category_map.get(component, FailureCategory.APPLICATION)

    def classify_severity(self, component: str, category: FailureCategory, is_cascade: bool = False) -> IncidentSeverity:
        """Determines incident severity level based on failure blast radius."""
        if component in ["postgresql", "document_storage"] and category == FailureCategory.DEPENDENCY:
            return IncidentSeverity.SEV_1_CRITICAL
        if component in ["redis_queue", "worker_fleet", "gemini_ai"]:
            return IncidentSeverity.SEV_2_MAJOR
        if category == FailureCategory.PERFORMANCE_DEGRADATION:
            return IncidentSeverity.SEV_4_WARNING
        return IncidentSeverity.SEV_3_MINOR
