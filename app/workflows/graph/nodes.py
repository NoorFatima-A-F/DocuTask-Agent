"""
Execution Graph Node Definitions.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ..domain.models import TaskDefinition


@dataclass
class GraphNode(ABC):
    """Base class for all graph execution nodes."""
    node_id: str
    name: str
    node_type: str = "task"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskNode(GraphNode):
    """Standard executable task node."""
    task_def: Optional[TaskDefinition] = None
    node_type: str = "task"


@dataclass
class DecisionNode(GraphNode):
    """Branching decision condition node."""
    condition_expression: str = ""
    branches: Dict[str, str] = field(default_factory=dict)  # result_value -> target_node_id
    node_type: str = "decision"


@dataclass
class ApprovalNode(GraphNode):
    """Human-in-the-loop approval gate node."""
    approver_role: str = "admin"
    timeout_hours: int = 24
    required_approvals: int = 1
    node_type: str = "approval"


@dataclass
class TimerNode(GraphNode):
    """Delay/Timer pause node."""
    duration_seconds: int = 0
    node_type: str = "timer"


@dataclass
class EventNode(GraphNode):
    """External event listener/wait node."""
    event_type: str = "custom.event"
    node_type: str = "event"


@dataclass
class AgentNode(GraphNode):
    """Autonomous AI agent execution node."""
    agent_role: str = "orchestrator"
    prompt_template: str = ""
    max_iterations: int = 5
    node_type: str = "agent"


@dataclass
class ConnectorNode(GraphNode):
    """External SaaS system connector action node."""
    connector_id: str = ""
    action_name: str = ""
    node_type: str = "connector"


@dataclass
class SubWorkflowNode(GraphNode):
    """Child sub-workflow invocation node."""
    sub_workflow_id: str = ""
    sub_workflow_version: str = "1.0.0"
    pass_context: bool = True
    node_type: str = "subworkflow"


@dataclass
class ParallelNode(GraphNode):
    """Parallel fan-out/fan-in synchronization node."""
    branch_node_ids: List[str] = field(default_factory=list)
    join_type: str = "all"  # all, any, n_of_m
    node_type: str = "parallel"
