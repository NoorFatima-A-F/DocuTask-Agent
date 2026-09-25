"""
Scientific Feature Store - Feature Registry
Declares canonical feature schemas, physical bounds, types, default imputations, and semantic categories.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class FeatureCategory(str, Enum):
    TELEMETRY = "telemetry"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    RESOURCE = "resource"
    COST = "cost"
    COMPLIANCE = "compliance"
    UNCERTAINTY = "uncertainty"


class NormalizationType(str, Enum):
    MIN_MAX = "min_max"
    Z_SCORE = "z_score"
    LOG = "log"
    SIGMOID = "sigmoid"
    IDENTITY = "identity"


@dataclass(frozen=True)
class FeatureDefinition:
    name: str
    category: FeatureCategory
    data_type: type
    min_bound: float
    max_bound: float
    default_value: float
    normalization_type: NormalizationType
    description: str
    unit: str = ""
    is_required: bool = True


# 16 Canonical Runtime Features as defined by QDIOP / SDIOP specification
CANONICAL_FEATURES: Dict[str, FeatureDefinition] = {
    "ocr_confidence": FeatureDefinition(
        name="ocr_confidence",
        category=FeatureCategory.QUALITY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.85,
        normalization_type=NormalizationType.IDENTITY,
        description="Confidence score output from OCR engine",
        unit="prob",
    ),
    "schema_validation_score": FeatureDefinition(
        name="schema_validation_score",
        category=FeatureCategory.QUALITY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=1.0,
        normalization_type=NormalizationType.IDENTITY,
        description="Proportion of extracted fields passing strict schema validation",
        unit="ratio",
    ),
    "latency_p95_ms": FeatureDefinition(
        name="latency_p95_ms",
        category=FeatureCategory.PERFORMANCE,
        data_type=float,
        min_bound=0.0,
        max_bound=60000.0,
        default_value=1200.0,
        normalization_type=NormalizationType.MIN_MAX,
        description="Historical p95 execution latency in milliseconds",
        unit="ms",
    ),
    "historical_success_rate": FeatureDefinition(
        name="historical_success_rate",
        category=FeatureCategory.PERFORMANCE,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.95,
        normalization_type=NormalizationType.IDENTITY,
        description="Empirical historical success rate for this task and domain",
        unit="prob",
    ),
    "retry_count": FeatureDefinition(
        name="retry_count",
        category=FeatureCategory.TELEMETRY,
        data_type=float,
        min_bound=0.0,
        max_bound=10.0,
        default_value=0.0,
        normalization_type=NormalizationType.MIN_MAX,
        description="Number of retries executed so far for the task",
        unit="count",
    ),
    "memory_similarity": FeatureDefinition(
        name="memory_similarity",
        category=FeatureCategory.QUALITY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.5,
        normalization_type=NormalizationType.IDENTITY,
        description="Vector cosine similarity to recalled episodic and semantic memories",
        unit="similarity",
    ),
    "document_complexity": FeatureDefinition(
        name="document_complexity",
        category=FeatureCategory.QUALITY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.5,
        normalization_type=NormalizationType.IDENTITY,
        description="Structural and visual complexity index of the document",
        unit="index",
    ),
    "worker_reliability": FeatureDefinition(
        name="worker_reliability",
        category=FeatureCategory.PERFORMANCE,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.98,
        normalization_type=NormalizationType.IDENTITY,
        description="Assigned worker empirical uptime and execution reliability",
        unit="prob",
    ),
    "gpu_load": FeatureDefinition(
        name="gpu_load",
        category=FeatureCategory.RESOURCE,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.25,
        normalization_type=NormalizationType.IDENTITY,
        description="Current normalized GPU compute load factor",
        unit="ratio",
    ),
    "queue_length": FeatureDefinition(
        name="queue_length",
        category=FeatureCategory.RESOURCE,
        data_type=float,
        min_bound=0.0,
        max_bound=1000.0,
        default_value=5.0,
        normalization_type=NormalizationType.LOG,
        description="Number of pending tasks in the execution queue",
        unit="count",
    ),
    "api_cost_usd": FeatureDefinition(
        name="api_cost_usd",
        category=FeatureCategory.COST,
        data_type=float,
        min_bound=0.0,
        max_bound=10.0,
        default_value=0.015,
        normalization_type=NormalizationType.MIN_MAX,
        description="Direct API provider cost in USD",
        unit="usd",
    ),
    "token_count": FeatureDefinition(
        name="token_count",
        category=FeatureCategory.RESOURCE,
        data_type=float,
        min_bound=0.0,
        max_bound=200000.0,
        default_value=2500.0,
        normalization_type=NormalizationType.LOG,
        description="Total input and output tokens consumed",
        unit="tokens",
    ),
    "human_validation_rate": FeatureDefinition(
        name="human_validation_rate",
        category=FeatureCategory.QUALITY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.98,
        normalization_type=NormalizationType.IDENTITY,
        description="Historical approval rate during human-in-the-loop review",
        unit="prob",
    ),
    "compliance_flags": FeatureDefinition(
        name="compliance_flags",
        category=FeatureCategory.COMPLIANCE,
        data_type=float,
        min_bound=0.0,
        max_bound=5.0,
        default_value=0.0,
        normalization_type=NormalizationType.MIN_MAX,
        description="Count of compliance alerts or regulatory checks triggered",
        unit="count",
    ),
    "anomaly_score": FeatureDefinition(
        name="anomaly_score",
        category=FeatureCategory.UNCERTAINTY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.05,
        normalization_type=NormalizationType.IDENTITY,
        description="Statistical outlier score from feature distribution model",
        unit="score",
    ),
    "epistemic_uncertainty": FeatureDefinition(
        name="epistemic_uncertainty",
        category=FeatureCategory.UNCERTAINTY,
        data_type=float,
        min_bound=0.0,
        max_bound=1.0,
        default_value=0.1,
        normalization_type=NormalizationType.IDENTITY,
        description="Model uncertainty due to data scarcity or novel domain distribution",
        unit="uncertainty",
    ),
}


class FeatureRegistry:
    """Registry maintaining registered features and schemas."""

    def __init__(self):
        self._registry: Dict[str, FeatureDefinition] = dict(CANONICAL_FEATURES)

    def register(self, feature_def: FeatureDefinition) -> None:
        self._registry[feature_def.name] = feature_def

    def get(self, name: str) -> Optional[FeatureDefinition]:
        return self._registry.get(name)

    def list_all(self) -> List[FeatureDefinition]:
        return list(self._registry.values())

    def get_names(self) -> List[str]:
        return list(self._registry.keys())

    def get_defaults(self) -> Dict[str, float]:
        return {name: defn.default_value for name, defn in self._registry.items()}


feature_registry = FeatureRegistry()
