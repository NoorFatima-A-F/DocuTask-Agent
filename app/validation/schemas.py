"""
Validation Subsystem Pydantic Schemas.
Defines gold dataset annotations, evaluation metric outputs, regression results, and evidence records.
Includes SHA-256 cryptographic hash chaining attributes for tamper-evident evidence auditing.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4
from pydantic import BaseModel, Field


class FieldAnnotation(BaseModel):
    """Annotation schema for a single extracted field."""
    field_name: str = Field(..., description="Target JSON field name")
    expected_value: Any = Field(..., description="Ground truth expected value")
    data_type: str = Field("string", description="Field data type ('string', 'number', 'array', 'boolean', 'object')")
    required: bool = Field(True, description="Whether field is strictly required")
    confidence_expectation: float = Field(0.9, description="Target minimum extraction confidence")


class DatasetMetadata(BaseModel):
    """Metadata describing a gold evaluation dataset entry."""
    document_id: str = Field(..., description="Unique dataset document identifier")
    document_type: str = Field(..., description="Document type category (invoice, receipt, contract, etc.)")
    page_count: int = Field(1, description="Page count")
    language: str = Field("eng", description="Primary document language")
    source: str = Field("synthetic_gold_standard", description="Dataset origin or provider")
    difficulty_level: str = Field("medium", description="Document difficulty ('easy', 'medium', 'hard')")


class GoldDatasetItem(BaseModel):
    """Gold standard dataset entry containing raw OCR text and ground truth annotations."""
    metadata: DatasetMetadata
    ocr_text: str = Field(..., description="Raw input OCR text string")
    ground_truth_json: Dict[str, Any] = Field(..., description="Ground truth target JSON object")
    annotations: List[FieldAnnotation] = Field(default_factory=list, description="Field-level validation rules")


class MetricEvaluationResult(BaseModel):
    """Calculated metric evaluation scores for an extraction run."""
    total_fields: int
    correct_fields: int
    missing_fields: int
    hallucinated_fields: int
    field_accuracy: float
    exact_match_accuracy: float
    schema_compliance_rate: float
    missing_field_rate: float
    hallucination_rate: float
    precision: float
    recall: float
    f1_score: float
    average_confidence: float
    confidence_correctness: float


class EvidenceRecord(BaseModel):
    """Structured evidence record proving evaluation execution results with SHA-256 hash chaining."""
    test_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = Field("production_audit", description="Execution environment")
    software_version: str = Field("1.0.0", description="App software version")
    model_version: str = Field("gemini-1.5-flash", description="LLM provider and model identifier")
    input_artifact: str = Field(..., description="Reference to input dataset item or filename")
    expected_behavior: Dict[str, Any] = Field(..., description="Ground truth target data")
    actual_behavior: Dict[str, Any] = Field(..., description="Actual AI extracted JSON output")
    metrics: MetricEvaluationResult
    pass_fail: str = Field("PASS", description="Overall evaluation verdict ('PASS' or 'FAIL')")
    evidence_location: str = Field(..., description="Path to persisted evidence JSON artifact")
    result_hash: str = Field("", description="SHA-256 cryptographic digest of record content")
    previous_hash: str = Field("GENESIS_HASH", description="SHA-256 hash of previous evidence record in chain")


class RegressionComparison(BaseModel):
    """Regression comparison result between baseline and current evaluation run."""
    run_id: str = Field(default_factory=lambda: str(uuid4()))
    baseline_version: str
    current_version: str
    baseline_accuracy: float
    current_accuracy: float
    accuracy_delta: float
    regression_severity: str = Field("NONE", description="'NONE', 'MINOR' (<2%), 'WARNING' (2-5%), 'CRITICAL' (>5%)")
    is_regression: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)
