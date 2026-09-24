"""Structural Causal Model (SCM) Engine for DocuTask ACOS.

Represents causal relationships as formal Structural Equations:
    X_i := f_i(PA_i, U_i)
with directed causal DAG topology, endogenous variables, and exogenous noise sources.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class CausalNode(BaseModel):
    """Variable node in a Structural Causal Model DAG."""
    node_id: str
    name: str
    description: str
    is_treatment: bool = False
    is_outcome: bool = False
    is_confounder: bool = False
    parents: List[str] = Field(default_factory=list)
    base_value: float = 0.0


class StructuralCausalModel:
    """Manages the causal DAG, structural equations, and observational sampling."""

    def __init__(self, model_name: str = "EnterpriseMissionSCM") -> None:
        self.model_name = model_name
        self.nodes: Dict[str, CausalNode] = {}
        self._initialize_canonical_scm()

    def _initialize_canonical_scm(self) -> None:
        """Constructs the canonical document processing causal graph:
        Document Complexity (Confounder) -> Worker Concurrency (Treatment)
        Document Complexity (Confounder) -> Total Latency (Outcome)
        Worker Concurrency (Treatment) -> GPU Memory Pressure (Mediator)
        GPU Memory Pressure (Mediator) -> Total Latency (Outcome)
        Worker Concurrency (Treatment) -> Total Cost (Outcome)
        """
        self.nodes["doc_complexity"] = CausalNode(
            node_id="doc_complexity",
            name="Document Complexity (C)",
            description="Inherent document noise, skew, and table density (Confounder)",
            is_confounder=True,
            base_value=1.2,
        )
        self.nodes["worker_concurrency"] = CausalNode(
            node_id="worker_concurrency",
            name="Worker Concurrency (X)",
            description="Number of parallel workers assigned (Treatment)",
            is_treatment=True,
            parents=["doc_complexity"],
            base_value=4.0,
        )
        self.nodes["gpu_memory_pressure"] = CausalNode(
            node_id="gpu_memory_pressure",
            name="GPU Memory Pressure (M)",
            description="Peak GPU VRAM allocation in MB (Mediator)",
            parents=["worker_concurrency", "doc_complexity"],
            base_value=3072.0,
        )
        self.nodes["total_latency_ms"] = CausalNode(
            node_id="total_latency_ms",
            name="Total Latency ms (Y_lat)",
            description="Critical path end-to-end execution time in ms (Outcome)",
            is_outcome=True,
            parents=["doc_complexity", "worker_concurrency", "gpu_memory_pressure"],
            base_value=850.0,
        )
        self.nodes["total_cost_usd"] = CausalNode(
            node_id="total_cost_usd",
            name="Total Cost USD (Y_cost)",
            description="Total monetary cost of tokens and worker leases (Outcome)",
            is_outcome=True,
            parents=["worker_concurrency", "doc_complexity"],
            base_value=0.0022,
        )

    def get_node(self, node_id: str) -> Optional[CausalNode]:
        return self.nodes.get(node_id)

    def list_nodes(self) -> List[CausalNode]:
        return list(self.nodes.values())

    def get_parents(self, node_id: str) -> List[str]:
        node = self.nodes.get(node_id)
        return node.parents if node else []
