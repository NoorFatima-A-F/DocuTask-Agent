"""
Metric Definitions and Registry Models for DocuTask Agent.
Defines strongly-typed, immutable metric definitions with required event types,
sampling rules, aggregation types, mathematical formulas, and scientific provenance requirements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class AggregationType(str, Enum):
    SUM = "SUM"
    MEAN = "MEAN"
    MEDIAN = "MEDIAN"
    RATIO = "RATIO"
    RATE = "RATE"
    PERCENTILE = "PERCENTILE"
    EWMA = "EWMA"
    COUNT = "COUNT"
    BAYESIAN_FUSION = "BAYESIAN_FUSION"


class MetricUnit(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    MILLISECONDS = "MILLISECONDS"
    SECONDS = "SECONDS"
    COUNT = "COUNT"
    RATIO = "RATIO"
    HERTZ = "HERTZ"
    BYTES = "BYTES"
    USD = "USD"
    TOKENS = "TOKENS"
    PROBABILITY = "PROBABILITY"


@dataclass(frozen=True)
class SamplingRule:
    """
    Defines how events are sampled from the runtime event stream for a metric.
    """
    window_type: str = "SLIDING_COUNT"  # SLIDING_COUNT, SLIDING_TIME, TUMBLING, ALL_SESSION
    window_size: int = 100
    filter_event_types: Set[str] = field(default_factory=set)
    filter_agent_ids: Optional[Set[str]] = None
    min_samples: int = 1


@dataclass(frozen=True)
class MetricDefinition:
    """
    Authoritative First-Class Metric Definition.
    No metric may be computed or rendered without a registered MetricDefinition.
    """
    id: str
    name: str
    description: str
    category: str  # EXECUTION, PLANNING, MEMORY, STATISTICAL, QUALITY, RESOURCE
    formula_id: str
    formula_expression: str
    formula_latex: str
    required_events: List[str] = field(default_factory=list)
    variables: List[str] = field(default_factory=list)
    aggregation_type: AggregationType = AggregationType.RATIO
    unit: MetricUnit = MetricUnit.RATIO
    minimum_sample_size: int = 5
    confidence_level: float = 0.95
    version: str = "2.0"
    tags: List[str] = field(default_factory=list)
    is_zero_trust_validated: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "formula_id": self.formula_id,
            "formula_expression": self.formula_expression,
            "formula_latex": self.formula_latex,
            "required_events": self.required_events,
            "variables": self.variables,
            "aggregation_type": self.aggregation_type.value,
            "unit": self.unit.value,
            "minimum_sample_size": self.minimum_sample_size,
            "confidence_level": self.confidence_level,
            "version": self.version,
            "tags": self.tags,
            "is_zero_trust_validated": self.is_zero_trust_validated,
        }
