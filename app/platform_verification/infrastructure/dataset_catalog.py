"""
Versioned Dataset Catalog with Integrity Checksums
"""
import hashlib
from typing import Dict, Any, List

class DatasetCatalog:
    def __init__(self):
        self._datasets: Dict[str, Dict[str, Any]] = {}
        self._seed_default_datasets()

    def _seed_default_datasets(self):
        default_ds = {
            "v1.0-gold": {
                "dataset_name": "Enterprise Invoice & Financial Benchmark",
                "version": "v1.0-gold",
                "sample_count": 500,
                "domain": "FINANCIAL_DOCUMENTS",
                "checksum": hashlib.sha256(b"DocuTask-Gold-Standard-Dataset-v1.0").hexdigest(),
                "test_cases": [
                    {"doc_id": "inv-001", "ground_truth_total": 12500.50, "vendor": "Acme Corp"},
                    {"doc_id": "inv-002", "ground_truth_total": 450.00, "vendor": "Global Logistics"},
                    {"doc_id": "inv-003", "ground_truth_total": 8920.00, "vendor": "TechSupply Inc"}
                ]
            }
        }
        self._datasets = default_ds

    def get_dataset(self, version: str = "v1.0-gold") -> Dict[str, Any]:
        return self._datasets.get(version, self._datasets["v1.0-gold"])

    def list_datasets(self) -> List[Dict[str, Any]]:
        return list(self._datasets.values())

dataset_catalog = DatasetCatalog()
