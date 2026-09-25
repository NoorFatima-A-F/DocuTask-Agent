"""
Knowledge Graph for Phase 13.5 (ARLP-KIP).
Represents semantic relationships, dependencies, and taxonomy among knowledge records.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class KnowledgeNode(BaseModel):
    node_id: str
    label: str
    node_type: str = "RULE"
    properties: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str = "ENABLES"
    weight: float = 1.0


class KnowledgeGraph:
    """
    In-memory semantic graph of institutional knowledge rules, strategies, and evidence nodes.
    """

    def __init__(self):
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._edges: List[KnowledgeEdge] = []
        self._seed_default_graph()

    def _seed_default_graph(self):
        self.add_node("kn-ocr-shard", "Parallel OCR Sharding", "EXECUTION_RULE", {"confidence": 0.965})
        self.add_node("kn-smt-verify", "Dynamic SMT Verification", "VALIDATION_STRATEGY", {"confidence": 0.942})
        self.add_node("kn-retry-backoff", "Exponential Jitter Backoff", "RESILIENCE_STRATEGY", {"confidence": 0.978})
        self.add_node("kn-dag-optimizer", "Dynamic DAG Topology Optimizer", "PLANNER_POLICY", {"confidence": 0.955})

        self.add_edge("kn-ocr-shard", "kn-smt-verify", "PRODUCES_EVIDENCE", 0.95)
        self.add_edge("kn-ocr-shard", "kn-retry-backoff", "FALLS_BACK_TO", 0.85)
        self.add_edge("kn-dag-optimizer", "kn-ocr-shard", "GOVERNS", 0.98)

    def add_node(self, node_id: str, label: str, node_type: str = "RULE", properties: Optional[Dict[str, Any]] = None):
        self._nodes[node_id] = KnowledgeNode(
            node_id=node_id,
            label=label,
            node_type=node_type,
            properties=properties or {},
        )

    def add_edge(self, source_id: str, target_id: str, relation: str = "ENABLES", weight: float = 1.0):
        self._edges.append(
            KnowledgeEdge(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                weight=weight,
            )
        )

    def get_density(self) -> float:
        n = len(self._nodes)
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1)
        return len(self._edges) / max_edges

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_count": len(self._nodes),
            "edge_count": len(self._edges),
            "density": round(self.get_density(), 4),
            "nodes": [n.model_dump() for n in self._nodes.values()],
            "edges": [e.model_dump() for e in self._edges],
        }


knowledge_graph = KnowledgeGraph()
