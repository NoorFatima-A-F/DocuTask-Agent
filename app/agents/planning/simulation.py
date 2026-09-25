"""
Planning Dry-Run Simulation Models.
Defines PlanningSimulation, SimulationResult, SimulationTrace, BottleneckPrediction, and ResourceForecast.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.agents.planning.contracts import Plan


class BottleneckPrediction(BaseModel):
    """Predicted execution bottleneck node."""
    node_id: str
    reason: str
    expected_delay_seconds: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class ResourceForecast(BaseModel):
    """Forecasted peak resource consumption during plan execution."""
    peak_tokens: int = Field(default=0, ge=0)
    peak_memory_mb: float = Field(default=128.0, ge=0.0)
    estimated_total_cost_usd: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class SimulationTrace(BaseModel):
    """Step-by-step execution simulation trace log."""
    step: int
    node_id: str
    simulated_duration_seconds: float = Field(default=0.0, ge=0.0)
    state_diff: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class SimulationResult(BaseModel):
    """Aggregate simulation outcome result."""
    is_feasible: bool = Field(default=True)
    total_simulated_duration_seconds: float = Field(default=0.0, ge=0.0)
    bottlenecks: List[BottleneckPrediction] = Field(default_factory=list)
    resource_forecast: ResourceForecast = Field(default_factory=ResourceForecast)
    traces: List[SimulationTrace] = Field(default_factory=list)
    model_config = {"frozen": True}


class PlanningSimulation:
    """Dry-run simulation engine simulating plan DAG execution deterministically."""

    @staticmethod
    def simulate(plan: Plan) -> SimulationResult:
        traces: List[SimulationTrace] = []
        total_duration = 0.0

        for i, (node_id, node) in enumerate(plan.graph.nodes.items(), start=1):
            dur = node.timeout_seconds
            total_duration += dur
            traces.append(SimulationTrace(step=i, node_id=node_id, simulated_duration_seconds=dur))

        forecast = ResourceForecast(
            peak_tokens=plan.statistics.estimated_tokens,
            estimated_total_cost_usd=plan.statistics.estimated_cost_usd
        )

        return SimulationResult(
            is_feasible=True,
            total_simulated_duration_seconds=total_duration,
            resource_forecast=forecast,
            traces=traces
        )
