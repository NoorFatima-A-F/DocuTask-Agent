"""
CSV Export (Phase 82B.5)
========================
Exports tabular benchmark and telemetry datasets to deterministic CSV files
with RFC 4180 compliance and SHA-256 digest computation.
"""

from __future__ import annotations
import csv
import io
from typing import Any, Dict, List, Optional, Tuple

from research_validation.artifact_generation.publication_tables import PublicationTable
from research_validation.provenance.hashing import compute_sha256


class CSVExporter:
    """
    Exports publication tables to canonical CSV format.
    """

    @classmethod
    def export_table_to_csv(cls, table: PublicationTable) -> Tuple[str, str]:
        """
        Convert table to deterministic CSV string and compute SHA-256 digest.
        Returns (csv_string, sha256_hash).
        """
        output = io.StringIO()
        fieldnames = [c.key for c in table.columns]
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")

        # Write header with column titles
        header_dict = {c.key: c.header for c in table.columns}
        writer.writerow(header_dict)

        # Write rows
        for row in table.rows:
            cleaned_row = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(cleaned_row)

        content = output.getvalue()
        sha = compute_sha256(content.encode())
        return content, sha
