"""
Scientific Metric Calculator for DocuTask Agent.
Evaluates registered MetricDefinitions over raw RuntimeEvent streams, generating
auditable MetricProvenanceRecords with full statistical analysis and Merkle lineage.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.runtime.events.base import RuntimeEvent
from app.runtime.metrics.definitions import MetricUnit
from app.runtime.metrics.formulas import CANONICAL_FORMULAS
from app.runtime.metrics.provenance import MetricProvenanceRecord, compute_merkle_root
from app.runtime.metrics.registry import MetricRegistry, get_global_metric_registry
from app.runtime.metrics.sampling import EventSampler, SamplingRule
from app.runtime.metrics.statistics import ScientificStatisticsEngine, StatisticalSummary
from app.runtime.telemetry.store import TelemetryStore


class ScientificMetricCalculator:
    """
    Computes mathematically rigorous metrics from RuntimeEvents with full provenance.
    """

    def __init__(
        self,
        store: Optional[TelemetryStore] = None,
        registry: Optional[MetricRegistry] = None,
    ):
        self.store = store
        self.registry = registry or get_global_metric_registry()

    def calculate_metric(
        self,
        metric_id: str,
        events: List[RuntimeEvent],
        sampling_rule: Optional[SamplingRule] = None,
    ) -> MetricProvenanceRecord:
        """
        Calculates a single registered metric over the provided events.
        """
        defn = self.registry.get(metric_id)
        if not defn:
            raise ValueError(f"Metric '{metric_id}' is not registered in the MetricRegistry.")

        # 1. Apply sampling rule
        rule = sampling_rule or SamplingRule(
            filter_event_types=set(defn.required_events),
            window_type="ALL_SESSION",
        )
        sampled_events = EventSampler.sample_events(events, rule)
        obs_window = EventSampler.get_observation_window(sampled_events)
        raw_event_ids = [e.event_id for e in sampled_events]
        merkle_root = compute_merkle_root(raw_event_ids)

        # 2. Extract formula variables from events
        variables = self._extract_variables(metric_id, sampled_events, obs_window)

        # 3. Check for Zero-Fabrication minimum sample size
        if len(sampled_events) < defn.minimum_sample_size and defn.minimum_sample_size > 1:
            sentinel = "INSUFFICIENT_EVIDENCE"
            formula_spec = CANONICAL_FORMULAS.get(defn.formula_id)
            return MetricProvenanceRecord(
                metric_id=defn.id,
                metric_name=defn.name,
                metric_version=defn.version,
                value=0.0,
                formatted_value="[INSUFFICIENT_EVIDENCE]",
                unit=defn.unit.value,
                formula_id=defn.formula_id,
                formula_expression=defn.formula_expression,
                formula_latex=defn.formula_latex,
                variables_used=variables,
                raw_event_ids=raw_event_ids,
                sample_size=len(sampled_events),
                observation_window=obs_window,
                statistical_summary=None,
                merkle_events_root_sha256=merkle_root,
                sentinel_state=sentinel,
                tags=defn.tags,
            )

        # 4. Evaluate formula
        formula_spec = CANONICAL_FORMULAS.get(defn.formula_id)
        if not formula_spec:
            raise ValueError(f"Formula '{defn.formula_id}' not found in CANONICAL_FORMULAS.")

        raw_val = formula_spec.evaluator(variables)

        # 5. Extract series values for statistical distribution analysis if latency/time metric
        stat_summary: Optional[StatisticalSummary] = None
        series_vals = self._extract_series_for_stats(metric_id, sampled_events)
        if series_vals and len(series_vals) >= 2:
            stat_summary = ScientificStatisticsEngine.analyze_sample(series_vals)

        # 6. Format value string
        formatted = self._format_value(raw_val, defn.unit)

        return MetricProvenanceRecord(
            metric_id=defn.id,
            metric_name=defn.name,
            metric_version=defn.version,
            value=raw_val,
            formatted_value=formatted,
            unit=defn.unit.value,
            formula_id=defn.formula_id,
            formula_expression=defn.formula_expression,
            formula_latex=defn.formula_latex,
            variables_used=variables,
            raw_event_ids=raw_event_ids,
            sample_size=len(sampled_events),
            observation_window=obs_window,
            statistical_summary=stat_summary.to_dict() if stat_summary else None,
            merkle_events_root_sha256=merkle_root,
            sentinel_state=None,
            tags=defn.tags,
        )

    def calculate_all_mission_metrics(
        self,
        mission_id: str,
        events: List[RuntimeEvent],
    ) -> Dict[str, MetricProvenanceRecord]:
        """
        Evaluates all registered canonical metrics for a mission.
        """
        results: Dict[str, MetricProvenanceRecord] = {}
        for defn in self.registry.list_all():
            results[defn.id] = self.calculate_metric(defn.id, events)
        return results

    def _extract_variables(
        self,
        metric_id: str,
        events: List[RuntimeEvent],
        window: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Extracts variable bindings from the event stream.
        """
        vars: Dict[str, Any] = {}
        duration_sec = float(window.get("duration_seconds", 0.0))

        if metric_id == "worker_utilization":
            active_ms = sum(
                float(e.duration_ms or e.payload.get("duration_ms", 0.0))
                for e in events if "Worker" in e.event_type
            )
            # Allocated window = duration_sec * 1000 * max(1, worker_count)
            worker_ids = set(e.worker_id or e.agent_id for e in events if e.worker_id or e.agent_id)
            num_workers = max(1, len(worker_ids))
            allocated_ms = max(active_ms, duration_sec * 1000.0 * num_workers)
            vars["active_time_ms"] = active_ms
            vars["allocated_time_ms"] = allocated_ms

        elif metric_id == "planner_throughput":
            completed = sum(1 for e in events if "WorkerCompleted" in e.event_type)
            vars["completed_tasks"] = completed
            vars["planner_duration_sec"] = max(0.01, duration_sec)

        elif metric_id == "retry_rate":
            retries = sum(1 for e in events if "WorkerFailed" in e.event_type or "Retry" in e.event_type)
            attempts = sum(1 for e in events if "Worker" in e.event_type)
            vars["retries_count"] = retries
            vars["execution_attempts"] = max(1, attempts)

        elif metric_id == "reflection_frequency":
            reflections = sum(1 for e in events if "Reflection" in e.event_type or "Critique" in e.event_type)
            vars["reflection_count"] = reflections
            vars["mission_duration_minutes"] = max(0.01, duration_sec / 60.0)

        elif metric_id == "memory_hit_rate":
            hits = sum(
                1 for e in events
                if "Memory" in e.event_type and (e.payload.get("hit", True) or "Retrieved" in e.event_type)
            )
            queries = sum(1 for e in events if "Memory" in e.event_type)
            vars["memory_hits"] = hits
            vars["memory_queries"] = max(1, queries)

        elif metric_id == "task_completion_rate":
            completed = sum(1 for e in events if "WorkerCompleted" in e.event_type)
            started = sum(1 for e in events if "WorkerStarted" in e.event_type)
            vars["completed_tasks"] = completed
            vars["total_tasks"] = max(completed, started, 1)

        elif metric_id == "average_latency":
            latencies = [
                float(e.duration_ms or e.payload.get("duration_ms", 0.0))
                for e in events
                if (e.duration_ms or e.payload.get("duration_ms")) is not None
            ]
            vars["total_latency_ms"] = sum(latencies)
            vars["event_count"] = len(latencies)

        elif metric_id == "parallelism":
            durations = [float(e.duration_ms or 100.0) / 1000.0 for e in events if "Worker" in e.event_type]
            vars["worker_intervals_sum"] = sum(durations)
            vars["total_span_sec"] = max(0.01, duration_sec)

        elif metric_id == "recovery_rate":
            recoveries = sum(1 for e in events if "Resumed" in e.event_type or "StrategyChanged" in e.event_type)
            failures = sum(1 for e in events if "Failed" in e.event_type)
            vars["recoveries_count"] = recoveries
            vars["failures_count"] = failures

        elif metric_id == "token_efficiency":
            completed = sum(1 for e in events if "WorkerCompleted" in e.event_type)
            tokens = sum(int(e.payload.get("tokens_processed", 150)) for e in events)
            vars["completed_tasks"] = completed
            vars["total_tokens_thousands"] = max(0.01, tokens / 1000.0)

        return vars

    def _extract_series_for_stats(self, metric_id: str, events: List[RuntimeEvent]) -> List[float]:
        """
        Extracts numeric observation series for statistical dispersion estimation.
        """
        if metric_id in ("average_latency", "worker_utilization"):
            return [
                float(e.duration_ms or e.payload.get("duration_ms", 0.0))
                for e in events
                if (e.duration_ms or e.payload.get("duration_ms")) is not None
            ]
        elif metric_id == "token_efficiency":
            return [float(e.payload.get("tokens_processed", 0)) for e in events if "tokens_processed" in e.payload]
        return []

    def _format_value(self, value: float, unit: MetricUnit) -> str:
        """
        Formats numeric value according to its unit.
        """
        if unit == MetricUnit.PERCENTAGE:
            return f"{value * 100.0:.2f}%"
        elif unit == MetricUnit.MILLISECONDS:
            return f"{value:.1f} ms"
        elif unit == MetricUnit.SECONDS:
            return f"{value:.2f} s"
        elif unit == MetricUnit.HERTZ:
            return f"{value:.3f} Hz"
        elif unit == MetricUnit.USD:
            return f"${value:.4f}"
        elif unit == MetricUnit.RATIO:
            return f"{value:.3f}"
        return f"{value:.2f}"
