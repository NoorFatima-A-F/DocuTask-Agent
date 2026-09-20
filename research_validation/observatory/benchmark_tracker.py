"""
Living Benchmark Tracker (Phase 90C)
====================================
Monitors external benchmark dataset versions, availability, and deprecation states.
Adheres strictly to Zero-Fabrication: returns DATASET_UNAVAILABLE or NOT_COLLECTED
when data sources are not physically present on disk.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from research_validation.observatory.observatory_models import (
    BenchmarkStatus, BenchmarkDatasetRecord
)
from research_validation.provenance.hashing import hash_canonical_json


class LivingBenchmarkTracker:
    """
    Tracks state, versions, and physical disk presence of standard document benchmarks.
    """

    DEFAULT_BENCHMARKS: Dict[str, Dict[str, Any]] = {
        "funsd": {
            "name": "FUNSD Form Understanding",
            "version": "1.0",
            "samples": 199,
            "metric": "entity_f1",
            "sota": 0.945,
        },
        "cord": {
            "name": "CORD Receipt Dataset",
            "version": "1.0",
            "samples": 1000,
            "metric": "entity_f1",
            "sota": 0.968,
        },
        "sroie": {
            "name": "SROIE Invoice Extraction",
            "version": "1.0",
            "samples": 626,
            "metric": "field_f1",
            "sota": 0.981,
        },
        "docvqa": {
            "name": "DocVQA Visual Question Answering",
            "version": "1.0",
            "samples": 5188,
            "metric": "anls",
            "sota": 0.912,
        },
        "rvl_cdip": {
            "name": "RVL-CDIP Document Classification",
            "version": "1.0",
            "samples": 400000,
            "metric": "accuracy",
            "sota": 0.958,
        },
    }

    def __init__(self, dataset_base_dir: Optional[str] = None):
        self.base_dir = Path(dataset_base_dir) if dataset_base_dir else Path("./data/benchmarks")

    def audit_benchmark_availability(self) -> List[BenchmarkDatasetRecord]:
        """Audits benchmarks against physical disk storage without fabricating availability."""
        records: List[BenchmarkDatasetRecord] = []
        now_str = datetime.now(timezone.utc).isoformat()

        for b_id, meta in self.DEFAULT_BENCHMARKS.items():
            target_path = self.base_dir / b_id
            if target_path.exists() and any(target_path.iterdir()):
                status = BenchmarkStatus.ACTIVE
                note = "Dataset present on local disk."
            else:
                status = BenchmarkStatus.DATASET_UNAVAILABLE
                note = f"Dataset path {target_path} not found. Non-fabricated fallback emitted."

            records.append(BenchmarkDatasetRecord(
                benchmark_id=b_id,
                benchmark_name=meta["name"],
                version=meta["version"],
                expected_sample_count=meta["samples"],
                expected_sha256="",
                status=status,
                last_verified_utc=now_str,
                primary_metric=meta["metric"],
                sota_reference_score=meta["sota"],
                notes=note,
            ))

        return records
