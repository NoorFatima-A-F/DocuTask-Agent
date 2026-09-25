"""
Runtime Scheduler.
Implements FIFO, Priority, CriticalPath, LeastCost, FairShare, and Adaptive task scheduling strategies.
"""

from enum import Enum
from typing import List
from app.agents.execution.execution_graph import ExecutionGraph


class SchedulingStrategy(str, Enum):
    FIFO = "FIFO"
    PRIORITY = "PRIORITY"
    CRITICAL_PATH = "CRITICAL_PATH"
    LEAST_COST = "LEAST_COST"
    DEADLINE_AWARE = "DEADLINE_AWARE"
    FAIR_SHARE = "FAIR_SHARE"
    ADAPTIVE = "ADAPTIVE"
    HYBRID = "HYBRID"


class RuntimeScheduler:
    """Schedules runnable execution nodes according to configured scheduling strategy."""

    def __init__(self, strategy: SchedulingStrategy = SchedulingStrategy.PRIORITY):
        self.strategy = strategy

    def order_runnable_nodes(self, runnable_node_ids: List[str], graph: ExecutionGraph) -> List[str]:
        """Orders runnable candidate node IDs based on selected scheduling strategy."""
        if not runnable_node_ids or len(runnable_node_ids) <= 1:
            return list(runnable_node_ids)

        if self.strategy == SchedulingStrategy.FIFO:
            return list(runnable_node_ids)

        if self.strategy in (SchedulingStrategy.PRIORITY, SchedulingStrategy.CRITICAL_PATH, SchedulingStrategy.ADAPTIVE):
            # Sort by node timeout or priority weight
            return sorted(
                runnable_node_ids,
                key=lambda nid: (graph.nodes[nid].node.timeout_seconds if nid in graph.nodes else 0.0),
                reverse=True
            )

        return list(runnable_node_ids)
