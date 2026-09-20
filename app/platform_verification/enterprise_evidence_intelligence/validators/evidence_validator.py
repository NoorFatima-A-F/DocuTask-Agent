"""
Phase 3P: Standardized Evidence Validator.
"""

from typing import List

from ..domain.interfaces import IEvidenceValidator
from ..domain.models import StandardizedEvidenceItem


class EvidenceValidator(IEvidenceValidator):
    """
    Validates that every evidence item conforms to the strict Phase 3P Universal Schema.
    """

    def validate(self, item: StandardizedEvidenceItem) -> bool:
        if not item.id or not item.id.startswith("EV-"):
            return False
        if not item.type or not item.category:
            return False
        if not item.component or not item.test_name:
            return False
        if not isinstance(item.metrics, dict):
            return False
        if not isinstance(item.artifacts, list):
            return False
        return True

    def validate_batch(self, items: List[StandardizedEvidenceItem]) -> bool:
        return all(self.validate(item) for item in items)
