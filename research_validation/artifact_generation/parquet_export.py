"""
Parquet Dataset Export (Phase 82B.5)
====================================
Columnar dataset export schemas and serialization for large-scale scientific
telemetry and multi-run benchmark datasets.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.artifact_generation.publication_tables import PublicationTable
from research_validation.provenance.hashing import hash_canonical_json, compute_sha256


@dataclass(frozen=True)
class ParquetSchemaField:
    name: str
    field_type: str  # "STRING", "FLOAT64", "INT64", "BOOLEAN"
    nullable: bool = True


@dataclass(frozen=True)
class ColumnarDatasetManifest:
    dataset_name: str
    schema_fields: Tuple[ParquetSchemaField, ...]
    row_count: int
    data_payload_json: str
    dataset_sha256: str
    created_at_utc: str


class ParquetDatasetExporter:
    """
    Handles columnar dataset definitions and metadata serialization.
    """

    @classmethod
    def export_table_columnar(
        cls,
        table: PublicationTable,
        dataset_name: Optional[str] = None,
    ) -> ColumnarDatasetManifest:
        """Convert publication table into columnar dataset representation."""
        now_str = datetime.now(timezone.utc).isoformat()
        dname = dataset_name or f"dataset_{table.table_id}"

        # Infer schema fields
        fields = []
        for col in table.columns:
            # Check first non-null row type
            inferred_type = "STRING"
            for row in table.rows:
                v = row.get(col.key)
                if isinstance(v, float):
                    inferred_type = "FLOAT64"
                    break
                elif isinstance(v, int):
                    inferred_type = "INT64"
                    break
                elif isinstance(v, bool):
                    inferred_type = "BOOLEAN"
                    break
            fields.append(ParquetSchemaField(name=col.key, field_type=inferred_type))

        # Convert to columnar dictionary: col_name -> list of values
        columnar_data = {c.key: [row.get(c.key) for row in table.rows] for c in table.columns}
        data_json = json.dumps(columnar_data, sort_keys=True)
        sha = compute_sha256(data_json.encode())

        return ColumnarDatasetManifest(
            dataset_name=dname,
            schema_fields=tuple(fields),
            row_count=len(table.rows),
            data_payload_json=data_json,
            dataset_sha256=sha,
            created_at_utc=now_str,
        )
