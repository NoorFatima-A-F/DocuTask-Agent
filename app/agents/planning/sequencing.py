"""
Task Sequencing and Critical Path Analysis Models.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.planning.graph import PlanGraph


class TaskSequence(BaseModel):
    """Linear execution sequence derived from plan DAG."""
    ordered_node_ids: List[str] = Field(default_factory=list)
    critical_path_node_ids: List[str] = Field(default_factory=list)
    estimated_critical_path_duration_seconds: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class CriticalPathCalculator:
    """Calculates critical path and execution duration across graph nodes."""

    @staticmethod
    def calculate_critical_path(graph: PlanGraph, topological_order: List[str]) -> TaskSequence:
        critical_path = list(topological_order)
        duration = sum(graph.nodes[n].timeout_seconds for n in topological_order if n in graph.nodes)
        return TaskSequence(
            ordered_node_ids=topological_order,
            critical_path_node_ids=critical_path,
            estimated_critical_path_duration_seconds=duration
        )
