"""
Recovery Planner.
Synthesizes a RecoveryGraph DAG corresponding to the selected recovery strategy.
"""

from uuid import uuid4
from app.agents.recovery.failure import Failure
from app.agents.recovery.recovery_graph import RecoveryEdge, RecoveryGraph, RecoveryNode
from app.agents.recovery.recovery_strategy import RecoveryStrategy, RecoveryStrategyDefinition


class RecoveryPlanner:
    """Plans recovery steps as an executable RecoveryGraph."""

    def plan_recovery(self, failure: Failure, strategy_def: RecoveryStrategyDefinition) -> RecoveryGraph:
        strat = strategy_def.strategy
        nodes = {}
        edges = []

        if strat == RecoveryStrategy.RETRY:
            n1 = RecoveryNode(node_id="step_1_reset", action="RESET_NODE_STATE", target_id=failure.identity.node_id)
            n2 = RecoveryNode(node_id="step_2_requeue", action="REQUEUE_FOR_EXECUTION", target_id=failure.identity.node_id)
            nodes[n1.node_id] = n1
            nodes[n2.node_id] = n2
            edges.append(RecoveryEdge(source_id=n1.node_id, target_id=n2.node_id))

        elif strat == RecoveryStrategy.RESTORE_CHECKPOINT:
            n1 = RecoveryNode(node_id="step_1_restore_cp", action="RESTORE_CHECKPOINT", target_id=str(failure.identity.execution_id))
            n2 = RecoveryNode(node_id="step_2_reconcile", action="RECONCILE_STATE", target_id=str(failure.identity.execution_id))
            nodes[n1.node_id] = n1
            nodes[n2.node_id] = n2
            edges.append(RecoveryEdge(source_id=n1.node_id, target_id=n2.node_id))

        elif strat == RecoveryStrategy.ALTERNATE_TOOL:
            n1 = RecoveryNode(node_id="step_1_switch_tool", action="SWITCH_TOOL_DESCRIPTOR", target_id=failure.identity.tool_name)
            n2 = RecoveryNode(node_id="step_2_requeue", action="REQUEUE_FOR_EXECUTION", target_id=failure.identity.node_id)
            nodes[n1.node_id] = n1
            nodes[n2.node_id] = n2
            edges.append(RecoveryEdge(source_id=n1.node_id, target_id=n2.node_id))

        elif strat == RecoveryStrategy.ROLLBACK:
            n1 = RecoveryNode(node_id="step_1_compensate", action="EXECUTE_COMPENSATION", target_id=failure.identity.node_id)
            n2 = RecoveryNode(node_id="step_2_rollback", action="ROLLBACK_WORKFLOW", target_id=str(failure.identity.execution_id))
            nodes[n1.node_id] = n1
            nodes[n2.node_id] = n2
            edges.append(RecoveryEdge(source_id=n1.node_id, target_id=n2.node_id))

        else:
            n1 = RecoveryNode(node_id="step_1_escalate", action="ESCALATE_INCIDENT", target_id=str(failure.identity.execution_id))
            nodes[n1.node_id] = n1

        return RecoveryGraph(graph_id=uuid4(), nodes=nodes, edges=edges)
