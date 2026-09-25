"""
Execution Subsystem Core Interfaces.
Defines IExecutionEngine, IRuntimeScheduler, IWorkerPool, and ICheckpointManager.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.execution.checkpoint_manager import ExecutionSnapshot
from app.agents.execution.context import ExecutionRequest, ExecutionResult
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.lease_manager import WorkerLease


class IExecutionEngine(ABC):
    """Abstract interface for stateful plan execution."""
    @abstractmethod
    async def execute(self, request: ExecutionRequest) -> ExecutionResult:
        pass


class IRuntimeScheduler(ABC):
    """Abstract interface for runtime node scheduling."""
    @abstractmethod
    def order_runnable_nodes(self, runnable_node_ids: List[str], graph: ExecutionGraph) -> List[str]:
        pass


class IWorkerPool(ABC):
    """Abstract interface for worker pool concurrency."""
    @abstractmethod
    async def acquire_worker(self, node_id: str, capability: Optional[str] = None) -> WorkerLease:
        pass

    @abstractmethod
    async def release_worker(self, lease: WorkerLease) -> None:
        pass


class ICheckpointManager(ABC):
    """Abstract interface for execution checkpointing."""
    @abstractmethod
    def create_checkpoint(
        self,
        execution_id: UUID,
        trigger: str,
        node_states: Dict[str, Any],
        outputs: Dict[str, Any],
        completed_nodes: List[str]
    ) -> ExecutionSnapshot:
        pass
