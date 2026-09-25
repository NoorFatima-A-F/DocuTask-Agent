"""
Dataset Domain: 9 Dataset Classifications, Versioning, Immutability Checksums, and Lineage DAGs.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class DatasetClassification(str, Enum):
    HAPPY_PATH = "HAPPY_PATH"
    BOUNDARY = "BOUNDARY"
    NEGATIVE = "NEGATIVE"
    ADVERSARIAL = "ADVERSARIAL"
    REGRESSION = "REGRESSION"
    STRESS = "STRESS"
    SYNTHETIC = "SYNTHETIC"
    PRODUCTION_SNAPSHOT = "PRODUCTION_SNAPSHOT"
    BENCHMARK = "BENCHMARK"


class DatasetLineage(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"lin_{uuid.uuid4().hex[:8]}")
    dataset_version_id: str
    original_sources: List[str] = Field(default_factory=list)
    transformation_pipeline: List[str] = Field(default_factory=list)
    generators_used: List[str] = Field(default_factory=list)
    anonymization_applied: bool = True
    validation_status: str = "PASSED"
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetVersion(BaseModel):
    dataset_version_id: str = Field(default_factory=lambda: f"dver_{uuid.uuid4().hex[:8]}")
    dataset_id: str
    semantic_version: str = "1.0.0"
    checksum_sha256: str
    item_count: int = 100
    size_bytes: int = 102400
    schema_version: str = "1.0.0"
    storage_location: str = "cas://datasets/verified"
    integrity_status: str = "VERIFIED"
    lineage: Optional[DatasetLineage] = None
    creator: str = "Data Engineer"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Dataset(BaseModel):
    dataset_id: str = Field(default_factory=lambda: f"dset_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    purpose: str
    classification: DatasetClassification = DatasetClassification.HAPPY_PATH
    owner: str = "AI Data Governance"
    source: str = "Gold Standard Ground Truth"
    current_version: str = "1.0.0"
    tags: List[str] = Field(default_factory=list)
    versions: List[DatasetVersion] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
