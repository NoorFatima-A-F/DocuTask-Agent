"""
Causal Analysis - Structural Causal Model (SCM)
Defines Directed Acyclic Graph (DAG) structural equations for document processing.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class CausalNode:
    node_id: str
    name: str
    node_type: str  # EXOGENOUS | INTERVENTION | MEDIATOR | OUTCOME
    parents: List[str]
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


CANONICAL_SCM_NODES = [
    CausalNode(
        node_id="complexity",
        name="Document Complexity (Z)",
        node_type="EXOGENOUS",
        parents=[],
        description="Layout density, table count, visual distortion, and page count.",
    ),
    CausalNode(
        node_id="ocr_noise",
        name="OCR Quality Noise (W)",
        node_type="EXOGENOUS",
        parents=["complexity"],
        description="Base optical character recognition confidence score.",
    ),
    CausalNode(
        node_id="model_choice",
        name="Planner Model Choice (X)",
        node_type="INTERVENTION",
        parents=["complexity", "ocr_noise"],
        description="Target routing decision (e.g. Gemini Pro vs Flash vs Flash-Lite).",
    ),
    CausalNode(
        node_id="retry_count",
        name="Retry Execution Count (R)",
        node_type="MEDIATOR",
        parents=["model_choice", "ocr_noise"],
        description="Transient network retry loops and validation backoff attempts.",
    ),
    CausalNode(
        node_id="latency_ms",
        name="End-to-End Latency (Y_L)",
        node_type="OUTCOME",
        parents=["model_choice", "retry_count", "complexity"],
        description="Total system processing time in milliseconds.",
    ),
    CausalNode(
        node_id="cost_usd",
        name="Execution Cost USD (Y_C)",
        node_type="OUTCOME",
        parents=["model_choice", "retry_count"],
        description="Total monetary cost incurred by LLM tokens and API calls.",
    ),
    CausalNode(
        node_id="accuracy",
        name="Extraction Accuracy (Y_A)",
        node_type="OUTCOME",
        parents=["model_choice", "ocr_noise", "complexity"],
        description="Ground truth field-level extraction exact-match score.",
    ),
]


class StructuralCausalModel:
    """Enterprise SCM DAG representing causal relationships in document pipelines."""

    def __init__(self):
        self.nodes = {n.node_id: n for n in CANONICAL_SCM_NODES}

    def list_nodes(self) -> List[Dict[str, Any]]:
        return [n.to_dict() for n in self.nodes.values()]

    def get_backdoor_adjustment_set(self, treatment: str, outcome: str) -> List[str]:
        """Identifies confounders for backdoor adjustment blocking spurious non-causal paths."""
        if treatment == "model_choice" and outcome in ["latency_ms", "accuracy", "cost_usd"]:
            return ["complexity", "ocr_noise"]
        return ["complexity"]
