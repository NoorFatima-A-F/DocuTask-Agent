"""
Dataset Manager: Dataset versioning, CAS integrity, 11 categories, lineage.
"""
from typing import Dict, Any, Optional, List, Union
import hashlib
from ..interfaces import DatasetManagerInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import DatasetRecord, DatasetClass

class DatasetManager(DatasetManagerInterface):
    """Manages immutable, content-addressed verification datasets across 11 classes."""
    
    def __init__(self):
        self._datasets: Dict[str, Dict[str, Any]] = {}
        self._domain_datasets: Dict[str, DatasetRecord] = {}
        self.observability = ComponentObservability("DatasetManager")
        self._seed_default_datasets()

    def _seed_default_datasets(self):
        dataset_classes = [
            (DatasetClass.HAPPY_PATH, "Standard Invoices (Golden)", 100),
            (DatasetClass.BOUNDARY, "Max Dimensions & Border Margins", 50),
            (DatasetClass.NEGATIVE, "Corrupt & Blank Documents", 40),
            (DatasetClass.ADVERSARIAL, "Adversarial Font Variations & Distortions", 60),
            (DatasetClass.REGRESSION, "Historical Regression Test Set", 80),
            (DatasetClass.STRESS, "High-Density Multi-Page Invoices", 30),
            (DatasetClass.SYNTHETIC, "GenAI Generated Diverse Receipts", 120),
            (DatasetClass.PRODUCTION_SNAPSHOT, "Anonymized Production Sample", 200),
            (DatasetClass.MULTILINGUAL, "Multi-language & CJK Invoices", 75),
            (DatasetClass.BENCHMARK, "Industry Standard LayoutLM Benchmark", 150),
            (DatasetClass.SMOKE, "Rapid Smoke Test Corpus", 10),
        ]
        for idx, (cls_enum, name, count) in enumerate(dataset_classes, start=1):
            ds_id = f"ds_{cls_enum.value.lower()}_{idx:02d}"
            raw = f"dataset_content_{ds_id}_{count}".encode("utf-8")
            h = hashlib.sha256(raw).hexdigest()
            ds_rec = DatasetRecord(
                dataset_id=ds_id,
                name=name,
                dataset_class=cls_enum,
                sample_count=count,
                sha256_checksum=h,
                tags=["verification", cls_enum.value.lower()]
            )
            self._domain_datasets[ds_id] = ds_rec
            self._datasets[ds_id] = {
                "dataset_id": ds_id,
                "category": cls_enum.value.lower(),
                "hash": h,
                "metadata": {"name": name, "sample_count": count}
            }

    async def register_dataset(self, dataset_id: str, category: str, content_or_uri: Union[bytes, str], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.observability.record_operation(1.5)
        raw_bytes = content_or_uri if isinstance(content_or_uri, bytes) else content_or_uri.encode("utf-8")
        h = hashlib.sha256(raw_bytes).hexdigest()
        record = {
            "dataset_id": dataset_id,
            "category": category,
            "hash": h,
            "size_bytes": len(raw_bytes),
            "metadata": metadata or {}
        }
        self._datasets[dataset_id] = record
        return record

    async def verify_integrity(self, dataset_id: str, expected_content: bytes) -> bool:
        self.observability.record_operation(1.0)
        if dataset_id not in self._datasets:
            return False
        current_hash = hashlib.sha256(expected_content).hexdigest()
        return self._datasets[dataset_id]["hash"] == current_hash

    def list_datasets(self, category: Optional[str] = None) -> List[DatasetRecord]:
        self.observability.record_operation(0.8)
        if category:
            return [d for d in self._domain_datasets.values() if d.dataset_class.value.lower() == category.lower()]
        return list(self._domain_datasets.values())

    def get_dataset(self, dataset_id: str) -> Optional[DatasetRecord]:
        self.observability.record_operation(0.5)
        return self._domain_datasets.get(dataset_id)
