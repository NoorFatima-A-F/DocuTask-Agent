"""
Dynamic Dependency Resolution Subsystem.

Evaluates hard, soft, optional, conditional, and runtime dependencies to determine
if an execution node is ready to be dispatched to a worker.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Set
from app.runtime.planning.graph.node import DAGNode, DependencySpec, DependencyType, NodeStatus


class DependencyResolver:
    """Evaluates multi-typed dependency readiness."""

    @classmethod
    def evaluate_node_dependencies(
        cls,
        node: DAGNode,
        completed_node_ids: Set[str],
        failed_node_ids: Set[str],
        context_data: Dict[str, Any],
    ) -> bool:
        """
        Returns True if all dependencies are satisfied according to their dependency types:
        - HARD: parent must be in completed_node_ids.
        - SOFT: parent in completed or failed (proceeds with partial payload).
        - OPTIONAL: automatically satisfied.
        - CONDITIONAL: evaluates boolean expression over context_data.
        """
        if node.status in (NodeStatus.COMPLETED, NodeStatus.RUNNING, NodeStatus.CANCELLED):
            return False

        for dep in node.dependencies:
            p_id = dep.parent_node_id

            if dep.dependency_type == DependencyType.HARD:
                if p_id not in completed_node_ids:
                    return False
                dep.is_satisfied = True

            elif dep.dependency_type == DependencyType.SOFT:
                if p_id not in completed_node_ids and p_id not in failed_node_ids:
                    return False
                dep.is_satisfied = True

            elif dep.dependency_type == DependencyType.CONDITIONAL:
                if p_id not in completed_node_ids:
                    return False
                if dep.condition_expr:
                    try:
                        allowed = {"True": True, "False": False, **context_data}
                        cond_result = bool(eval(dep.condition_expr, {"__builtins__": {}}, allowed))
                        if not cond_result:
                            return False
                    except Exception:
                        return False
                dep.is_satisfied = True

            elif dep.dependency_type == DependencyType.OPTIONAL:
                dep.is_satisfied = True

        return True
