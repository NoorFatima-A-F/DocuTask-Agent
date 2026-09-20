"""
Benchmark Evaluator.
Benchmarks completed agent runs against standard service-level objectives (SLOs) and performance baselines.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class BenchmarkCriteria(BaseModel):
    """Target thresholds for benchmark compliance."""
    max_duration_ms: float = 15000.0
    max_cost_usd: float = 0.25
    max_tokens: int = 10000
    min_task_success_rate: float = 0.95

    model_config = {"frozen": True}


class BenchmarkReport(BaseModel):
    """Outcome of benchmarking against baseline criteria."""
    passed_all: bool
    duration_passed: bool
    cost_passed: bool
    tokens_passed: bool
    success_rate_passed: bool
    benchmark_score: float = Field(ge=0.0, le=1.0)
    details: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class BenchmarkEvaluator:
    """Evaluates execution against target performance and budget benchmarks."""

    def __init__(self, criteria: BenchmarkCriteria = BenchmarkCriteria()):
        self.criteria = criteria

    def evaluate_benchmark(self, trace: ExecutionTraceEnvelope) -> BenchmarkReport:
        """Evaluates trace against preset benchmark thresholds."""
        dur_ok = trace.total_duration_ms <= self.criteria.max_duration_ms
        cost_ok = trace.cost_usd <= self.criteria.max_cost_usd

        total_tokens = trace.token_usage.get("prompt_tokens", 0) + trace.token_usage.get("completion_tokens", 0)
        tokens_ok = total_tokens <= self.criteria.max_tokens

        total_tasks = len(trace.tasks)
        completed = sum(1 for t in trace.tasks if t.status == "COMPLETED")
        rate = completed / total_tasks if total_tasks > 0 else (1.0 if trace.final_state == "COMPLETED" else 0.0)
        rate_ok = rate >= self.criteria.min_task_success_rate

        passed_all = dur_ok and cost_ok and tokens_ok and rate_ok
        score = sum([dur_ok, cost_ok, tokens_ok, rate_ok]) / 4.0

        return BenchmarkReport(
            passed_all=passed_all,
            duration_passed=dur_ok,
            cost_passed=cost_ok,
            tokens_passed=tokens_ok,
            success_rate_passed=rate_ok,
            benchmark_score=score,
            details={
                "actual_duration_ms": trace.total_duration_ms,
                "actual_cost_usd": trace.cost_usd,
                "actual_tokens": total_tokens,
                "actual_success_rate": rate
            }
        )
