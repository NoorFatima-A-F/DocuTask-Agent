"""
Master Adaptive Replanner.

Coordinates failure-driven replanning, runtime DAG mutation, strategy switching,
and recovery branch injection during live mission execution.
"""

from __future__ import annotations

from typing import List, Optional
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.graph_mutator import GraphMutationRecord, GraphMutator
from app.runtime.planning.replanning.recovery_graph import RecoveryGraphGenerator
from app.runtime.planning.replanning.strategy_switch import PlanningStrategy


class AdaptiveReplanner:
    """Master replanner capable of restructuring in-flight DAGs upon failure or low confidence."""

    def __init__(self, current_strategy: PlanningStrategy = PlanningStrategy.PROBABILISTIC) -> None:
        self.current_strategy = current_strategy
        self.mutation_history: List[GraphMutationRecord] = []

    def handle_node_failure(
        self,
        dag: ExecutionDAG,
        failed_node_id: str,
        error_reason: str,
        resume_node_id: Optional[str] = None,
    ) -> GraphMutationRecord:
        """
        Synthesizes recovery branch and mutates live DAG:
        Failed Node -> Recovery Pipeline -> Resume Target
        """
        failed_node = dag.nodes.get(failed_node_id)
        task_type = failed_node.task_type if failed_node else "GENERAL"

        # 1. Select recovery nodes based on task type
        if "OCR" in task_type or "IMAGE" in task_type:
            recovery_nodes = RecoveryGraphGenerator.generate_ocr_enhancement_recovery(
                mission_id=dag.mission_id, failed_node_id=failed_node_id
            )
        else:
            recovery_nodes = RecoveryGraphGenerator.generate_smt_schema_relaxation_recovery(
                mission_id=dag.mission_id, failed_node_id=failed_node_id
            )

        # 2. Determine resume target (first child of failed node if not specified)
        if not resume_node_id:
            children = dag._adjacency_out.get(failed_node_id, [])
            resume_node_id = children[0] if children else failed_node_id

        # 3. Apply mutation
        mutation_rec = GraphMutator.inject_recovery_branch(
            dag=dag,
            failed_node_id=failed_node_id,
            recovery_nodes=recovery_nodes,
            resume_target_node_id=resume_node_id,
            reason=f"Adaptive Replanning on {task_type} Failure: {error_reason}",
        )
        self.mutation_history.append(mutation_rec)
        return mutation_rec

    def handle_low_confidence(
        self,
        dag: ExecutionDAG,
        node_id: str,
        observed_confidence: float,
    ) -> GraphMutationRecord:
        """Injects secondary verification when intermediate confidence drops below threshold."""
        dag.nodes.get(node_id)
        children = dag._adjacency_out.get(node_id, [])
        target_id = children[0] if children else node_id

        enhancement_nodes = RecoveryGraphGenerator.generate_ocr_enhancement_recovery(
            mission_id=dag.mission_id, failed_node_id=node_id
        )

        mutation_rec = GraphMutator.inject_recovery_branch(
            dag=dag,
            failed_node_id=node_id,
            recovery_nodes=enhancement_nodes,
            resume_target_node_id=target_id,
            reason=f"Confidence Drop ({observed_confidence:.2f} < 0.70): Injected adaptive enhancement filter.",
        )
        self.mutation_history.append(mutation_rec)
        return mutation_rec
