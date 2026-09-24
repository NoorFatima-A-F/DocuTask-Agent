"""
Decision Graph (Decision DAG) Subsystem.
Constructs directed acyclic causal graphs of planner decisions and deliberate state transitions.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.runtime.decision.provenance_engine import DecisionRecord


class DecisionGraphNode(BaseModel):
    id: str
    label: str
    decision_type: str
    decision_record: DecisionRecord
    status: str = "CONFIRMED"
    confidence: float
    assigned_worker: str


class DecisionGraphEdge(BaseModel):
    id: str
    source: str
    target: str
    causal_relation: str = "INFORMS"  # INFORMS, CONSTRAINS, ENABLES, MUTATES


class DecisionGraph(BaseModel):
    mission_id: str
    nodes: List[DecisionGraphNode] = Field(default_factory=list)
    edges: List[DecisionGraphEdge] = Field(default_factory=list)
    root_decision_id: Optional[str] = None
    total_decisions: int = 0


class DecisionGraphBuilder:
    """Builds a DecisionGraph from a list of DecisionRecords."""

    @staticmethod
    def build_graph(mission_id: str, decisions: List[DecisionRecord]) -> DecisionGraph:
        nodes: List[DecisionGraphNode] = []
        edges: List[DecisionGraphEdge] = []
        root_id: Optional[str] = None

        # Sort chronologically
        sorted_decisions = sorted(decisions, key=lambda d: d.timestamp)

        for idx, d in enumerate(sorted_decisions):
            node = DecisionGraphNode(
                id=d.decision_id,
                label=d.selected_plan,
                decision_type=d.goal,
                decision_record=d,
                confidence=d.confidence,
                assigned_worker=d.assigned_worker,
            )
            nodes.append(node)

            if d.parent_decision_id:
                edges.append(DecisionGraphEdge(
                    id=f"edge_{d.parent_decision_id}_{d.decision_id}",
                    source=d.parent_decision_id,
                    target=d.decision_id,
                    causal_relation="INFORMS",
                ))
            elif idx > 0:
                # Link sequential decisions if no explicit parent is set
                prev_d = sorted_decisions[idx - 1]
                edges.append(DecisionGraphEdge(
                    id=f"edge_{prev_d.decision_id}_{d.decision_id}",
                    source=prev_d.decision_id,
                    target=d.decision_id,
                    causal_relation="INFORMS",
                ))
            else:
                root_id = d.decision_id

        return DecisionGraph(
            mission_id=mission_id,
            nodes=nodes,
            edges=edges,
            root_decision_id=root_id,
            total_decisions=len(nodes),
        )
