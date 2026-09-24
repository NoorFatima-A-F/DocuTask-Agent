"""
Enterprise Workflow Simulator.
Performs dry-run simulations with mock capabilities to estimate expected duration, token cost, and failure probabilities.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from ..domain.models import TaskType, WorkflowDefinition
from ..compiler.compiler import WorkflowCompiler


@dataclass
class SimulationReport:
    workflow_id: str
    is_valid: bool
    estimated_duration_ms: float
    estimated_cost_cents: float
    total_tasks: int
    parallel_branches_count: int
    mock_results: Dict[str, Any] = field(default_factory=dict)
    potential_bottlenecks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "is_valid": self.is_valid,
            "estimated_duration_ms": round(self.estimated_duration_ms, 2),
            "estimated_cost_cents": round(self.estimated_cost_cents, 2),
            "total_tasks": self.total_tasks,
            "parallel_branches_count": self.parallel_branches_count,
            "potential_bottlenecks": self.potential_bottlenecks,
        }


class WorkflowSimulator:
    """Dry-run simulator for workflows."""

    @classmethod
    def simulate(cls, definition: WorkflowDefinition) -> SimulationReport:
        """Simulate workflow execution."""
        WorkflowCompiler.compile(definition)

        total_duration = 0.0
        total_cost = 0.0
        bottlenecks = []

        for task in definition.tasks:
            # Baseline estimation heuristics
            if task.type == TaskType.AI:
                task_dur = 1200.0  # ~1.2s
                task_cost = 0.15   # ~15 cents
            elif task.type == TaskType.HUMAN or task.type == TaskType.APPROVAL:
                task_dur = 3600000.0  # ~1 hour SLA
                task_cost = 0.0
                bottlenecks.append(f"Human gate '{task.id}' introduces external wait time")
            elif task.type == TaskType.CONNECTOR:
                task_dur = 250.0   # ~250ms
                task_cost = 0.01
            else:
                task_dur = 50.0    # ~50ms
                task_cost = 0.0

            total_duration += task_dur
            total_cost += task_cost

        return SimulationReport(
            workflow_id=definition.id,
            is_valid=True,
            estimated_duration_ms=total_duration,
            estimated_cost_cents=total_cost,
            total_tasks=len(definition.tasks),
            parallel_branches_count=len([t for t in definition.tasks if t.type == TaskType.PARALLEL]),
            potential_bottlenecks=bottlenecks,
        )
