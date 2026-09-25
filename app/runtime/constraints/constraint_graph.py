"""
Scientific Constraints - Constraint Graph
Represents constraint dependency graphs, detecting binding constraints and conflict cycles.
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class ConstraintNode:
    id: str
    name: str
    constraint_type: str  # HARD or SOFT
    expression: str
    threshold: float
    is_binding: bool = False
    slack: float = 0.0


class ConstraintGraph:
    """Dependency graph for operational and legal constraints."""

    def __init__(self):
        self.nodes: Dict[str, ConstraintNode] = {}
        self.edges: List[Tuple[str, str, str]] = []  # (from_id, to_id, relation)

    def add_constraint(self, node: ConstraintNode) -> None:
        self.nodes[node.id] = node

    def add_dependency(self, source_id: str, target_id: str, relation: str = "constrains") -> None:
        self.edges.append((source_id, target_id, relation))

    def detect_conflicts(self) -> List[str]:
        """Detects contradictory constraint specifications (e.g. min_accuracy=0.99 with budget=0.0001)."""
        conflicts = []
        if "budget" in self.nodes and "accuracy" in self.nodes:
            b_thresh = self.nodes["budget"].threshold
            a_thresh = self.nodes["accuracy"].threshold
            if b_thresh < 0.001 and a_thresh > 0.95:
                conflicts.append("Infeasible trade-off: Ultra-low budget (<$0.001) conflicts with ultra-high accuracy (>0.95)")
        return conflicts

    def get_graph_data(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "type": n.constraint_type,
                    "expression": n.expression,
                    "threshold": n.threshold,
                    "is_binding": n.is_binding,
                    "slack": round(n.slack, 4),
                }
                for n in self.nodes.values()
            ],
            "edges": [{"from": e[0], "to": e[1], "relation": e[2]} for e in self.edges],
        }
