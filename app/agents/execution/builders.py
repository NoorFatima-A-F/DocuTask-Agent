"""
Fluent Builders Suite for Runtime Execution.
Provides ExecutionRequestBuilder, ExecutionSessionBuilder, RuntimeContextBuilder,
WorkerBuilder, CheckpointBuilder, and ExecutionResultBuilder.
"""

from typing import Any, Dict, List
from uuid import UUID
from app.agents.execution.checkpoint_manager import CheckpointMetadata, ExecutionSnapshot
from app.agents.execution.context import ExecutionRequest, ExecutionResult, RuntimeContext
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.worker import Worker, WorkerStatus
from app.agents.planning.contracts import Plan


class RuntimeContextBuilder:
    """Fluent builder for RuntimeContext."""

    def __init__(self):
        self._tenant_id = "default"
        self._max_concurrency = 4
        self._timeout_seconds = 3600.0
        self._token_limit = 50000
        self._parameters: Dict[str, Any] = {}

    def with_tenant(self, tenant_id: str) -> "RuntimeContextBuilder":
        self._tenant_id = tenant_id
        return self

    def with_concurrency(self, limit: int) -> "RuntimeContextBuilder":
        self._max_concurrency = limit
        return self

    def with_timeout(self, seconds: float) -> "RuntimeContextBuilder":
        self._timeout_seconds = seconds
        return self

    def with_token_limit(self, tokens: int) -> "RuntimeContextBuilder":
        self._token_limit = tokens
        return self

    def build(self) -> RuntimeContext:
        return RuntimeContext(
            tenant_id=self._tenant_id,
            max_concurrency=self._max_concurrency,
            timeout_seconds=self._timeout_seconds,
            token_budget_limit=self._token_limit,
            parameters=self._parameters
        )


class ExecutionRequestBuilder:
    """Fluent builder for ExecutionRequest."""

    def __init__(self, plan: Plan):
        self._plan = plan
        self._context = RuntimeContext()
        self._inputs: Dict[str, Any] = {}

    def with_context(self, context: RuntimeContext) -> "ExecutionRequestBuilder":
        self._context = context
        return self

    def with_input(self, key: str, value: Any) -> "ExecutionRequestBuilder":
        self._inputs[key] = value
        return self

    def build(self) -> ExecutionRequest:
        return ExecutionRequest(
            plan=self._plan,
            context=self._context,
            initial_inputs=self._inputs
        )


class WorkerBuilder:
    """Fluent builder for Worker."""

    def __init__(self, worker_id: str):
        self._worker_id = worker_id
        self._capabilities: List[str] = ["DEFAULT"]

    def with_capability(self, capability: str) -> "WorkerBuilder":
        self._capabilities.append(capability)
        return self

    def build(self) -> Worker:
        return Worker(
            worker_id=self._worker_id,
            capabilities=self._capabilities,
            status=WorkerStatus.IDLE
        )


class CheckpointBuilder:
    """Fluent builder for ExecutionSnapshot."""

    def __init__(self, execution_id: UUID):
        self._execution_id = execution_id
        self._trigger = "MANUAL"
        self._node_states: Dict[str, ExecutionLifecycleState] = {}
        self._outputs: Dict[str, Any] = {}
        self._completed_nodes: List[str] = []

    def with_trigger(self, trigger: str) -> "CheckpointBuilder":
        self._trigger = trigger
        return self

    def with_node_state(self, node_id: str, state: ExecutionLifecycleState) -> "CheckpointBuilder":
        self._node_states[node_id] = state
        return self

    def build(self) -> ExecutionSnapshot:
        meta = CheckpointMetadata(execution_id=self._execution_id, trigger=self._trigger)
        return ExecutionSnapshot(
            metadata=meta,
            node_states=self._node_states,
            accumulated_outputs=self._outputs,
            completed_node_ids=self._completed_nodes
        )


class ExecutionResultBuilder:
    """Fluent builder for ExecutionResult."""

    def __init__(self, execution_id: UUID, plan_id: UUID):
        self._execution_id = execution_id
        self._plan_id = plan_id
        self._state = ExecutionLifecycleState.COMPLETED
        self._outputs: Dict[str, Any] = {}
        self._errors: List[str] = []

    def with_state(self, state: ExecutionLifecycleState) -> "ExecutionResultBuilder":
        self._state = state
        return self

    def with_output(self, key: str, value: Any) -> "ExecutionResultBuilder":
        self._outputs[key] = value
        return self

    def add_error(self, error: str) -> "ExecutionResultBuilder":
        self._errors.append(error)
        return self

    def build(self) -> ExecutionResult:
        return ExecutionResult(
            execution_id=self._execution_id,
            plan_id=self._plan_id,
            lifecycle_state=self._state,
            outputs=self._outputs,
            errors=self._errors
        )
