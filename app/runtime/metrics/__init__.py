"""
Scientific Metric Provenance, Explainable Confidence, and Statistical Engine.
"""

from app.runtime.metrics.definitions import (
    AggregationType,
    MetricDefinition,
    MetricUnit,
    SamplingRule,
)
from app.runtime.metrics.formulas import CANONICAL_FORMULAS, FormulaSpec
from app.runtime.metrics.statistics import (
    ScientificStatisticsEngine,
    StatisticalSummary,
)
from app.runtime.metrics.sampling import EventSampler
from app.runtime.metrics.confidence import (
    BayesianConfidenceEngine,
    BayesianConfidenceResult,
    EvidenceSignal,
)
from app.runtime.metrics.provenance import (
    MetricProvenanceRecord,
    compute_merkle_root,
)
from app.runtime.metrics.registry import (
    MetricRegistry,
    get_global_metric_registry,
)
from app.runtime.metrics.calculator import ScientificMetricCalculator
from app.runtime.metrics.validation import MetricValidator
from app.runtime.metrics.versioning import MetricVersionManager

__all__ = [
    "AggregationType",
    "MetricDefinition",
    "MetricUnit",
    "SamplingRule",
    "CANONICAL_FORMULAS",
    "FormulaSpec",
    "ScientificStatisticsEngine",
    "StatisticalSummary",
    "EventSampler",
    "BayesianConfidenceEngine",
    "BayesianConfidenceResult",
    "EvidenceSignal",
    "MetricProvenanceRecord",
    "compute_merkle_root",
    "MetricRegistry",
    "get_global_metric_registry",
    "ScientificMetricCalculator",
    "MetricValidator",
    "MetricVersionManager",
]
