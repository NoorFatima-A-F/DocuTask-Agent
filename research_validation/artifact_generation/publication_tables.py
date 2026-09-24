"""
Publication Tables Generator (Phase 82B.5)
==========================================
Generates formatted scientific tables with standard errors, confidence intervals,
and effect sizes across datasets and baselines.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class TableColumn:
    key: str
    header: str
    alignment: str = "left"  # "left", "center", "right"


@dataclass(frozen=True)
class PublicationTable:
    table_id: str
    title: str
    caption: str
    columns: Tuple[TableColumn, ...]
    rows: Tuple[Dict[str, Any], ...]
    originating_experiment_ids: Tuple[str, ...]
    table_digest_sha256: str
    created_at_utc: str


class PublicationTableGenerator:
    """
    Synthesizes structured tabular data suitable for multi-format export.
    """

    @classmethod
    def create_benchmark_comparison_table(
        cls,
        dataset_results: List[Dict[str, Any]],
        title: str = "Document Understanding Benchmark Performance",
        caption: str = "Macro F1, ANLS, and Latency percentiles across canonical evaluation sets.",
        originating_exp_id: str = "exp_default",
    ) -> PublicationTable:
        """Construct a standardized benchmark comparison table."""
        now_str = datetime.now(timezone.utc).isoformat()
        tbl_id = f"tbl_bench_{originating_exp_id[:8]}"

        columns = (
            TableColumn("dataset", "Dataset", "left"),
            TableColumn("samples", "Samples", "right"),
            TableColumn("precision", "Precision", "right"),
            TableColumn("recall", "Recall", "right"),
            TableColumn("f1_score", "F1 Score (95% CI)", "right"),
            TableColumn("p99_latency_ms", "P99 Latency (ms)", "right"),
            TableColumn("evidence_level", "Evidence Quality", "center"),
        )

        rows = tuple(dataset_results)
        payload = {
            "title": title,
            "columns": [c.header for c in columns],
            "rows": list(rows),
            "exp_id": originating_exp_id,
        }
        digest = hash_canonical_json(payload)

        return PublicationTable(
            table_id=tbl_id,
            title=title,
            caption=caption,
            columns=columns,
            rows=rows,
            originating_experiment_ids=(originating_exp_id,),
            table_digest_sha256=digest,
            created_at_utc=now_str,
        )
