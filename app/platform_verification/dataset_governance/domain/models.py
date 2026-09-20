"""
Domain Models for Enterprise Verification Dataset Architecture & Test Data Governance.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
import uuid


class DatasetCategory(str, Enum):
    HAPPY_PATH = "HAPPY_PATH"
    BOUNDARY = "BOUNDARY"
    NEGATIVE = "NEGATIVE"
    ADVERSARIAL = "ADVERSARIAL"
    REGRESSION = "REGRESSION"
    PERFORMANCE = "PERFORMANCE"
    MULTILINGUAL = "MULTILINGUAL"
    SYNTHETIC = "SYNTHETIC"
    PRODUCTION_REPRESENTATIVE = "PRODUCTION_REPRESENTATIVE"


class DatasetLifecycleState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    USED = "USED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class DataSensitivityLevel(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"


class DatasetPermission(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    MODIFY = "MODIFY"
    EXPORT = "EXPORT"
    APPROVE = "APPROVE"


class ReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DatasetSample(BaseModel):
    sample_id: str = Field(default_factory=lambda: f"smp_{uuid.uuid4().hex[:8]}")
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    language: str = "en"
    partition: str = "eval"  # train, eval, test, benchmark
    content_hash: str = ""

    def compute_hash(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()

    def __init__(self, **data):
        super().__init__(**data)
        if not self.content_hash and self.content:
            self.content_hash = self.compute_hash()


class GroundTruthAnnotation(BaseModel):
    annotation_id: str = Field(default_factory=lambda: f"ann_{uuid.uuid4().hex[:8]}")
    sample_id: str
    expected_output: Dict[str, Any]
    label: str = "VALID"
    annotator: str = "Principal Verification Annotator"
    confidence: float = 1.0
    review_status: ReviewStatus = ReviewStatus.APPROVED
    reviewed_by: Optional[str] = "QA Lead"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetMetadata(BaseModel):
    dataset_id: str
    name: str
    version: str = "1.0.0"
    description: str
    owner: str = "Data Governance Squad"
    purpose: str
    category: DatasetCategory
    sensitivity: DataSensitivityLevel = DataSensitivityLevel.INTERNAL
    schema_version: str = "1.0.0"
    license: str = "Proprietary Enterprise"
    sample_count: int = 0
    ground_truth_count: int = 0
    lifecycle_state: DatasetLifecycleState = DatasetLifecycleState.CREATED
    manifest_hash: str = ""
    created_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetQualityReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"dqr_{uuid.uuid4().hex[:8]}")
    dataset_id: str
    version: str
    accuracy_score: float = 1.0       # Weight: 30%
    completeness_score: float = 1.0   # Weight: 20%
    diversity_score: float = 1.0      # Weight: 20%
    consistency_score: float = 1.0    # Weight: 15%
    freshness_score: float = 1.0      # Weight: 15%
    composite_quality_score: float = 1.0
    is_acceptable: bool = True
    issues_detected: List[str] = Field(default_factory=list)
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetSnapshot(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"ds_snap_{uuid.uuid4().hex[:8]}")
    dataset_id: str
    version: str
    manifest_hash: str
    sample_count: int
    schema_version: str
    ground_truth_version: str = "1.0.0"
    ground_truth_hash: str
    captured_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DatasetLineageNode(BaseModel):
    lineage_id: str = Field(default_factory=lambda: f"lin_{uuid.uuid4().hex[:8]}")
    dataset_id: str
    version: str
    source_origin: str
    transformation_step: str
    applied_cleaners: List[str] = Field(default_factory=list)
    annotated_by: str
    usage_verifications: List[str] = Field(default_factory=list)
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
