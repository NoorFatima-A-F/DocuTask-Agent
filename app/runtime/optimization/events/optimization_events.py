"""
Phase 13.6 Optimization & Economic Orchestration Domain Events (ARIA-EOP).
Typed immutable events capturing optimization lifecycles, resource allocations, routing decisions, and budget reservations.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


def _gen_id(prefix: str = "opt_evt") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseOptimizationEvent(BaseModel):
    event_id: str = Field(default_factory=_gen_id)
    mission_id: Optional[str] = "mission-001"
    event_type: str
    timestamp: str = Field(default_factory=_now_iso)
    payload: Dict[str, Any] = Field(default_factory=dict)
    provenance_hash: Optional[str] = None


# Alias for domain event base
OptimizationDomainEvent = BaseOptimizationEvent


class OptimizationStarted(BaseOptimizationEvent):
    event_type: str = "optimization.started"
    objective: str = "BALANCED_UTILITY"
    budget_limit_usd: float = 1.00
    deadline_ms: float = 5000.0


class OptimizationCompleted(BaseOptimizationEvent):
    event_type: str = "optimization.completed"
    optimization_id: str = Field(default_factory=lambda: _gen_id("opt"))
    selected_strategy_id: str = "strat_wavefront_opt"
    utility_score: float = 0.945
    expected_cost_usd: float = 0.0032
    expected_duration_ms: float = 1850.0


class StrategyEvaluated(BaseOptimizationEvent):
    event_type: str = "optimization.strategy.evaluated"
    strategy_id: str = "strat_01"
    strategy_name: str = "High-Throughput Wavefront"
    utility_score: float = 0.92
    cost_usd: float = 0.003
    latency_ms: float = 1900.0


class ResourceAllocated(BaseOptimizationEvent):
    event_type: str = "optimization.resource.allocated"
    resource_id: str = "worker-pool-ocr-01"
    resource_type: str = "WORKER_POOL"
    allocated_units: int = 4
    remaining_capacity: int = 12


class ModelSelected(BaseOptimizationEvent):
    event_type: str = "optimization.routing.model_selected"
    task_id: str = "task-extract-01"
    model_id: str = "gemini-1.5-flash"
    rationale: str = "Low complexity invoice suitable for high-speed Flash model."


class WorkerSelected(BaseOptimizationEvent):
    event_type: str = "optimization.routing.worker_selected"
    task_id: str = "task-ocr-01"
    worker_id: str = "worker-tesseract-pool-02"


class BudgetReserved(BaseOptimizationEvent):
    event_type: str = "optimization.budget.reserved"
    envelope_id: str = "env-mission-001"
    amount_usd: float = 0.05
    remaining_budget_usd: float = 0.95


class BudgetExceeded(BaseOptimizationEvent):
    event_type: str = "optimization.budget.exceeded"
    requested_usd: float = 1.20
    budget_limit_usd: float = 1.00


class ConstraintViolated(BaseOptimizationEvent):
    event_type: str = "optimization.constraint.violated"
    constraint_name: str = "MAX_LATENCY_MS"
    threshold: float = 3000.0
    actual_value: float = 3450.0


class SimulationCompleted(BaseOptimizationEvent):
    event_type: str = "optimization.simulation.completed"
    simulation_id: str = Field(default_factory=lambda: _gen_id("sim"))
    scenarios_evaluated: int = 5
    best_scenario_id: str = "scenario-parallel-4"


class OptimizationRejected(BaseOptimizationEvent):
    event_type: str = "optimization.rejected"
    reason: str = "Candidate violates minimum confidence constraint (0.85)"


class OptimizationApplied(BaseOptimizationEvent):
    event_type: str = "optimization.applied"
    optimization_id: str = Field(default_factory=lambda: _gen_id("opt"))
    runtime_directives_count: int = 4
