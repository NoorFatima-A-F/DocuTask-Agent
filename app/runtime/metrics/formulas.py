"""
Deterministic Mathematical Formulas for DocuTask Agent.
Provides explicit equation mappings, LaTeX representations, and deterministic evaluators.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass(frozen=True)
class FormulaSpec:
    """
    Specification of a deterministic mathematical formula.
    """
    formula_id: str
    name: str
    expression: str
    latex: str
    description: str
    variables: List[str]
    evaluator: Callable[[Dict[str, Any]], float]


def _eval_worker_utilization(vars: Dict[str, Any]) -> float:
    active = float(vars.get("active_time_ms", 0.0))
    allocated = float(vars.get("allocated_time_ms", 0.0))
    if allocated <= 0.0:
        return 0.0
    return min(1.0, max(0.0, active / allocated))


def _eval_planner_throughput(vars: Dict[str, Any]) -> float:
    completed = float(vars.get("completed_tasks", 0.0))
    duration_sec = float(vars.get("planner_duration_sec", 0.0))
    if duration_sec <= 0.0:
        return 0.0
    return completed / duration_sec


def _eval_retry_rate(vars: Dict[str, Any]) -> float:
    retries = float(vars.get("retries_count", 0.0))
    attempts = float(vars.get("execution_attempts", 0.0))
    if attempts <= 0.0:
        return 0.0
    return min(1.0, retries / attempts)


def _eval_reflection_frequency(vars: Dict[str, Any]) -> float:
    reflections = float(vars.get("reflection_count", 0.0))
    duration_min = float(vars.get("mission_duration_minutes", 0.0))
    if duration_min <= 0.0:
        return 0.0
    return reflections / duration_min


def _eval_memory_hit_rate(vars: Dict[str, Any]) -> float:
    hits = float(vars.get("memory_hits", 0.0))
    queries = float(vars.get("memory_queries", 0.0))
    if queries <= 0.0:
        return 0.0
    return min(1.0, hits / queries)


def _eval_task_completion_rate(vars: Dict[str, Any]) -> float:
    completed = float(vars.get("completed_tasks", 0.0))
    total = float(vars.get("total_tasks", 0.0))
    if total <= 0.0:
        return 0.0
    return min(1.0, completed / total)


def _eval_average_latency(vars: Dict[str, Any]) -> float:
    total_latency_ms = float(vars.get("total_latency_ms", 0.0))
    event_count = float(vars.get("event_count", 0.0))
    if event_count <= 0.0:
        return 0.0
    return total_latency_ms / event_count


def _eval_parallelism(vars: Dict[str, Any]) -> float:
    worker_intervals_sum = float(vars.get("worker_intervals_sum", 0.0))
    total_span_sec = float(vars.get("total_span_sec", 0.0))
    if total_span_sec <= 0.0:
        return 1.0
    return max(1.0, worker_intervals_sum / total_span_sec)


def _eval_recovery_rate(vars: Dict[str, Any]) -> float:
    recoveries = float(vars.get("recoveries_count", 0.0))
    failures = float(vars.get("failures_count", 0.0))
    if failures <= 0.0:
        return 1.0 if recoveries > 0 else 0.0
    return min(1.0, recoveries / failures)


def _eval_token_efficiency(vars: Dict[str, Any]) -> float:
    tasks = float(vars.get("completed_tasks", 0.0))
    tokens_k = float(vars.get("total_tokens_thousands", 0.0))
    if tokens_k <= 0.0:
        return 0.0
    return tasks / tokens_k


CANONICAL_FORMULAS: Dict[str, FormulaSpec] = {
    "FORMULA_WORKER_UTILIZATION": FormulaSpec(
        formula_id="FORMULA_WORKER_UTILIZATION",
        name="Worker Utilization Formula",
        expression="sum(active_worker_time) / sum(allocated_worker_time)",
        latex=r"\mathcal{U} = \frac{\sum_{i=1}^W t_{\text{active}, i}}{\sum_{i=1}^W t_{\text{allocated}, i}}",
        description="Ratio of total active execution duration to total allocated worker window duration.",
        variables=["active_time_ms", "allocated_time_ms"],
        evaluator=_eval_worker_utilization,
    ),
    "FORMULA_PLANNER_THROUGHPUT": FormulaSpec(
        formula_id="FORMULA_PLANNER_THROUGHPUT",
        name="Planner Throughput Formula",
        expression="completed_tasks / planner_duration_sec",
        latex=r"\mathcal{T}_P = \frac{N_{\text{completed}}}{\Delta t_{\text{planner}}}",
        description="Rate of successfully planned and completed tasks per second of planner runtime.",
        variables=["completed_tasks", "planner_duration_sec"],
        evaluator=_eval_planner_throughput,
    ),
    "FORMULA_RETRY_RATE": FormulaSpec(
        formula_id="FORMULA_RETRY_RATE",
        name="Execution Retry Rate Formula",
        expression="retries_count / execution_attempts",
        latex=r"\mathcal{R}_{\text{retry}} = \frac{N_{\text{retries}}}{N_{\text{attempts}}}",
        description="Fraction of worker execution attempts that required automatic replanning or retries.",
        variables=["retries_count", "execution_attempts"],
        evaluator=_eval_retry_rate,
    ),
    "FORMULA_REFLECTION_FREQUENCY": FormulaSpec(
        formula_id="FORMULA_REFLECTION_FREQUENCY",
        name="Reflection Frequency Formula",
        expression="reflection_count / mission_duration_minutes",
        latex=r"\mathcal{F}_{\text{refl}} = \frac{N_{\text{reflections}}}{\Delta t_{\text{minutes}}}",
        description="Frequency of cognitive reflection and critique events per mission runtime minute.",
        variables=["reflection_count", "mission_duration_minutes"],
        evaluator=_eval_reflection_frequency,
    ),
    "FORMULA_MEMORY_HIT_RATE": FormulaSpec(
        formula_id="FORMULA_MEMORY_HIT_RATE",
        name="Memory Hit Rate Formula",
        expression="memory_hits / memory_queries",
        latex=r"\mathcal{H}_{\text{mem}} = \frac{N_{\text{hits}}}{N_{\text{queries}}}",
        description="Empirical recall hit rate from Episodic, Long-Term, and Invariant memory stores.",
        variables=["memory_hits", "memory_queries"],
        evaluator=_eval_memory_hit_rate,
    ),
    "FORMULA_TASK_COMPLETION_RATE": FormulaSpec(
        formula_id="FORMULA_TASK_COMPLETION_RATE",
        name="Task Completion Rate Formula",
        expression="completed_tasks / total_tasks",
        latex=r"\mathcal{C}_{\text{task}} = \frac{N_{\text{completed}}}{N_{\text{total}}}",
        description="Fraction of total planned DAG nodes that have attained verified completion.",
        variables=["completed_tasks", "total_tasks"],
        evaluator=_eval_task_completion_rate,
    ),
    "FORMULA_AVERAGE_LATENCY": FormulaSpec(
        formula_id="FORMULA_AVERAGE_LATENCY",
        name="Average Event Latency Formula",
        expression="sum(latency_ms) / event_count",
        latex=r"\bar{\mathcal{L}} = \frac{1}{N} \sum_{i=1}^N \ell_i",
        description="Sample mean execution latency across all measured worker runtime spans.",
        variables=["total_latency_ms", "event_count"],
        evaluator=_eval_average_latency,
    ),
    "FORMULA_PARALLELISM": FormulaSpec(
        formula_id="FORMULA_PARALLELISM",
        name="Worker Parallelism Factor Formula",
        expression="sum(worker_intervals) / total_span_sec",
        latex=r"\mathcal{P} = \frac{1}{T} \int_0^T w(t) \, dt",
        description="Mean number of concurrent worker processes active across the observation period.",
        variables=["worker_intervals_sum", "total_span_sec"],
        evaluator=_eval_parallelism,
    ),
    "FORMULA_RECOVERY_RATE": FormulaSpec(
        formula_id="FORMULA_RECOVERY_RATE",
        name="Fault Recovery Rate Formula",
        expression="recoveries_count / failures_count",
        latex=r"\mathcal{R}_{\text{rec}} = \frac{N_{\text{recovered}}}{N_{\text{failed}}}",
        description="Fraction of runtime exceptions and schema violations autonomously recovered.",
        variables=["recoveries_count", "failures_count"],
        evaluator=_eval_recovery_rate,
    ),
    "FORMULA_TOKEN_EFFICIENCY": FormulaSpec(
        formula_id="FORMULA_TOKEN_EFFICIENCY",
        name="Token Cost Efficiency Formula",
        expression="completed_tasks / (total_tokens / 1000)",
        latex=r"\mathcal{E}_{\text{token}} = \frac{N_{\text{tasks}}}{10^{-3} \cdot \text{Tokens}}",
        description="Completed tasks produced per 1,000 language model tokens processed.",
        variables=["completed_tasks", "total_tokens_thousands"],
        evaluator=_eval_token_efficiency,
    ),
}
