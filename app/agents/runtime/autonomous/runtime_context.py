"""
Runtime Context for Autonomous Agent Operating System.
Provides shared mutable state, telemetry, and checkpoint references across cognitive cycles.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.intelligence.goal.goal_specification import GoalSpecification
from app.agents.planning.execution_plan import ExecutionPlan
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph


@dataclass
class RuntimeContext:
    """Execution session state container for an autonomous execution cycle."""

    execution_id: str = field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:12]}")
    session_id: str = field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:8]}")
    document_id: str = ""
    goal_text: str = ""
    goal_spec: Optional[GoalSpecification] = None
    active_plan: Optional[ExecutionPlan] = None
    task_graph: Optional[DynamicTaskGraph] = None
    extracted_data: Dict[str, Any] = field(default_factory=dict)
    intermediate_results: Dict[str, Any] = field(default_factory=dict)
    errors_encountered: List[str] = field(default_factory=list)
    iteration_count: int = 0
    max_iterations: int = 5
    started_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    total_cost_usd: float = 0.0
    is_paused: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def elapsed_time_seconds(self) -> float:
        end = self.completed_at if self.completed_at else time.time()
        return end - self.started_at

    def record_error(self, error: str) -> None:
        self.errors_encountered.append(error)

    def set_output(self, key: str, value: Any) -> None:
        self.intermediate_results[key] = value
        if isinstance(value, dict):
            self.extracted_data.update(value)

    def get_output(self, key: str, default: Any = None) -> Any:
        return self.intermediate_results.get(key, default)
