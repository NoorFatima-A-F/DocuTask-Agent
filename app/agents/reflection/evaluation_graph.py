"""
Evaluation Graph DAG Representation.
Models dependency-driven evaluation stages to allow concurrent, parallelizable analysis of traces.
"""

from typing import Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.exceptions import InvalidEvaluationGraphError


class EvaluationStageNode(BaseModel):
    """An individual evaluation stage in the evaluation DAG."""
    stage_id: str
    evaluator_name: str
    dimension: str
    dependencies: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class EvaluationGraph(BaseModel):
    """Directed graph of evaluation stages ensuring ordered evaluation and metric readiness."""
    graph_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, EvaluationStageNode] = Field(default_factory=dict)

    def add_stage(self, stage: EvaluationStageNode) -> None:
        """Adds an evaluation stage."""
        self.nodes[stage.stage_id] = stage

    def get_execution_order(self) -> List[str]:
        """Calculates topological sort of evaluation stages."""
        in_degree: Dict[str, int] = {s_id: 0 for s_id in self.nodes}
        adj: Dict[str, List[str]] = {s_id: [] for s_id in self.nodes}

        for s_id, node in self.nodes.items():
            for dep in node.dependencies:
                if dep in adj:
                    adj[dep].append(s_id)
                    in_degree[s_id] += 1
                else:
                    raise InvalidEvaluationGraphError(f"Missing dependency {dep} for stage {s_id}")

        queue = [s_id for s_id, deg in in_degree.items() if deg == 0]
        ordered: List[str] = []

        while queue:
            curr = queue.pop(0)
            ordered.append(curr)
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if len(ordered) != len(self.nodes):
            raise InvalidEvaluationGraphError("Cycle detected in EvaluationGraph dependencies")

        return ordered
