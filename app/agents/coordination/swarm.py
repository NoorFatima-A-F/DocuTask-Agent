"""
Swarm Intelligence and Execution Engine.
Supports fan-out/fan-in, map-reduce task partitioning, cooperative solving, and ensemble decision aggregation.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.agent import Agent


class SwarmExecutionPattern(str, Enum):
    """Patterns of swarm intelligence execution."""
    FAN_OUT_FAN_IN = "FAN_OUT_FAN_IN"
    MAP_REDUCE = "MAP_REDUCE"
    COOPERATIVE_SOLVING = "COOPERATIVE_SOLVING"
    COMPETITIVE_SOLVING = "COMPETITIVE_SOLVING"
    ENSEMBLE_VOTING = "ENSEMBLE_VOTING"


class SwarmTask(BaseModel):
    """Task item distributed across swarm agents."""
    task_id: str
    input_data: Any
    assigned_agent_id: Optional[UUID] = None

    model_config = {"frozen": True}


class SwarmResult(BaseModel):
    """Aggregated output from swarm execution."""
    swarm_id: UUID = Field(default_factory=uuid4)
    pattern: SwarmExecutionPattern
    individual_results: Dict[str, Any] = Field(default_factory=dict)
    aggregated_output: Any = None
    participating_agents_count: int = 0

    model_config = {"frozen": True}


class SwarmEngine:
    """Orchestrates swarm workflows (fan-out/fan-in, map-reduce, and ensemble)."""

    def fan_out(self, items: List[Any], swarm_agents: List[Agent]) -> List[SwarmTask]:
        """Partitions input items across available swarm agents in round-robin fashion."""
        if not swarm_agents:
            return []

        tasks: List[SwarmTask] = []
        agent_count = len(swarm_agents)
        for i, item in enumerate(items):
            assigned_agent = swarm_agents[i % agent_count]
            tasks.append(SwarmTask(
                task_id=f"swarm_subtask_{i}",
                input_data=item,
                assigned_agent_id=assigned_agent.agent_id
            ))
        return tasks

    def fan_in_aggregate(
        self,
        subtask_results: Dict[str, Any],
        reducer: Optional[Callable[[List[Any]], Any]] = None
    ) -> Any:
        """Aggregates distributed subtask results into a single synthesized payload."""
        values = list(subtask_results.values())
        if reducer:
            return reducer(values)
        return values

    def ensemble_decision(self, agent_outputs: List[Dict[str, Any]], key: str = "decision") -> Any:
        """Determines majority consensus across competitive/ensemble agent outputs."""
        if not agent_outputs:
            return None

        votes: Dict[Any, int] = {}
        for out in agent_outputs:
            val = out.get(key)
            if val is not None:
                votes[val] = votes.get(val, 0) + 1

        if not votes:
            return None
        return max(votes, key=votes.get)
