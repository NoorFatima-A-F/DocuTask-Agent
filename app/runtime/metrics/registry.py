"""
Central Metric Registry for DocuTask Agent.
Stores and validates all registered MetricDefinitions.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.runtime.metrics.definitions import (
    AggregationType,
    MetricDefinition,
    MetricUnit,
)
from app.runtime.metrics.formulas import CANONICAL_FORMULAS


class MetricRegistry:
    """
    Central repository of all metric definitions.
    """

    def __init__(self):
        self._definitions: Dict[str, MetricDefinition] = {}
        self._register_canonical_definitions()

    def _register_canonical_definitions(self):
        """
        Pre-registers all standard execution, planning, memory, and statistical metrics.
        """
        canonical_list = [
            MetricDefinition(
                id="worker_utilization",
                name="Worker Utilization",
                description="Percentage of allocated worker execution time actively utilized.",
                category="EXECUTION",
                formula_id="FORMULA_WORKER_UTILIZATION",
                formula_expression=CANONICAL_FORMULAS["FORMULA_WORKER_UTILIZATION"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_WORKER_UTILIZATION"].latex,
                required_events=["WorkerStarted", "WorkerPaused", "WorkerResumed", "WorkerCompleted"],
                variables=["active_time_ms", "allocated_time_ms"],
                aggregation_type=AggregationType.RATIO,
                unit=MetricUnit.PERCENTAGE,
                minimum_sample_size=2,
                confidence_level=0.95,
                version="2.0",
                tags=["runtime", "workers", "efficiency"],
            ),
            MetricDefinition(
                id="planner_throughput",
                name="Planner Throughput",
                description="Tasks completed per second of active planner runtime.",
                category="PLANNING",
                formula_id="FORMULA_PLANNER_THROUGHPUT",
                formula_expression=CANONICAL_FORMULAS["FORMULA_PLANNER_THROUGHPUT"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_PLANNER_THROUGHPUT"].latex,
                required_events=["PlannerStarted", "PlannerCompleted", "WorkerCompleted"],
                variables=["completed_tasks", "planner_duration_sec"],
                aggregation_type=AggregationType.RATE,
                unit=MetricUnit.HERTZ,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["planner", "throughput"],
            ),
            MetricDefinition(
                id="retry_rate",
                name="Execution Retry Rate",
                description="Fraction of worker execution attempts that triggered automatic retries.",
                category="EXECUTION",
                formula_id="FORMULA_RETRY_RATE",
                formula_expression=CANONICAL_FORMULAS["FORMULA_RETRY_RATE"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_RETRY_RATE"].latex,
                required_events=["WorkerStarted", "WorkerFailed", "WorkerCompleted"],
                variables=["retries_count", "execution_attempts"],
                aggregation_type=AggregationType.RATIO,
                unit=MetricUnit.PERCENTAGE,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["reliability", "fault-tolerance"],
            ),
            MetricDefinition(
                id="reflection_frequency",
                name="Reflection Frequency",
                description="Cognitive reflection and critique events per mission runtime minute.",
                category="QUALITY",
                formula_id="FORMULA_REFLECTION_FREQUENCY",
                formula_expression=CANONICAL_FORMULAS["FORMULA_REFLECTION_FREQUENCY"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_REFLECTION_FREQUENCY"].latex,
                required_events=["ReflectionStarted", "ReflectionCompleted", "CritiqueGenerated"],
                variables=["reflection_count", "mission_duration_minutes"],
                aggregation_type=AggregationType.RATE,
                unit=MetricUnit.HERTZ,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["cognition", "reflection"],
            ),
            MetricDefinition(
                id="memory_hit_rate",
                name="Memory Hit Rate",
                description="Recall accuracy and reuse rate from Episodic and Long-Term Memory.",
                category="MEMORY",
                formula_id="FORMULA_MEMORY_HIT_RATE",
                formula_expression=CANONICAL_FORMULAS["FORMULA_MEMORY_HIT_RATE"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_MEMORY_HIT_RATE"].latex,
                required_events=["MemoryRetrieved", "MemoryCreated", "InvariantApplied"],
                variables=["memory_hits", "memory_queries"],
                aggregation_type=AggregationType.RATIO,
                unit=MetricUnit.PERCENTAGE,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["memory", "experience"],
            ),
            MetricDefinition(
                id="task_completion_rate",
                name="Task Completion Rate",
                description="Proportion of total planned DAG nodes that have been successfully executed.",
                category="EXECUTION",
                formula_id="FORMULA_TASK_COMPLETION_RATE",
                formula_expression=CANONICAL_FORMULAS["FORMULA_TASK_COMPLETION_RATE"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_TASK_COMPLETION_RATE"].latex,
                required_events=["TaskGraphGenerated", "WorkerCompleted", "WorkerFailed"],
                variables=["completed_tasks", "total_tasks"],
                aggregation_type=AggregationType.RATIO,
                unit=MetricUnit.PERCENTAGE,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["dag", "progress"],
            ),
            MetricDefinition(
                id="average_latency",
                name="Average Event Latency",
                description="Sample mean execution latency across all worker spans.",
                category="STATISTICAL",
                formula_id="FORMULA_AVERAGE_LATENCY",
                formula_expression=CANONICAL_FORMULAS["FORMULA_AVERAGE_LATENCY"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_AVERAGE_LATENCY"].latex,
                required_events=["WorkerCompleted", "PlannerCompleted", "ReflectionCompleted"],
                variables=["total_latency_ms", "event_count"],
                aggregation_type=AggregationType.MEAN,
                unit=MetricUnit.MILLISECONDS,
                minimum_sample_size=2,
                confidence_level=0.95,
                version="2.0",
                tags=["latency", "performance"],
            ),
            MetricDefinition(
                id="parallelism",
                name="Worker Parallelism Factor",
                description="Mean concurrent workers executing tasks across observation window.",
                category="RESOURCE",
                formula_id="FORMULA_PARALLELISM",
                formula_expression=CANONICAL_FORMULAS["FORMULA_PARALLELISM"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_PARALLELISM"].latex,
                required_events=["WorkerStarted", "WorkerCompleted"],
                variables=["worker_intervals_sum", "total_span_sec"],
                aggregation_type=AggregationType.MEAN,
                unit=MetricUnit.COUNT,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["concurrency", "scaling"],
            ),
            MetricDefinition(
                id="recovery_rate",
                name="Autonomous Recovery Rate",
                description="Fraction of encountered failures autonomously recovered via replanning.",
                category="QUALITY",
                formula_id="FORMULA_RECOVERY_RATE",
                formula_expression=CANONICAL_FORMULAS["FORMULA_RECOVERY_RATE"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_RECOVERY_RATE"].latex,
                required_events=["WorkerFailed", "WorkerResumed", "StrategyChanged"],
                variables=["recoveries_count", "failures_count"],
                aggregation_type=AggregationType.RATIO,
                unit=MetricUnit.PERCENTAGE,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["self-healing", "resilience"],
            ),
            MetricDefinition(
                id="token_efficiency",
                name="Token Efficiency",
                description="Tasks successfully delivered per 1,000 language model tokens.",
                category="RESOURCE",
                formula_id="FORMULA_TOKEN_EFFICIENCY",
                formula_expression=CANONICAL_FORMULAS["FORMULA_TOKEN_EFFICIENCY"].expression,
                formula_latex=CANONICAL_FORMULAS["FORMULA_TOKEN_EFFICIENCY"].latex,
                required_events=["WorkerCompleted", "TelemetryUpdated"],
                variables=["completed_tasks", "total_tokens_thousands"],
                aggregation_type=AggregationType.RATE,
                unit=MetricUnit.RATIO,
                minimum_sample_size=1,
                confidence_level=0.95,
                version="2.0",
                tags=["tokens", "cost"],
            ),
        ]

        for defn in canonical_list:
            self.register(defn)

    def register(self, definition: MetricDefinition) -> None:
        self._definitions[definition.id] = definition

    def get(self, metric_id: str) -> Optional[MetricDefinition]:
        return self._definitions.get(metric_id)

    def list_all(self) -> List[MetricDefinition]:
        return list(self._definitions.values())

    def list_by_category(self, category: str) -> List[MetricDefinition]:
        return [d for d in self._definitions.values() if d.category == category]


_GLOBAL_METRIC_REGISTRY: Optional[MetricRegistry] = None


def get_global_metric_registry() -> MetricRegistry:
    global _GLOBAL_METRIC_REGISTRY
    if _GLOBAL_METRIC_REGISTRY is None:
        _GLOBAL_METRIC_REGISTRY = MetricRegistry()
    return _GLOBAL_METRIC_REGISTRY
