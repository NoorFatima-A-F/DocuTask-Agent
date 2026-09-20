"""Hierarchical Task Network (HTN) Graph Synthesis Engine for DocuTask ACOS.

Deconstructs high-level goal intents into hierarchical compound tasks, recursively expands them
into primitive operators, and synthesizes topologically ordered, executable DAGs.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class PrimitiveOperatorNode(BaseModel):
    """Atomic primitive operator node in an executable DAG."""
    node_id: str = Field(default_factory=lambda: f"op_{uuid.uuid4().hex[:8]}")
    name: str
    operator_type: str  # 'OCR_SCAN', 'TABLE_PARSE', 'SCHEMA_VALIDATE', 'NER_EXTRACT', 'DB_RECONCILE', 'VERIFIER'
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    estimated_latency_ms: float = 120.0
    estimated_cost_usd: float = 0.0004
    failure_probability: float = 0.03
    preconditions: List[str] = Field(default_factory=list)
    postconditions: List[str] = Field(default_factory=list)


class HTNTask(BaseModel):
    """Compound or primitive HTN task."""
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str
    is_compound: bool = True
    subtasks: List[str] = Field(default_factory=list)
    primitive_operator: Optional[PrimitiveOperatorNode] = None


class SynthesizedDAG(BaseModel):
    """Topologically sorted synthesized DAG ready for kernel execution."""
    dag_id: str = Field(default_factory=lambda: f"dag_syn_{uuid.uuid4().hex[:8]}")
    goal_intent: str
    nodes: Dict[str, PrimitiveOperatorNode] = Field(default_factory=dict)
    adjacency: Dict[str, List[str]] = Field(default_factory=dict)  # node_id -> [downstream_node_ids]
    critical_path_ms: float = 0.0
    total_estimated_cost_usd: float = 0.0
    structural_depth: int = 1
    parallelism_width: int = 1


class HTNGraphSynthesizer:
    """Synthesizes valid execution graphs from high-level goal intents using HTN rules."""

    def __init__(self) -> None:
        self._decomposition_rules: Dict[str, List[List[str]]] = {
            "extract_financial_invoice": [
                ["preprocess_document", "extract_tabular_line_items", "reconcile_totals", "verify_compliance"],
                ["preprocess_document", "neural_layout_ocr", "extract_key_values", "verify_compliance"],
            ],
            "preprocess_document": [
                ["deskew_enhance_image", "detect_orientation", "segment_pages"],
            ],
            "extract_tabular_line_items": [
                ["detect_table_borders", "extract_table_cells", "align_tax_columns"],
            ],
            "reconcile_totals": [
                ["sum_line_items", "compute_subtotal_tax", "cross_verify_grand_total"],
            ],
            "verify_compliance": [
                ["pydantic_schema_check", "audit_provenance_seal"],
            ],
            "neural_layout_ocr": [
                ["cloud_vision_ocr", "spatial_box_binding"],
            ],
            "extract_key_values": [
                ["ner_entity_tagging", "json_key_value_builder"],
            ],
        }

    def synthesize_dag(self, goal_intent: str = "extract_financial_invoice", branch_index: int = 0) -> SynthesizedDAG:
        """Deconstructs goal intent into an executable primitive DAG."""
        dag = SynthesizedDAG(goal_intent=goal_intent)
        
        # 1. Expand HTN hierarchy
        top_tasks = self._decomposition_rules.get(goal_intent, [["preprocess_document", "extract_tabular_line_items", "verify_compliance"]])
        selected_sequence = top_tasks[branch_index % len(top_tasks)]
        
        expanded_primitive_names: List[str] = []
        for task_name in selected_sequence:
            if task_name in self._decomposition_rules:
                sub = self._decomposition_rules[task_name][0]
                expanded_primitive_names.extend(sub)
            else:
                expanded_primitive_names.append(task_name)

        # 2. Instantiate primitive operators
        prev_node_id: Optional[str] = None
        total_latency = 0.0
        total_cost = 0.0

        for idx, op_name in enumerate(expanded_primitive_names):
            op = PrimitiveOperatorNode(
                name=op_name,
                operator_type=self._resolve_operator_type(op_name),
                estimated_latency_ms=100.0 + (idx * 25.0),
                estimated_cost_usd=0.0002 + (idx * 0.0001),
                inputs=[f"artifact_{idx}"] if idx > 0 else ["raw_document_input"],
                outputs=[f"artifact_{idx+1}"],
            )
            dag.nodes[op.node_id] = op
            dag.adjacency[op.node_id] = []
            
            if prev_node_id:
                dag.adjacency[prev_node_id].append(op.node_id)
            
            total_latency += op.estimated_latency_ms
            total_cost += op.estimated_cost_usd
            prev_node_id = op.node_id

        dag.critical_path_ms = round(total_latency, 2)
        dag.total_estimated_cost_usd = round(total_cost, 6)
        dag.structural_depth = len(dag.nodes)
        dag.parallelism_width = 1

        return dag

    def _resolve_operator_type(self, op_name: str) -> str:
        if "ocr" in op_name or "vision" in op_name:
            return "OCR_SCAN"
        if "table" in op_name or "cell" in op_name:
            return "TABLE_PARSE"
        if "reconcile" in op_name or "verify" in op_name or "check" in op_name:
            return "VERIFIER"
        if "ner" in op_name or "extract" in op_name or "json" in op_name:
            return "NER_EXTRACT"
        return "PREPROCESS"
