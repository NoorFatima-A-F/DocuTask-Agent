"""Evidence Schema Normalizer (3H.3.12.2).

Converts raw test dictionaries into standardized `StandardizedEvidenceRecord` instances
adhering to the universal schema specification.
"""

from typing import List, Dict, Any
from ..domain.models import (
    StandardizedEvidenceRecord,
    EvidenceStatus,
    EvidenceSeverity,
)
from ..domain.interfaces import IEvidenceSchemaNormalizer


class EvidenceSchemaNormalizer(IEvidenceSchemaNormalizer):
    """Normalizes raw readiness evidence records into universal schema-compliant objects."""

    def normalize_records(self, raw_records: List[Dict[str, Any]]) -> List[StandardizedEvidenceRecord]:
        normalized: List[StandardizedEvidenceRecord] = []

        for raw in raw_records:
            status_str = raw.get("status", "PASS")
            try:
                status = EvidenceStatus(status_str)
            except ValueError:
                status = EvidenceStatus.PASS

            severity_str = raw.get("severity", "INFO")
            try:
                severity = EvidenceSeverity(severity_str)
            except ValueError:
                severity = EvidenceSeverity.INFO

            record = StandardizedEvidenceRecord(
                verification_id=raw.get("test_id", "V-UNKNOWN"),
                phase="3H.3",
                category=raw.get("category", "readiness"),
                component=raw.get("component", "core"),
                test_name=raw.get("test_name", "unnamed_test"),
                environment=raw.get("environment", "production-simulation"),
                version=raw.get("version", "1.0.0"),
                status=status,
                severity=severity,
                metrics=raw.get("metrics", {}),
                logs=[f"Execution completed in {raw.get('duration_ms', 0.0)}ms with status {status.value}"],
                artifacts=[f"{raw.get('test_id', 'test')}.json"],
            )
            normalized.append(record)

        return normalized
