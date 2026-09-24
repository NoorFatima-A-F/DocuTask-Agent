"""
Evidence Schema Versioning & Migration Framework.
Enforces semantic versioning (SemVer 2.0.0) across all evidence, statistical,
benchmark, evaluation protocol, and report schemas with automated migration pipelines.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class SchemaType(str, Enum):
    EVIDENCE_ITEM = "EVIDENCE_ITEM"
    STATISTICS_REPORT = "STATISTICS_REPORT"
    BENCHMARK_PROFILE = "BENCHMARK_PROFILE"
    EVALUATION_PROTOCOL = "EVALUATION_PROTOCOL"
    VISUALIZATION = "VISUALIZATION"
    REPORT = "REPORT"


@dataclass
class SchemaMetadata:
    """Schema descriptor containing SemVer specification."""

    schema_type: SchemaType
    version: str  # e.g. "2.0.0"
    schema_url: str
    required_fields: List[str]
    is_deprecated: bool = False


class EvidenceSchemaVersioning:
    """
    Validates evidence payload compatibility and executes schema migrations across versions.
    """

    SCHEMAS: Dict[Tuple[SchemaType, str], SchemaMetadata] = {
        (SchemaType.EVIDENCE_ITEM, "1.0.0"): SchemaMetadata(
            schema_type=SchemaType.EVIDENCE_ITEM,
            version="1.0.0",
            schema_url="https://schema.aaos.dev/v1/evidence-item.json",
            required_fields=["evidence_id", "title", "evidence_type", "source"],
        ),
        (SchemaType.EVIDENCE_ITEM, "2.0.0"): SchemaMetadata(
            schema_type=SchemaType.EVIDENCE_ITEM,
            version="2.0.0",
            schema_url="https://schema.aaos.dev/v2/evidence-item.json",
            required_fields=["evidence_id", "title", "evidence_type", "source", "item_hash", "reproducibility"],
        ),
        (SchemaType.STATISTICS_REPORT, "2.0.0"): SchemaMetadata(
            schema_type=SchemaType.STATISTICS_REPORT,
            version="2.0.0",
            schema_url="https://schema.aaos.dev/v2/statistics-report.json",
            required_fields=["sample_size", "mean", "median", "ci_95_t", "percentiles"],
        ),
        (SchemaType.BENCHMARK_PROFILE, "2.0.0"): SchemaMetadata(
            schema_type=SchemaType.BENCHMARK_PROFILE,
            version="2.0.0",
            schema_url="https://schema.aaos.dev/v2/benchmark-profile.json",
            required_fields=["benchmark_name", "iterations", "statistics", "calibration", "environment"],
        ),
    }

    @classmethod
    def validate_payload(
        cls,
        schema_type: SchemaType,
        version: str,
        payload: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """Validates payload against required schema fields."""
        schema_key = (schema_type, version)
        if schema_key not in cls.SCHEMAS:
            return False, [f"Unrecognized schema version: {schema_type.value}:{version}"]

        schema = cls.SCHEMAS[schema_key]
        missing = [f for f in schema.required_fields if f not in payload]

        if missing:
            return False, [f"Missing required fields for {schema_type.value} v{version}: {missing}"]

        return True, []

    @classmethod
    def migrate_v1_to_v2_evidence_item(cls, v1_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Migrates a v1.0.0 evidence item to the v2.0.0 enterprise schema."""
        v2 = dict(v1_payload)
        if "reproducibility" not in v2:
            v2["reproducibility"] = "DETERMINISTIC"
        if "schema_version" not in v2:
            v2["schema_version"] = "2.0.0"
        return v2
