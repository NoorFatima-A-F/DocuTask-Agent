"""
Workflow Graph & Topology Domain Models.
Defines WorkflowNode, WorkflowEdge, WorkflowGraph, WorkflowStage, WorkflowTemplate, WorkflowSnapshot.
Supports Linear, Conditional, Parallel, Fan-out, Fan-in, and DAG workflow structures without containing execution logic directly.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.domain.enums import WorkflowType
from app.agents.domain.policies import ExecutionPolicy
from app.agents.domain.tasks import AgentTask
from app.agents.domain.value_objects import TaskID, WorkflowID


class WorkflowNode(BaseModel):
    """Node in a workflow graph representing an executable task specification."""

    node_id: str
    task: AgentTask
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class WorkflowEdge(BaseModel):
    """Directed edge in a workflow graph linking source node to target node."""

    edge_id: str
    source_node_id: str
    target_node_id: str
    condition_expression: Optional[str] = Field(default=None)

    model_config = {"frozen": True}


class WorkflowGraph(BaseModel):
    """Directed Acyclic Graph (DAG) workflow topology definition."""

    workflow_id: WorkflowID = Field(default_factory=WorkflowID)
    name: str = Field(default="WorkflowGraph")
    workflow_type: WorkflowType = Field(default=WorkflowType.DAG)
    version: str = Field(default="v1.0")
    
    nodes: Dict[str, WorkflowNode] = Field(default_factory=dict)
    edges: List[WorkflowEdge] = Field(default_factory=list)
    execution_policy: ExecutionPolicy = Field(default_factory=ExecutionPolicy)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}

    def add_node(self, node: WorkflowNode) -> "WorkflowGraph":
        """Returns a new WorkflowGraph instance with the added node."""
        new_nodes = dict(self.nodes)
        new_nodes[node.node_id] = node
        return WorkflowGraph(
            workflow_id=self.workflow_id,
            name=self.name,
            workflow_type=self.workflow_type,
            version=self.version,
            nodes=new_nodes,
            edges=self.edges,
            execution_policy=self.execution_policy,
            metadata=self.metadata
        )

    def add_edge(self, edge: WorkflowEdge) -> "WorkflowGraph":
        """Returns a new WorkflowGraph instance with the added edge."""
        new_edges = list(self.edges)
        new_edges.append(edge)
        return WorkflowGraph(
            workflow_id=self.workflow_id,
            name=self.name,
            workflow_type=self.workflow_type,
            version=self.version,
            nodes=self.nodes,
            edges=new_edges,
            execution_policy=self.execution_policy,
            metadata=self.metadata
        )


class WorkflowStage(BaseModel):
    """Group of parallel workflow nodes executing within a single stage."""

    stage_id: str
    stage_name: str
    nodes: List[WorkflowNode] = Field(default_factory=list)

    model_config = {"frozen": True}


class WorkflowTemplate(BaseModel):
    """Reusable workflow definition template."""

    template_id: str
    name: str
    description: str
    graph: WorkflowGraph

    model_config = {"frozen": True}


class WorkflowSnapshot(BaseModel):
    """State snapshot of a workflow graph for checkpointing."""

    snapshot_id: str
    workflow_id: WorkflowID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_node_ids: List[str] = Field(default_factory=list)
    pending_node_ids: List[str] = Field(default_factory=list)
    failed_node_ids: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
