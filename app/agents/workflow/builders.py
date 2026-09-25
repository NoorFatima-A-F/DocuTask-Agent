"""
Workflow Fluent Builders.
Provides declarative, fluent builder patterns for constructing WorkflowNodes, WorkflowGraphs, WorkflowDefinitions, and Requests.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from app.agents.workflow.context import WorkflowContext, WorkflowRequest
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_edge import WorkflowEdge
from app.agents.workflow.workflow_graph import WorkflowGraph
from app.agents.workflow.workflow_node import WorkflowNode, WorkflowNodeType
from app.agents.workflow.workflow_version import WorkflowVersion


class WorkflowNodeBuilder:
    """Fluent builder for WorkflowNode."""

    def __init__(self, node_id: str, name: str) -> None:
        self._node_id = node_id
        self._name = name
        self._node_type = WorkflowNodeType.TASK
        self._handler = "default_handler"
        self._parameters: Dict[str, Any] = {}
        self._compensating_handler: Optional[str] = None
        self._timeout_seconds: float = 300.0
        self._retry_limit: int = 3

    def with_type(self, node_type: WorkflowNodeType) -> "WorkflowNodeBuilder":
        self._node_type = node_type
        return self

    def with_handler(self, handler: str) -> "WorkflowNodeBuilder":
        self._handler = handler
        return self

    def with_parameters(self, params: Dict[str, Any]) -> "WorkflowNodeBuilder":
        self._parameters = params
        return self

    def with_compensating_handler(self, compensating_handler: str) -> "WorkflowNodeBuilder":
        self._compensating_handler = compensating_handler
        return self

    def with_timeout(self, timeout_seconds: float) -> "WorkflowNodeBuilder":
        self._timeout_seconds = timeout_seconds
        return self

    def with_retry_limit(self, retries: int) -> "WorkflowNodeBuilder":
        self._retry_limit = retries
        return self

    def build(self) -> WorkflowNode:
        return WorkflowNode(
            node_id=self._node_id,
            name=self._name,
            node_type=self._node_type,
            handler=self._handler,
            parameters=self._parameters,
            compensating_handler=self._compensating_handler,
            timeout_seconds=self._timeout_seconds,
            retry_limit=self._retry_limit,
        )


class WorkflowGraphBuilder:
    """Fluent builder for WorkflowGraph."""

    def __init__(self) -> None:
        self._nodes: Dict[str, WorkflowNode] = {}
        self._edges: List[WorkflowEdge] = []

    def add_node(self, node: WorkflowNode) -> "WorkflowGraphBuilder":
        self._nodes[node.node_id] = node
        return self

    def add_edge(
        self,
        from_node: str,
        to_node: str,
        condition: Optional[str] = None,
        is_default: bool = False,
    ) -> "WorkflowGraphBuilder":
        self._edges.append(
            WorkflowEdge(
                from_node=from_node,
                to_node=to_node,
                condition=condition,
                is_default=is_default,
            )
        )
        return self

    def build(self) -> WorkflowGraph:
        return WorkflowGraph(nodes=self._nodes, edges=self._edges)


class WorkflowDefinitionBuilder:
    """Fluent builder for WorkflowDefinition."""

    def __init__(self, name: str) -> None:
        self._definition_id = uuid4()
        self._name = name
        self._description = ""
        self._version = WorkflowVersion(major=1, minor=0, patch=0)
        self._graph_builder = WorkflowGraphBuilder()
        self._is_active = True

    def with_id(self, definition_id: UUID) -> "WorkflowDefinitionBuilder":
        self._definition_id = definition_id
        return self

    def with_description(self, description: str) -> "WorkflowDefinitionBuilder":
        self._description = description
        return self

    def with_version(self, major: int, minor: int = 0, patch: int = 0) -> "WorkflowDefinitionBuilder":
        self._version = WorkflowVersion(major=major, minor=minor, patch=patch)
        return self

    def add_node(self, node: WorkflowNode) -> "WorkflowDefinitionBuilder":
        self._graph_builder.add_node(node)
        return self

    def add_edge(
        self,
        from_node: str,
        to_node: str,
        condition: Optional[str] = None,
        is_default: bool = False,
    ) -> "WorkflowDefinitionBuilder":
        self._graph_builder.add_edge(from_node, to_node, condition, is_default)
        return self

    def build(self) -> WorkflowDefinition:
        return WorkflowDefinition(
            definition_id=self._definition_id,
            name=self._name,
            description=self._description,
            version=self._version,
            graph=self._graph_builder.build(),
            is_active=self._is_active,
        )


class WorkflowRequestBuilder:
    """Fluent builder for WorkflowRequest."""

    def __init__(self, definition_id: UUID) -> None:
        self._definition_id = definition_id
        self._input_data: Dict[str, Any] = {}
        self._tenant_id = "default"
        self._correlation_id = str(uuid4())
        self._max_duration_seconds = 86400.0
        self._parent_instance_id: Optional[UUID] = None

    def with_input(self, key: str, value: Any) -> "WorkflowRequestBuilder":
        self._input_data[key] = value
        return self

    def with_inputs(self, inputs: Dict[str, Any]) -> "WorkflowRequestBuilder":
        self._input_data.update(inputs)
        return self

    def with_tenant(self, tenant_id: str) -> "WorkflowRequestBuilder":
        self._tenant_id = tenant_id
        return self

    def with_correlation_id(self, correlation_id: str) -> "WorkflowRequestBuilder":
        self._correlation_id = correlation_id
        return self

    def with_max_duration(self, seconds: float) -> "WorkflowRequestBuilder":
        self._max_duration_seconds = seconds
        return self

    def with_parent(self, parent_id: UUID) -> "WorkflowRequestBuilder":
        self._parent_instance_id = parent_id
        return self

    def build(self) -> WorkflowRequest:
        return WorkflowRequest(
            definition_id=self._definition_id,
            input_data=self._input_data,
            parent_instance_id=self._parent_instance_id,
            context=WorkflowContext(
                tenant_id=self._tenant_id,
                correlation_id=self._correlation_id,
                max_duration_seconds=self._max_duration_seconds,
            ),
        )
