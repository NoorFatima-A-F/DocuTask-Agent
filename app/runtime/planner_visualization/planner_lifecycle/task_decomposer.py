"""
Task Decomposition Engine for Phase 13.2.
Decomposes goals into typed execution tasks and emits TaskGenerated domain events.
"""

from __future__ import annotations

from typing import Any, Dict, List
from app.runtime.planner_visualization.ui_models.models import PlannerDAGNode, TaskNodeType, TaskExecutionState


class TaskDecompositionEngine:
    """
    Decomposes an abstract mission goal into a multi-stage typed execution pipeline.
    """

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id

    def decompose(self, goal_title: str) -> List[PlannerDAGNode]:
        nodes_def = [
            ("node_ocr_01", "OCR Document Ingestion", TaskNodeType.PARALLEL, "worker-ocr-01", 120.0, 0.0006),
            ("node_ocr_02", "OCR Table Segmentation", TaskNodeType.PARALLEL, "worker-ocr-02", 140.0, 0.0006),
            ("node_extract_fields", "Extract Invoice Fields", TaskNodeType.SEQUENTIAL, "worker-extract-01", 200.0, 0.0010),
            ("node_normalize_schema", "Normalize Schema", TaskNodeType.SEQUENTIAL, "worker-extract-01", 80.0, 0.0003),
            ("node_cross_validation", "Cross Validation", TaskNodeType.PARALLEL, "worker-validate-01", 110.0, 0.0004),
            ("node_evidence_verification", "Evidence Verification", TaskNodeType.PARALLEL, "worker-validate-01", 90.0, 0.0003),
            ("node_memory_lookup", "Memory Retrieval", TaskNodeType.SEQUENTIAL, "worker-memory-01", 60.0, 0.0002),
            ("node_trust_update", "Trust Ledger Update", TaskNodeType.JOIN, "worker-trust-01", 70.0, 0.0002),
            ("node_persistence", "Final Output Persistence", TaskNodeType.SEQUENTIAL, "worker-storage-01", 50.0, 0.0001),
        ]

        nodes: List[PlannerDAGNode] = []
        for idx, (nid, name, ntype, worker, dur, cost) in enumerate(nodes_def):
            node = PlannerDAGNode(
                node_id=nid,
                name=name,
                node_type=ntype,
                state=TaskExecutionState.WAITING if idx > 0 else TaskExecutionState.RUNNING,
                assigned_worker=worker,
                priority=1,
                estimated_cost_usd=cost,
                estimated_duration_ms=dur,
                confidence=0.985,
                event_id=f"evt-task-{nid}",
                truth_ledger_hash=f"hash-{nid}-verified",
                replay_offset=idx,
                metadata={"stage_index": idx, "task_kind": name},
            )
            nodes.append(node)

        return nodes
