"""
Sequential Task Executor.
Executes linear task nodes one by one.
"""

from typing import Any, Dict, List
from app.agents.execution.execution_context import TaskExecutionContext
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.executor import NodeExecutor


class SequentialExecutor:
    """Executes task nodes strictly sequentially."""

    def __init__(self, node_executor: NodeExecutor):
        self.node_executor = node_executor

    async def execute_sequence(
        self,
        node_ids: List[str],
        graph: ExecutionGraph,
        execution_id: Any
    ) -> List[Dict[str, Any]]:
        results = []
        for nid in node_ids:
            exec_node = graph.get_node(nid)
            if exec_node:
                ctx = TaskExecutionContext(
                    execution_id=execution_id,
                    node_id=nid,
                    capability_requirement=exec_node.node.capability_requirement,
                    parameters=exec_node.node.parameters
                )
                res = await self.node_executor.execute_node(exec_node, ctx)
                results.append(res)
        return results
