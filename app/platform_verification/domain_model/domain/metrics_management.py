"""
Metrics Domain: 5 High-Impact Metric Categories (Correctness, Performance, Reliability, AI Quality, Cost).
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class MetricCategory(str, Enum):
    CORRECTNESS = "CORRECTNESS"    # Accuracy, Precision, Recall, F1, Exact Match
    PERFORMANCE = "PERFORMANCE"    # Latency, Throughput, P95, P99
    RELIABILITY = "RELIABILITY"    # Failure Rate, MTBF, MTTR, Resilience
    AI_QUALITY = "AI_QUALITY"      # Grounding, Faithfulness, Hallucination, Citation Accuracy
    COST = "COST"                  # Token Usage, Compute Cost, Storage Cost


class MetricDefinition(BaseModel):
    metric_id: str = Field(default_factory=lambda: f"met_def_{uuid.uuid4().hex[:8]}")
    name: str
    category: MetricCategory
    formula: str
    unit: str = "ratio"
    version: str = "1.0.0"
    description: str = ""


class MetricResult(BaseModel):
    result_id: str = Field(default_factory=lambda: f"met_res_{uuid.uuid4().hex[:8]}")
    execution_id: str
    metric_id: str
    metric_name: str
    category: MetricCategory
    value: float
    unit: str
    confidence_score: float = 1.0
    passed: bool = True
    raw_samples_count: int = 1
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
