"""
Autonomous Execution Graph Builder.

Synthesizes complete ExecutionDAG models from mission goals and task decomposition intents.
Generates balanced pipeline topologies with data/control edges and initial cost/runtime estimates.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.edge import DAGEdge, EdgeType
from app.runtime.planning.graph.node import DAGNode, DependencySpec, DependencyType, NodeStatus


class ExecutionGraphBuilder:
    """Builds fully specified ExecutionDAG instances from domain mission templates."""

    @classmethod
    def build_financial_invoice_audit_dag(
        cls, mission_id: str, document_id: Optional[str] = None
    ) -> ExecutionDAG:
        """Synthesizes standard 5-stage parallel invoice audit DAG."""
        dag = ExecutionDAG(dag_id=f"dag-{uuid.uuid4().hex[:8]}", mission_id=mission_id)

        # 1. OCR Stage
        n_ocr = DAGNode(
            node_id="node_ocr_01",
            mission_id=mission_id,
            name="Adaptive Holdout OCR Scan",
            task_type="OCR",
            priority=10,
            estimated_cost_usd=0.0008,
            estimated_tokens=400,
            estimated_runtime_ms=350.0,
            required_capabilities=["OCR", "VISION"],
            inputs={"document_id": document_id or "doc_sample_01"},
        )
        dag.add_node(n_ocr)

        # 2. Parallel Extraction: Line Items & Metadata
        n_extract_items = DAGNode(
            node_id="node_extract_items",
            mission_id=mission_id,
            name="Table Line-Item Parsing",
            task_type="EXTRACTION",
            priority=20,
            estimated_cost_usd=0.0012,
            estimated_tokens=800,
            estimated_runtime_ms=280.0,
            required_capabilities=["EXTRACTION", "NLP"],
        )
        dag.add_node(n_extract_items)

        n_extract_meta = DAGNode(
            node_id="node_extract_meta",
            mission_id=mission_id,
            name="Vendor & Tax Header Extraction",
            task_type="EXTRACTION",
            priority=20,
            estimated_cost_usd=0.0006,
            estimated_tokens=400,
            estimated_runtime_ms=180.0,
            required_capabilities=["EXTRACTION", "NLP"],
        )
        dag.add_node(n_extract_meta)

        # Wire OCR -> Extractions
        dag.add_edge(DAGEdge(source_node_id=n_ocr.node_id, target_node_id=n_extract_items.node_id))
        dag.add_edge(DAGEdge(source_node_id=n_ocr.node_id, target_node_id=n_extract_meta.node_id))

        # 3. Formal SMT Verification
        n_smt = DAGNode(
            node_id="node_smt_verify",
            mission_id=mission_id,
            name="SMT Arithmetic Invariant Proof",
            task_type="VALIDATION",
            priority=15,
            estimated_cost_usd=0.0002,
            estimated_tokens=100,
            estimated_runtime_ms=60.0,
            required_capabilities=["GOVERNANCE", "SMT"],
        )
        dag.add_node(n_smt)
        dag.add_edge(DAGEdge(source_node_id=n_extract_items.node_id, target_node_id=n_smt.node_id))
        dag.add_edge(DAGEdge(source_node_id=n_extract_meta.node_id, target_node_id=n_smt.node_id))

        # 4. Meta-Reflection & Distillation
        n_reflection = DAGNode(
            node_id="node_reflection",
            mission_id=mission_id,
            name="Meta-Cognitive Self-Critique",
            task_type="REFLECTION",
            priority=30,
            estimated_cost_usd=0.0004,
            estimated_tokens=250,
            estimated_runtime_ms=90.0,
            required_capabilities=["REFLECTION", "MEMORY"],
        )
        dag.add_node(n_reflection)
        dag.add_edge(DAGEdge(source_node_id=n_smt.node_id, target_node_id=n_reflection.node_id))

        return dag

    @classmethod
    def build_custom_dag(
        cls,
        mission_id: str,
        tasks: List[Dict[str, Any]],
        dependencies: List[Tuple[str, str]],
    ) -> ExecutionDAG:
        """Constructs a custom DAG from task dicts and dependency tuples (src_id, tgt_id)."""
        dag = ExecutionDAG(dag_id=f"dag-{uuid.uuid4().hex[:8]}", mission_id=mission_id)

        for t in tasks:
            node = DAGNode(
                node_id=t.get("node_id", f"node-{uuid.uuid4().hex[:6]}"),
                mission_id=mission_id,
                name=t.get("name", "Task Node"),
                task_type=t.get("task_type", "GENERAL"),
                priority=t.get("priority", 50),
                estimated_cost_usd=t.get("estimated_cost_usd", 0.001),
                estimated_tokens=t.get("estimated_tokens", 500),
                estimated_runtime_ms=t.get("estimated_runtime_ms", 200.0),
                required_capabilities=t.get("required_capabilities", ["GENERAL"]),
                inputs=t.get("inputs", {}),
            )
            dag.add_node(node)

        for src, tgt in dependencies:
            dag.add_edge(DAGEdge(source_node_id=src, target_node_id=tgt))

        return dag
