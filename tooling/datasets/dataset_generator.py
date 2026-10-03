"""
Synthetic Dataset Generator and Lineage Manager.
Produces deterministic test datasets across all 10 standard dataset classes with SHA-256 CAS hashes.
"""
import hashlib
import json
from typing import Dict, Any, List

DATASET_CLASSES = [
    "HAPPY_PATH", "BOUNDARY", "NEGATIVE", "ADVERSARIAL",
    "MULTILINGUAL", "REGRESSION", "STRESS", "BENCHMARK",
    "SYNTHETIC", "PRODUCTION_SNAPSHOT"
]

class DatasetGenerator:
    """Generates parameterized test records for verification testing."""
    @staticmethod
    def generate_dataset(dataset_class: str, sample_count: int = 10) -> Dict[str, Any]:
        if dataset_class not in DATASET_CLASSES:
            raise ValueError(f"Unknown dataset class: {dataset_class}")

        records: List[Dict[str, Any]] = []
        for i in range(sample_count):
            records.append({
                "record_id": f"rec_{dataset_class.lower()}_{i}",
                "input_payload": f"Sample document payload {i} for {dataset_class}",
                "expected_entities": {"invoice_total": 100.0 + i, "currency": "USD"},
                "metadata": {"class": dataset_class, "index": i}
            })

        payload_bytes = json.dumps(records, sort_keys=True).encode("utf-8")
        sha256_hash = hashlib.sha256(payload_bytes).hexdigest()

        return {
            "dataset_class": dataset_class,
            "sample_count": sample_count,
            "sha256_fingerprint": sha256_hash,
            "records": records
        }
