"""
DAG Builder Engine for Phase 13.2.
Constructs DAG structures with Split, Merge, Parallel, Sequential, Conditional, Retry, Recovery, Barrier, and Join nodes.
"""

from __future__ import annotations

from typing import Dict, List
from datetime import datetime, timezone

from app.runtime.planner_visualization.ui_models.models import (
    PlannerDAGNode,
    PlannerDAGEdge,
    PlannerDAGSnapshot,
    TaskNodeType,
    TaskExecutionState,
    PlannerStateEnum,
)
from app.runtime.planner_visualization.dag.critical_path import CriticalPathEngine


class DAGBuilderEngine:
    """
    Constructs and verifies execution DAG topologies for autonomous missions.
    """

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id
        self.version = 1
        self.nodes: Dict[str, PlannerDAGNode] = {}
        self.edges: List[PlannerDAGEdge] = []
        self._init_default_dag()

    def _init_default_dag(self):
        default_nodes = [
            PlannerDAGNode(
                node_id="node_goal_ingress",
                name="Mission Goal Ingress",
                node_type=TaskNodeType.SEQUENTIAL,
                state=TaskExecutionState.COMPLETED,
                assigned_worker="worker-planner-01",
                estimated_duration_ms=45.0,
                actual_duration_ms=42.0,
                confidence=0.99,
                event_id="evt-dag-001",
                truth_ledger_hash="hash-dag-001-c8a1",
                replay_offset=0,
            ),
            PlannerDAGNode(
                node_id="node_split_ocr",
                name="Split OCR Chunks",
                node_type=TaskNodeType.SPLIT,
                state=TaskExecutionState.COMPLETED,
                assigned_worker="worker-dag-01",
                parent_ids=["node_goal_ingress"],
                dependencies=["node_goal_ingress"],
                estimated_duration_ms=30.0,
                actual_duration_ms=28.0,
                confidence=0.99,
                event_id="evt-dag-002",
                truth_ledger_hash="hash-dag-002-d9b2",
                replay_offset=1,
            ),
            PlannerDAGNode(
                node_id="node_ocr_chunk_1",
                name="OCR Page 1-2 (Raster)",
                node_type=TaskNodeType.PARALLEL,
                state=TaskExecutionState.COMPLETED,
                assigned_worker="worker-ocr-01",
                parent_ids=["node_split_ocr"],
                dependencies=["node_split_ocr"],
                estimated_duration_ms=180.0,
                actual_duration_ms=175.0,
                confidence=0.992,
                event_id="evt-dag-003",
                truth_ledger_hash="hash-dag-003-e0c3",
                replay_offset=2,
            ),
            PlannerDAGNode(
                node_id="node_ocr_chunk_2",
                name="OCR Page 3-4 (Tables)",
                node_type=TaskNodeType.PARALLEL,
                state=TaskExecutionState.COMPLETED,
                assigned_worker="worker-ocr-02",
                parent_ids=["node_split_ocr"],
                dependencies=["node_split_ocr"],
                estimated_duration_ms=210.0,
                actual_duration_ms=205.0,
                confidence=0.988,
                event_id="evt-dag-004",
                truth_ledger_hash="hash-dag-004-f1d4",
                replay_offset=3,
            ),
            PlannerDAGNode(
                node_id="node_merge_ocr",
                name="Merge OCR Texts",
                node_type=TaskNodeType.MERGE,
                state=TaskExecutionState.RUNNING,
                assigned_worker="worker-extract-01",
                parent_ids=["node_ocr_chunk_1", "node_ocr_chunk_2"],
                dependencies=["node_ocr_chunk_1", "node_ocr_chunk_2"],
                estimated_duration_ms=60.0,
                confidence=0.99,
                event_id="evt-dag-005",
                truth_ledger_hash="hash-dag-005-a2e5",
                replay_offset=4,
            ),
            PlannerDAGNode(
                node_id="node_extract_schema",
                name="Extract Financial Schema",
                node_type=TaskNodeType.SEQUENTIAL,
                state=TaskExecutionState.WAITING,
                assigned_worker="worker-extract-01",
                parent_ids=["node_merge_ocr"],
                dependencies=["node_merge_ocr"],
                estimated_duration_ms=140.0,
                confidence=0.97,
                event_id="evt-dag-006",
                truth_ledger_hash="hash-dag-006-b3f6",
                replay_offset=5,
            ),
            PlannerDAGNode(
                node_id="node_validate_invariants",
                name="Scientific Validation Check",
                node_type=TaskNodeType.CONDITIONAL,
                state=TaskExecutionState.WAITING,
                assigned_worker="worker-validate-01",
                parent_ids=["node_extract_schema"],
                dependencies=["node_extract_schema"],
                estimated_duration_ms=90.0,
                confidence=0.995,
                event_id="evt-dag-007",
                truth_ledger_hash="hash-dag-007-c4a7",
                replay_offset=6,
            ),
            PlannerDAGNode(
                node_id="node_barrier_governance",
                name="Governance Sync Barrier",
                node_type=TaskNodeType.BARRIER,
                state=TaskExecutionState.WAITING,
                assigned_worker="worker-gov-01",
                parent_ids=["node_validate_invariants"],
                dependencies=["node_validate_invariants"],
                estimated_duration_ms=50.0,
                confidence=0.999,
                event_id="evt-dag-008",
                truth_ledger_hash="hash-dag-008-d5b8",
                replay_offset=7,
            ),
            PlannerDAGNode(
                node_id="node_join_finalize",
                name="Join & Truth Ledger Commit",
                node_type=TaskNodeType.JOIN,
                state=TaskExecutionState.WAITING,
                assigned_worker="worker-trust-01",
                parent_ids=["node_barrier_governance"],
                dependencies=["node_barrier_governance"],
                estimated_duration_ms=40.0,
                confidence=1.0,
                event_id="evt-dag-009",
                truth_ledger_hash="hash-dag-009-e6c9",
                replay_offset=8,
            ),
        ]

        default_edges = [
            PlannerDAGEdge(source="node_goal_ingress", target="node_split_ocr"),
            PlannerDAGEdge(source="node_split_ocr", target="node_ocr_chunk_1"),
            PlannerDAGEdge(source="node_split_ocr", target="node_ocr_chunk_2"),
            PlannerDAGEdge(source="node_ocr_chunk_1", target="node_merge_ocr"),
            PlannerDAGEdge(source="node_ocr_chunk_2", target="node_merge_ocr"),
            PlannerDAGEdge(source="node_merge_ocr", target="node_extract_schema"),
            PlannerDAGEdge(source="node_extract_schema", target="node_validate_invariants"),
            PlannerDAGEdge(source="node_validate_invariants", target="node_barrier_governance"),
            PlannerDAGEdge(source="node_barrier_governance", target="node_join_finalize"),
        ]

        self.nodes = {n.node_id: n for n in default_nodes}
        self.edges = default_edges

    def get_snapshot(self) -> PlannerDAGSnapshot:
        cpm_res = CriticalPathEngine.compute_critical_path(list(self.nodes.values()), self.edges)
        completed = sum(1 for n in self.nodes.values() if n.state == TaskExecutionState.COMPLETED)

        return PlannerDAGSnapshot(
            mission_id=self.mission_id,
            version=self.version,
            state=PlannerStateEnum.EXECUTING,
            nodes=list(self.nodes.values()),
            edges=self.edges,
            critical_path=cpm_res["critical_path_nodes"],
            critical_path_duration_ms=cpm_res["total_duration_ms"],
            total_nodes=len(self.nodes),
            completed_nodes=completed,
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
